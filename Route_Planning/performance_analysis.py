"""
Performance Analysis Script for MRT Route Planner
Collects performance metrics for all algorithms across multiple test routes
"""

import statistics
from task1_route_planning import MRTNetwork, SearchAlgorithms
from mrt_network_data import TEST_PAIRS_TODAY, TEST_PAIRS_FUTURE

def run_performance_analysis():
    """Run comprehensive performance analysis"""
    
    print("MRT Route Planner - Performance Analysis")
    print("=" * 60)
    
    # Test both network modes
    modes = ["today", "future"]
    results = {}
    
    for mode in modes:
        print(f"\nAnalyzing {mode.upper()} network...")
        
        network = MRTNetwork(mode=mode)
        searcher = SearchAlgorithms(network)
        
        # Select test pairs based on mode
        test_pairs = TEST_PAIRS_TODAY if mode == "today" else TEST_PAIRS_FUTURE
        
        # Initialize results storage
        mode_results = {
            'BFS': {'runtimes': [], 'nodes_expanded': [], 'path_costs': [], 'success_rate': 0},
            'DFS': {'runtimes': [], 'nodes_expanded': [], 'path_costs': [], 'success_rate': 0},
            'GBFS': {'runtimes': [], 'nodes_expanded': [], 'path_costs': [], 'success_rate': 0},
            'A*': {'runtimes': [], 'nodes_expanded': [], 'path_costs': [], 'success_rate': 0}
        }
        
        # Run tests for each algorithm
        algorithms = [
            ('BFS', searcher.bfs),
            ('DFS', searcher.dfs),
            ('GBFS', searcher.gbfs),
            ('A*', searcher.astar)
        ]
        
        total_tests = len(test_pairs)
        
        for origin, destination in test_pairs:
            # Skip if stations don't exist in current mode
            if origin not in network.stations or destination not in network.stations:
                continue
                
            print(f"  Testing: {origin} → {destination}")
            
            for algo_name, algo_func in algorithms:
                try:
                    path, stats = algo_func(origin, destination)
                    
                    if path:
                        mode_results[algo_name]['runtimes'].append(stats['runtime'])
                        mode_results[algo_name]['nodes_expanded'].append(stats['nodes_expanded'])
                        mode_results[algo_name]['path_costs'].append(stats['path_cost'])
                        mode_results[algo_name]['success_rate'] += 1
                    
                except Exception as e:
                    print(f"    Error in {algo_name}: {e}")
        
        # Calculate success rates
        for algo_name in mode_results:
            mode_results[algo_name]['success_rate'] = (
                mode_results[algo_name]['success_rate'] / total_tests * 100
            )
        
        results[mode] = mode_results
    
    return results

def print_performance_summary(results):
    """Print formatted performance summary"""
    
    print("\n" + "=" * 80)
    print("PERFORMANCE ANALYSIS SUMMARY")
    print("=" * 80)
    
    for mode in results:
        print(f"\n{mode.upper()} NETWORK RESULTS:")
        print("-" * 50)
        
        # Table header
        print(f"{'Algorithm':<10} {'Avg Runtime (ms)':<18} {'Avg Nodes':<12} {'Avg Path Cost':<15} {'Success Rate':<12}")
        print("-" * 70)
        
        for algo_name, data in results[mode].items():
            if data['runtimes']:
                avg_runtime = statistics.mean(data['runtimes']) * 1000  # Convert to ms
                avg_nodes = statistics.mean(data['nodes_expanded'])
                avg_cost = statistics.mean(data['path_costs'])
                success_rate = data['success_rate']
                
                print(f"{algo_name:<10} {avg_runtime:<18.4f} {avg_nodes:<12.1f} {avg_cost:<15.2f} {success_rate:<12.1f}%")
            else:
                print(f"{algo_name:<10} {'No data':<18} {'No data':<12} {'No data':<15} {'0.0%':<12}")

def generate_comparison_data(results):
    """Generate data for comparison table"""
    
    print("\n" + "=" * 80)
    print("DATA FOR PERFORMANCE COMPARISON TABLE")
    print("=" * 80)
    
    # Combine data from both modes for overall averages
    combined_results = {
        'BFS': {'runtimes': [], 'nodes_expanded': [], 'path_costs': []},
        'DFS': {'runtimes': [], 'nodes_expanded': [], 'path_costs': []},
        'GBFS': {'runtimes': [], 'nodes_expanded': [], 'path_costs': []},
        'A*': {'runtimes': [], 'nodes_expanded': [], 'path_costs': []}
    }
    
    # Combine data from both modes
    for mode in results:
        for algo_name in combined_results:
            combined_results[algo_name]['runtimes'].extend(results[mode][algo_name]['runtimes'])
            combined_results[algo_name]['nodes_expanded'].extend(results[mode][algo_name]['nodes_expanded'])
            combined_results[algo_name]['path_costs'].extend(results[mode][algo_name]['path_costs'])
    
    print("\nFor your Performance Analysis & Comparison table:")
    print("-" * 60)
    
    for algo_name, data in combined_results.items():
        if data['runtimes']:
            avg_runtime = statistics.mean(data['runtimes']) * 1000  # Convert to ms
            avg_nodes = statistics.mean(data['nodes_expanded'])
            
            # Determine path quality
            if algo_name == 'BFS':
                quality = "Optimal*"
            elif algo_name == 'A*':
                quality = "Optimal**"
            elif algo_name == 'GBFS':
                quality = "Good heuristic dependent"
            else:  # DFS
                quality = "Suboptimal"
            
            print(f"{algo_name:<4} | {avg_runtime:>8.2f} ms | {avg_nodes:>8.1f} | {quality}")
        else:
            print(f"{algo_name:<4} | No data available")
    
    print("\n* BFS finds optimal path by number of stations")
    print("** A* finds optimal path by travel time")

def analyze_mode_differences(results):
    """Analyze differences between today and future modes"""
    
    print("\n" + "=" * 80)
    print("TODAY vs FUTURE MODE ANALYSIS")
    print("=" * 80)
    
    if 'today' in results and 'future' in results:
        print("\nKey Findings:")
        
        # Compare A* performance (most relevant for practical use)
        today_astar = results['today']['A*']
        future_astar = results['future']['A*']
        
        if today_astar['runtimes'] and future_astar['runtimes']:
            today_avg_cost = statistics.mean(today_astar['path_costs'])
            future_avg_cost = statistics.mean(future_astar['path_costs'])
            
            improvement = ((today_avg_cost - future_avg_cost) / today_avg_cost) * 100
            
            print(f"• Average travel time improvement in Future Mode: {improvement:.1f}%")
            print(f"• Today network average: {today_avg_cost:.2f} minutes")
            print(f"• Future network average: {future_avg_cost:.2f} minutes")
        
        print("\nFuture Mode Benefits:")
        print("• TEL Extension provides direct T5 access")
        print("• CRL extension improves northern connectivity")
        print("• Reduced transfer requirements for cross-island travel")
        print("• Enhanced network redundancy")

def main():
    """Main function"""
    try:
        # Run performance analysis
        results = run_performance_analysis()
        
        # Print detailed summary
        print_performance_summary(results)
        
        # Generate comparison table data
        generate_comparison_data(results)
        
        # Analyze mode differences
        analyze_mode_differences(results)
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()