"""
Complete Singapore MRT Dataset
Including all operational and future lines with station coordinates and connections
"""

STATION_COORDINATES = {
    # ============ EAST-WEST LINE (EWL) - Green ============
    # Main trunk (West to East)
    "Pasir Ris": (1.3730, 103.9492),
    "Tanah Merah": (1.3274, 103.9465),
    "Simei": (1.3434, 103.9533),
    "Tampines": (1.3537, 103.9453),
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
    "Jurong East": (1.3332, 103.7424),
    "Chinese Garden": (1.3422, 103.7324),
    "Lakeside": (1.3446, 103.7208),
    "Boon Lay": (1.3386, 103.7060),
    "Pioneer": (1.3378, 103.6975),
    "Joo Koon": (1.3277, 103.6782),
    "Gul Circle": (1.3193, 103.6605),
    "Tuas Crescent": (1.3212, 103.6493),
    "Tuas West Road": (1.3299, 103.6395),
    "Tuas Link": (1.3404, 103.6368),
    
    # Changi Airport Branch
    "Expo": (1.3352, 103.9615),
    "Changi Airport": (1.3574, 103.9886),
    
    # ============ NORTH-SOUTH LINE (NSL) - Red ============
    "Jurong East": (1.3332, 103.7424),  # Already defined (interchange)
    "Bukit Batok": (1.3490, 103.7496),
    "Bukit Gombak": (1.3588, 103.7518),
    "Choa Chu Kang": (1.3854, 103.7443),
    "Yew Tee": (1.3972, 103.7473),
    "Kranji": (1.4251, 103.7619),
    "Marsiling": (1.4326, 103.7738),
    "Woodlands": (1.4370, 103.7865),
    "Admiralty": (1.4406, 103.8009),
    "Sembawang": (1.4491, 103.8201),
    "Canberra": (1.4431, 103.8298),
    "Yishun": (1.4294, 103.8350),
    "Khatib": (1.4172, 103.8329),
    "Yio Chu Kang": (1.3819, 103.8450),
    "Ang Mo Kio": (1.3700, 103.8495),
    "Bishan": (1.3509, 103.8484),
    "Braddell": (1.3403, 103.8468),
    "Toa Payoh": (1.3327, 103.8473),
    "Novena": (1.3203, 103.8438),
    "Newton": (1.3127, 103.8383),
    "Orchard": (1.3041, 103.8320),
    "Somerset": (1.3004, 103.8390),
    "Dhoby Ghaut": (1.2989, 103.8456),
    "City Hall": (1.2932, 103.8520),  # Already defined (interchange)
    "Raffles Place": (1.2839, 103.8512),  # Already defined (interchange)
    "Marina Bay": (1.2760, 103.8544),
    "Marina South Pier": (1.2710, 103.8630),
    
    # ============ NORTH-EAST LINE (NEL) - Purple ============
    "HarbourFront": (1.2653, 103.8219),
    "Outram Park": (1.2801, 103.8397),  # Already defined (interchange)
    "Chinatown": (1.2845, 103.8440),
    "Clarke Quay": (1.2886, 103.8465),
    "Dhoby Ghaut": (1.2989, 103.8456),  # Already defined (interchange)
    "Little India": (1.3068, 103.8492),
    "Farrer Park": (1.3123, 103.8535),
    "Boon Keng": (1.3196, 103.8618),
    "Potong Pasir": (1.3312, 103.8693),
    "Woodleigh": (1.3388, 103.8710),
    "Serangoon": (1.3496, 103.8736),
    "Kovan": (1.3607, 103.8848),
    "Hougang": (1.3711, 103.8924),
    "Buangkok": (1.3828, 103.8929),
    "Sengkang": (1.3916, 103.8951),
    "Punggol": (1.4054, 103.9022),
    
    # ============ CIRCLE LINE (CCL) - Yellow/Orange ============
    "Dhoby Ghaut": (1.2989, 103.8456),  # Already defined (interchange)
    "Bras Basah": (1.2968, 103.8507),
    "Esplanade": (1.2935, 103.8555),
    "Promenade": (1.2930, 103.8611),
    "Nicoll Highway": (1.2998, 103.8634),
    "Stadium": (1.3030, 103.8753),
    "Mountbatten": (1.3066, 103.8824),
    "Dakota": (1.3083, 103.8877),
    "Paya Lebar": (1.3177, 103.8926),  # Already defined (interchange)
    "MacPherson": (1.3269, 103.8900),
    "Tai Seng": (1.3358, 103.8877),
    "Bartley": (1.3425, 103.8792),
    "Serangoon": (1.3496, 103.8736),  # Already defined (interchange)
    "Lorong Chuan": (1.3516, 103.8637),
    "Bishan": (1.3509, 103.8484),  # Already defined (interchange)
    "Marymount": (1.3486, 103.8393),
    "Caldecott": (1.3377, 103.8394),
    "Botanic Gardens": (1.3226, 103.8154),
    "Farrer Road": (1.3172, 103.8071),
    "Holland Village": (1.3118, 103.7958),
    "Buona Vista": (1.3071, 103.7906),  # Already defined (interchange)
    "one-north": (1.2999, 103.7873),
    "Kent Ridge": (1.2934, 103.7846),
    "Haw Par Villa": (1.2824, 103.7818),
    "Pasir Panjang": (1.2762, 103.7915),
    "Labrador Park": (1.2722, 103.8023),
    "Telok Blangah": (1.2706, 103.8096),
    "HarbourFront": (1.2653, 103.8219),  # Already defined (interchange)
    
    # Circle Line Extension (CCL6)
    "Marina Bay": (1.2760, 103.8544),  # Already defined (interchange)
    "Bayfront": (1.2820, 103.8594),
    
    # ============ DOWNTOWN LINE (DTL) - Blue ============
    "Bukit Panjang": (1.3790, 103.7619),
    "Cashew": (1.3692, 103.7643),
    "Hillview": (1.3626, 103.7675),
    "Beauty World": (1.3414, 103.7758),
    "King Albert Park": (1.3353, 103.7835),
    "Sixth Avenue": (1.3306, 103.7968),
    "Tan Kah Kee": (1.3257, 103.8072),
    "Botanic Gardens": (1.3226, 103.8154),  # Already defined (interchange)
    "Stevens": (1.3198, 103.8256),
    "Newton": (1.3127, 103.8383),  # Already defined (interchange)
    "Little India": (1.3068, 103.8492),  # Already defined (interchange)
    "Rochor": (1.3038, 103.8519),
    "Bugis": (1.3001, 103.8560),  # Already defined (interchange)
    "Promenade": (1.2930, 103.8611),  # Already defined (interchange)
    "Bayfront": (1.2820, 103.8594),  # Already defined (interchange)
    "Downtown": (1.2795, 103.8524),
    "Telok Ayer": (1.2823, 103.8484),
    "Chinatown": (1.2845, 103.8440),  # Already defined (interchange)
    "Fort Canning": (1.2918, 103.8444),
    "Bencoolen": (1.2989, 103.8509),
    "Jalan Besar": (1.3053, 103.8556),
    "Bendemeer": (1.3140, 103.8620),
    "Geylang Bahru": (1.3212, 103.8713),
    "Mattar": (1.3266, 103.8829),
    "MacPherson": (1.3269, 103.8900),  # Already defined (interchange)
    "Ubi": (1.3300, 103.8994),
    "Kaki Bukit": (1.3347, 103.9080),
    "Bedok North": (1.3347, 103.9177),
    "Bedok Reservoir": (1.3370, 103.9322),
    "Tampines West": (1.3452, 103.9383),
    "Tampines": (1.3537, 103.9453),  # Already defined (interchange)
    "Tampines East": (1.3562, 103.9546),
    "Upper Changi": (1.3427, 103.9614),
    "Expo": (1.3352, 103.9615),  # Already defined (interchange)
    
    # Downtown Line Extension (DTL3e)
    "Sungei Bedok": (1.3206, 103.9449),
    
    # ============ THOMSON-EAST COAST LINE (TEL) - Brown ============
    # Thomson Line Section
    "Woodlands North": (1.4481, 103.7850),
    "Woodlands": (1.4370, 103.7865),  # Already defined (interchange)
    "Woodlands South": (1.4279, 103.7948),
    "Springleaf": (1.4172, 103.8179),
    "Lentor": (1.3849, 103.8364),
    "Mayflower": (1.3654, 103.8363),
    "Bright Hill": (1.3620, 103.8321),
    "Upper Thomson": (1.3548, 103.8301),
    "Caldecott": (1.3377, 103.8394),  # Already defined (interchange)
    "Mount Pleasant": (1.3265, 103.8349),
    "Stevens": (1.3198, 103.8256),  # Already defined (interchange)
    "Napier": (1.3117, 103.8140),
    "Orchard Boulevard": (1.3025, 103.8227),
    "Orchard": (1.3041, 103.8320),  # Already defined (interchange)
    "Great World": (1.2935, 103.8324),
    "Havelock": (1.2887, 103.8350),
    "Outram Park": (1.2801, 103.8397),  # Already defined (interchange)
    "Maxwell": (1.2803, 103.8438),
    "Shenton Way": (1.2791, 103.8493),
    "Marina Bay": (1.2760, 103.8544),  # Already defined (interchange)
    "Marina South": (1.2706, 103.8635),
    "Gardens by the Bay": (1.2815, 103.8636),
    
    # East Coast Line Section
    "Founders' Memorial": (1.2840, 103.8698),
    "Tanjong Rhu": (1.2943, 103.8689),
    "Katong Park": (1.3010, 103.8891),
    "Tanjong Katong": (1.3051, 103.8951),
    "Marine Parade": (1.3018, 103.9063),
    "Marine Terrace": (1.3062, 103.9153),
    "Siglap": (1.3134, 103.9279),
    "Bayshore": (1.3451, 103.9733),
    "Bedok South": (1.3212, 103.9392),
    "Sungei Bedok": (1.3206, 103.9449),  # Already defined (interchange)
    
    # ============ FUTURE: CROSS ISLAND LINE (CRL) - Green (anticipated) ============
    "Punggol": (1.4054, 103.9022),  # Already defined (interchange)
    "Pasir Ris": (1.3730, 103.9492),  # Already defined (interchange)
    "Loyang": (1.3689, 103.9732),
    "Changi Terminal 5": (1.3650, 104.0200),  # Future terminal
    
    # ============ BUKIT PANJANG LRT (BPLRT) - Grey ============
    "Choa Chu Kang": (1.3854, 103.7443),  # Already defined (interchange)
    "South View": (1.3800, 103.7445),
    "Keat Hong": (1.3785, 103.7489),
    "Teck Whye": (1.3765, 103.7528),
    "Phoenix": (1.3788, 103.7586),
    "Bukit Panjang": (1.3790, 103.7619),  # Already defined (interchange)
    "Petir": (1.3778, 103.7663),
    "Pending": (1.3764, 103.7708),
    "Bangkit": (1.3798, 103.7725),
    "Fajar": (1.3842, 103.7715),
    "Segar": (1.3876, 103.7694),
    "Jelapang": (1.3864, 103.7642),
    "Senja": (1.3827, 103.7621),
    "Ten Mile Junction": (1.3817, 103.7600),
    
    # ============ SENGKANG-PUNGGOL LRT (SPLRT) - Grey ============
    # Sengkang Loop
    "Sengkang": (1.3916, 103.8951),  # Already defined (interchange)
    "Compassvale": (1.3947, 103.9005),
    "Rumbia": (1.3995, 103.9059),
    "Bakau": (1.4015, 103.9059),
    "Kangkar": (1.4026, 103.9019),
    "Ranggung": (1.4010, 103.8979),
    "Cheng Lim": (1.3960, 103.8937),
    "Farmway": (1.3918, 103.8894),
    "Kupang": (1.3950, 103.8896),
    "Thanggam": (1.3976, 103.8908),
    "Fernvale": (1.3918, 103.8760),
    "Layar": (1.3922, 103.8806),
    "Tongkang": (1.3893, 103.8856),
    
    # Punggol Loop
    "Punggol": (1.4054, 103.9022),  # Already defined (interchange)
    "Cove": (1.3996, 103.9057),
    "Meridian": (1.3975, 103.9089),
    "Coral Edge": (1.3938, 103.9120),
    "Riviera": (1.3914, 103.9113),
    "Kadaloor": (1.3896, 103.9082),
    "Oasis": (1.3920, 103.9026),
    "Damai": (1.3951, 103.9075),
    "Sam Kee": (1.4078, 103.9036),
    "Teck Lee": (1.4105, 103.9057),
    "Punggol Point": (1.4175, 103.9064),
    "Samudera": (1.4150, 103.9020),
    "Nibong": (1.4125, 103.8998),
    "Sumang": (1.4089, 103.8984),
    "Soo Teck": (1.4063, 103.8969),
}

