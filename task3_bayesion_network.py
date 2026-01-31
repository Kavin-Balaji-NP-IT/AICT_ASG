

import itertools

# States for all variables
# Weather conditions
weather_states = ["Clear", "Rainy", "Thunderstorms"]

# Time of day
time_states = ["Morning", "Afternoon", "Evening"]

# Day type
day_states = ["Weekday", "Weekend"]

# Network mode
# Today = current network
# Future = TELe + CRL network changes
mode_states = ["Today", "Future"]

# Integration works level (systems integration works)
# None = no major works
# Minor = some works, some adjustments
# Major = heavy works, more disruptions
intensity_states = ["None", "Minor", "Major"]

# Service status (what commuters experience)
service_status_states = ["Normal", "Reduced", "Disrupted"]

# Demand proxy (how many people want to travel)
demand_proxy_states = ["Low", "Medium", "High"]

# Final output: crowding risk
crowding_risk_states = ["Low", "Medium", "High"]


# 2) PRIORS (how often things happen, simple assumptions)
# Weather probabilities (example assumptions)
weather_probability = {"Clear": 0.70, "Rainy": 0.20, "Thunderstorms": 0.10}

# Assume time periods are equally likely
time_probability = {"Morning": 1/3, "Afternoon": 1/3, "Evening": 1/3}

# 5 weekdays, 2 weekend days
day_probability = {"Weekday": 5/7, "Weekend": 2/7}

# We test Today and Future equally in the model
mode_probability = {"Today": 0.50, "Future": 0.50}

# Integration works are usually none/minor, major is rarer
intensity_probability = {"None": 0.80, "Minor": 0.15, "Major": 0.05}


# 3) CPT: Service Status GIVEN Integration Works
#    (Integration works -> service adjustments)
# Meaning: If works are major, reduced/disrupted service becomes more likely.
service_given_intensity_probs = {
    "None":  {"Normal": 0.90, "Reduced": 0.09, "Disrupted": 0.01},
    "Minor": {"Normal": 0.60, "Reduced": 0.30, "Disrupted": 0.10},
    "Major": {"Normal": 0.20, "Reduced": 0.40, "Disrupted": 0.40},
}


# 4) CPT: Demand Proxy GIVEN Weather, Time, Day, Mode
def get_demand_proxy_distribution(weather, time_of_day, day_type, network_mode):
    """
    This function estimates how BUSY demand is (Low/Medium/High).
    It does NOT output crowding risk yet.
    It just outputs DemandProxy probabilities.

    Idea:
    - Morning/Evening busier than afternoon
    - Weekdays slightly busier
    - Rain/storm can push people to MRT
    - Future mode spreads demand a little due to better connectivity
    """

    demand_score = 0.0

    # Time effect: morning & evening higher
    demand_score += {"Morning": 2.0, "Afternoon": 1.2, "Evening": 2.6}[time_of_day]

    # Weekday effect: slightly higher
    demand_score += {"Weekday": 0.5, "Weekend": 0.3}[day_type]

    # Weather effect: rain/storm increases demand a bit
    demand_score += {"Clear": 0.0, "Rainy": 0.3, "Thunderstorms": 0.4}[weather]

    # Future mode: small decrease because extra connectivity spreads load
    demand_score += {"Today": 0.0, "Future": -0.2}[network_mode]

    # Convert score into a Low/Medium/High probability distribution
    if demand_score < 1.8:
        return {"Low": 0.60, "Medium": 0.30, "High": 0.10}
    elif demand_score < 2.4:
        return {"Low": 0.30, "Medium": 0.50, "High": 0.20}
    elif demand_score < 3.0:
        return {"Low": 0.15, "Medium": 0.45, "High": 0.40}
    else:
        return {"Low": 0.10, "Medium": 0.30, "High": 0.60}


# 5)  Crowding Risk GIVEN Demand Proxy, Service Status, Mode
# Base table for TODAY mode.
# Future mode will make a small improvement later.
crowding_risk_given_demand_and_service_today = {
    ("Low",    "Normal"):    {"Low": 0.80, "Medium": 0.18, "High": 0.02},
    ("Medium", "Normal"):    {"Low": 0.30, "Medium": 0.55, "High": 0.15},
    ("High",   "Normal"):    {"Low": 0.10, "Medium": 0.40, "High": 0.50},

    ("Low",    "Reduced"):   {"Low": 0.60, "Medium": 0.30, "High": 0.10},
    ("Medium", "Reduced"):   {"Low": 0.20, "Medium": 0.50, "High": 0.30},
    ("High",   "Reduced"):   {"Low": 0.05, "Medium": 0.35, "High": 0.60},

    ("Low",    "Disrupted"): {"Low": 0.20, "Medium": 0.30, "High": 0.50},
    ("Medium", "Disrupted"): {"Low": 0.05, "Medium": 0.25, "High": 0.70},
    ("High",   "Disrupted"): {"Low": 0.02, "Medium": 0.18, "High": 0.80},
}

def get_crowding_risk_distribution(demand_proxy, service_status, network_mode):
    """
    This function estimates crowding risk (Low/Medium/High)
    given:
      - demand_proxy (Low/Medium/High)
      - service_status (Normal/Reduced/Disrupted)
      - network_mode (Today/Future)

    Future mode:
      We slightly reduce "High" risk (shift a bit to "Medium")
      because TELe+CRL adds more route options and spreads load.
    """

    dist = dict(crowding_risk_given_demand_and_service_today[(demand_proxy, service_status)])

    # Apply small Future improvement
    if network_mode == "Future":
        shift = 0.05 if service_status != "Disrupted" else 0.02
        moved = min(shift, dist["High"])
        dist["High"] -= moved
        dist["Medium"] += moved

    return dist


