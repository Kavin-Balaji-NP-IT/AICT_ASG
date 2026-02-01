"""
Logical Inference - Web Application
A Flask web interface for logical inference and service advisory consistency checking
"""

from flask import Flask, render_template, request, jsonify
import json
from task2_logical_inference import Scenario, Route, evaluate_route, check_advisory_consistency
from logic_rules_data import TEST_SCENARIOS, LOGICAL_RULES, SYMBOL_DEFINITIONS

app = Flask(__name__)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/symbols')
def get_symbols():
    """Get all available symbols and their definitions"""
    return jsonify({'symbols': SYMBOL_DEFINITIONS})

@app.route('/api/rules')
def get_rules():
    """Get all logical rules"""
    return jsonify({'rules': LOGICAL_RULES})

@app.route('/api/presets')
def get_presets():
    """Get predefined preset scenarios matching the desktop GUI"""
    presets = {
        "Scenario 1 (A1)": {
            "mode": "today",
            "status": "normal",
            "integration_works": False,
            "exists": "TanahMerah,Expo,ChangiAirport",
            "open_stations": "TanahMerah,Expo,ChangiAirport",
            "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport",
            "recommended_routes": "",
            "served_by_tel": "",
            "route_name": "EWL_AirportBranch",
            "route_stations": "TanahMerah,Expo,ChangiAirport",
        },
        "Scenario 2 (A2)": {
            "mode": "today",
            "status": "normal",
            "integration_works": False,
            "exists": "SungeiBedok,TanahMerah,Expo,ChangiAirport",
            "open_stations": "SungeiBedok,TanahMerah,Expo,ChangiAirport",
            "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport",
            "recommended_routes": "",
            "served_by_tel": "",
            "route_name": "Future_TEL_To_T5",
            "route_stations": "SungeiBedok,T5,TanahMerah",
        },
        "Scenario 3 (A3)": {
            "mode": "today",
            "status": "normal",
            "integration_works": False,
            "exists": "TanahMerah,Expo,ChangiAirport",
            "open_stations": "TanahMerah,Expo,ChangiAirport",
            "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport",
            "recommended_routes": "",
            "served_by_tel": "",
            "route_name": "Direct_TanahMerah_To_Changi",
            "route_stations": "TanahMerah,ChangiAirport",
        },
        "Scenario 4 (A4)": {
            "mode": "future",
            "status": "normal",
            "integration_works": False,
            "exists": "SungeiBedok,T5,TanahMerah",
            "open_stations": "SungeiBedok,T5,TanahMerah",
            "open_edges": "SungeiBedok,T5\nT5,TanahMerah",
            "recommended_routes": "",
            "served_by_tel": "",
            "route_name": "Future_TEL_To_T5",
            "route_stations": "SungeiBedok,T5,TanahMerah",
        },
        "Scenario 5 (A5)": {
            "mode": "future",
            "status": "delay",
            "integration_works": True,
            "exists": "TanahMerah,Expo,ChangiAirport",
            "open_stations": "TanahMerah,Expo,ChangiAirport",
            "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport",
            "recommended_routes": "EWL_AirportBranch",
            "served_by_tel": "",
            "route_name": "EWL_AirportBranch",
            "route_stations": "TanahMerah,Expo,ChangiAirport",
        },
        "Scenario 6 (A6)": {
            "mode": "future",
            "status": "scheduled_maintenance",
            "integration_works": False,
            "exists": "TanahMerah,Expo,ChangiAirport,T5,SungeiBedok",
            "open_stations": "TanahMerah,ChangiAirport,T5,SungeiBedok",
            "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport\nSungeiBedok,T5\nT5,TanahMerah",
            "recommended_routes": "",
            "served_by_tel": "",
            "route_name": "EWL_AirportBranch",
            "route_stations": "TanahMerah,Expo,ChangiAirport",
        },
    }
    
    return jsonify({'presets': presets})