TODAY_MODE_CONNECTIONS = [
    # ============ EAST-WEST LINE (EWL) - Green ============
    # Main trunk (West to East)
    ("Tuas Link", "Tuas West Road", 2, "EWL"),
    ("Tuas West Road", "Tuas Crescent", 2, "EWL"),
    ("Tuas Crescent", "Gul Circle", 2, "EWL"),
    ("Gul Circle", "Joo Koon", 2, "EWL"),
    ("Joo Koon", "Pioneer", 2, "EWL"),
    ("Pioneer", "Boon Lay", 2, "EWL"),
    ("Boon Lay", "Lakeside", 2, "EWL"),
    ("Lakeside", "Chinese Garden", 2, "EWL"),
    ("Chinese Garden", "Jurong East", 2, "EWL"),
    ("Jurong East", "Clementi", 3, "EWL"),
    ("Clementi", "Dover", 2, "EWL"),
    ("Dover", "Buona Vista", 2, "EWL"),
    ("Buona Vista", "Commonwealth", 2, "EWL"),
    ("Commonwealth", "Queenstown", 2, "EWL"),
    ("Queenstown", "Redhill", 2, "EWL"),
    ("Redhill", "Tiong Bahru", 2, "EWL"),
    ("Tiong Bahru", "Outram Park", 2, "EWL"),
    ("Outram Park", "Tanjong Pagar", 2, "EWL"),
    ("Tanjong Pagar", "Raffles Place", 2, "EWL"),
    ("Raffles Place", "City Hall", 2, "EWL"),
    ("City Hall", "Bugis", 2, "EWL"),
    ("Bugis", "Lavender", 2, "EWL"),
    ("Lavender", "Kallang", 2, "EWL"),
    ("Kallang", "Aljunied", 2, "EWL"),
    ("Aljunied", "Paya Lebar", 2, "EWL"),
    ("Paya Lebar", "Eunos", 2, "EWL"),
    ("Eunos", "Kembangan", 2, "EWL"),
    ("Kembangan", "Bedok", 2, "EWL"),
    ("Bedok", "Tanah Merah", 2, "EWL"),
    ("Tanah Merah", "Simei", 2, "EWL"),
    ("Simei", "Tampines", 2, "EWL"),
    ("Tampines", "Pasir Ris", 2, "EWL"),
    
    # Changi Airport Branch
    ("Tanah Merah", "Expo", 3, "EWL"),
    ("Expo", "Changi Airport", 3, "EWL"),
    
    # ============ NORTH-SOUTH LINE (NSL) - Red ============
    ("Jurong East", "Bukit Batok", 2, "NSL"),
    ("Bukit Batok", "Bukit Gombak", 2, "NSL"),
    ("Bukit Gombak", "Choa Chu Kang", 2, "NSL"),
    ("Choa Chu Kang", "Yew Tee", 2, "NSL"),
    ("Yew Tee", "Kranji", 3, "NSL"),
    ("Kranji", "Marsiling", 2, "NSL"),
    ("Marsiling", "Woodlands", 2, "NSL"),
    ("Woodlands", "Admiralty", 2, "NSL"),
    ("Admiralty", "Sembawang", 2, "NSL"),
    ("Sembawang", "Canberra", 2, "NSL"),
    ("Canberra", "Yishun", 2, "NSL"),
    ("Yishun", "Khatib", 2, "NSL"),
    ("Khatib", "Yio Chu Kang", 3, "NSL"),
    ("Yio Chu Kang", "Ang Mo Kio", 2, "NSL"),
    ("Ang Mo Kio", "Bishan", 2, "NSL"),
    ("Bishan", "Braddell", 2, "NSL"),
    ("Braddell", "Toa Payoh", 2, "NSL"),
    ("Toa Payoh", "Novena", 2, "NSL"),
    ("Novena", "Newton", 2, "NSL"),
    ("Newton", "Orchard", 2, "NSL"),
    ("Orchard", "Somerset", 2, "NSL"),
    ("Somerset", "Dhoby Ghaut", 2, "NSL"),
    ("Dhoby Ghaut", "City Hall", 2, "NSL"),
    ("City Hall", "Raffles Place", 2, "NSL"),
    ("Raffles Place", "Marina Bay", 2, "NSL"),
    ("Marina Bay", "Marina South Pier", 2, "NSL"),
    
    # ============ NORTH-EAST LINE (NEL) - Purple ============
    ("HarbourFront", "Outram Park", 3, "NEL"),
    ("Outram Park", "Chinatown", 2, "NEL"),
    ("Chinatown", "Clarke Quay", 2, "NEL"),
    ("Clarke Quay", "Dhoby Ghaut", 2, "NEL"),
    ("Dhoby Ghaut", "Little India", 2, "NEL"),
    ("Little India", "Farrer Park", 2, "NEL"),
    ("Farrer Park", "Boon Keng", 2, "NEL"),
    ("Boon Keng", "Potong Pasir", 2, "NEL"),
    ("Potong Pasir", "Woodleigh", 2, "NEL"),
    ("Woodleigh", "Serangoon", 2, "NEL"),
    ("Serangoon", "Kovan", 2, "NEL"),
    ("Kovan", "Hougang", 2, "NEL"),
    ("Hougang", "Buangkok", 2, "NEL"),
    ("Buangkok", "Sengkang", 2, "NEL"),
    ("Sengkang", "Punggol", 2, "NEL"),
    
    # ============ CIRCLE LINE (CCL) - Yellow/Orange ============
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
    ("Serangoon", "Lorong Chuan", 2, "CCL"),
    ("Lorong Chuan", "Bishan", 2, "CCL"),
    ("Bishan", "Marymount", 2, "CCL"),
    ("Marymount", "Caldecott", 2, "CCL"),
    ("Caldecott", "Botanic Gardens", 2, "CCL"),
    ("Botanic Gardens", "Farrer Road", 2, "CCL"),
    ("Farrer Road", "Holland Village", 2, "CCL"),
    ("Holland Village", "Buona Vista", 2, "CCL"),
    ("Buona Vista", "one-north", 2, "CCL"),
    ("one-north", "Kent Ridge", 2, "CCL"),
    ("Kent Ridge", "Haw Par Villa", 2, "CCL"),
    ("Haw Par Villa", "Pasir Panjang", 2, "CCL"),
    ("Pasir Panjang", "Labrador Park", 2, "CCL"),
    ("Labrador Park", "Telok Blangah", 2, "CCL"),
    ("Telok Blangah", "HarbourFront", 2, "CCL"),
    
    # Circle Line Extension (CCL6)
    ("HarbourFront", "Bayfront", 3, "CCL"),
    ("Bayfront", "Marina Bay", 2, "CCL"),
    
    # ============ DOWNTOWN LINE (DTL) - Blue ============
    ("Bukit Panjang", "Cashew", 2, "DTL"),
    ("Cashew", "Hillview", 2, "DTL"),
    ("Hillview", "Beauty World", 2, "DTL"),
    ("Beauty World", "King Albert Park", 2, "DTL"),
    ("King Albert Park", "Sixth Avenue", 2, "DTL"),
    ("Sixth Avenue", "Tan Kah Kee", 2, "DTL"),
    ("Tan Kah Kee", "Botanic Gardens", 2, "DTL"),
    ("Botanic Gardens", "Stevens", 2, "DTL"),
    ("Stevens", "Newton", 2, "DTL"),
    ("Newton", "Little India", 2, "DTL"),
    ("Little India", "Rochor", 2, "DTL"),
    ("Rochor", "Bugis", 2, "DTL"),
    ("Bugis", "Promenade", 2, "DTL"),
    ("Promenade", "Bayfront", 2, "DTL"),
    ("Bayfront", "Downtown", 2, "DTL"),
    ("Downtown", "Telok Ayer", 2, "DTL"),
    ("Telok Ayer", "Chinatown", 2, "DTL"),
    ("Chinatown", "Fort Canning", 2, "DTL"),
    ("Fort Canning", "Bencoolen", 2, "DTL"),
    ("Bencoolen", "Jalan Besar", 2, "DTL"),
    ("Jalan Besar", "Bendemeer", 2, "DTL"),
    ("Bendemeer", "Geylang Bahru", 2, "DTL"),
    ("Geylang Bahru", "Mattar", 2, "DTL"),
    ("Mattar", "MacPherson", 2, "DTL"),
    ("MacPherson", "Ubi", 2, "DTL"),
    ("Ubi", "Kaki Bukit", 2, "DTL"),
    ("Kaki Bukit", "Bedok North", 2, "DTL"),
    ("Bedok North", "Bedok Reservoir", 2, "DTL"),
    ("Bedok Reservoir", "Tampines West", 2, "DTL"),
    ("Tampines West", "Tampines", 2, "DTL"),
    ("Tampines", "Tampines East", 2, "DTL"),
    ("Tampines East", "Upper Changi", 2, "DTL"),
    ("Upper Changi", "Expo", 2, "DTL"),
    
    # DTL Extension (DTL3e)
    ("Expo", "Sungei Bedok", 2, "DTL"),
    
    # ============ THOMSON-EAST COAST LINE (TEL) - Brown ============
    # Thomson Section
    ("Woodlands North", "Woodlands", 2, "TEL"),
    ("Woodlands", "Woodlands South", 2, "TEL"),
    ("Woodlands South", "Springleaf", 3, "TEL"),
    ("Springleaf", "Lentor", 2, "TEL"),
    ("Lentor", "Mayflower", 2, "TEL"),
    ("Mayflower", "Bright Hill", 2, "TEL"),
    ("Bright Hill", "Upper Thomson", 2, "TEL"),
    ("Upper Thomson", "Caldecott", 2, "TEL"),
    ("Caldecott", "Mount Pleasant", 2, "TEL"),
    ("Mount Pleasant", "Stevens", 2, "TEL"),
    ("Stevens", "Napier", 2, "TEL"),
    ("Napier", "Orchard Boulevard", 2, "TEL"),
    ("Orchard Boulevard", "Orchard", 2, "TEL"),
    ("Orchard", "Great World", 2, "TEL"),
    ("Great World", "Havelock", 2, "TEL"),
    ("Havelock", "Outram Park", 2, "TEL"),
    ("Outram Park", "Maxwell", 2, "TEL"),
    ("Maxwell", "Shenton Way", 2, "TEL"),
    ("Shenton Way", "Marina Bay", 2, "TEL"),
    ("Marina Bay", "Marina South", 2, "TEL"),
    ("Marina South", "Gardens by the Bay", 2, "TEL"),
    
    # East Coast Section
    ("Gardens by the Bay", "Founders' Memorial", 2, "TEL"),
    ("Founders' Memorial", "Tanjong Rhu", 2, "TEL"),
    ("Tanjong Rhu", "Katong Park", 2, "TEL"),
    ("Katong Park", "Tanjong Katong", 2, "TEL"),
    ("Tanjong Katong", "Marine Parade", 2, "TEL"),
    ("Marine Parade", "Marine Terrace", 2, "TEL"),
    ("Marine Terrace", "Siglap", 2, "TEL"),
    ("Siglap", "Bayshore", 3, "TEL"),
    ("Bayshore", "Bedok South", 2, "TEL"),
    ("Bedok South", "Sungei Bedok", 2, "TEL"),
]

