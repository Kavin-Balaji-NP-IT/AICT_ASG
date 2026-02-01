"""
MRT Route Planner - Web Application
A Flask web interface for planning MRT routes in Singapore
"""

from flask import Flask, render_template, request, jsonify
import json
from task1_route_planning import MRTNetwork, SearchAlgorithms
from mrt_network_data import LINE_NAMES, LINE_COLORS, TEST_PAIRS_TODAY, TEST_PAIRS_FUTURE, FUTURE_ONLY_STATIONS

app = Flask(__name__)

# Global variables for network and searcher
networks = {}
searchers = {}

def initialize_networks():
    """Initialize both network modes"""
    global networks, searchers
    
    for mode in ['today', 'future']:
        networks[mode] = MRTNetwork(mode=mode)
        searchers[mode] = SearchAlgorithms(networks[mode])

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/stations/<mode>')
def get_stations(mode):
    """Get list of stations for a given mode"""
    if mode not in networks:
        return jsonify({'error': 'Invalid mode'}), 400
    
    # Use the network's method to get available stations for the mode
    stations = networks[mode].get_available_stations()
    return jsonify({'stations': stations})

@app.route('/api/test-routes/<mode>')
def get_test_routes(mode):
    """Get test routes for a given mode"""
    if mode == 'today':
        routes = [{'name': f"{origin} → {dest}", 'origin': origin, 'destination': dest} 
                 for origin, dest in TEST_PAIRS_TODAY]
    elif mode == 'future':
        routes = [{'name': f"{origin} → {dest}", 'origin': origin, 'destination': dest} 
                 for origin, dest in TEST_PAIRS_FUTURE]
    else:
        return jsonify({'error': 'Invalid mode'}), 400
    
    return jsonify({'routes': routes})

@app.route('/api/plan-route', methods=['POST'])
def plan_route():
    """Plan a route using specified algorithm(s)"""
    data = request.get_json()
    
    origin = data.get('origin')
    destination = data.get('destination')
    mode = data.get('mode', 'today')
    algorithm = data.get('algorithm', 'all')
    
    # Validate inputs
    if not origin or not destination:
        return jsonify({'error': 'Origin and destination are required'}), 400
    
    if mode not in networks:
        return jsonify({'error': 'Invalid mode'}), 400
    
    network = networks[mode]
    
    # Check if stations are available in the selected mode
    if not network.is_station_available(origin):
        return jsonify({'error': f'Station "{origin}" is not available in {mode} mode'}), 400
    
    if not network.is_station_available(destination):
        return jsonify({'error': f'Station "{destination}" is not available in {mode} mode'}), 400
    
    if origin == destination:
        return jsonify({'error': 'Origin and destination cannot be the same'}), 400
    
    # Get searcher for the mode
    searcher = searchers[mode]
    
    # Define algorithms to run
    if algorithm == 'all':
        algorithms = [
            ('BFS', searcher.bfs),
            ('DFS', searcher.dfs),
            ('GBFS', searcher.gbfs),
            ('A*', searcher.astar)
        ]
    else:
        algo_map = {
            'BFS': searcher.bfs,
            'DFS': searcher.dfs,
            'GBFS': searcher.gbfs,
            'A*': searcher.astar
        }
        if algorithm not in algo_map:
            return jsonify({'error': f'Invalid algorithm: {algorithm}'}), 400
        algorithms = [(algorithm, algo_map[algorithm])]
    
    # Run algorithms
    results = {
        'origin': origin,
        'destination': destination,
        'mode': mode,
        'algorithms': {}
    }
    
    for algo_name, algo_func in algorithms:
        try:
            path, stats = algo_func(origin, destination)
            
            detailed_route = []
            if path and len(path) > 1:
                detailed_route = get_detailed_route(networks[mode], path)
            
            results['algorithms'][algo_name] = {
                'path': path,
                'stats': stats,
                'detailed_route': detailed_route
            }
        except Exception as e:
            results['algorithms'][algo_name] = {
                'path': None,
                'stats': {'error': str(e)},
                'detailed_route': []
            }
    
    return jsonify(results)

def get_detailed_route(network, path):
    """Get detailed route with line information"""
    if not path or len(path) < 2:
        return []
    
    detailed = []
    current_line = None
    
    for i in range(len(path) - 1):
        current_station = path[i]
        next_station = path[i + 1]
        
        # Find the line for this segment
        for neighbor, travel_time, line in network.get_neighbors(current_station):
            if neighbor == next_station:
                if current_line != line:
                    if current_line is not None:
                        detailed.append({
                            'type': 'transfer',
                            'station': current_station,
                            'from_line': current_line,
                            'to_line': line,
                            'text': f"Transfer to {LINE_NAMES.get(line, line)} at {current_station}"
                        })
                    detailed.append({
                        'type': 'line_start',
                        'line': line,
                        'text': f"Take {LINE_NAMES.get(line, line)}"
                    })
                    current_line = line
                
                detailed.append({
                    'type': 'segment',
                    'from': current_station,
                    'to': next_station,
                    'time': travel_time,
                    'line': line,
                    'text': f"{current_station} → {next_station} ({travel_time} min)"
                })
                break
    
    return detailed

if __name__ == '__main__':
    print("Initializing MRT networks...")
    initialize_networks()
    print("Networks initialized successfully!")
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)