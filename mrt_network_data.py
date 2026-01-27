"""
MRT Network Data Configuration
Contains station coordinates and network connections for both Today and Future modes
"""

# Station coordinates (latitude, longitude)
# Used for heuristic calculation in pathfinding algorithms
STATION_COORDINATES = {
    # East-West Line & TEL stations
    "Changi Airport": (1.3574, 103.9886),
    "Expo": (1.3352, 103.9615),
    "Tanah Merah": (1.3274, 103.9465),
    "Bedok": (1.3240, 103.9300),
    "Kembangan": (1.3208, 103.9132),
    "Eunos": (1.3199, 103.9033),
    "Paya Lebar": (1.3177, 103.8926),
    "Aljunied": (1.3165, 103.8827),
    "Kallang": (1.3114, 103.8714),
    "Lavender": (1.3075, 103.8631),
    "Bugis": (1.3001, 103.8560),
    "City Hall": (1.2932, 103.8520),
    "Raffles Place": (1.2839, 103.8512),
    "Tanjong Pagar": (1.2764, 103.8458),
    "Outram Park": (1.2801, 103.8397),
    "Tiong Bahru": (1.2862, 103.8269),
    "Redhill": (1.2897, 103.8168),
    "Queenstown": (1.2943, 103.8059),
    "Commonwealth": (1.3025, 103.7980),
    "Buona Vista": (1.3071, 103.7906),
    "Dover": (1.3113, 103.7785),
    "Clementi": (1.3150, 103.7654),
    "Chinese Garden": (1.3422, 103.7324),
    "Lakeside": (1.3446, 103.7208),
    "Boon Lay": (1.3386, 103.7060),
    "Jurong East": (1.3332, 103.7424),
    
    # North-South Line
    "Bishan": (1.3509, 103.8484),
    "Ang Mo Kio": (1.3700, 103.8495),
    "Yio Chu Kang": (1.3819, 103.8450),
    "Orchard": (1.3041, 103.8320),
    "Somerset": (1.3004, 103.8390),
    "Dhoby Ghaut": (1.2989, 103.8456),
    "Marina Bay": (1.2760, 103.8544),
    "Marina South Pier": (1.2710, 103.8630),
    
    # Circle Line
    "HarbourFront": (1.2653, 103.8219),
    "Telok Blangah": (1.2706, 103.8096),
    "Labrador Park": (1.2722, 103.8023),
    "Pasir Panjang": (1.2762, 103.7915),
    "Haw Par Villa": (1.2824, 103.7818),
    "Kent Ridge": (1.2934, 103.7846),
    "one-north": (1.2999, 103.7873),
    "Botanic Gardens": (1.3226, 103.8154),
    "Farrer Road": (1.3172, 103.8071),
    "Holland Village": (1.3118, 103.7958),
    "Serangoon": (1.3496, 103.8736),
    "Bartley": (1.3425, 103.8792),
    "Tai Seng": (1.3358, 103.8877),
    "MacPherson": (1.3269, 103.8900),
    "Dakota": (1.3083, 103.8877),
    "Mountbatten": (1.3066, 103.8824),
    "Stadium": (1.3030, 103.8753),
    "Nicoll Highway": (1.2998, 103.8634),
    "Promenade": (1.2930, 103.8611),
    "Esplanade": (1.2935, 103.8555),
    "Bras Basah": (1.2968, 103.8507),
    
    # Downtown Line
    "Chinatown": (1.2845, 103.8440),
    "Telok Ayer": (1.2823, 103.8484),
    "Downtown": (1.2795, 103.8524),
    "Bayfront": (1.2820, 103.8594),
    "Gardens by the Bay": (1.2815, 103.8636),
    
    # Thomson-East Coast Line
    "Sungei Bedok": (1.3206, 103.9449),
    "Bayshore": (1.3451, 103.9733),
    "Upper Changi": (1.3427, 103.9614),
    "Tanjong Rhu": (1.2943, 103.8689),
    "Katong Park": (1.3010, 103.8891),
    "Tanjong Katong": (1.3051, 103.8951),
    "Marine Parade": (1.3018, 103.9063),
    "Marine Terrace": (1.3062, 103.9153),
    "Siglap": (1.3134, 103.9279),
    "Bedok South": (1.3212, 103.9392),
    
    # Future stations
    "Changi Terminal 5": (1.3650, 104.0200),  # Approximate future location
    
    # Cross Island Line (future)
    "Punggol": (1.4054, 103.9022),
    "Pasir Ris": (1.3730, 103.9492),
}

