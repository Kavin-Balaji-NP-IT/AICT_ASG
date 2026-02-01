# Crowding Risk Prediction - Interactive GUI Dashboard

A comprehensive scenario simulator dashboard for predicting crowding risk in the Changi Airport T5 corridor using Bayesian Networks. This tool allows users to compare "Today" vs "Future" network modes and analyze the impact of various factors on crowding risk.

## Features

### 🎯 **Split-View Comparison Dashboard**
- **Side-by-side comparison** of Today vs Future network modes
- **Real-time updates** as you adjust input variables
- **Interactive controls** for all input variables (Weather, Time, Day Type, Service Status)
- **Visual probability distributions** with risk scoring

### 📊 **Comprehensive Analysis**
- **Bayesian Network visualization** showing variable dependencies
- **Conditional Probability Tables (CPT)** with heatmaps
- **Risk scoring system** (Low=1, Medium=2, High=3)
- **Detailed network structure** documentation

### 🎮 **Scenario Library**
- **Predefined scenarios** for common situations:
  - Morning Rush Hour - Clear Weather
  - Evening Peak - Rainy Weather  
  - Weekend Leisure Travel
  - Service Disruption - Peak Hour
  - Thunderstorm + Reduced Service
  - Optimal Conditions
- **One-click loading** to Today, Future, or Both modes

### 📈 **Export & Analysis**
- **CSV export** of results for further analysis
- **Sync functionality** to copy settings between modes
- **Reset controls** for quick scenario changes

## Installation

### Prerequisites
- Python 3.7 or higher
- Required packages (install via pip):

```bash
pip install numpy pandas matplotlib seaborn
```

Or install all requirements at once:
```bash
pip install -r requirements.txt
```

### Running the Application

**Option 1: Direct launch**
```bash
python crowding_risk_gui.py
```

**Option 2: Using launcher script**
```bash
python run_gui.py
```

## User Interface Guide

### Main Dashboard (Tab 1: Today vs Future Comparison)

#### Left Panel - Today Mode (Red)
- **Input Variables**: Adjust Weather, Time of Day, Day Type, and Service Status
- **Results Display**: 
  - Crowding Risk Distribution (bar chart)
  - Demand Distribution (bar chart)
  - Risk Score with color-coded level
  - Current settings summary

#### Right Panel - Future Mode (Green)  
- **Same controls** as Today mode but for Future network scenario
- **Independent settings** allow different configurations
- **Visual comparison** with Today mode results

#### Control Buttons
- **Sync Settings**: Copy Today mode settings to Future mode
- **Reset All**: Reset both modes to default values
- **Export Results**: Save current analysis to CSV file

### Detailed Analysis (Tab 2)

#### Network Structure Documentation
- **Complete Bayesian Network description**
- **Variable dependencies** and relationships
- **Key insights** about the model

#### Probability Visualizations
- **Service Status by Mode**: Bar chart comparing reliability
- **Weather Distribution**: Pie chart of Singapore climate patterns  
- **Crowding Risk Heatmap**: Scenario comparison matrix

### Scenario Library (Tab 3)

#### Predefined Scenarios
Each scenario includes:
- **Descriptive name** and explanation
- **Specific variable settings**
- **Load buttons** for Today, Future, or Both modes

## Understanding the Results

### Risk Score Interpretation
- **1.0 - 1.5**: 🟢 **LOW RISK** - Minimal crowding expected
- **1.5 - 2.5**: 🟡 **MEDIUM RISK** - Moderate crowding possible  
- **2.5 - 3.0**: 🔴 **HIGH RISK** - Significant crowding likely

### Key Variables

#### Input Variables (Nodes A-F)
- **W (Weather)**: Clear, Rainy, Thunderstorms
- **T (Time of Day)**: Morning, Afternoon, Evening
- **D (Day Type)**: Weekday, Weekend  
- **M (Network Mode)**: Today, Future
- **S (Service Status)**: Normal, Reduced, Disrupted
- **P (Demand Proxy)**: Low, Medium, High (computed)

#### Output Variable
- **C (Crowding Risk)**: Low, Medium, High (target prediction)

### Network Mode Differences

#### Today Mode
- **Current network** with existing infrastructure
- **Higher disruption risk** during integration work
- **Limited alternative routes** during service issues

#### Future Mode  
- **TELe (Thomson-East Coast Line extension)** operational
- **CRL (Cross Island Line)** providing alternatives
- **Improved service reliability** and capacity
- **Better resilience** during disruptions

## Example Usage Scenarios

### 1. Morning Commute Analysis
1. Set both modes to: Weather=Clear, Time=Morning, Day=Weekday, Service=Normal
2. Compare risk scores between Today and Future
3. Observe how TELe/CRL reduces crowding risk

### 2. Service Disruption Impact
1. Load "Service Disruption - Peak Hour" scenario to both modes
2. Compare how Future mode handles disruptions better
3. Note the difference in High Risk probabilities

### 3. Weather Impact Assessment  
1. Start with optimal conditions (Clear weather)
2. Change to Rainy, then Thunderstorms
3. Observe how weather affects demand and crowding

### 4. Weekend vs Weekday Patterns
1. Compare Weekend afternoon vs Weekday morning
2. Note different demand patterns and risk levels
3. Analyze how day type affects travel behavior

## Technical Details

### Bayesian Network Structure
```
    W ──┐
    T ──┼─→ P ──┐
    D ──┤       │
    M ──┼───────┼─→ C
        │       │
        └─→ S ──┘
```

### Key Relationships
- **Service Status** depends on Network Mode (Future mode more reliable)
- **Demand** influenced by Weather, Time, Day Type, and Mode
- **Crowding Risk** determined by Demand, Service Status, and Mode
- **Future mode** provides 15-25% reduction in high crowding probability

### Probability Calculations
- Uses **exact inference** via enumeration
- **Conditional probability tables** based on Singapore MRT data
- **Risk scoring** weighted by probability distribution

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Install missing packages
pip install numpy pandas matplotlib seaborn
```

**GUI Not Displaying Properly**
- Ensure you have tkinter installed (usually comes with Python)
- Try running with Python 3.8+ for best compatibility

**Plots Not Updating**
- Check that matplotlib backend supports GUI
- Try restarting the application

### Performance Tips
- The application loads quickly as it uses efficient exact inference
- All calculations are performed in real-time
- Export large scenario analyses to CSV for external processing

## File Structure
```
Crowding_Risk/
├── crowding_risk_bn.py      # Core Bayesian Network implementation
├── crowding_risk_gui.py     # Main GUI application  
├── run_gui.py              # Launcher script
├── requirements.txt        # Python dependencies
└── README.md              # This documentation
```

## Future Enhancements

Potential improvements for the dashboard:
- **Sensitivity analysis** tools
- **Monte Carlo simulation** capabilities  
- **Historical data integration**
- **Real-time MRT data** feeds
- **Mobile-responsive** web version
- **Advanced export** options (PDF reports)

## Support

For technical issues or questions about the Bayesian Network model:
1. Check the **Detailed Analysis** tab for network documentation
2. Review **probability relationships** in the CPT visualizations
3. Use **predefined scenarios** to understand expected behaviors
4. Export results to CSV for detailed analysis in external tools

---

**Note**: This tool is designed for scenario analysis and planning purposes. Actual crowding conditions may vary based on real-world factors not captured in the model.