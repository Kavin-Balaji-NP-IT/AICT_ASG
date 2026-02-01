
from typing import List, Set, Tuple, Dict
from dataclasses import dataclass, field

Station = str
RouteName = str
Edge = Tuple[Station, Station]

@dataclass
class Scenario:
    mode: str  # "today" or "future"
    status: str  # "normal" | "delay" | "disrupted" | "scheduled_maintenance"
    exists: Set[Station] = field(default_factory=set)          # stations that exist in this mode
    open_stations: Set[Station] = field(default_factory=set)   # stations currently open
    open_edges: Set[Edge] = field(default_factory=set)         # track segments open (a,b) directional or treat as undirected
    integration_works: bool = False
    recommended_routes: Set[RouteName] = field(default_factory=set)

    # Optional: if you want to model "served by TEL"
    served_by_tel: Set[Station] = field(default_factory=set)


@dataclass
class Route:
    name: RouteName
    stations: List[Station]  # ordered list, e.g. ["TanahMerah", "Expo", "ChangiAirport"]

    def edges(self) -> List[Edge]:
        return [(self.stations[i], self.stations[i+1]) for i in range(len(self.stations)-1)]


# --- helpers ---
def is_edge_open(open_edges: Set[Edge], a: Station, b: Station) -> bool:
    # Treat as undirected: (a,b) or (b,a) counts
    return (a, b) in open_edges or (b, a) in open_edges


def evaluate_route(route: Route, sc: Scenario) -> Dict:
    """
    Returns:
      {
        "valid": bool,
        "warning": bool,
        "violations": [rule_numbers],
        "notes": [strings]
      }
    """
    violations = []
    notes = []
    warning = False
    valid = True

    # Rule 1: Mode(today) -> ¬Exists(T5, today)
    # In practice: if mode=today, T5 must NOT be used.
    if sc.mode == "today":
        if "T5" in route.stations:
            valid = False
            violations.append(1)
            notes.append("Today mode: T5 does not exist, so route using T5 is invalid.")

    # Rule 2: using a station that doesn't exist in this mode -> invalid
    for s in route.stations:
        if s not in sc.exists:
            valid = False
            violations.append(2)
            notes.append(f"Station '{s}' does not exist in mode={sc.mode}.")
            break

    # Rule 3: UseStation(r,s) and ¬Open(s) -> ¬Valid(r)
    for s in route.stations:
        if s not in sc.open_stations:
            valid = False
            violations.append(3)
            notes.append(f"Station '{s}' is not open.")
            break

    # Rule 4: UseEdge(r,a,b) and ¬OpenEdge(a,b) -> ¬Valid(r)
    for (a, b) in route.edges():
        if not is_edge_open(sc.open_edges, a, b):
            valid = False
            violations.append(4)
            notes.append(f"Edge {a} -> {b} is not open.")
            break

    # Rule 8: Mode(today) and UseStation(r,ChangiAirport) -> UseStation(r,Expo)
    if sc.mode == "today" and "ChangiAirport" in route.stations:
        if "Expo" not in route.stations:
            valid = False
            violations.append(8)
            notes.append("Today mode: any route to ChangiAirport must include Expo.")

    # Rule 5: Status(delay/disrupted) -> CorridorRestricted; CorridorRestricted -> IntegrationWorks
    # Implementation: if delay/disrupted, assume integration works constraints apply.
    corridor_restricted = sc.status in ("delay", "disrupted")
    implied_integration = sc.integration_works or corridor_restricted

    # Rule 6: Mode(future) and IntegrationWorks -> AvoidRoutes(EWL_AirportBranch)
    # We'll interpret: if route name is the airport branch and integration works, it's "valid but avoid" (warning).
    if sc.mode == "future" and implied_integration:
        if route.name == "EWL_AirportBranch":
            warning = True
            notes.append("Future + integration works: EWL_AirportBranch should be avoided (warning).")

    return {
        "valid": valid,
        "warning": warning and valid,  # only show warning if still valid
        "violations": sorted(set(violations)),
        "notes": notes
    }


