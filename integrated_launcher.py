"""
ChangiLink AI - Integrated System Launcher
Runs all three AI systems together: Route Planning, Logical Inference, and Crowding Risk
"""

import subprocess
import threading
import time
import webbrowser
import sys
import os
from pathlib import Path

class IntegratedLauncher:
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent
        
        # System configurations
        self.systems = {
            'Route Planning': {
                'dir': self.base_dir / 'Route_Planning',
                'script': 'web_app.py',
                'port': 5000,
                'url': 'http://localhost:5000',
                'description': 'MRT Route Planning with A*, BFS, DFS, GBFS algorithms'
            },
            'Logical Inference': {
                'dir': self.base_dir / 'Logical_Inference',
                'script': 'web_app.py',
                'port': 5001,
                'url': 'http://localhost:5001',
                'description': 'Service Advisory Consistency Checking & Route Validation'
            },
            'Crowding Risk': {
                'dir': self.base_dir / 'Crowding_Risk',
                'script': 'web_app.py',
                'port': 5002,
                'url': 'http://localhost:5002',
                'description': 'Bayesian Network Crowding Risk Assessment'
            }
        }
    
    def print_banner(self):
        """Print the system banner"""
        print("=" * 80)
        print("🚇 ChangiLink AI - Integrated Transportation Intelligence System")
        print("=" * 80)
        print("🎯 Comprehensive MRT Network Analysis & Planning Suite")
        print()
        print("📋 Available Systems:")
        for name, config in self.systems.items():
            print(f"   • {name}: {config['description']}")
        print()
        print("🌐 Web Interfaces:")
        for name, config in self.systems.items():
            print(f"   • {name}: {config['url']}")
        print("=" * 80)
        print()
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = ['flask']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"   ✅ {package}")
            except ImportError:
                print(f"   ❌ {package} (missing)")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
            print("📦 Install with: pip install " + " ".join(missing_packages))
            return False
        
        print("✅ All dependencies satisfied!")
        return True
    
    def start_system(self, name, config):
        """Start a single system"""
        try:
            print(f"🚀 Starting {name}...")
            
            # Change to system directory
            os.chdir(config['dir'])
            
            # Start the web application
            process = subprocess.Popen(
                [sys.executable, config['script']],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes.append({
                'name': name,
                'process': process,
                'config': config
            })
            
            print(f"   ✅ {name} started on {config['url']}")
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to start {name}: {e}")
            return False
    
    def wait_for_systems(self):
        """Wait for all systems to be ready"""
        print("\n⏳ Waiting for systems to initialize...")
        time.sleep(5)  # Give systems time to start
        print("   ✅ Systems should be ready now")
        return list(self.systems.keys())
    
    def open_browsers(self):
        """Open web browsers for all systems"""
        print("\n🌐 Opening web interfaces...")
        
        # Create a main dashboard HTML
        self.create_dashboard()
        
        # Open the main dashboard
        dashboard_path = self.base_dir / 'dashboard.html'
        webbrowser.open(f'file://{dashboard_path.absolute()}')
        print("   ✅ Main dashboard opened")
        
        # Optional: Open individual systems
        # for name, config in self.systems.items():
        #     webbrowser.open(config['url'])
        #     print(f"   ✅ {name} opened")
    
    def create_dashboard(self):
        """Create a main dashboard HTML file"""
        dashboard_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChangiLink AI - Main Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .systems-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            padding: 40px;
        }}
        
        .system-card {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s;
            border: 2px solid transparent;
        }}
        
        .system-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            border-color: #3498db;
        }}
        
        .system-icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}
        
        .system-title {{
            font-size: 1.5em;
            color: #2c3e50;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .system-description {{
            color: #666;
            margin-bottom: 25px;
            line-height: 1.6;
        }}
        
        .system-button {{
            background: #3498db;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }}
        
        .system-button:hover {{
            background: #2980b9;
            transform: translateY(-2px);
        }}
        
        .footer {{
            background: #34495e;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #27ae60;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚇 ChangiLink AI</h1>
            <p>Integrated Transportation Intelligence System</p>
        </div>
        
        <div class="systems-grid">
            <div class="system-card">
                <div class="system-icon">🗺️</div>
                <div class="system-title">Route Planning</div>
                <div class="system-description">
                    Advanced pathfinding with A*, BFS, DFS, and GBFS algorithms.
                    Compare performance across today's and future MRT networks.
                </div>
                <a href="{self.systems['Route Planning']['url']}" class="system-button" target="_blank">
                    <span class="status-indicator"></span>Launch Route Planner
                </a>
            </div>
            
            <div class="system-card">
                <div class="system-icon">🧠</div>
                <div class="system-title">Logical Inference</div>
                <div class="system-description">
                    Service advisory consistency checking and route validation.
                    Logical reasoning for transportation decision making.
                </div>
                <a href="{self.systems['Logical Inference']['url']}" class="system-button" target="_blank">
                    <span class="status-indicator"></span>Launch Logic System
                </a>
            </div>
            
            <div class="system-card">
                <div class="system-icon">📊</div>
                <div class="system-title">Crowding Risk</div>
                <div class="system-description">
                    Bayesian network analysis for crowding risk assessment.
                    Predictive modeling for passenger flow management.
                </div>
                <a href="{self.systems['Crowding Risk']['url']}" class="system-button" target="_blank">
                    <span class="status-indicator"></span>Launch Risk Analysis
                </a>
            </div>
        </div>
        
        <div class="footer">
            <p>🎯 All systems operational and ready for analysis</p>
            <p style="margin-top: 10px; opacity: 0.8;">
                Route Planning: localhost:5000 | Logical Inference: localhost:5001 | Crowding Risk: localhost:5002
            </p>
        </div>
    </div>
    
    <script>
        // Check system status periodically
        function checkSystemStatus() {{
            const systems = [
                {{name: 'Route Planning', url: '{self.systems['Route Planning']['url']}'}},
                {{name: 'Logical Inference', url: '{self.systems['Logical Inference']['url']}'}},
                {{name: 'Crowding Risk', url: '{self.systems['Crowding Risk']['url']}'}}
            ];
            
            systems.forEach(system => {{
                fetch(system.url)
                    .then(response => {{
                        if (response.ok) {{
                            console.log(`✅ ${{system.name}} is running`);
                        }}
                    }})
                    .catch(error => {{
                        console.log(`⚠️ ${{system.name}} may be starting...`);
                    }});
            }});
        }}
        
        // Check status on load and every 30 seconds
        checkSystemStatus();
        setInterval(checkSystemStatus, 30000);
    </script>
</body>
</html>
        """
        
        dashboard_path = self.base_dir / 'dashboard.html'
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
    
    def monitor_systems(self):
        """Monitor running systems"""
        print("\n📊 System Monitor:")
        print("   Press Ctrl+C to stop all systems")
        print("   Systems running in background...")
        
        try:
            while True:
                time.sleep(5)
                
                # Check if any process has died
                for proc_info in self.processes:
                    if proc_info['process'].poll() is not None:
                        print(f"   ⚠️  {proc_info['name']} has stopped")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down all systems...")
            self.cleanup()
    
    def cleanup(self):
        """Clean up all processes"""
        for proc_info in self.processes:
            try:
                proc_info['process'].terminate()
                proc_info['process'].wait(timeout=5)
                print(f"   ✅ {proc_info['name']} stopped")
            except:
                try:
                    proc_info['process'].kill()
                    print(f"   🔥 {proc_info['name']} force stopped")
                except:
                    print(f"   ❌ Could not stop {proc_info['name']}")
        
        print("\n✅ All systems stopped. Thank you for using ChangiLink AI!")
    
    def run(self):
        """Main execution method"""
        self.print_banner()
        
        # Check dependencies
        if not self.check_dependencies():
            print("\n❌ Please install missing dependencies before continuing.")
            return
        
        print("\n🚀 Starting all systems...")
        
        # Start all systems
        failed_systems = []
        for name, config in self.systems.items():
            if not self.start_system(name, config):
                failed_systems.append(name)
        
        if failed_systems:
            print(f"\n⚠️  Some systems failed to start: {', '.join(failed_systems)}")
        
        # Wait for systems to be ready
        time.sleep(5)
        
        # Open browsers
        self.open_browsers()
        
        print("\n🎉 ChangiLink AI is ready!")
        print("\n📋 Quick Start Guide:")
        print("   1. Use the main dashboard to access all systems")
        print("   2. Route Planning: Plan optimal MRT routes")
        print("   3. Logical Inference: Validate service advisories")
        print("   4. Crowding Risk: Assess passenger flow risks")
        
        # Monitor systems
        self.monitor_systems()

def main():
    """Main function"""
    launcher = IntegratedLauncher()
    launcher.run()

if __name__ == "__main__":
    main()