# 🚇 ChangiLink AI - Transportation Intelligence System

A comprehensive AI-powered suite for Singapore MRT network analysis, route planning, logical inference, and crowding risk assessment.

## 🎯 Overview

ChangiLink AI integrates three powerful AI systems:

1. **🗺️ Route Planning** - Advanced pathfinding with A*, BFS, DFS, GBFS algorithms
2. **🧠 Logical Inference** - Service advisory consistency checking & route validation  
3. **📊 Crowding Risk** - Bayesian network crowding risk assessment

## � Installation

### Step 1: Install Python
Make sure you have **Python 3.7 or higher** installed:
```bash
python --version
```

### Step 2: Install Required Packages
Install all required dependencies with one command:
```bash
pip install flask numpy pandas requests
```

**Individual package installation (if needed):**
```bash
pip install flask      # Web framework
pip install numpy      # Numerical computing
pip install pandas     # Data manipulation
pip install requests   # HTTP library
```

## 🚀 Quick Start - How to Run

### Step 3: Verify Installation
Check that all packages are installed correctly:
```bash
python -c "import flask, numpy, pandas, requests; print('✅ All packages installed successfully!')"
```

If you see any import errors, install the missing packages using the commands above.

### Option 1: One-Command Launch (Recommended) ⭐

**Windows:**
```bash
start_changilink_ai.bat
```

**Linux/Mac:**
```bash
chmod +x start_changilink_ai.sh
./start_changilink_ai.sh
```

**Direct Python (All platforms):**
```bash
python integrated_launcher.py
```

### Option 2: Manual Launch (Individual Systems)

If you prefer to run systems individually:

```bash
# Terminal 1 - Route Planning
cd Route_Planning
python web_app.py

# Terminal 2 - Logical Inference  
cd Logical_Inference
python web_app.py

# Terminal 3 - Crowding Risk
cd Crowding_Risk
python web_app.py
```

## 🌐 Access the Systems

After launching, the systems will be available at:

- **📋 Main Dashboard**: Opens automatically (integrated view of all systems)
- **🗺️ Route Planning**: http://localhost:5000
- **🧠 Logical Inference**: http://localhost:5001  
- **📊 Crowding Risk**: http://localhost:5002

## 📖 What Each System Does

### 🗺️ Route Planning System
- **Purpose**: Find optimal routes in Singapore MRT network
- **Features**: 
  - Compare A*, BFS, DFS, Greedy Best-First Search algorithms
  - Today's network vs Future network (with TEL/CRL extensions)
  - Real station data with travel times and transfers
  - Performance analysis and visualization

**How to use:**
1. Select network mode (Today/Future)
2. Choose origin and destination stations
3. Select algorithm or compare all algorithms
4. View detailed results and performance metrics

### 🧠 Logical Inference System  
- **Purpose**: Validate service advisories and route consistency using logical rules
- **Features**:
  - Preset scenarios (A1-A6) matching assignment requirements
  - Custom scenario creation
  - Advisory consistency checking
  - Route validation against operational constraints

**How to use:**
1. Load a preset scenario (A1-A6) or create custom scenario
2. Configure network conditions and operational status
3. Define route to validate
4. Run consistency check and route evaluation

### 📊 Crowding Risk Assessment
- **Purpose**: Predict crowding risks using Bayesian networks
- **Features**:
  - Probabilistic risk modeling
  - Multiple risk factors analysis (weather, events, time)
  - Interactive dashboard with real-time calculations
  - Risk level predictions and recommendations

**How to use:**
1. Set station and time parameters
2. Configure risk factors (weather conditions, special events, etc.)
3. Run Bayesian network analysis
4. View risk probabilities and safety recommendations

## 🔧 System Requirements

- **Python**: 3.7 or higher
- **RAM**: 4GB recommended
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)
- **Network**: Localhost access for web interfaces
- **OS**: Windows, Linux, or macOS

## 🛠️ Troubleshooting

### Common Issues

**"Port already in use" error:**
```bash
# Check what's using the ports
netstat -an | findstr :5000
netstat -an | findstr :5001  
netstat -an | findstr :5002

# Kill processes if needed, then restart
```

**"Module not found" error:**
```bash
# Install missing dependencies
pip install flask numpy pandas requests
```

**Systems not starting:**
- Verify Python 3.7+ is installed: `python --version`
- Check all files are in correct directories
- Ensure firewall allows localhost connections
- Try running individual systems manually to isolate issues

### Testing Individual Systems

```bash
# Test Route Planning
cd Route_Planning && python web_app.py

# Test Logical Inference  
cd Logical_Inference && python web_app.py

# Test Crowding Risk
cd Crowding_Risk && python web_app.py
```

## 📁 Project Structure

```
ChangiLink_AI/
├── 🚀 integrated_launcher.py          # Main launcher script
├── 📋 dashboard.html                  # Auto-generated main dashboard
├── 🖥️ start_changilink_ai.bat        # Windows launcher
├── 🖥️ start_changilink_ai.sh         # Linux/Mac launcher
├── 📖 README.md                       # This file
├── 📖 README_INTEGRATED.md            # Detailed technical documentation
├── 🗺️ Route_Planning/                # Route planning system
│   ├── web_app.py                    # Flask web server
│   ├── task1_route_planning.py       # Core algorithms
│   ├── mrt_network_data.py           # Network data
│   └── templates/index.html          # Web interface
├── 🧠 Logical_Inference/             # Logical inference system
│   ├── web_app.py                    # Flask web server
│   ├── task2_logical_inference.py    # Logic engine
│   ├── logic_rules_data.py           # Rules and scenarios
│   └── templates/index.html          # Web interface
└── 📊 Crowding_Risk/                 # Crowding risk system
    ├── web_app.py                    # Flask web server
    ├── crowding_risk_bn.py           # Bayesian network
    └── crowding_risk_dashboard.html  # Standalone dashboard
```

## 🎓 Educational Features

This system demonstrates:
- **Algorithm Comparison**: Side-by-side performance analysis of pathfinding algorithms
- **Logical Reasoning**: Rule-based validation and consistency checking
- **Probabilistic Modeling**: Bayesian networks for risk assessment
- **Web Development**: Modern Flask-based web applications
- **System Integration**: Multi-service architecture with unified dashboard

## 🔄 Stopping the System

To stop all systems:
- **Integrated mode**: Press `Ctrl+C` in the terminal running the launcher
- **Manual mode**: Press `Ctrl+C` in each terminal window

The system will gracefully shut down all services and clean up resources.

## 📞 Support

For technical issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Review `README_INTEGRATED.md` for detailed technical information
4. Test individual systems to isolate problems

---

**🎉 Ready to explore Singapore's MRT network with AI-powered analysis!**

Start with: `python integrated_launcher.py` or use the platform-specific launch scripts.