# 6) INFERENCE: P(CrowdingRisk | Evidence)
def infer_crowding_risk(evidence):
    """
    evidence is your SCENARIO input.
    Example:
      {
        "Weather": "Rainy",
        "TimeOfDay": "Evening",
        "DayType": "Weekday",
        "NetworkMode": "Today",
        "ServiceStatus": "Reduced"
      }

    This function will:
    - try all combinations (brute force)
    - keep only those matching the evidence
    - multiply probabilities (Bayesian calculation)
    - sum results
    - normalize -> final P(CrowdingRisk)
    """

    totals = {"Low": 0.0, "Medium": 0.0, "High": 0.0}

    # loop all possible combinations
    for weather, time_of_day, day_type, network_mode, works_level, current_service, demand_proxy, crowding_risk in itertools.product(
        weather_states,
        time_states,
        day_states,
        mode_states,
        intensity_states,
        service_status_states,
        demand_proxy_states,
        crowding_risk_states
    ):
        # current full assignment of all variables
        assignment = {
            "Weather": weather,
            "TimeOfDay": time_of_day,
            "DayType": day_type,
            "NetworkMode": network_mode,
            "IntegrationWorks": works_level,
            "ServiceStatus": current_service,
            "DemandProxy": demand_proxy,
            "CrowdingRisk": crowding_risk
        }

        # skip if doesn't match evidence
        mismatch = False
        for key, value in evidence.items():
            if assignment[key] != value:
                mismatch = True
                break
        if mismatch:
            continue

        # compute joint probability
        prob = 1.0

        # priors
        prob *= weather_probability[weather]
        prob *= time_probability[time_of_day]
        prob *= day_probability[day_type]
        prob *= mode_probability[network_mode]
        prob *= intensity_probability[works_level]

        # ServiceStatus | IntegrationWorks
        prob *= service_given_intensity_probs[works_level][current_service]

        # DemandProxy | Weather, Time, Day, Mode
        demand_dist = get_demand_proxy_distribution(weather, time_of_day, day_type, network_mode)
        prob *= demand_dist[demand_proxy]

        # CrowdingRisk | DemandProxy, ServiceStatus, Mode
        risk_dist = get_crowding_risk_distribution(demand_proxy, current_service, network_mode)
        prob *= risk_dist[crowding_risk]

        totals[crowding_risk] += prob

    # normalize to make totals sum to 1
    total_sum = sum(totals.values())
    for k in totals:
        totals[k] /= total_sum

    return totals


# 7) PRINT HELPER (one function call = one scenario)
def show_scenario(name, evidence):
    """
    Runs inference for ONE scenario and prints results.
    """
    dist = infer_crowding_risk(evidence)
    print("\n" + name)
    print("Evidence:", evidence)
    print(f"  P(CrowdingRisk=Low)   = {dist['Low']:.3f}")
    print(f"  P(CrowdingRisk=Medium)= {dist['Medium']:.3f}")
    print(f"  P(CrowdingRisk=High)  = {dist['High']:.3f}")


# 8) SCENARIOS  Each show_scenario() = ONE scenario test.
#    Today vs Future pairs: same evidence except NetworkMode.

# Pair 1: Clear evening + normal (Today vs Future)
show_scenario(
    "1) Today Mode: Clear evening weekday + normal (baseline)",
    {"Weather":"Clear","TimeOfDay":"Evening","DayType":"Weekday","NetworkMode":"Today","ServiceStatus":"Normal"}
)
show_scenario(
    "2) Future Mode: Clear evening weekday + normal (compare)",
    {"Weather":"Clear","TimeOfDay":"Evening","DayType":"Weekday","NetworkMode":"Future","ServiceStatus":"Normal"}
)

#  Rainy evening + reduced (Today vs Future)
show_scenario(
    "3) Today Mode: Rainy evening weekday + reduced (baseline)",
    {"Weather":"Rainy","TimeOfDay":"Evening","DayType":"Weekday","NetworkMode":"Today","ServiceStatus":"Reduced"}
)
show_scenario(
    "4) Future Mode: Rainy evening weekday + reduced (compare)",
    {"Weather":"Rainy","TimeOfDay":"Evening","DayType":"Weekday","NetworkMode":"Future","ServiceStatus":"Reduced"}
)

#  Clear morning + normal (Today vs Future)
show_scenario(
    "5) Today Mode: Clear morning weekday + normal",
    {"Weather":"Clear","TimeOfDay":"Morning","DayType":"Weekday","NetworkMode":"Today","ServiceStatus":"Normal"}
)
show_scenario(
    "6) Future Mode: Clear morning weekday + normal",
    {"Weather":"Clear","TimeOfDay":"Morning","DayType":"Weekday","NetworkMode":"Future","ServiceStatus":"Normal"}
)

# Disrupted service near airport corridor (integration works case)
show_scenario(
    "7) Disrupted service near airport corridor (works/disruption scenario)",
    {"Weather":"Clear","TimeOfDay":"Evening","DayType":"Weekday","NetworkMode":"Today","ServiceStatus":"Disrupted"}
)

# Weekend afternoon + normal
show_scenario(
    "8) Weekend afternoon + normal service",
    {"Weather":"Clear","TimeOfDay":"Afternoon","DayType":"Weekend","NetworkMode":"Today","ServiceStatus":"Normal"}
)