# Additional connections for FUTURE MODE (with TEL Extension and CRL)
FUTURE_MODE_ADDITIONAL_CONNECTIONS = [
    # TEL Extension: Sungei Bedok → Changi Terminal 5 → Tanah Merah
    ("Sungei Bedok", "Bayshore", 2, "TEL"),  # This replaces the reverse direction
    ("Bayshore", "Upper Changi", 2, "TEL"),
    ("Upper Changi", "Changi Terminal 5", 3, "TEL"),
    ("Changi Terminal 5", "Expo", 3, "TEL"),
    
    # Convert Expo-Changi Airport to TEL (replaces EWL connection)
    ("Expo", "Tanah Merah", 2, "TEL"),
    ("Tanah Merah", "Changi Airport", 3, "TEL"),
    
    # Cross Island Line (CRL) - Phase 1
    ("Punggol", "Pasir Ris", 4, "CRL"),
    ("Pasir Ris", "Loyang", 3, "CRL"),
    ("Loyang", "Changi Terminal 5", 4, "CRL"),
]

# Connections to remove in FUTURE MODE (converted from EWL/DTL to TEL)
FUTURE_MODE_REMOVED_CONNECTIONS = [
    ("Expo", "Changi Airport", "EWL"),  # This becomes TEL in future
    ("Tanah Merah", "Expo", "EWL"),  # This becomes TEL in future
]

