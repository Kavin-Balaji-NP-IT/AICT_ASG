"""
MRT Route Planner - User Interface
A graphical interface for planning MRT routes in Singapore
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Optional, List, Dict
from task1_route_planning import MRTNetwork, SearchAlgorithms
from mrt_network_data import LINE_COLORS, LINE_NAMES, INTERCHANGE_STATIONS


class RouteResultWindow:
    """Window to display route planning results"""
    
    def __init__(self, parent, route_data):
        self.window = tk.Toplevel(parent)
        self.window.title("Route Planning Results")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.route_data = route_data
        self.setup_ui()
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"800x600+{x}+{y}")
    
    def setup_ui(self):
        """Setup the results window UI"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Route Planning Results", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="Route Details")
        
        # Statistics tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Algorithm Statistics")
        
        # Setup results tab
        self.setup_results_tab(results_frame)
        
        # Setup statistics tab
        self.setup_stats_tab(stats_frame)
        
        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=self.window.destroy)
        close_button.grid(row=2, column=0, pady=(20, 0))
    
    def setup_results_tab(self, parent):
        """Setup the route results tab"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # Scrollable text widget
        text_frame = ttk.Frame(parent)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padding="10")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbar
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Insert route data
        self.display_route_results(text_widget)
        
        # Make text widget read-only
        text_widget.configure(state='disabled')
    
    def setup_stats_tab(self, parent):
        """Setup the statistics comparison tab"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # Create treeview for statistics
        tree_frame = ttk.Frame(parent, padding="10")
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Treeview with columns
        columns = ('Algorithm', 'Path Found', 'Path Length', 'Cost (min)', 'Nodes Expanded', 'Runtime (ms)')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Populate statistics
        self.populate_statistics(tree)
    
    def display_route_results(self, text_widget):
        """Display route results in text widget"""
        content = []
        
        if 'error' in self.route_data:
            content.append(f"ERROR: {self.route_data['error']}\n")
            text_widget.insert(tk.END, '\n'.join(content))
            return
        
        # Route information
        origin = self.route_data.get('origin', 'Unknown')
        destination = self.route_data.get('destination', 'Unknown')
        mode = self.route_data.get('mode', 'today')
        
        content.append(f"Route: {origin} → {destination}")
        content.append(f"Network Mode: {mode.title()}")
        content.append("=" * 60)
        content.append("")
        
        # Display results for each algorithm
        algorithms = ['BFS', 'DFS', 'GBFS', 'A*']
        
        for algo in algorithms:
            if algo in self.route_data:
                result = self.route_data[algo]
                content.append(f"{algo} Results:")
                content.append("-" * 30)
                
                if 'path' in result and result['path']:
                    path = result['path']
                    stats = result['stats']
                    
                    content.append(f"Path Found: {' → '.join(path)}")
                    content.append(f"Stations: {len(path)}")
                    content.append(f"Travel Time: {stats.get('path_cost', 0):.2f} minutes")
                    content.append(f"Nodes Expanded: {stats.get('nodes_expanded', 0)}")
                    content.append(f"Runtime: {stats.get('runtime', 0)*1000:.4f} ms")
                    
                    # Add detailed route with lines if available
                    if 'detailed_route' in result:
                        content.append("\nDetailed Route:")
                        for step in result['detailed_route']:
                            content.append(f"  {step}")
                else:
                    content.append("No path found")
                    if 'error' in result.get('stats', {}):
                        content.append(f"Error: {result['stats']['error']}")
                
                content.append("")
        
        text_widget.insert(tk.END, '\n'.join(content))
    
    def populate_statistics(self, tree):
        """Populate the statistics treeview"""
        algorithms = ['BFS', 'DFS', 'GBFS', 'A*']
        
        for algo in algorithms:
            if algo in self.route_data:
                result = self.route_data[algo]
                
                if 'path' in result and result['path']:
                    stats = result['stats']
                    values = (
                        algo,
                        "Yes",
                        len(result['path']),
                        f"{stats.get('path_cost', 0):.2f}",
                        stats.get('nodes_expanded', 0),
                        f"{stats.get('runtime', 0)*1000:.4f}"
                    )
                else:
                    values = (
                        algo,
                        "No",
                        "-",
                        "-",
                        result.get('stats', {}).get('nodes_expanded', 0),
                        f"{result.get('stats', {}).get('runtime', 0)*1000:.4f}"
                    )
                
                tree.insert('', tk.END, values=values)


