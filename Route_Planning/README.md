# Singapore MRT Route Planner

A comprehensive route planning web application for Singapore's MRT (Mass Rapid Transit) system with a modern web interface.

## Features

### Network Modes
- **Today's Network**: Current operational MRT network
- **Future Network**: Includes Thomson-East Coast Line extensions and Cross Island Line

### Search Algorithms
- **Breadth-First Search (BFS)**: Finds shortest path by number of stations
- **Depth-First Search (DFS)**: Explores paths deeply before backtracking
- **Greedy Best-First Search (GBFS)**: Uses heuristic to guide search toward goal
- **A* Search**: Optimal pathfinding combining actual cost and heuristic

### User Interface Features
- **Modern Web Interface**: Responsive design that works on desktop and mobile
- **Station Selection**: Dropdown menus with all available stations
- **Algorithm Comparison**: Run single algorithm or compare all algorithms
- **Quick Test Routes**: Pre-configured popular routes for testing
- **Detailed Results**: Shows path, travel time, transfers, and algorithm statistics
- **Network Mode Switching**: Toggle between current and future network configurations
- **Real-time Updates**: Live status updates and error handling

## How to Use

### Running the Application
```bash
cd Route_Planning
python web_app.py
```

Then open your web browser and go to: **http://localhost:5000**

### Planning a Route
1. **Start the Web Server**: Run `python web_app.py` and open http://localhost:5000
2. **Select Network Mode**: Choose between "Today's Network" or "Future Network"
3. **Choose Stations**: 
   - Select origin station from "From" dropdown
   - Select destination station from "To" dropdown
   - Use the swap button (⇅) to quickly reverse the route
4. **Select Algorithm**: Choose a specific algorithm or "All Algorithms" for comparison
5. **Plan Route**: Click "Plan Route" button to start the search
6. **View Results**: Results display detailed path information and statistics

### Quick Test Routes
Use the pre-configured test route buttons for common journeys:

**Today's Network:**
- Changi Airport → City Hall
- Boon Lay → Punggol  
- HarbourFront → Woodlands

**Future Network:**
- Changi Terminal 5 → Marina Bay
- Pasir Ris → Changi Terminal 5
- Boon Lay → Changi Terminal 5

### Understanding Results

#### Route Details Display
- **Path**: Station-by-station route with visual arrows
- **Travel Time**: Total journey time including transfers
- **Detailed Route**: Line-by-line breakdown with transfer points
- **Algorithm Statistics**: Performance metrics for each algorithm

#### Algorithm Statistics Grid
- **Path Found**: Whether a route was discovered
- **Path Length**: Number of stations in the route
- **Cost**: Total travel time in minutes
- **Nodes Expanded**: Algorithm efficiency metric
- **Runtime**: Time taken to find the solution

## Data Sources

### Official References
All MRT network data is sourced from official Land Transport Authority (LTA) Singapore resources:

- **Official MRT Network Map**: Land Transport Authority (LTA) Singapore
  - Source: https://www.lta.gov.sg/content/ltagov/en/map/rail.html
  - Current operational network map showing all MRT and LRT lines
  - Used for: Line routing, station connectivity, interchange identification

- **Station Locations**: OpenStreetMap & LTA Data Mall
  - Geographic coordinates (latitude/longitude) for all stations
  - Used for: Heuristic calculations in A* and GBFS algorithms
  - Data validated against official LTA station databases

- **Travel Times**: Based on LTA operational data
  - Inter-station travel times: 2-4 minutes depending on distance
  - Transfer penalties: 3 minutes per line change
  - Source: LTA Service Standards and typical MRT operations

- **Future Network Planning**: LTA Rail Network Expansion Plans
  - Thomson-East Coast Line Extension to Changi Terminal 5
  - Cross Island Line Phase 1 (Punggol to Aviation Park)
  - Source: https://www.lta.gov.sg/content/ltagov/en/upcoming_projects.html

### Line Color Codes
Official LTA line colors used in visualizations:
- **East-West Line**: #009645 (Green)
- **North-South Line**: #D42E12 (Red)
- **North-East Line**: #9900AA (Purple)
- **Circle Line**: #FA9E0D (Orange)
- **Downtown Line**: #005EC4 (Blue)
- **Thomson-East Coast Line**: #9D5B25 (Brown)
- **Cross Island Line**: #76C044 (Light Green - anticipated)

### Dataset Statistics
- **Total Stations**: 186 (including LRT stations)
- **Operational MRT Lines**: 6 lines
- **Future Lines**: 1 (Cross Island Line)
- **Interchange Stations**: 32 multi-line transfer points
- **Total Connections**: 169 (current), 178 (future)
- **Last Updated**: February 2026

### Disclaimer
This dataset represents the Singapore MRT network as of February 2026. Station names, line routes, and operational details are subject to change by the Land Transport Authority. For official and real-time information, please refer to:
- **LTA Website**: https://www.lta.gov.sg
- **SMRT**: https://www.smrt.com.sg
- **SBS Transit**: https://www.sbstransit.com.sg

## Network Data

### Lines Included
- **East-West Line (EWL)**: Green line including Changi Airport branch
- **North-South Line (NSL)**: Red line from Jurong East to Marina South Pier
- **North-East Line (NEL)**: Purple line from HarbourFront to Punggol
- **Circle Line (CCL)**: Orange line with Marina Bay extension
- **Downtown Line (DTL)**: Blue line with Sungei Bedok extension
- **Thomson-East Coast Line (TEL)**: Brown line (current and future sections)
- **Cross Island Line (CRL)**: Future green line (Future Network mode only)

### Key Features
- **Interchange Stations**: Automatic transfer detection and penalty calculation
- **Realistic Travel Times**: Based on actual MRT operational data
- **Geographic Coordinates**: Enables heuristic calculations for A* and GBFS
- **Transfer Penalties**: 3-minute penalty for line changes

## Technical Details

### Files Structure
- `web_app.py`: Flask web application server
- `task1_route_planning.py`: Core routing algorithms and network classes
- `mrt_network_data.py`: Complete MRT network dataset
- `templates/index.html`: Web interface HTML template
- `singapore_mrt_complete.py`: Comprehensive dataset with all stations and connections

### Algorithm Performance
- **BFS**: Guarantees shortest path by station count
- **A***: Guarantees optimal path by travel time
- **GBFS**: Fast but may not find optimal path
- **DFS**: Generally inefficient for route planning

### Transfer Handling
The system automatically detects when routes require transfers between different MRT lines and applies appropriate time penalties to provide realistic journey times.

## Requirements
- Python 3.7+
- Flask (`pip install flask`)
- No additional dependencies required

## Visualizations

The project includes comprehensive MRT network visualizations:
- Current network map with all operational lines
- Future network map with planned extensions
- Network statistics infographic
- Official LTA map styling with proper color coding

## Future Enhancements
- Real-time service disruption integration
- Accessibility routing options
- Cost calculation including fares
- Mobile-responsive web interface
- Integration with bus and other transport modes
- Peak hour timing considerations
- Express vs regular service routing

## Credits & Attribution

**Data Sources:**
- Land Transport Authority (LTA) Singapore
- OpenStreetMap Contributors
- LTA Data Mall

**Map Design:**
- Based on official LTA MRT network maps
- Schematic representation for clarity

**Project Purpose:**
Educational route planning application demonstrating graph search algorithms on real-world transportation networks.

---

© 2026 - Singapore MRT Route Planner
Data accurate as of February 2026
For official MRT information, visit https://www.lta.gov.sg