# Recommended test origin-destination pairs
TEST_PAIRS_TODAY = [
    ("Changi Airport", "City Hall"),
    ("Changi Airport", "Orchard"),
    ("Changi Airport", "Gardens by the Bay"),
    ("Boon Lay", "Punggol"),
    ("HarbourFront", "Woodlands"),
    ("Jurong East", "Marina Bay"),
]

TEST_PAIRS_FUTURE = [
    ("Changi Airport", "City Hall"),
    ("Changi Airport", "Orchard"),
    ("Changi Terminal 5", "Marina Bay"),
    ("Changi Terminal 5", "Punggol"),
    ("Changi Terminal 5", "HarbourFront"),
    ("Pasir Ris", "Changi Terminal 5"),
    ("Boon Lay", "Changi Terminal 5"),
]

# Cost parameters
TRANSFER_PENALTY_MINUTES = 3  # Time penalty when changing lines
BASE_TRAVEL_TIME_SHORT = 2    # Minutes between nearby stations
BASE_TRAVEL_TIME_MEDIUM = 3   # Minutes between medium distance stations
BASE_TRAVEL_TIME_LONG = 4     # Minutes between distant stations

# Heuristic parameters
AVERAGE_MRT_SPEED_KMH = 60    # Average MRT speed for heuristic calculation
EARTH_RADIUS_KM = 6371        # Earth radius for Haversine formula