class MRTRoutePlannerApp:
    """Main application class for MRT Route Planner"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Singapore MRT Route Planner")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Initialize network and searcher
        self.network = None
        self.searcher = None
        self.current_mode = "today"
        
        # Station lists for autocomplete
        self.station_names = []
        
        self.setup_ui()
        self.update_network()
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
    
    def setup_ui(self):
        """Setup the main application UI"""
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Singapore MRT Route Planner", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 30))
        
        # Network mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Network Mode", padding="10")
        mode_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.mode_var = tk.StringVar(value="today")
        today_radio = ttk.Radiobutton(mode_frame, text="Today's Network", 
                                     variable=self.mode_var, value="today",
                                     command=self.on_mode_change)
        future_radio = ttk.Radiobutton(mode_frame, text="Future Network (with TEL Extension & CRL)", 
                                      variable=self.mode_var, value="future",
                                      command=self.on_mode_change)
        
        today_radio.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        future_radio.grid(row=0, column=1, sticky=tk.W)
        
        # Station selection
        station_frame = ttk.LabelFrame(main_frame, text="Route Planning", padding="10")
        station_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        station_frame.columnconfigure(1, weight=1)
        
        # Origin station
        ttk.Label(station_frame, text="From:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.origin_var = tk.StringVar()
        self.origin_combo = ttk.Combobox(station_frame, textvariable=self.origin_var, 
                                        width=30, state="readonly")
        self.origin_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 10))
        
        # Destination station
        ttk.Label(station_frame, text="To:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.destination_var = tk.StringVar()
        self.destination_combo = ttk.Combobox(station_frame, textvariable=self.destination_var, 
                                             width=30, state="readonly")
        self.destination_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 10))
        
        # Swap button
        swap_button = ttk.Button(station_frame, text="⇅ Swap", command=self.swap_stations)
        swap_button.grid(row=0, column=2, rowspan=2, padx=(10, 0))
        
        # Algorithm selection
        algo_frame = ttk.LabelFrame(main_frame, text="Search Algorithm", padding="10")
        algo_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.algorithm_var = tk.StringVar(value="all")
        
        algorithms = [
            ("All Algorithms", "all"),
            ("Breadth-First Search (BFS)", "BFS"),
            ("Depth-First Search (DFS)", "DFS"),
            ("Greedy Best-First Search (GBFS)", "GBFS"),
            ("A* Search", "A*")
        ]
        
        for i, (text, value) in enumerate(algorithms):
            radio = ttk.Radiobutton(algo_frame, text=text, variable=self.algorithm_var, value=value)
            radio.grid(row=i//2, column=i%2, sticky=tk.W, padx=(0, 20), pady=2)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 20))
        
        self.plan_button = ttk.Button(button_frame, text="Plan Route", 
                                     command=self.plan_route, style="Accent.TButton")
        self.plan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_selections)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Quick test buttons
        test_frame = ttk.LabelFrame(main_frame, text="Quick Test Routes", padding="10")
        test_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.setup_test_buttons(test_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
    
    def setup_test_buttons(self, parent):
        """Setup quick test route buttons"""
        test_routes_today = [
            ("Changi Airport → City Hall", "Changi Airport", "City Hall"),
            ("Boon Lay → Punggol", "Boon Lay", "Punggol"),
            ("HarbourFront → Woodlands", "HarbourFront", "Woodlands")
        ]
        
        test_routes_future = [
            ("Changi Terminal 5 → Marina Bay", "Changi Terminal 5", "Marina Bay"),
            ("Pasir Ris → Changi Terminal 5", "Pasir Ris", "Changi Terminal 5"),
            ("Boon Lay → Changi Terminal 5", "Boon Lay", "Changi Terminal 5")
        ]
        
        # Store test routes for dynamic updates
        self.test_routes_today = test_routes_today
        self.test_routes_future = test_routes_future
        
        # Create buttons frame
        self.test_buttons_frame = ttk.Frame(parent)
        self.test_buttons_frame.pack(fill=tk.X)
        
        self.update_test_buttons()
    
    def update_test_buttons(self):
        """Update test buttons based on current mode"""
        # Clear existing buttons
        for widget in self.test_buttons_frame.winfo_children():
            widget.destroy()
        
        # Select appropriate test routes
        test_routes = self.test_routes_today if self.current_mode == "today" else self.test_routes_future
        
        for i, (text, origin, destination) in enumerate(test_routes):
            button = ttk.Button(self.test_buttons_frame, text=text,
                               command=lambda o=origin, d=destination: self.set_test_route(o, d))
            button.grid(row=i//2, column=i%2, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Configure grid weights
        self.test_buttons_frame.columnconfigure(0, weight=1)
        self.test_buttons_frame.columnconfigure(1, weight=1)
    
    def set_test_route(self, origin: str, destination: str):
        """Set a test route"""
        if origin in self.station_names:
            self.origin_var.set(origin)
        if destination in self.station_names:
            self.destination_var.set(destination)
        self.status_var.set(f"Test route set: {origin} → {destination}")
    
    def update_network(self):
        """Update network based on current mode"""
        self.status_var.set("Updating network...")
        self.root.update()
        
        try:
            self.network = MRTNetwork(mode=self.current_mode)
            self.searcher = SearchAlgorithms(self.network)
            
            # Update station lists
            self.station_names = sorted(list(self.network.stations))
            self.origin_combo['values'] = self.station_names
            self.destination_combo['values'] = self.station_names
            
            # Update test buttons
            self.update_test_buttons()
            
            self.status_var.set(f"Network updated: {len(self.station_names)} stations ({self.current_mode} mode)")
            
        except Exception as e:
            self.status_var.set(f"Error updating network: {str(e)}")
            messagebox.showerror("Error", f"Failed to update network: {str(e)}")
    
    def on_mode_change(self):
        """Handle network mode change"""
        new_mode = self.mode_var.get()
        if new_mode != self.current_mode:
            self.current_mode = new_mode
            self.clear_selections()
            self.update_network()
    
    def swap_stations(self):
        """Swap origin and destination stations"""
        origin = self.origin_var.get()
        destination = self.destination_var.get()
        self.origin_var.set(destination)
        self.destination_var.set(origin)
        self.status_var.set("Stations swapped")
    
    def clear_selections(self):
        """Clear all selections"""
        self.origin_var.set("")
        self.destination_var.set("")
        self.algorithm_var.set("all")
        self.status_var.set("Selections cleared")
    
    def validate_inputs(self) -> bool:
        """Validate user inputs"""
        origin = self.origin_var.get().strip()
        destination = self.destination_var.get().strip()
        
        if not origin:
            messagebox.showerror("Error", "Please select an origin station")
            return False
        
        if not destination:
            messagebox.showerror("Error", "Please select a destination station")
            return False
        
        if origin == destination:
            messagebox.showerror("Error", "Origin and destination cannot be the same")
            return False
        
        if origin not in self.station_names:
            messagebox.showerror("Error", f"Invalid origin station: {origin}")
            return False
        
        if destination not in self.station_names:
            messagebox.showerror("Error", f"Invalid destination station: {destination}")
            return False
        
        return True
    
    def plan_route(self):
        """Plan route using selected algorithm(s)"""
        if not self.validate_inputs():
            return
        
        origin = self.origin_var.get().strip()
        destination = self.destination_var.get().strip()
        selected_algo = self.algorithm_var.get()
        
        self.status_var.set("Planning route...")
        self.plan_button.configure(state='disabled')
        self.root.update()
        
        try:
            # Run route planning in a separate thread to avoid UI freezing
            threading.Thread(target=self._run_route_planning, 
                           args=(origin, destination, selected_algo), 
                           daemon=True).start()
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.plan_button.configure(state='normal')
            messagebox.showerror("Error", f"Route planning failed: {str(e)}")
    
    def _run_route_planning(self, origin: str, destination: str, selected_algo: str):
        """Run route planning in background thread"""
        try:
            results = {
                'origin': origin,
                'destination': destination,
                'mode': self.current_mode
            }
            
            # Define algorithms to run
            if selected_algo == "all":
                algorithms = [
                    ("BFS", self.searcher.bfs),
                    ("DFS", self.searcher.dfs),
                    ("GBFS", self.searcher.gbfs),
                    ("A*", self.searcher.astar)
                ]
            else:
                algo_map = {
                    "BFS": self.searcher.bfs,
                    "DFS": self.searcher.dfs,
                    "GBFS": self.searcher.gbfs,
                    "A*": self.searcher.astar
                }
                algorithms = [(selected_algo, algo_map[selected_algo])]
            
            # Run selected algorithms
            for algo_name, algo_func in algorithms:
                path, stats = algo_func(origin, destination)
                results[algo_name] = {
                    'path': path,
                    'stats': stats,
                    'detailed_route': self._get_detailed_route(path) if path else None
                }
            
            # Update UI in main thread
            self.root.after(0, self._show_results, results)
            
        except Exception as e:
            error_msg = f"Route planning failed: {str(e)}"
            self.root.after(0, self._show_error, error_msg)
    
    def _get_detailed_route(self, path: List[str]) -> List[str]:
        """Get detailed route with line information"""
        if not path or len(path) < 2:
            return []
        
        detailed = []
        current_line = None
        
        for i in range(len(path) - 1):
            current_station = path[i]
            next_station = path[i + 1]
            
            # Find the line for this segment
            for neighbor, travel_time, line in self.network.get_neighbors(current_station):
                if neighbor == next_station:
                    if current_line != line:
                        if current_line is not None:
                            detailed.append(f"  → Transfer to {LINE_NAMES.get(line, line)} at {current_station}")
                        detailed.append(f"  → Take {LINE_NAMES.get(line, line)}")
                        current_line = line
                    
                    detailed.append(f"    {current_station} → {next_station} ({travel_time} min)")
                    break
        
        return detailed
    
    def _show_results(self, results: Dict):
        """Show results in UI (called from main thread)"""
        self.plan_button.configure(state='normal')
        self.status_var.set("Route planning completed")
        
        # Show results window
        RouteResultWindow(self.root, results)
    
    def _show_error(self, error_msg: str):
        """Show error in UI (called from main thread)"""
        self.plan_button.configure(state='normal')
        self.status_var.set("Route planning failed")
        messagebox.showerror("Error", error_msg)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main function to start the application"""
    try:
        app = MRTRoutePlannerApp()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")


if __name__ == "__main__":
    main()