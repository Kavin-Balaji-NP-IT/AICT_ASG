#!/usr/bin/env python3
"""
Crowding Risk Bayesian Network - Interactive GUI Dashboard
A comprehensive scenario simulator with split-view comparison between Today and Future modes
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from crowding_risk_bn import BayesianNetwork
import seaborn as sns

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class CrowdingRiskGUI:
    """Interactive GUI for Crowding Risk Bayesian Network Analysis"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Crowding Risk Prediction - Scenario Simulator Dashboard")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize Bayesian Network
        self.bn = BayesianNetwork()
        
        # Variables for storing current settings
        self.today_vars = {}
        self.future_vars = {}
        self.init_variables()
        
        # Create GUI
        self.setup_gui()
        
        # Initial calculation
        self.update_analysis()
    
    def init_variables(self):
        """Initialize tkinter variables for both modes"""
        # Today mode variables
        self.today_vars = {
            'W': tk.StringVar(value='Clear'),
            'T': tk.StringVar(value='Morning'),
            'D': tk.StringVar(value='Weekday'),
            'S': tk.StringVar(value='Normal')
        }
        
        # Future mode variables (initially same as today)
        self.future_vars = {
            'W': tk.StringVar(value='Clear'),
            'T': tk.StringVar(value='Morning'),
            'D': tk.StringVar(value='Weekday'),
            'S': tk.StringVar(value='Normal')
        }
        
        # Bind change events
        for var in self.today_vars.values():
            var.trace('w', self.on_variable_change)
        for var in self.future_vars.values():
            var.trace('w', self.on_variable_change)
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="Crowding Risk Prediction - Scenario Simulator Dashboard",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Changi Airport T5 Corridor - Bayesian Network Analysis",
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        subtitle_label.pack()
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Tab 1: Split View Comparison
        self.create_comparison_tab()
        
        # Tab 2: Detailed Analysis
        self.create_analysis_tab()
        
        # Tab 3: Scenario Library
        self.create_scenario_tab()
    
    def create_comparison_tab(self):
        """Create the main comparison tab with split view"""
        comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(comparison_frame, text="Today vs Future Comparison")
        
        # Split into left (Today) and right (Future) panels
        paned_window = tk.PanedWindow(comparison_frame, orient=tk.HORIZONTAL, bg='#f0f0f0')
        paned_window.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Today Mode Panel
        today_panel = self.create_mode_panel(paned_window, "Today Mode", "today", '#e74c3c')
        paned_window.add(today_panel, minsize=750)
        
        # Future Mode Panel
        future_panel = self.create_mode_panel(paned_window, "Future Mode", "future", '#27ae60')
        paned_window.add(future_panel, minsize=750)
        
        # Control buttons at bottom
        control_frame = tk.Frame(comparison_frame, bg='#f0f0f0')
        control_frame.pack(fill='x', pady=10)
        
        # Sync button
        sync_btn = tk.Button(
            control_frame,
            text="Sync Settings (Today → Future)",
            command=self.sync_settings,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        )
        sync_btn.pack(side='left', padx=10)
        
        # Reset button
        reset_btn = tk.Button(
            control_frame,
            text="Reset All",
            command=self.reset_all,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        )
        reset_btn.pack(side='left', padx=10)
        
        # Export button
        export_btn = tk.Button(
            control_frame,
            text="Export Results",
            command=self.export_results,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        )
        export_btn.pack(side='right', padx=10)
    
    def create_mode_panel(self, parent, title, mode, color):
        """Create a panel for either Today or Future mode"""
        # Main panel frame
        panel = tk.Frame(parent, bg='white', relief='raised', bd=2)
        
        # Header
        header_frame = tk.Frame(panel, bg=color, height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text=title,
            font=('Arial', 16, 'bold'),
            bg=color,
            fg='white'
        )
        header_label.pack(expand=True)
        
        # Content area
        content_frame = tk.Frame(panel, bg='white')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Input controls
        controls_frame = tk.LabelFrame(
            content_frame,
            text="Input Variables",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Get the appropriate variable set
        vars_dict = self.today_vars if mode == 'today' else self.future_vars
        
        # Weather control
        self.create_variable_control(controls_frame, "Weather (W)", 'W', 
                                   self.bn.domains['W'], vars_dict, 0)
        
        # Time of Day control
        self.create_variable_control(controls_frame, "Time of Day (T)", 'T',
                                   self.bn.domains['T'], vars_dict, 1)
        
        # Day Type control
        self.create_variable_control(controls_frame, "Day Type (D)", 'D',
                                   self.bn.domains['D'], vars_dict, 2)
        
        # Service Status control
        self.create_variable_control(controls_frame, "Service Status (S)", 'S',
                                   self.bn.domains['S'], vars_dict, 3)
        
        # Results area
        results_frame = tk.LabelFrame(
            content_frame,
            text="Prediction Results",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        results_frame.pack(fill='both', expand=True)
        
        # Create matplotlib figure for this mode
        fig = Figure(figsize=(7, 8), facecolor='white')
        canvas = FigureCanvasTkAgg(fig, results_frame)
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Store references
        if mode == 'today':
            self.today_fig = fig
            self.today_canvas = canvas
        else:
            self.future_fig = fig
            self.future_canvas = canvas
        
        return panel
    
    def create_variable_control(self, parent, label, var_name, options, vars_dict, row):
        """Create a control for a single variable"""
        # Label
        label_widget = tk.Label(
            parent,
            text=label,
            font=('Arial', 10, 'bold'),
            bg='white',
            anchor='w'
        )
        label_widget.grid(row=row, column=0, sticky='w', padx=10, pady=5)
        
        # Radio buttons
        radio_frame = tk.Frame(parent, bg='white')
        radio_frame.grid(row=row, column=1, sticky='w', padx=10, pady=5)
        
        for i, option in enumerate(options):
            radio = tk.Radiobutton(
                radio_frame,
                text=option,
                variable=vars_dict[var_name],
                value=option,
                bg='white',
                font=('Arial', 9),
                command=self.update_analysis
            )
            radio.pack(side='left', padx=5)
    
    def create_analysis_tab(self):
        """Create detailed analysis tab"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="Detailed Analysis")
        
        # Create scrollable frame
        canvas = tk.Canvas(analysis_frame, bg='white')
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Analysis content
        self.create_analysis_content(scrollable_frame)
    
    def create_analysis_content(self, parent):
        """Create content for detailed analysis tab"""
        # Title
        title_label = tk.Label(
            parent,
            text="Detailed Bayesian Network Analysis",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Network structure diagram
        structure_frame = tk.LabelFrame(
            parent,
            text="Network Structure",
            font=('Arial', 12, 'bold'),
            bg='white'
        )
        structure_frame.pack(fill='x', padx=20, pady=10)
        
        structure_text = tk.Text(
            structure_frame,
            height=15,
            width=80,
            font=('Courier', 10),
            bg='#f8f9fa',
            wrap='word'
        )
        structure_text.pack(padx=10, pady=10)
        
        # Insert network description
        network_description = """
BAYESIAN NETWORK STRUCTURE:
═══════════════════════════════════════════════════════════════════════════════

Variables and Dependencies:
──────────────────────────

• W (Weather): Clear, Rainy, Thunderstorms
  └─ Independent variable (no parents)
  └─ Based on Singapore meteorological data

• T (Time of Day): Morning, Afternoon, Evening  
  └─ Independent variable (no parents)
  └─ Represents analysis time periods

• D (Day Type): Weekday, Weekend
  └─ Independent variable (no parents)
  └─ Affects commuter vs leisure travel patterns

• M (Network Mode): Today, Future
  └─ Independent variable (scenario selection)
  └─ Today: Current network, Future: With TELe/CRL

• S (Service Status): Normal, Reduced, Disrupted
  └─ Depends on: M (Network Mode)
  └─ Future mode has better service reliability

• P (Demand Proxy): Low, Medium, High
  └─ Depends on: W, T, D, M (Weather, Time, Day Type, Mode)
  └─ Represents passenger demand levels

• C (Crowding Risk): Low, Medium, High [TARGET VARIABLE]
  └─ Depends on: P, S, M (Demand, Service Status, Mode)
  └─ The main prediction output

Network Topology:
─────────────────

    W ──┐
    T ──┼─→ P ──┐
    D ──┤       │
    M ──┼───────┼─→ C
        │       │
        └─→ S ──┘

Key Insights:
─────────────

1. Mode (M) affects both Service Status and Crowding Risk directly
2. Future mode provides better infrastructure capacity and reliability
3. Weather, Time, and Day Type influence demand patterns
4. Service disruptions significantly amplify crowding risk
5. TELe/CRL extensions provide alternative routes reducing bottlenecks
        """
        
        structure_text.insert('1.0', network_description)
        structure_text.config(state='disabled')
        
        # Probability tables summary
        cpt_frame = tk.LabelFrame(
            parent,
            text="Key Probability Relationships",
            font=('Arial', 12, 'bold'),
            bg='white'
        )
        cpt_frame.pack(fill='x', padx=20, pady=10)
        
        # Create matplotlib figure for CPT visualization
        cpt_fig = Figure(figsize=(12, 8), facecolor='white')
        cpt_canvas = FigureCanvasTkAgg(cpt_fig, cpt_frame)
        cpt_canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        self.cpt_fig = cpt_fig
        self.cpt_canvas = cpt_canvas
        self.update_cpt_visualization()
    
    def create_scenario_tab(self):
        """Create predefined scenarios tab"""
        scenario_frame = ttk.Frame(self.notebook)
        self.notebook.add(scenario_frame, text="Scenario Library")
        
        # Title
        title_label = tk.Label(
            scenario_frame,
            text="Predefined Scenario Library",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Scenarios list
        scenarios_frame = tk.Frame(scenario_frame, bg='white')
        scenarios_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Define predefined scenarios
        self.scenarios = [
            {
                'name': 'Morning Rush Hour - Clear Weather',
                'description': 'Peak morning commute with optimal conditions',
                'settings': {'W': 'Clear', 'T': 'Morning', 'D': 'Weekday', 'S': 'Normal'}
            },
            {
                'name': 'Evening Peak - Rainy Weather',
                'description': 'Evening rush with adverse weather conditions',
                'settings': {'W': 'Rainy', 'T': 'Evening', 'D': 'Weekday', 'S': 'Normal'}
            },
            {
                'name': 'Weekend Leisure Travel',
                'description': 'Typical weekend afternoon travel patterns',
                'settings': {'W': 'Clear', 'T': 'Afternoon', 'D': 'Weekend', 'S': 'Normal'}
            },
            {
                'name': 'Service Disruption - Peak Hour',
                'description': 'Major service disruption during morning peak',
                'settings': {'W': 'Clear', 'T': 'Morning', 'D': 'Weekday', 'S': 'Disrupted'}
            },
            {
                'name': 'Thunderstorm + Reduced Service',
                'description': 'Severe weather with service impacts',
                'settings': {'W': 'Thunderstorms', 'T': 'Evening', 'D': 'Weekday', 'S': 'Reduced'}
            },
            {
                'name': 'Optimal Conditions',
                'description': 'Best case scenario with all favorable conditions',
                'settings': {'W': 'Clear', 'T': 'Afternoon', 'D': 'Weekend', 'S': 'Normal'}
            }
        ]
        
        # Create scenario buttons
        for i, scenario in enumerate(self.scenarios):
            scenario_btn_frame = tk.Frame(scenarios_frame, bg='white', relief='raised', bd=1)
            scenario_btn_frame.pack(fill='x', pady=5)
            
            # Scenario info
            info_frame = tk.Frame(scenario_btn_frame, bg='white')
            info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)
            
            name_label = tk.Label(
                info_frame,
                text=scenario['name'],
                font=('Arial', 12, 'bold'),
                bg='white',
                anchor='w'
            )
            name_label.pack(anchor='w')
            
            desc_label = tk.Label(
                info_frame,
                text=scenario['description'],
                font=('Arial', 10),
                bg='white',
                fg='#7f8c8d',
                anchor='w'
            )
            desc_label.pack(anchor='w')
            
            settings_label = tk.Label(
                info_frame,
                text=f"Settings: {scenario['settings']}",
                font=('Arial', 9),
                bg='white',
                fg='#95a5a6',
                anchor='w'
            )
            settings_label.pack(anchor='w')
            
            # Load buttons
            btn_frame = tk.Frame(scenario_btn_frame, bg='white')
            btn_frame.pack(side='right', padx=10, pady=5)
            
            load_today_btn = tk.Button(
                btn_frame,
                text="Load to Today",
                command=lambda s=scenario: self.load_scenario('today', s),
                bg='#e74c3c',
                fg='white',
                font=('Arial', 9),
                padx=10
            )
            load_today_btn.pack(side='top', pady=2)
            
            load_future_btn = tk.Button(
                btn_frame,
                text="Load to Future",
                command=lambda s=scenario: self.load_scenario('future', s),
                bg='#27ae60',
                fg='white',
                font=('Arial', 9),
                padx=10
            )
            load_future_btn.pack(side='top', pady=2)
            
            load_both_btn = tk.Button(
                btn_frame,
                text="Load to Both",
                command=lambda s=scenario: self.load_scenario('both', s),
                bg='#3498db',
                fg='white',
                font=('Arial', 9),
                padx=10
            )
            load_both_btn.pack(side='top', pady=2)
    
    def load_scenario(self, target, scenario):
        """Load a predefined scenario"""
        settings = scenario['settings']
        
        if target in ['today', 'both']:
            for var, value in settings.items():
                self.today_vars[var].set(value)
        
        if target in ['future', 'both']:
            for var, value in settings.items():
                self.future_vars[var].set(value)
        
        self.update_analysis()
        messagebox.showinfo("Scenario Loaded", f"'{scenario['name']}' loaded to {target} mode(s)")
    
    def on_variable_change(self, *args):
        """Handle variable changes"""
        self.update_analysis()
    
    def update_analysis(self):
        """Update all analysis displays"""
        self.update_comparison_plots()
        self.update_cpt_visualization()
    
    def update_comparison_plots(self):
        """Update the comparison plots for both modes"""
        # Clear previous plots
        self.today_fig.clear()
        self.future_fig.clear()
        
        # Get current evidence for both modes
        today_evidence = {var: val.get() for var, val in self.today_vars.items()}
        today_evidence['M'] = 'Today'
        
        future_evidence = {var: val.get() for var, val in self.future_vars.items()}
        future_evidence['M'] = 'Future'
        
        # Run inference
        today_crowding = self.bn.inference('C', today_evidence)
        today_demand = self.bn.inference('P', today_evidence)
        
        future_crowding = self.bn.inference('C', future_evidence)
        future_demand = self.bn.inference('P', future_evidence)
        
        # Plot Today mode
        self.plot_mode_results(self.today_fig, today_crowding, today_demand, 
                              today_evidence, "Today Mode", '#e74c3c')
        
        # Plot Future mode
        self.plot_mode_results(self.future_fig, future_crowding, future_demand,
                              future_evidence, "Future Mode", '#27ae60')
        
        # Refresh canvases
        self.today_canvas.draw()
        self.future_canvas.draw()
    
    def plot_mode_results(self, fig, crowding_dist, demand_dist, evidence, title, color):
        """Plot results for a single mode"""
        # Create subplots
        gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1], hspace=0.4, wspace=0.3)
        
        # Crowding Risk Distribution (main plot)
        ax1 = fig.add_subplot(gs[0, :])
        crowding_values = list(crowding_dist.keys())
        crowding_probs = list(crowding_dist.values())
        
        bars1 = ax1.bar(crowding_values, crowding_probs, color=[color, color, color], alpha=0.7)
        ax1.set_title(f'{title} - Crowding Risk Distribution', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Probability')
        ax1.set_ylim(0, 1)
        
        # Add probability labels on bars
        for bar, prob in zip(bars1, crowding_probs):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{prob:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Demand Distribution
        ax2 = fig.add_subplot(gs[1, 0])
        demand_values = list(demand_dist.keys())
        demand_probs = list(demand_dist.values())
        
        bars2 = ax2.bar(demand_values, demand_probs, color='#3498db', alpha=0.7)
        ax2.set_title('Demand Distribution', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Probability')
        ax2.set_ylim(0, 1)
        
        for bar, prob in zip(bars2, demand_probs):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{prob:.2f}', ha='center', va='bottom', fontsize=8)
        
        # Risk Score and Summary
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.axis('off')
        
        # Calculate risk score
        risk_score = (crowding_dist['Low'] * 1 + 
                     crowding_dist['Medium'] * 2 + 
                     crowding_dist['High'] * 3)
        
        # Risk level color
        if risk_score < 1.5:
            risk_color = '#27ae60'  # Green
            risk_level = 'LOW'
        elif risk_score < 2.5:
            risk_color = '#f39c12'  # Orange
            risk_level = 'MEDIUM'
        else:
            risk_color = '#e74c3c'  # Red
            risk_level = 'HIGH'
        
        # Display risk score
        ax3.text(0.5, 0.8, 'RISK SCORE', ha='center', va='center', 
                fontsize=12, fontweight='bold', transform=ax3.transAxes)
        ax3.text(0.5, 0.6, f'{risk_score:.3f}', ha='center', va='center',
                fontsize=20, fontweight='bold', color=risk_color, transform=ax3.transAxes)
        ax3.text(0.5, 0.4, risk_level, ha='center', va='center',
                fontsize=14, fontweight='bold', color=risk_color, transform=ax3.transAxes)
        
        # Current Settings
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis('off')
        
        settings_text = f"""Current Settings:
Weather: {evidence['W']} | Time: {evidence['T']} | Day: {evidence['D']} | Service: {evidence['S']}

Key Probabilities:
• P(Crowding = High) = {crowding_dist['High']:.3f}
• P(Crowding = Medium) = {crowding_dist['Medium']:.3f}  
• P(Crowding = Low) = {crowding_dist['Low']:.3f}"""
        
        ax4.text(0.05, 0.95, settings_text, ha='left', va='top', fontsize=9,
                transform=ax4.transAxes, bbox=dict(boxstyle="round,pad=0.3", 
                facecolor='#f8f9fa', alpha=0.8))
    
    def update_cpt_visualization(self):
        """Update the CPT visualization in the analysis tab"""
        if not hasattr(self, 'cpt_fig'):
            return
        
        self.cpt_fig.clear()
        
        # Create subplots for different CPT visualizations
        gs = self.cpt_fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # 1. Service Status by Mode
        ax1 = self.cpt_fig.add_subplot(gs[0, 0])
        modes = ['Today', 'Future']
        service_states = ['Normal', 'Reduced', 'Disrupted']
        
        service_data = []
        for mode in modes:
            mode_probs = [self.bn.cpts['S'][mode][state] for state in service_states]
            service_data.append(mode_probs)
        
        x = np.arange(len(service_states))
        width = 0.35
        
        ax1.bar(x - width/2, service_data[0], width, label='Today', color='#e74c3c', alpha=0.7)
        ax1.bar(x + width/2, service_data[1], width, label='Future', color='#27ae60', alpha=0.7)
        
        ax1.set_title('Service Status by Network Mode')
        ax1.set_xlabel('Service Status')
        ax1.set_ylabel('Probability')
        ax1.set_xticks(x)
        ax1.set_xticklabels(service_states)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Weather Distribution
        ax2 = self.cpt_fig.add_subplot(gs[0, 1])
        weather_states = list(self.bn.cpts['W'].keys())
        weather_probs = list(self.bn.cpts['W'].values())
        
        colors = ['#f39c12', '#3498db', '#9b59b6']
        ax2.pie(weather_probs, labels=weather_states, colors=colors, autopct='%1.1f%%')
        ax2.set_title('Weather Distribution\n(Singapore Climate)')
        
        # 3. Crowding Risk Heatmap (sample scenarios)
        ax3 = self.cpt_fig.add_subplot(gs[1, :])
        
        # Create sample scenarios matrix
        scenarios_matrix = []
        scenario_labels = []
        
        sample_scenarios = [
            ('Clear', 'Morning', 'Weekday', 'Normal'),
            ('Clear', 'Morning', 'Weekday', 'Reduced'),
            ('Clear', 'Morning', 'Weekday', 'Disrupted'),
            ('Rainy', 'Evening', 'Weekday', 'Normal'),
            ('Rainy', 'Evening', 'Weekday', 'Reduced'),
            ('Thunderstorms', 'Evening', 'Weekday', 'Normal')
        ]
        
        for scenario in sample_scenarios:
            w, t, d, s = scenario
            scenario_label = f"{w[:4]}-{t[:3]}-{d[:3]}-{s[:3]}"
            scenario_labels.append(scenario_label)
            
            # Get crowding probabilities for both modes
            today_evidence = {'W': w, 'T': t, 'D': d, 'S': s, 'M': 'Today'}
            future_evidence = {'W': w, 'T': t, 'D': d, 'S': s, 'M': 'Future'}
            
            today_crowding = self.bn.inference('C', today_evidence)
            future_crowding = self.bn.inference('C', future_evidence)
            
            scenarios_matrix.append([
                today_crowding['High'], future_crowding['High']
            ])
        
        scenarios_matrix = np.array(scenarios_matrix)
        
        im = ax3.imshow(scenarios_matrix.T, cmap='Reds', aspect='auto', vmin=0, vmax=1)
        ax3.set_title('High Crowding Risk Probability - Scenario Comparison')
        ax3.set_xlabel('Scenarios')
        ax3.set_ylabel('Network Mode')
        ax3.set_xticks(range(len(scenario_labels)))
        ax3.set_xticklabels(scenario_labels, rotation=45, ha='right')
        ax3.set_yticks([0, 1])
        ax3.set_yticklabels(['Today', 'Future'])
        
        # Add colorbar
        cbar = self.cpt_fig.colorbar(im, ax=ax3, shrink=0.8)
        cbar.set_label('P(Crowding = High)')
        
        # Add text annotations
        for i in range(len(scenario_labels)):
            for j in range(2):
                text = ax3.text(i, j, f'{scenarios_matrix[i, j]:.3f}',
                               ha="center", va="center", color="white" if scenarios_matrix[i, j] > 0.5 else "black")
        
        self.cpt_canvas.draw()
    
    def sync_settings(self):
        """Sync Today settings to Future mode"""
        for var in self.today_vars:
            self.future_vars[var].set(self.today_vars[var].get())
        self.update_analysis()
        messagebox.showinfo("Settings Synced", "Today mode settings copied to Future mode")
    
    def reset_all(self):
        """Reset all settings to defaults"""
        defaults = {'W': 'Clear', 'T': 'Morning', 'D': 'Weekday', 'S': 'Normal'}
        
        for var in defaults:
            self.today_vars[var].set(defaults[var])
            self.future_vars[var].set(defaults[var])
        
        self.update_analysis()
        messagebox.showinfo("Reset Complete", "All settings reset to defaults")
    
    def export_results(self):
        """Export current results to CSV"""
        try:
            # Get current evidence
            today_evidence = {var: val.get() for var, val in self.today_vars.items()}
            today_evidence['M'] = 'Today'
            
            future_evidence = {var: val.get() for var, val in self.future_vars.items()}
            future_evidence['M'] = 'Future'
            
            # Run inference
            today_crowding = self.bn.inference('C', today_evidence)
            future_crowding = self.bn.inference('C', future_evidence)
            
            # Create results dataframe
            results = []
            for mode, evidence, crowding in [('Today', today_evidence, today_crowding),
                                           ('Future', future_evidence, future_crowding)]:
                risk_score = (crowding['Low'] * 1 + crowding['Medium'] * 2 + crowding['High'] * 3)
                results.append({
                    'Mode': mode,
                    'Weather': evidence['W'],
                    'Time': evidence['T'],
                    'Day_Type': evidence['D'],
                    'Service_Status': evidence['S'],
                    'P_Crowding_Low': crowding['Low'],
                    'P_Crowding_Medium': crowding['Medium'],
                    'P_Crowding_High': crowding['High'],
                    'Risk_Score': risk_score
                })
            
            df = pd.DataFrame(results)
            
            # Save to CSV
            filename = 'crowding_risk_results.csv'
            df.to_csv(filename, index=False)
            
            messagebox.showinfo("Export Complete", f"Results exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = CrowdingRiskGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()