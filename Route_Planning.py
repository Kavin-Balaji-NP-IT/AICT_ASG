"""
Task 1: Route Planning with Search Algorithms
Implements BFS, DFS, GBFS, and A* for MRT route planning
Supports both Today Mode and Future Mode (with TELe/CRL)
"""

import heapq
import time
import math
from collections import deque
from typing import Dict, List, Tuple, Set, Optional

# Import network data from separate data file
from mrt_network_data import (
    STATION_COORDINATES,
    TODAY_MODE_CONNECTIONS,
    FUTURE_MODE_ADDITIONAL_CONNECTIONS,
    FUTURE_MODE_REMOVED_CONNECTIONS,
    TEST_PAIRS_TODAY,
    TEST_PAIRS_FUTURE,
    TRANSFER_PENALTY_MINUTES,
    AVERAGE_MRT_SPEED_KMH,
    EARTH_RADIUS_KM,
)


class MRTNetwork:
    """Represents the MRT network as a graph"""
    
    def __init__(self, mode="today"):
        """
        Initialize MRT network
        mode: "today" or "future"
        """
        self.mode = mode
        self.graph = {}  # adjacency list: {station: [(neighbor, travel_time, line)]}
        self.coordinates = STATION_COORDINATES.copy()
        self.stations = set()
        self._build_network()
    
    def _build_network(self):
        """Build the MRT network graph based on mode"""
        
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
    
    def _remove_edge(self, station1: str, station2: str, line: str):
        """Remove a specific edge between stations for a given line"""
        if station1 in self.graph:
            self.graph[station1] = [
                (n, t, l) for n, t, l in self.graph[station1]
                if not (n == station2 and l == line)
            ]
        if station2 in self.graph:
            self.graph[station2] = [
                (n, t, l) for n, t, l in self.graph[station2]
                if not (n == station1 and l == line)
            ]
    
    def _build_today_network(self):
        """Build current network (Today Mode) from data file"""
        for station1, station2, travel_time, line in TODAY_MODE_CONNECTIONS:
            self._add_edge(station1, station2, travel_time, line)
    
    def _build_future_network(self):
        """Build future network with TELe and CRL extensions from data file"""
        
        # Start with today's network
        self._build_today_network()
        
        # Remove connections that are converted in future mode
        for station1, station2, line in FUTURE_MODE_REMOVED_CONNECTIONS:
            self._remove_edge(station1, station2, line)
        
        # Add new future connections
        for station1, station2, travel_time, line in FUTURE_MODE_ADDITIONAL_CONNECTIONS:
            self._add_edge(station1, station2, travel_time, line)
    
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
                    cost += TRANSFER_PENALTY_MINUTES
                
                # Add crowding penalty
                cost += crowding_penalty
                
                return cost
        
        return float('inf')
    
    def heuristic(self, station1: str, station2: str) -> float:
        """
        Calculate heuristic (straight-line distance converted to time)
        Using Haversine formula for lat/lon coordinates
        Assumes average MRT speed from data configuration
        """
        if station1 not in self.coordinates or station2 not in self.coordinates:
            return 0
        
        lat1, lon1 = self.coordinates[station1]
        lat2, lon2 = self.coordinates[station2]
        
        # Haversine formula
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) ** 2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        distance = EARTH_RADIUS_KM * c
        
        # Convert to time (using configured average speed)
        time_estimate = (distance / AVERAGE_MRT_SPEED_KMH) * 60  # in minutes
        
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
                        total_cost += TRANSFER_PENALTY_MINUTES
                    current_line = line
                    break
        
        return total_cost


def run_experiments():
    """Run experiments comparing all algorithms in both modes"""
    
    modes = ["today", "future"]
    
    for mode in modes:
        print(f"\n{'='*80}")
        print(f"NETWORK MODE: {mode.upper()}")
        print(f"{'='*80}\n")
        
        network = MRTNetwork(mode=mode)
        searcher = SearchAlgorithms(network)
        
        # Select appropriate test pairs based on mode
        test_pairs = TEST_PAIRS_TODAY if mode == "today" else TEST_PAIRS_FUTURE
        
        for origin, destination in test_pairs:
            # Skip if stations don't exist in current mode
            if origin not in network.stations or destination not in network.stations:
                print(f"\nRoute: {origin} → {destination}")
                print("-" * 80)
                print(f"Skipped: Station not available in {mode} mode\n")
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
    

if __name__ == "__main__":
    main()