@app.route('/api/load-preset/<preset_name>')
def load_preset(preset_name):
    """Load a specific preset scenario"""
    try:
        response = get_presets()
        presets = response.get_json()['presets']
        
        if preset_name not in presets:
            return jsonify({'error': 'Preset not found'}), 404
        
        return jsonify({'preset': presets[preset_name]})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/check-consistency', methods=['POST'])
def check_consistency():
    """Check advisory consistency for a scenario"""
    data = request.get_json()
    
    try:
        # Parse scenario data
        scenario = parse_scenario_from_request(data)
        
        # Check consistency
        result = check_advisory_consistency(scenario)
        
        return jsonify({
            'consistent': result['consistent'],
            'violations': result['violations'],
            'notes': result['notes']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/evaluate-route', methods=['POST'])
def evaluate_route_endpoint():
    """Evaluate a route against a scenario"""
    data = request.get_json()
    
    try:
        # Parse scenario and route data
        scenario = parse_scenario_from_request(data['scenario'])
        route = parse_route_from_request(data['route'])
        
        # Evaluate route
        result = evaluate_route(route, scenario)
        
        return jsonify({
            'valid': result['valid'],
            'warning': result['warning'],
            'violations': result['violations'],
            'notes': result['notes']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/run-full-analysis', methods=['POST'])
def run_full_analysis():
    """Run both consistency check and route evaluation"""
    data = request.get_json()
    
    try:
        # Parse data
        scenario = parse_scenario_from_request(data['scenario'])
        route = parse_route_from_request(data['route'])
        
        # Run both analyses
        consistency_result = check_advisory_consistency(scenario)
        route_result = evaluate_route(route, scenario)
        
        return jsonify({
            'consistency': {
                'consistent': consistency_result['consistent'],
                'violations': consistency_result['violations'],
                'notes': consistency_result['notes']
            },
            'route': {
                'valid': route_result['valid'],
                'warning': route_result['warning'],
                'violations': route_result['violations'],
                'notes': route_result['notes']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def parse_scenario_from_request(data):
    """Parse scenario data from request"""
    mode = data.get('mode', 'today')
    status = data.get('status', 'normal')
    integration_works = data.get('integration_works', False)
    
    # Parse sets from comma-separated strings
    exists = parse_set_from_string(data.get('exists', ''))
    open_stations = parse_set_from_string(data.get('open_stations', ''))
    recommended_routes = parse_set_from_string(data.get('recommended_routes', ''))
    served_by_tel = parse_set_from_string(data.get('served_by_tel', ''))
    
    # Parse edges
    open_edges = parse_edges_from_string(data.get('open_edges', ''))
    
    return Scenario(
        mode=mode,
        status=status,
        exists=exists,
        open_stations=open_stations,
        open_edges=open_edges,
        integration_works=integration_works,
        recommended_routes=recommended_routes,
        served_by_tel=served_by_tel
    )

def parse_route_from_request(data):
    """Parse route data from request"""
    name = data.get('name', 'UnnamedRoute')
    stations_str = data.get('stations', '')
    
    # Parse stations from comma-separated string
    stations = [s.strip() for s in stations_str.split(',') if s.strip()]
    
    return Route(name=name, stations=stations)

def parse_set_from_string(text):
    """Parse a set from comma-separated string"""
    if not text:
        return set()
    return {item.strip() for item in text.split(',') if item.strip()}

def parse_edges_from_string(text):
    """Parse edges from string format"""
    edges = set()
    if not text:
        return edges
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        # Handle different formats: A,B or A->B or A → B
        line = line.replace('->', ',').replace('→', ',').replace('—', ',')
        parts = [p.strip() for p in line.split(',') if p.strip()]
        if len(parts) == 2:
            edges.add((parts[0], parts[1]))
    
    return edges

if __name__ == '__main__':
    print("Initializing Logical Inference System...")
    print("Starting web server...")
    print("Open your browser and go to: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)