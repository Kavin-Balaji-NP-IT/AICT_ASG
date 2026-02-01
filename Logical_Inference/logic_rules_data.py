"""
Task 2: Logical Inference Data
Contains logical rules, symbols, and test scenarios for service advisory consistency checking
"""

# =============================================================================
# PROPOSITIONAL SYMBOLS DEFINITION
# =============================================================================

# Symbol naming convention:
# - Station status: station_operational_<CODE>
# - Line status: line_operational_<LINE>
# - Advisory status: advisory_<TYPE>_<LOCATION>
# - Route validity: route_valid_<FROM>_<TO>
# - Service level: service_<LEVEL>_<LOCATION>
# - Mode: mode_<MODE>

# Example symbols and their meanings
SYMBOL_DEFINITIONS = {
    # Station operational status
    "station_operational_CA": "Changi Airport station is operational",
    "station_operational_T5": "Changi Terminal 5 station is operational",
    "station_operational_TM": "Tanah Merah station is operational",
    "station_operational_EXP": "Expo station is operational",
    "station_operational_PL": "Paya Lebar station is operational",
    "station_operational_CH": "City Hall station is operational",
    
    # Line operational status
    "line_operational_EWL": "East-West Line is fully operational",
    "line_operational_TEL": "Thomson-East Coast Line is fully operational",
    "line_operational_CRL": "Cross Island Line is fully operational",
    "line_operational_NSL": "North-South Line is fully operational",
    "line_operational_CCL": "Circle Line is fully operational",
    
    # Service level
    "service_normal_airport_corridor": "Normal service in airport corridor",
    "service_reduced_airport_corridor": "Reduced service in airport corridor",
    "service_suspended_TM_EXP": "Service suspended between Tanah Merah and Expo",
    "service_suspended_EXP_CA": "Service suspended between Expo and Changi Airport",
    
    # Network mode
    "mode_today": "Network is in Today mode (current configuration)",
    "mode_future": "Network is in Future mode (with TELe/CRL)",
    
    # Systems integration work
    "systems_integration_active": "Systems integration work is ongoing",
    "platform_conversion_TM": "Platform conversion work at Tanah Merah",
    "platform_conversion_EXP": "Platform conversion work at Expo",
    "platform_conversion_CA": "Platform conversion work at Changi Airport",
    
    # Transfer availability
    "transfer_available_TM": "Transfer available at Tanah Merah",
    "transfer_available_PL": "Transfer available at Paya Lebar",
    "transfer_available_BV": "Transfer available at Buona Vista",
    
    # Route validity
    "route_valid_CA_CH": "Route from Changi Airport to City Hall is valid",
    "route_valid_T5_PL": "Route from Terminal 5 to Paya Lebar is valid",
    "route_via_TM": "Route goes through Tanah Merah",
    "route_via_EXP": "Route goes through Expo",
    
    # Service advisories
    "advisory_avoid_EWL_airport": "Advisory to avoid EWL airport branch",
    "advisory_use_alternative_route": "Advisory to use alternative route",
    "advisory_expect_delays": "Advisory to expect delays",
    "advisory_no_service_CA": "Advisory of no service to Changi Airport",
    
    # Peak hour status
    "peak_hour": "Currently peak hour",
    "off_peak": "Currently off-peak hour",
    
    # Additional service status
    "bus_bridging_active": "Bus bridging service is active",
    "shuttle_service_active": "Shuttle train service is active",
}

# =============================================================================
# LOGICAL RULES
# =============================================================================

# Rules are represented as implications: (premises, conclusion)
# Premises is a list of symbols (all must be true)
# Conclusion is a single symbol
# Use '~' prefix to negate a symbol

