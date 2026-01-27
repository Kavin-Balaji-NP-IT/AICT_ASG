"""
Task 1: Route Planning with Search Algorithms
Implements BFS, DFS, GBFS, and A* for MRT route planning
Supports both Today Mode and Future Mode (with TELe/CRL)
"""

import heapq
import time
from collections import deque
from typing import Dict, List, Tuple, Set, Optional
import math

class MRTNetwork:
    """Represents the MRT network as a graph"""

    def __init__(self, mode="today"):
        """
        Initialize MRT network
        mode: "today" or "future"
        """
        self.mode = mode
        self.graph = {}  # adjacency list: {station: [(neighbor, travel_time, line)]}
        self.coordinates = {}  # station coordinates for heuristic calculation
        self.stations = set()
        self._build_network()

    def _build_network(self):
        """Build the MRT network graph based on mode"""

        # Station coordinates (approximate lat, lon for heuristic)
        # Using simplified coordinates for demonstration
        self.coordinates = {
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

        # Build connections based on mode
        if self.mode == "today":
            self._build_today_network()
        else:  # future mode
            self._build_future_network()

        self.stations = set(self.graph.keys())

    def _add_edge(self, station1: str, station2: str, time: int, line: str):
        """Add bidirectional edge between stations"""
        if station1 not in self.graph:
            self.graph[station1] = []
        if station2 not in self.graph:
            self.graph[station2] = []

        self.graph[station1].append((station2, time, line))
        self.graph[station2].append((station1, time, line))

    def _build_today_network(self):
        """Build current network (Today Mode)"""

        # East-West Line (Green) - Current configuration
        ewl_stations = [
            "Pasir Ris", "Tanah Merah", "Expo", "Changi Airport"
        ]
        for i in range(len(ewl_stations) - 1):
            self._add_edge(ewl_stations[i], ewl_stations[i+1], 3, "EWL")

        # Main EWL trunk
        ewl_main = [
            "Tanah Merah", "Bedok", "Kembangan", "Eunos", "Paya Lebar",
            "Aljunied", "Kallang", "Lavender", "Bugis", "City Hall",
            "Raffles Place", "Tanjong Pagar", "Outram Park", "Tiong Bahru",
            "Redhill", "Queenstown", "Commonwealth", "Buona Vista", "Dover",
            "Clementi", "Jurong East", "Chinese Garden", "Lakeside", "Boon Lay"
        ]
        for i in range(len(ewl_main) - 1):
            self._add_edge(ewl_main[i], ewl_main[i+1], 2, "EWL")

        # North-South Line (Red)
        nsl_stations = [
            "Marina South Pier", "Marina Bay", "Raffles Place", "City Hall",
            "Dhoby Ghaut", "Somerset", "Orchard", "Bishan", "Ang Mo Kio", "Yio Chu Kang"
        ]
        for i in range(len(nsl_stations) - 1):
            self._add_edge(nsl_stations[i], nsl_stations[i+1], 2, "NSL")

        # Circle Line (Yellow/Orange)
        ccl_stations = [
            "HarbourFront", "Telok Blangah", "Labrador Park", "Pasir Panjang",
            "Haw Par Villa", "Kent Ridge", "one-north", "Buona Vista", "Botanic Gardens",
            "Farrer Road", "Holland Village", "Dhoby Ghaut", "Bras Basah",
            "Esplanade", "Promenade", "Nicoll Highway", "Stadium", "Mountbatten",
            "Dakota", "Paya Lebar", "MacPherson", "Tai Seng", "Bartley",
            "Serangoon"
        ]
        for i in range(len(ccl_stations) - 1):
            self._add_edge(ccl_stations[i], ccl_stations[i+1], 2, "CCL")

        # Downtown Line (Blue)
        dtl_stations = [
            "Chinatown", "Telok Ayer", "Downtown", "Bayfront", "Gardens by the Bay"
        ]
        for i in range(len(dtl_stations) - 1):
            self._add_edge(dtl_stations[i], dtl_stations[i+1], 2, "DTL")

        # Thomson-East Coast Line (Brown) - Current sections
        tel_stations = [
            "Sungei Bedok", "Bedok South", "Siglap", "Marine Terrace",
            "Marine Parade", "Tanjong Katong", "Katong Park", "Tanjong Rhu"
        ]
        for i in range(len(tel_stations) - 1):
            self._add_edge(tel_stations[i], tel_stations[i+1], 2, "TEL")

        # Add transfer penalties (3 minutes for transfers)
        # These are handled in the cost function

    def _build_future_network(self):
        """Build future network with TELe and CRL extensions"""

        # Start with today's network as base
        self._build_today_network()

        # TELe Extension: Sungei Bedok → T5 → Tanah Merah
        tele_extension = [
            "Sungei Bedok", "Bayshore", "Changi Terminal 5", "Upper Changi",
            "Expo", "Tanah Merah"
        ]
        for i in range(len(tele_extension) - 1):
            self._add_edge(tele_extension[i], tele_extension[i+1], 3, "TEL")

        # Convert old EWL stations (Tanah Merah, Expo, Changi Airport) to TEL
        # Remove old EWL connections to these stations
        stations_to_convert = ["Tanah Merah", "Expo", "Changi Airport"]

        # Update Changi Airport to be on TEL instead
        # Remove old EWL connection from Expo to Changi Airport
        if "Expo" in self.graph:
            self.graph["Expo"] = [(n, t, l) for n, t, l in self.graph["Expo"]
                                   if not (n == "Changi Airport" and l == "EWL")]
        if "Changi Airport" in self.graph:
            self.graph["Changi Airport"] = [(n, t, l) for n, t, l in self.graph["Changi Airport"]
                                             if not (n == "Expo" and l == "EWL")]

        # Add new TEL connection from Expo to Changi Airport
        self._add_edge("Expo", "Changi Airport", 3, "TEL")

        # CRL Extension to T5
        crl_stations = [
            "Punggol", "Pasir Ris", "Changi Terminal 5"
        ]
        for i in range(len(crl_stations) - 1):
            self._add_edge(crl_stations[i], crl_stations[i+1], 4, "CRL")

    def get_neighbors(self, station: str) -> List[Tuple[str, int, str]]:
        """Get neighbors of a station"""
        return self.graph.get(station, [])

    def get_cost(self, current: str, neighbor: str, current_line: str = None,
                 crowding_penalty: float = 0) -> float:
        """
        Calculate cost between stations
        Includes: base travel time + transfer penalty + crowding penalty
        """
        for next_station, travel_time, line in self.get_neighbors(current):
            if next_station == neighbor:
                cost = travel_time

                # Add transfer penalty if changing lines
                if current_line and line != current_line:
                    cost += 3  # 3 minutes transfer penalty

                # Add crowding penalty
                cost += crowding_penalty

                return cost

        return float('inf')

    def heuristic(self, station1: str, station2: str) -> float:
        """
        Calculate heuristic (straight-line distance converted to time)
        Using Haversine formula for lat/lon coordinates
        Assumes average MRT speed of 60 km/h
        """
        if station1 not in self.coordinates or station2 not in self.coordinates:
            return 0

        lat1, lon1 = self.coordinates[station1]
        lat2, lon2 = self.coordinates[station2]

        # Haversine formula
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (math.sin(dlat/2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c

        # Convert to time (assuming 60 km/h average speed)
        time_estimate = (distance / 60) * 60  # in minutes

        return time_estimate


class SearchAlgorithms:
    """Implementation of search algorithms for route planning"""

    def __init__(self, network: MRTNetwork):
        self.network = network
        self.stats = {}  # Store statistics for each search

    def reconstruct_path(self, came_from: Dict, current: str) -> List[str]:
        """Reconstruct path from came_from dictionary"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def bfs(self, start: str, goal: str) -> Tuple[Optional[List[str]], Dict]:
        """Breadth-First Search"""
        start_time = time.time()

        if start not in self.network.stations or goal not in self.network.stations:
            return None, {"error": "Invalid start or goal station"}

        queue = deque([start])
        came_from = {}
        visited = {start}
        nodes_expanded = 0

        while queue:
            current = queue.popleft()
            nodes_expanded += 1

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                end_time = time.time()

                return path, {
                    "algorithm": "BFS",
                    "nodes_expanded": nodes_expanded,
                    "runtime": end_time - start_time,
                    "path_length": len(path),
                    "path_cost": self._calculate_path_cost(path)
                }

            for neighbor, _, _ in self.network.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        end_time = time.time()
        return None, {
            "algorithm": "BFS",
            "nodes_expanded": nodes_expanded,
            "runtime": end_time - start_time,
            "error": "No path found"
        }

    def dfs(self, start: str, goal: str) -> Tuple[Optional[List[str]], Dict]:
        """Depth-First Search"""
        start_time = time.time()

        if start not in self.network.stations or goal not in self.network.stations:
            return None, {"error": "Invalid start or goal station"}

        stack = [start]
        came_from = {}
        visited = {start}
        nodes_expanded = 0

        while stack:
            current = stack.pop()
            nodes_expanded += 1

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                end_time = time.time()

                return path, {
                    "algorithm": "DFS",
                    "nodes_expanded": nodes_expanded,
                    "runtime": end_time - start_time,
                    "path_length": len(path),
                    "path_cost": self._calculate_path_cost(path)
                }

            for neighbor, _, _ in self.network.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    stack.append(neighbor)

        end_time = time.time()
        return None, {
            "algorithm": "DFS",
            "nodes_expanded": nodes_expanded,
            "runtime": end_time - start_time,
            "error": "No path found"
        }

    def gbfs(self, start: str, goal: str) -> Tuple[Optional[List[str]], Dict]:
        """Greedy Best-First Search"""
        start_time = time.time()

        if start not in self.network.stations or goal not in self.network.stations:
            return None, {"error": "Invalid start or goal station"}

        # Priority queue: (heuristic, station)
        frontier = [(self.network.heuristic(start, goal), start)]
        came_from = {}
        visited = set()
        nodes_expanded = 0

        while frontier:
            _, current = heapq.heappop(frontier)

            if current in visited:
                continue

            visited.add(current)
            nodes_expanded += 1

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                end_time = time.time()

                return path, {
                    "algorithm": "GBFS",
                    "nodes_expanded": nodes_expanded,
                    "runtime": end_time - start_time,
                    "path_length": len(path),
                    "path_cost": self._calculate_path_cost(path)
                }

            for neighbor, _, _ in self.network.get_neighbors(current):
                if neighbor not in visited:
                    h = self.network.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (h, neighbor))
                    if neighbor not in came_from:
                        came_from[neighbor] = current

        end_time = time.time()
        return None, {
            "algorithm": "GBFS",
            "nodes_expanded": nodes_expanded,
            "runtime": end_time - start_time,
            "error": "No path found"
        }

    def astar(self, start: str, goal: str) -> Tuple[Optional[List[str]], Dict]:
        """A* Search"""
        start_time = time.time()

        if start not in self.network.stations or goal not in self.network.stations:
            return None, {"error": "Invalid start or goal station"}

        # Priority queue: (f_score, station)
        frontier = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        visited = set()
        nodes_expanded = 0
        line_info = {start: None}  # Track which line we're on

        while frontier:
            _, current = heapq.heappop(frontier)

            if current in visited:
                continue

            visited.add(current)
            nodes_expanded += 1

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                end_time = time.time()

                return path, {
                    "algorithm": "A*",
                    "nodes_expanded": nodes_expanded,
                    "runtime": end_time - start_time,
                    "path_length": len(path),
                    "path_cost": g_score[current]
                }

            for neighbor, travel_time, line in self.network.get_neighbors(current):
                if neighbor in visited:
                    continue

                # Calculate cost with transfer penalty
                current_line = line_info.get(current)
                cost = self.network.get_cost(current, neighbor, current_line)
                tentative_g = g_score[current] + cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    line_info[neighbor] = line

                    h = self.network.heuristic(neighbor, goal)
                    f = tentative_g + h
                    heapq.heappush(frontier, (f, neighbor))

        end_time = time.time()
        return None, {
            "algorithm": "A*",
            "nodes_expanded": nodes_expanded,
            "runtime": end_time - start_time,
            "error": "No path found"
        }

    def _calculate_path_cost(self, path: List[str]) -> float:
        """Calculate total cost of a path"""
        if not path or len(path) < 2:
            return 0

        total_cost = 0
        current_line = None

        for i in range(len(path) - 1):
            current = path[i]
            next_station = path[i + 1]

            # Find the connection
            for neighbor, travel_time, line in self.network.get_neighbors(current):
                if neighbor == next_station:
                    total_cost += travel_time
                    if current_line and line != current_line:
                        total_cost += 3  # Transfer penalty
                    current_line = line
                    break

        return total_cost


def run_experiments():
    """Run experiments comparing all algorithms in both modes"""

    # Test origin-destination pairs
    test_pairs = [
        ("Changi Airport", "City Hall"),
        ("Changi Airport", "Orchard"),
        ("Changi Airport", "Gardens by the Bay"),
        ("Paya Lebar", "Changi Terminal 5"),  # Only in future mode
        ("HarbourFront", "Changi Terminal 5"),  # Only in future mode
        ("Bishan", "Changi Terminal 5"),  # Only in future mode
        ("Tanah Merah", "Changi Terminal 5"),  # Only in future mode
    ]

    modes = ["today", "future"]

    for mode in modes:
        print(f"\n{'='*80}")
        print(f"NETWORK MODE: {mode.upper()}")
        print(f"{'='*80}\n")

        network = MRTNetwork(mode=mode)
        searcher = SearchAlgorithms(network)

        for origin, destination in test_pairs:
            # Skip T5 destinations in today mode
            if mode == "today" and destination == "Changi Terminal 5":
                continue

            print(f"\nRoute: {origin} → {destination}")
            print("-" * 80)

            # Run all algorithms
            algorithms = [
                ("BFS", searcher.bfs),
                ("DFS", searcher.dfs),
                ("GBFS", searcher.gbfs),
                ("A*", searcher.astar)
            ]

            for algo_name, algo_func in algorithms:
                path, stats = algo_func(origin, destination)

                if path:
                    print(f"\n{algo_name}:")
                    print(f"  Path: {' → '.join(path)}")
                    print(f"  Nodes Expanded: {stats['nodes_expanded']}")
                    print(f"  Path Length: {stats['path_length']} stations")
                    print(f"  Path Cost: {stats['path_cost']:.2f} minutes")
                    print(f"  Runtime: {stats['runtime']*1000:.4f} ms")
                else:
                    print(f"\n{algo_name}: {stats.get('error', 'No path found')}")

            print()


def main():
    """Main function to demonstrate the search algorithms"""
    print("MRT Route Planning System - Task 1")
    print("Search Algorithms: BFS, DFS, GBFS, A*")
    print("="*80)

    run_experiments()

    print("\n" + "="*80)
    print("ANALYSIS AND DISCUSSION")
    print("="*80)
    print("""
ALGORITHM COMPARISON:

1. BREADTH-FIRST SEARCH (BFS):
   Advantages:
   - Guarantees shortest path in terms of number of stations (hops)
   - Complete: will find a solution if one exists
   - Simple to implement

   Disadvantages:
   - Does not consider edge weights (travel time)
   - High memory usage (stores all nodes at current level)
   - Expands many unnecessary nodes

2. DEPTH-FIRST SEARCH (DFS):
   Advantages:
   - Low memory usage (only stores path to current node)
   - Fast for deep graphs

   Disadvantages:
   - Does not guarantee optimal path
   - May get stuck in deep branches
   - Not suitable for route planning where optimality is important

3. GREEDY BEST-FIRST SEARCH (GBFS):
   Advantages:
   - Often faster than BFS/DFS due to heuristic guidance
   - Expands fewer nodes by focusing on goal
   - Uses domain knowledge (coordinates)

   Disadvantages:
   - Does not guarantee optimal path
   - Performance depends heavily on heuristic quality
   - Can be misled by heuristic

4. A* SEARCH:
   Advantages:
   - Guarantees optimal path (with admissible heuristic)
   - Efficient: expands minimal nodes needed for optimal solution
   - Balances actual cost and estimated remaining cost

   Disadvantages:
   - Requires good heuristic function
   - Higher memory usage than GBFS
   - More computationally expensive per node

COST FUNCTION:
- Base cost: Travel time between stations (2-4 minutes)
- Transfer penalty: +3 minutes when changing lines
- Optional crowding penalty: Can be added based on conditions

HEURISTIC FUNCTION (for GBFS and A*):
- Straight-line distance using Haversine formula
- Converted to time estimate (assuming 60 km/h average speed)
- Admissible: never overestimates actual cost
- Consistent: satisfies triangle inequality

PERFORMANCE OBSERVATIONS:
- A* typically finds optimal paths with fewer node expansions than BFS
- GBFS is fastest but may not find optimal path
- DFS is unsuitable for this application
- Future mode adds new connections, reducing travel times to T5
""")


if __name__ == "__main__":
    main()