def check_advisory_consistency(sc: Scenario) -> Dict:
    """
    Checks global advisory contradictions (not route-specific).
    Returns { "consistent": bool, "violations": [rule_numbers], "notes": [...] }
    """
    violations = []
    notes = []

    corridor_restricted = sc.status in ("delay", "disrupted")
    implied_integration = sc.integration_works or corridor_restricted

    # Rule 7: Mode(Future) ∧ IntegrationWorks ∧ Recommended(EWL_AirportBranch) -> Inconsistent
    if sc.mode == "future" and implied_integration and ("EWL_AirportBranch" in sc.recommended_routes):
        violations.append(7)
        notes.append("Future + integration works: recommending EWL_AirportBranch is inconsistent.")

    # Rule 10: Mode(Future) -> ServedByTEL(TanahMerah) ∧ ServedByTEL(Expo) ∧ ServedByTEL(ChangiAirport)
    # If you provide served_by_tel facts, you can verify. If not, skip.
    if sc.mode == "future" and sc.served_by_tel:
        needed = {"TanahMerah", "Expo", "ChangiAirport"}
        missing = needed - sc.served_by_tel
        if missing:
            violations.append(10)
            notes.append(f"Future mode: missing TEL service for {sorted(missing)} (violates Rule 10).")

    return {
        "consistent": len(violations) == 0,
        "violations": sorted(set(violations)),
        "notes": notes
    }


# ----------------------------
# Example: implement your scenarios as data
# ----------------------------
def run_scenario(title: str, sc: Scenario, routes: List[Route]):
    print(f"\n=== {title} ===")

    adv = check_advisory_consistency(sc)
    print("Advisories:", "Consistent" if adv["consistent"] else "Inconsistent")
    if adv["violations"]:
        print("Advisory rule violations:", adv["violations"])
    for n in adv["notes"]:
        print("-", n)

    for r in routes:
        res = evaluate_route(r, sc)
        if res["valid"] and res["warning"]:
            rv = "Valid (Warning)"
        else:
            rv = "Valid" if res["valid"] else "Invalid"

        print(f"\nRoute '{r.name}': {rv}")
        if res["violations"]:
            print("Route rule violations:", res["violations"])
        for n in res["notes"]:
            print("-", n)


if __name__ == "__main__":
    # Scenario 1 example (A1)
    sc1 = Scenario(
        mode="today",
        status="normal",
        exists={"TanahMerah", "Expo", "ChangiAirport"},
        open_stations={"TanahMerah", "Expo", "ChangiAirport"},
        open_edges={("TanahMerah","Expo"), ("Expo","ChangiAirport")},
        integration_works=False,
        recommended_routes=set()
    )
    r1 = Route(name="EWL_AirportBranch", stations=["TanahMerah","Expo","ChangiAirport"])
    run_scenario("Scenario 1 (A1)", sc1, [r1])

    # Scenario 2 example (A2)
    sc2 = Scenario(
        mode="today",
        status="normal",
        exists={"SungeiBedok", "TanahMerah", "Expo", "ChangiAirport"},  # notice: no T5
        open_stations={"SungeiBedok","TanahMerah","Expo","ChangiAirport"},
        open_edges={("TanahMerah","Expo"), ("Expo","ChangiAirport")},
        integration_works=False
    )
    r2 = Route(name="Future_TEL_To_T5", stations=["SungeiBedok","T5","TanahMerah"])
    run_scenario("Scenario 2 (A2)", sc2, [r2])

    # Scenario 3 example (A3)
    sc3 = Scenario(
        mode="today",
        status="normal",
        exists={"TanahMerah", "Expo", "ChangiAirport"},
        open_stations={"TanahMerah","Expo","ChangiAirport"},
        open_edges={("TanahMerah","Expo"), ("Expo","ChangiAirport")}
    )
    r3 = Route(name="Direct_TanahMerah_To_Changi", stations=["TanahMerah","ChangiAirport"])
    run_scenario("Scenario 3 (A3)", sc3, [r3])

    # Scenario 4 example (A4)
    sc4 = Scenario(
        mode="future",
        status="normal",
        exists={"SungeiBedok", "T5", "TanahMerah"},
        open_stations={"SungeiBedok","T5","TanahMerah"},
        open_edges={("SungeiBedok","T5"), ("T5","TanahMerah")}
    )
    r4 = Route(name="Future_TEL_To_T5", stations=["SungeiBedok","T5","TanahMerah"])
    run_scenario("Scenario 4 (A4)", sc4, [r4])

    # Scenario 5 example (A5)
    sc5 = Scenario(
        mode="future",
        status="delay",  # implies corridor restricted -> integration works
        exists={"TanahMerah", "Expo", "ChangiAirport"},
        open_stations={"TanahMerah","Expo","ChangiAirport"},
        open_edges={("TanahMerah","Expo"), ("Expo","ChangiAirport")},
        integration_works=True,
        recommended_routes={"EWL_AirportBranch"}  # triggers Rule 7 inconsistency
    )
    r5 = Route(name="EWL_AirportBranch", stations=["TanahMerah","Expo","ChangiAirport"])
    run_scenario("Scenario 5 (A5)", sc5, [r5])