LOGICAL_RULES = [
    # Rule 1: If systems integration is active, then service is reduced in airport corridor
    {
        "id": "R1",
        "description": "Systems integration work causes reduced service",
        "premises": ["systems_integration_active"],
        "conclusion": "service_reduced_airport_corridor",
        "plain_english": "If systems integration work is ongoing, then service is reduced in the airport corridor"
    },
    
    # Rule 2: If service is suspended between stations, the line is not fully operational
    {
        "id": "R2",
        "description": "Suspended segment means line not fully operational",
        "premises": ["service_suspended_TM_EXP"],
        "conclusion": "~line_operational_EWL",
        "plain_english": "If service is suspended between Tanah Merah and Expo, then EWL is not fully operational"
    },
    
    # Rule 3: Platform conversion at a station means that station requires reduced service
    {
        "id": "R3",
        "description": "Platform conversion requires service adjustment",
        "premises": ["platform_conversion_TM"],
        "conclusion": "service_reduced_airport_corridor",
        "plain_english": "If platform conversion is happening at Tanah Merah, then service is reduced in airport corridor"
    },
    
    # Rule 4: Terminal 5 only exists in future mode
    {
        "id": "R4",
        "description": "T5 requires future mode",
        "premises": ["station_operational_T5"],
        "conclusion": "mode_future",
        "plain_english": "If Terminal 5 station is operational, then the network must be in Future mode"
    },
    
    # Rule 5: If today mode is active, T5 cannot be operational
    {
        "id": "R5",
        "description": "T5 doesn't exist in today mode",
        "premises": ["mode_today"],
        "conclusion": "~station_operational_T5",
        "plain_english": "If network is in Today mode, then Terminal 5 station cannot be operational"
    },
    
    # Rule 6: Route to Changi Airport requires either EWL or TEL operational
    {
        "id": "R6",
        "description": "Airport access requires operational line",
        "premises": ["route_valid_CA_CH", "~line_operational_EWL"],
        "conclusion": "line_operational_TEL",
        "plain_english": "If route to Changi Airport is valid and EWL is not operational, then TEL must be operational"
    },
    
    # Rule 7: If service is suspended to Changi Airport, route to CA is not valid
    {
        "id": "R7",
        "description": "No service means no valid route",
        "premises": ["service_suspended_EXP_CA"],
        "conclusion": "~route_valid_CA_CH",
        "plain_english": "If service is suspended between Expo and Changi Airport, then route to CA is not valid"
    },
    
    # Rule 8: Bus bridging active implies service suspended on some segment
    {
        "id": "R8",
        "description": "Bus bridging indicates service disruption",
        "premises": ["bus_bridging_active"],
        "conclusion": "service_reduced_airport_corridor",
        "plain_english": "If bus bridging service is active, then normal service is disrupted in airport corridor"
    },
    
    # Rule 9: Normal service and reduced service are mutually exclusive
    {
        "id": "R9",
        "description": "Service levels are mutually exclusive",
        "premises": ["service_normal_airport_corridor"],
        "conclusion": "~service_reduced_airport_corridor",
        "plain_english": "If service is normal in airport corridor, then service cannot be reduced"
    },
    
    # Rule 10: Multiple platform conversions require systems integration
    {
        "id": "R10",
        "description": "Platform conversions are part of systems integration",
        "premises": ["platform_conversion_TM", "platform_conversion_EXP"],
        "conclusion": "systems_integration_active",
        "plain_english": "If platform conversions are happening at both Tanah Merah and Expo, then systems integration work is active"
    },
    
    # Rule 11: CRL operational implies future mode
    {
        "id": "R11",
        "description": "CRL only exists in future",
        "premises": ["line_operational_CRL"],
        "conclusion": "mode_future",
        "plain_english": "If Cross Island Line is operational, then network must be in Future mode"
    },
    
    # Rule 12: Future mode and today mode are mutually exclusive
    {
        "id": "R12",
        "description": "Network modes are mutually exclusive",
        "premises": ["mode_future"],
        "conclusion": "~mode_today",
        "plain_english": "If network is in Future mode, then it cannot be in Today mode"
    },
    
    # Rule 13: If station is not operational, routes through it are invalid
    {
        "id": "R13",
        "description": "Non-operational station blocks routes",
        "premises": ["~station_operational_TM", "route_via_TM"],
        "conclusion": "~route_valid_CA_CH",
        "plain_english": "If Tanah Merah station is not operational and route goes through TM, then route is not valid"
    },
    
    # Rule 14: Peak hour with reduced service requires advisory
    {
        "id": "R14",
        "description": "Peak hour disruption requires advisory",
        "premises": ["peak_hour", "service_reduced_airport_corridor"],
        "conclusion": "advisory_expect_delays",
        "plain_english": "If it's peak hour and service is reduced, then advisory to expect delays should be issued"
    },
]

# =============================================================================
# TEST SCENARIOS
# =============================================================================

