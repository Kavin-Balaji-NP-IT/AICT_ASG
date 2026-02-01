"""
Crowding Risk Prediction - Web Application
A Flask web server that serves the standalone HTML dashboard
"""

from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Main page"""
    with open('crowding_risk_dashboard.html', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    print("Starting Crowding Risk Dashboard Web Server...")
    print("Open your browser and go to: http://localhost:5000")
    print("The dashboard uses embedded Bayesian Network calculations.")
    app.run(debug=True, host='0.0.0.0', port=5000)