# Network connections for TODAY MODE (current network)
# Format: List of (station1, station2, travel_time_minutes, line_code)
TODAY_MODE_CONNECTIONS = [
    # East-West Line (Green) - Airport Branch
    ("Pasir Ris", "Tanah Merah", 3, "EWL"),
    ("Tanah Merah", "Expo", 3, "EWL"),
    ("Expo", "Changi Airport", 3, "EWL"),
    
    # East-West Line - Main Trunk
    ("Tanah Merah", "Bedok", 2, "EWL"),
    ("Bedok", "Kembangan", 2, "EWL"),
    ("Kembangan", "Eunos", 2, "EWL"),
    ("Eunos", "Paya Lebar", 2, "EWL"),
    ("Paya Lebar", "Aljunied", 2, "EWL"),
    ("Aljunied", "Kallang", 2, "EWL"),
    ("Kallang", "Lavender", 2, "EWL"),
    ("Lavender", "Bugis", 2, "EWL"),
    ("Bugis", "City Hall", 2, "EWL"),
    ("City Hall", "Raffles Place", 2, "EWL"),
    ("Raffles Place", "Tanjong Pagar", 2, "EWL"),
    ("Tanjong Pagar", "Outram Park", 2, "EWL"),
    ("Outram Park", "Tiong Bahru", 2, "EWL"),
    ("Tiong Bahru", "Redhill", 2, "EWL"),
    ("Redhill", "Queenstown", 2, "EWL"),
    ("Queenstown", "Commonwealth", 2, "EWL"),
    ("Commonwealth", "Buona Vista", 2, "EWL"),
    ("Buona Vista", "Dover", 2, "EWL"),
    ("Dover", "Clementi", 2, "EWL"),
    ("Clementi", "Jurong East", 2, "EWL"),
    ("Jurong East", "Chinese Garden", 2, "EWL"),
    ("Chinese Garden", "Lakeside", 2, "EWL"),
    ("Lakeside", "Boon Lay", 2, "EWL"),
    
    # North-South Line (Red)
    ("Marina South Pier", "Marina Bay", 2, "NSL"),
    ("Marina Bay", "Raffles Place", 2, "NSL"),
    ("Raffles Place", "City Hall", 2, "NSL"),
    ("City Hall", "Dhoby Ghaut", 2, "NSL"),
    ("Dhoby Ghaut", "Somerset", 2, "NSL"),
    ("Somerset", "Orchard", 2, "NSL"),
    ("Orchard", "Bishan", 2, "NSL"),
    ("Bishan", "Ang Mo Kio", 2, "NSL"),
    ("Ang Mo Kio", "Yio Chu Kang", 2, "NSL"),
    
    # Circle Line (Yellow/Orange)
    ("HarbourFront", "Telok Blangah", 2, "CCL"),
    ("Telok Blangah", "Labrador Park", 2, "CCL"),
    ("Labrador Park", "Pasir Panjang", 2, "CCL"),
    ("Pasir Panjang", "Haw Par Villa", 2, "CCL"),
    ("Haw Par Villa", "Kent Ridge", 2, "CCL"),
    ("Kent Ridge", "one-north", 2, "CCL"),
    ("one-north", "Buona Vista", 2, "CCL"),
    ("Buona Vista", "Botanic Gardens", 2, "CCL"),
    ("Botanic Gardens", "Farrer Road", 2, "CCL"),
    ("Farrer Road", "Holland Village", 2, "CCL"),
    ("Holland Village", "Dhoby Ghaut", 2, "CCL"),
    ("Dhoby Ghaut", "Bras Basah", 2, "CCL"),
    ("Bras Basah", "Esplanade", 2, "CCL"),
    ("Esplanade", "Promenade", 2, "CCL"),
    ("Promenade", "Nicoll Highway", 2, "CCL"),
    ("Nicoll Highway", "Stadium", 2, "CCL"),
    ("Stadium", "Mountbatten", 2, "CCL"),
    ("Mountbatten", "Dakota", 2, "CCL"),
    ("Dakota", "Paya Lebar", 2, "CCL"),
    ("Paya Lebar", "MacPherson", 2, "CCL"),
    ("MacPherson", "Tai Seng", 2, "CCL"),
    ("Tai Seng", "Bartley", 2, "CCL"),
    ("Bartley", "Serangoon", 2, "CCL"),
    
    # Downtown Line (Blue)
    ("Chinatown", "Telok Ayer", 2, "DTL"),
    ("Telok Ayer", "Downtown", 2, "DTL"),
    ("Downtown", "Bayfront", 2, "DTL"),
    ("Bayfront", "Gardens by the Bay", 2, "DTL"),
    
    # Thomson-East Coast Line (Brown) - Current sections
    ("Sungei Bedok", "Bedok South", 2, "TEL"),
    ("Bedok South", "Siglap", 2, "TEL"),
    ("Siglap", "Marine Terrace", 2, "TEL"),
    ("Marine Terrace", "Marine Parade", 2, "TEL"),
    ("Marine Parade", "Tanjong Katong", 2, "TEL"),
    ("Tanjong Katong", "Katong Park", 2, "TEL"),
    ("Katong Park", "Tanjong Rhu", 2, "TEL"),
]