TEST_SCENARIOS = [
    # Scenario 1: Valid - Today mode normal operations
    {
        "id": "S1",
        "name": "Today Mode - Normal Operations",
        "mode": "today",
        "description": "Normal operations in today's network",
        "facts": [
            "mode_today",
            "line_operational_EWL",
            "station_operational_CA",
            "station_operational_TM",
            "service_normal_airport_corridor",
            "route_valid_CA_CH",
        ],
        "expected_result": "valid",
        "expected_inferences": [
            "~station_operational_T5",  # From R5
            "~service_reduced_airport_corridor",  # From R9
            "~mode_future",  # From R12
        ]
    },
    
    # Scenario 2: Invalid - Contradictory service levels
    {
        "id": "S2",
        "name": "Invalid - Contradictory Service Levels",
        "mode": "today",
        "description": "Claims both normal and reduced service simultaneously",
        "facts": [
            "service_normal_airport_corridor",
            "service_reduced_airport_corridor",
        ],
        "expected_result": "invalid",
        "violated_rules": ["R9"],
        "explanation": "Rule R9 states normal and reduced service are mutually exclusive"
    },
    
    # Scenario 3: Valid - Future mode with T5 operational
    {
        "id": "S3",
        "name": "Future Mode - T5 Operational",
        "mode": "future",
        "description": "Terminal 5 operational in future mode",
        "facts": [
            "mode_future",
            "station_operational_T5",
            "line_operational_TEL",
            "line_operational_CRL",
            "route_valid_T5_PL",
        ],
        "expected_result": "valid",
        "expected_inferences": [
            "~mode_today",  # From R12
        ]
    },
    
    # Scenario 4: Invalid - T5 operational in today mode
    {
        "id": "S4",
        "name": "Invalid - T5 in Today Mode",
        "mode": "today",
        "description": "Claims T5 is operational in today mode (impossible)",
        "facts": [
            "mode_today",
            "station_operational_T5",
        ],
        "expected_result": "invalid",
        "violated_rules": ["R5"],
        "explanation": "Rule R5 states T5 cannot be operational in Today mode"
    },
    
    # Scenario 5: Valid with inference - Systems integration work
    {
        "id": "S5",
        "name": "Future Mode - Systems Integration Active",
        "mode": "future",
        "description": "Systems integration work causing service adjustments",
        "facts": [
            "mode_future",
            "systems_integration_active",
            "platform_conversion_TM",
            "platform_conversion_EXP",
        ],
        "expected_result": "valid",
        "expected_inferences": [
            "service_reduced_airport_corridor",  # From R1
            "~service_normal_airport_corridor",  # Derived from reduced service
        ]
    },
    
    # Scenario 6: Invalid - Contradictory mode claims
    {
        "id": "S6",
        "name": "Invalid - Both Modes Active",
        "mode": "invalid",
        "description": "Claims both today and future mode simultaneously",
        "facts": [
            "mode_today",
            "mode_future",
        ],
        "expected_result": "invalid",
        "violated_rules": ["R12"],
        "explanation": "Rule R12 states future and today modes are mutually exclusive"
    },
    
    # Scenario 7: Valid - Bus bridging during disruption
    {
        "id": "S7",
        "name": "Today Mode - Bus Bridging Active",
        "mode": "today",
        "description": "Bus bridging service during disruption",
        "facts": [
            "mode_today",
            "bus_bridging_active",
            "service_suspended_TM_EXP",
            "peak_hour",
        ],
        "expected_result": "valid",
        "expected_inferences": [
            "service_reduced_airport_corridor",  # From R8
            "~line_operational_EWL",  # From R2
            "advisory_expect_delays",  # From R14
        ]
    },
    
    # Scenario 8: Invalid - Service suspended but line claims to be operational
    {
        "id": "S8",
        "name": "Invalid - Suspended Service with Operational Line",
        "mode": "today",
        "description": "Claims line is operational despite suspended segment",
        "facts": [
            "service_suspended_TM_EXP",
            "line_operational_EWL",
        ],
        "expected_result": "invalid",
        "violated_rules": ["R2"],
        "explanation": "Rule R2 states suspended segment means line is not fully operational"
    },
    
    # Scenario 9: Valid - CRL in future mode
    {
        "id": "S9",
        "name": "Future Mode - CRL Extension Active",
        "mode": "future",
        "description": "Cross Island Line operational to T5",
        "facts": [
            "line_operational_CRL",
            "station_operational_T5",
        ],
        "expected_result": "valid",
        "expected_inferences": [
            "mode_future",  # From R11 and R4
            "~mode_today",  # From R12
        ]
    },
    
    # Scenario 10: Complex valid scenario - Peak hour disruption with advisories
    {
        "id": "S10",
        "name": "Future Mode - Peak Hour Disruption with Multiple Factors",
        "mode": "future",
        "description": "Complex scenario with systems integration during peak hour",
        "facts": [
            "mode_future",
            "peak_hour",
            "platform_conversion_TM",
            "platform_conversion_EXP",
            "station_operational_T5",
            "line_operational_CRL",
        ],
        "expected_result": "valid",
        "expected_inferences": [
            "systems_integration_active",  # From R10
            "service_reduced_airport_corridor",  # From R1
            "advisory_expect_delays",  # From R14
            "~mode_today",  # From R12
        ]
    },
]

# =============================================================================
# ADDITIONAL CONFIGURATION
# =============================================================================

# Stations that only exist in future mode
FUTURE_ONLY_STATIONS = ["T5"]

# Lines that only exist in future mode
FUTURE_ONLY_LINES = ["CRL"]

# Service level hierarchy (mutually exclusive)
SERVICE_LEVELS = [
    "service_normal_airport_corridor",
    "service_reduced_airport_corridor",
]

# Network modes (mutually exclusive)
NETWORK_MODES = [
    "mode_today",
    "mode_future",
]