# Line colors for visualization
LINE_COLORS = {
    "EWL": "#009645",  # Green
    "NSL": "#D42E12",  # Red
    "NEL": "#9900AA",  # Purple
    "CCL": "#FA9E0D",  # Orange/Yellow
    "DTL": "#005EC4",  # Blue
    "TEL": "#9D5B25",  # Brown
    "CRL": "#76C044",  # Light Green (anticipated)
    "BPLRT": "#748477",  # Grey
    "SPLRT": "#748477",  # Grey
}

# Line names
LINE_NAMES = {
    "EWL": "East-West Line",
    "NSL": "North-South Line",
    "NEL": "North-East Line",
    "CCL": "Circle Line",
    "DTL": "Downtown Line",
    "TEL": "Thomson-East Coast Line",
    "CRL": "Cross Island Line (Future)",
    "BPLRT": "Bukit Panjang LRT",
    "SPLRT": "Sengkang-Punggol LRT",
}

# Station interchange information
INTERCHANGE_STATIONS = {
    "Jurong East": ["EWL", "NSL"],
    "Buona Vista": ["EWL", "CCL"],
    "City Hall": ["EWL", "NSL"],
    "Raffles Place": ["EWL", "NSL"],
    "Outram Park": ["EWL", "NEL", "TEL"],
    "Dhoby Ghaut": ["NSL", "NEL", "CCL"],
    "Bishan": ["NSL", "CCL"],
    "Serangoon": ["NEL", "CCL"],
    "Paya Lebar": ["EWL", "CCL"],
    "Bayfront": ["CCL", "DTL"],
    "Promenade": ["CCL", "DTL"],
    "Bugis": ["EWL", "DTL"],
    "Chinatown": ["NEL", "DTL"],
    "MacPherson": ["CCL", "DTL"],
    "Botanic Gardens": ["CCL", "DTL"],
    "Stevens": ["DTL", "TEL"],
    "Caldecott": ["CCL", "TEL"],
    "Marina Bay": ["NSL", "CCL", "TEL"],
    "Woodlands": ["NSL", "TEL"],
    "Expo": ["EWL", "DTL"],
    "Sungei Bedok": ["DTL", "TEL"],
    "Newton": ["NSL", "DTL"],
    "Little India": ["NEL", "DTL"],
    "Orchard": ["NSL", "TEL"],
    "HarbourFront": ["NEL", "CCL"],
    "Punggol": ["NEL", "CRL"],  # Future
    "Pasir Ris": ["EWL", "CRL"],  # Future
    "Tanah Merah": ["EWL", "TEL"],  # Future
    "Choa Chu Kang": ["NSL", "BPLRT"],
    "Bukit Panjang": ["DTL", "BPLRT"],
    "Sengkang": ["NEL", "SPLRT"],
    "Tampines": ["EWL", "DTL"],
}

if __name__ == "__main__":
    print(f"Total stations: {len(STATION_COORDINATES)}")
    print(f"Total connections (today): {len(TODAY_MODE_CONNECTIONS)}")
    print(f"Total connections (future): {len(TODAY_MODE_CONNECTIONS) + len(FUTURE_MODE_ADDITIONAL_CONNECTIONS) - len(FUTURE_MODE_REMOVED_CONNECTIONS)}")
    print(f"\nLines: {', '.join(LINE_NAMES.values())}")
    print(f"\nInterchange stations: {len(INTERCHANGE_STATIONS)}")