# Additional connections for FUTURE MODE (with TELe and CRL)
# These will be added to TODAY_MODE_CONNECTIONS
FUTURE_MODE_ADDITIONAL_CONNECTIONS = [
    # TELe Extension: Sungei Bedok → T5 → Tanah Merah
    ("Sungei Bedok", "Bayshore", 3, "TEL"),
    ("Bayshore", "Changi Terminal 5", 3, "TEL"),
    ("Changi Terminal 5", "Upper Changi", 3, "TEL"),
    ("Upper Changi", "Expo", 3, "TEL"),
    ("Expo", "Tanah Merah", 3, "TEL"),
    
    # Convert Expo-Changi Airport to TEL (replaces EWL connection)
    ("Expo", "Changi Airport", 3, "TEL"),
    
    # CRL Extension to T5
    ("Punggol", "Pasir Ris", 4, "CRL"),
    ("Pasir Ris", "Changi Terminal 5", 4, "CRL"),
]

# Connections to remove in FUTURE MODE (converted from EWL to TEL)
FUTURE_MODE_REMOVED_CONNECTIONS = [
    ("Expo", "Changi Airport", "EWL"),  # This becomes TEL in future
]

# Recommended test origin-destination pairs
TEST_PAIRS_TODAY = [
    ("Changi Airport", "City Hall"),
    ("Changi Airport", "Orchard"),
    ("Changi Airport", "Gardens by the Bay"),
]

TEST_PAIRS_FUTURE = [
    ("Changi Airport", "City Hall"),
    ("Changi Airport", "Orchard"),
    ("Changi Airport", "Gardens by the Bay"),
    ("Paya Lebar", "Changi Terminal 5"),
    ("HarbourFront", "Changi Terminal 5"),
    ("Bishan", "Changi Terminal 5"),
    ("Tanah Merah", "Changi Terminal 5"),
]

# Cost parameters
TRANSFER_PENALTY_MINUTES = 3  # Time penalty when changing lines
BASE_TRAVEL_TIME_SHORT = 2    # Minutes between nearby stations
BASE_TRAVEL_TIME_MEDIUM = 3   # Minutes between medium distance stations
BASE_TRAVEL_TIME_LONG = 4     # Minutes between distant stations

# Heuristic parameters
AVERAGE_MRT_SPEED_KMH = 60    # Average MRT speed for heuristic calculation
EARTH_RADIUS_KM = 6371        # Earth radius for Haversine formula

# Line colors for visualization (optional)
LINE_COLORS = {
    "EWL": "Green",
    "NSL": "Red",
    "CCL": "Yellow",
    "DTL": "Blue",
    "TEL": "Brown",
    "CRL": "Orange",
}

# Line names
LINE_NAMES = {
    "EWL": "East-West Line",
    "NSL": "North-South Line",
    "CCL": "Circle Line",
    "DTL": "Downtown Line",
    "TEL": "Thomson-East Coast Line",
    "CRL": "Cross Island Line",
}