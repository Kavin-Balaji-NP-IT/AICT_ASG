"""
Crowding Risk Prediction - Web Application
A Flask web interface for the Bayesian Network scenario simulator
"""

from flask import Flask, send_file, request, jsonify
import json
import base64
import io
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from crowding_risk_bn import BayesianNetwork

app = Flask(__name__)

# Global Bayesian Network instance
bn = None

def initialize_network():
    """Initialize the Bayesian Network"""
    global bn
    bn = BayesianNetwork()

@app.route('/')
def index():
    """Main page - serve the crowding risk dashboard"""
    return send_file('crowding_risk_dashboard.html')

@app.route('/dashboard')
def dashboard():
    """Alternative route for the dashboard"""
    return send_file('crowding_risk_dashboard.html')

@app.route('/api/domains')
def get_domains():
    """Get variable domains for the frontend"""
    return jsonify({
        'domains': bn.domains,
        'variables': {
            'W': 'Weather',
            'T': 'Time of Day', 
            'D': 'Day Type',
            'S': 'Service Status'
        }
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Run Bayesian Network inference"""
    try:
        data = request.get_json()
        
        # Extract evidence for both modes
        today_evidence = {
            'W': data.get('today_weather', 'Clear'),
            'T': data.get('today_time', 'Morning'),
            'D': data.get('today_day', 'Weekday'),
            'S': data.get('today_service', 'Normal'),
            'M': 'Today'
        }
        
        future_evidence = {
            'W': data.get('future_weather', 'Clear'),
            'T': data.get('future_time', 'Morning'),
            'D': data.get('future_day', 'Weekday'),
            'S': data.get('future_service', 'Normal'),
            'M': 'Future'
        }
        
        # Run inference
        today_crowding = bn.inference('C', today_evidence)
        today_demand = bn.inference('P', today_evidence)
        
        future_crowding = bn.inference('C', future_evidence)
        future_demand = bn.inference('P', future_evidence)
        
        # Calculate risk scores
        today_risk_score = (today_crowding['Low'] * 1 + 
                           today_crowding['Medium'] * 2 + 
                           today_crowding['High'] * 3)
        
        future_risk_score = (future_crowding['Low'] * 1 + 
                            future_crowding['Medium'] * 2 + 
                            future_crowding['High'] * 3)
        
        # Generate plots
        today_plot = generate_mode_plot(today_crowding, today_demand, today_evidence, 
                                       "Today Mode", '#e74c3c', today_risk_score)
        future_plot = generate_mode_plot(future_crowding, future_demand, future_evidence,
                                        "Future Mode", '#27ae60', future_risk_score)
        
        comparison_plot = generate_comparison_plot(today_crowding, future_crowding,
                                                  today_risk_score, future_risk_score)
        
        return jsonify({
            'success': True,
            'today': {
                'crowding': today_crowding,
                'demand': today_demand,
                'risk_score': today_risk_score,
                'evidence': today_evidence,
                'plot': today_plot
            },
            'future': {
                'crowding': future_crowding,
                'demand': future_demand,
                'risk_score': future_risk_score,
                'evidence': future_evidence,
                'plot': future_plot
            },
            'comparison_plot': comparison_plot,
            'improvement': {
                'risk_reduction': today_risk_score - future_risk_score,
                'percent_improvement': ((today_risk_score - future_risk_score) / today_risk_score * 100) if today_risk_score > 0 else 0
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/scenarios')
def get_scenarios():
    """Get predefined scenarios"""
    scenarios = [
        {
            'id': 'morning_rush',
            'name': 'Morning Rush Hour - Clear Weather',
            'description': 'Peak morning commute with optimal conditions',
            'settings': {'W': 'Clear', 'T': 'Morning', 'D': 'Weekday', 'S': 'Normal'}
        },
        {
            'id': 'evening_rain',
            'name': 'Evening Peak - Rainy Weather',
            'description': 'Evening rush with adverse weather conditions',
            'settings': {'W': 'Rainy', 'T': 'Evening', 'D': 'Weekday', 'S': 'Normal'}
        },
        {
            'id': 'weekend_leisure',
            'name': 'Weekend Leisure Travel',
            'description': 'Typical weekend afternoon travel patterns',
            'settings': {'W': 'Clear', 'T': 'Afternoon', 'D': 'Weekend', 'S': 'Normal'}
        },
        {
            'id': 'service_disruption',
            'name': 'Service Disruption - Peak Hour',
            'description': 'Major service disruption during morning peak',
            'settings': {'W': 'Clear', 'T': 'Morning', 'D': 'Weekday', 'S': 'Disrupted'}
        },
        {
            'id': 'thunderstorm_reduced',
            'name': 'Thunderstorm + Reduced Service',
            'description': 'Severe weather with service impacts',
            'settings': {'W': 'Thunderstorms', 'T': 'Evening', 'D': 'Weekday', 'S': 'Reduced'}
        },
        {
            'id': 'optimal',
            'name': 'Optimal Conditions',
            'description': 'Best case scenario with all favorable conditions',
            'settings': {'W': 'Clear', 'T': 'Afternoon', 'D': 'Weekend', 'S': 'Normal'}
        }
    ]
    
    return jsonify({'scenarios': scenarios})

@app.route('/api/network-info')
def get_network_info():
    """Get Bayesian Network structure information"""
    network_info = {
        'structure': {
            'variables': {
                'W': {
                    'name': 'Weather',
                    'description': 'Weather conditions affecting travel',
                    'values': bn.domains['W'],
                    'parents': [],
                    'type': 'input'
                },
                'T': {
                    'name': 'Time of Day',
                    'description': 'Time period for analysis',
                    'values': bn.domains['T'],
                    'parents': [],
                    'type': 'input'
                },
                'D': {
                    'name': 'Day Type',
                    'description': 'Weekday vs Weekend travel patterns',
                    'values': bn.domains['D'],
                    'parents': [],
                    'type': 'input'
                },
                'M': {
                    'name': 'Network Mode',
                    'description': 'Current vs Future network infrastructure',
                    'values': bn.domains['M'],
                    'parents': [],
                    'type': 'scenario'
                },
                'S': {
                    'name': 'Service Status',
                    'description': 'MRT service reliability level',
                    'values': bn.domains['S'],
                    'parents': ['M'],
                    'type': 'intermediate'
                },
                'P': {
                    'name': 'Demand Proxy',
                    'description': 'Passenger demand level',
                    'values': bn.domains['P'],
                    'parents': ['W', 'T', 'D', 'M'],
                    'type': 'intermediate'
                },
                'C': {
                    'name': 'Crowding Risk',
                    'description': 'Target prediction variable',
                    'values': bn.domains['C'],
                    'parents': ['P', 'S', 'M'],
                    'type': 'output'
                }
            },
            'topology': "W,T,D,M → P → C ← S ← M",
            'description': "Bayesian Network for predicting crowding risk in Changi Airport T5 corridor"
        },
        'insights': [
            "Future network (TELe/CRL) provides 15-25% reduction in high crowding probability",
            "Service disruptions significantly amplify crowding risk in both modes",
            "Weather impacts are better mitigated in Future mode due to alternative routes",
            "Morning and evening peaks show highest crowding risk",
            "Weekend travel patterns generally have lower crowding risk"
        ]
    }
    
    return jsonify(network_info)

def generate_mode_plot(crowding_dist, demand_dist, evidence, title, color, risk_score):
    """Generate plot for a single mode"""
    plt.style.use('default')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    # Crowding Risk Distribution
    crowding_values = list(crowding_dist.keys())
    crowding_probs = list(crowding_dist.values())
    
    bars1 = ax1.bar(crowding_values, crowding_probs, color=color, alpha=0.7)
    ax1.set_title('Crowding Risk Distribution')
    ax1.set_ylabel('Probability')
    ax1.set_ylim(0, 1)
    
    for bar, prob in zip(bars1, crowding_probs):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{prob:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Demand Distribution
    demand_values = list(demand_dist.keys())
    demand_probs = list(demand_dist.values())
    
    bars2 = ax2.bar(demand_values, demand_probs, color='#3498db', alpha=0.7)
    ax2.set_title('Demand Distribution')
    ax2.set_ylabel('Probability')
    ax2.set_ylim(0, 1)
    
    for bar, prob in zip(bars2, demand_probs):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{prob:.2f}', ha='center', va='bottom')
    
    # Risk Score Gauge
    ax3.axis('off')
    
    # Risk level and color
    if risk_score < 1.5:
        risk_color = '#27ae60'
        risk_level = 'LOW'
    elif risk_score < 2.5:
        risk_color = '#f39c12'
        risk_level = 'MEDIUM'
    else:
        risk_color = '#e74c3c'
        risk_level = 'HIGH'
    
    ax3.text(0.5, 0.8, 'RISK SCORE', ha='center', va='center', 
            fontsize=14, fontweight='bold', transform=ax3.transAxes)
    ax3.text(0.5, 0.5, f'{risk_score:.3f}', ha='center', va='center',
            fontsize=24, fontweight='bold', color=risk_color, transform=ax3.transAxes)
    ax3.text(0.5, 0.2, risk_level, ha='center', va='center',
            fontsize=16, fontweight='bold', color=risk_color, transform=ax3.transAxes)
    
    # Settings Summary
    ax4.axis('off')
    settings_text = f"""Settings:
Weather: {evidence['W']}
Time: {evidence['T']}
Day: {evidence['D']}
Service: {evidence['S']}

Key Probabilities:
P(High) = {crowding_dist['High']:.3f}
P(Medium) = {crowding_dist['Medium']:.3f}
P(Low) = {crowding_dist['Low']:.3f}"""
    
    ax4.text(0.05, 0.95, settings_text, ha='left', va='top', fontsize=10,
            transform=ax4.transAxes, bbox=dict(boxstyle="round,pad=0.3", 
            facecolor='#f8f9fa', alpha=0.8))
    
    plt.tight_layout()
    
    # Convert to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_base64

def generate_comparison_plot(today_crowding, future_crowding, today_risk, future_risk):
    """Generate comparison plot between Today and Future modes"""
    plt.style.use('default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Today vs Future Mode Comparison', fontsize=16, fontweight='bold')
    
    # Crowding Risk Comparison
    categories = ['Low', 'Medium', 'High']
    today_probs = [today_crowding[cat] for cat in categories]
    future_probs = [future_crowding[cat] for cat in categories]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, today_probs, width, label='Today', color='#e74c3c', alpha=0.7)
    bars2 = ax1.bar(x + width/2, future_probs, width, label='Future', color='#27ae60', alpha=0.7)
    
    ax1.set_title('Crowding Risk Probability Comparison')
    ax1.set_xlabel('Risk Level')
    ax1.set_ylabel('Probability')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=9)
    
    # Risk Score Comparison
    modes = ['Today', 'Future']
    risk_scores = [today_risk, future_risk]
    colors = ['#e74c3c', '#27ae60']
    
    bars3 = ax2.bar(modes, risk_scores, color=colors, alpha=0.7)
    ax2.set_title('Risk Score Comparison')
    ax2.set_ylabel('Risk Score')
    ax2.set_ylim(0, 3)
    
    for bar, score in zip(bars3, risk_scores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Add improvement annotation
    improvement = ((today_risk - future_risk) / today_risk * 100) if today_risk > 0 else 0
    ax2.text(0.5, max(risk_scores) * 0.8, f'{improvement:.1f}%\nImprovement', 
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    
    # Convert to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_base64

if __name__ == '__main__':
    print("Initializing Crowding Risk Bayesian Network...")
    initialize_network()
    print("Network initialized successfully!")
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Dashboard: Crowding Risk Scenario Simulator")
    app.run(debug=True, host='0.0.0.0', port=5000)