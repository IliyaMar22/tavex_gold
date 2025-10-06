"""
Main execution script for Tavex Gold Subscription Monte Carlo Simulation.

This script demonstrates the complete workflow:
1. Fetch historical gold price data
2. Run Monte Carlo simulations for multiple time periods
3. Generate comprehensive analysis and visualizations
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

from data_acquisition import GoldDataAcquisition
from monte_carlo_engine import TavexGoldSimulation
from analysis import TavexAnalysis

def main():
    """
    Main execution function for the Tavex gold simulation.
    """
    print("="*60)
    print("TAVEX GOLD SUBSCRIPTION MONTE CARLO SIMULATION")
    print("="*60)
    
    # Configuration
    config = {
        'tavex_buy_price': 124.24,      # EUR per gram
        'tavex_sell_price': 111.97,     # EUR per gram
        'monthly_grams': 4.0,           # grams per month
        'bonus_grams_per_year': 4.0,    # bonus grams per year
        'simulation_periods': [36, 60, 120],  # months: 3, 5, 10 years
        'num_simulations': 10000,       # number of Monte Carlo runs
        'data_file': 'gold_historical_data.csv'
    }
    
    print(f"Configuration:")
    print(f"- Tavex Buy Price: €{config['tavex_buy_price']:.2f}/gram")
    print(f"- Tavex Sell Price: €{config['tavex_sell_price']:.2f}/gram")
    print(f"- Monthly Purchase: {config['monthly_grams']} grams")
    print(f"- Bonus Gold: {config['bonus_grams_per_year']} grams/year")
    print(f"- Simulation Periods: {[f'{p/12:.0f} years' for p in config['simulation_periods']]}")
    print(f"- Number of Simulations: {config['num_simulations']:,}")
    print()
    
    # Step 1: Data Acquisition
    print("Step 1: Fetching Historical Gold Price Data")
    print("-" * 40)
    
    acquisition = GoldDataAcquisition()
    
    # Try to load existing data first
    if os.path.exists(config['data_file']):
        print(f"Loading existing data from {config['data_file']}...")
        try:
            historical_data = acquisition.load_data(config['data_file'])
        except Exception as e:
            print(f"Error loading existing data: {e}")
            print("Fetching fresh data...")
            historical_data = acquisition.fetch_historical_data()
            acquisition.save_data(historical_data, config['data_file'])
    else:
        print("No existing data found. Fetching fresh data...")
        historical_data = acquisition.fetch_historical_data()
        acquisition.save_data(historical_data, config['data_file'])
    
    # Get return statistics
    return_stats = acquisition.get_return_statistics(historical_data)
    print(f"\nHistorical Return Statistics:")
    print(f"- Mean Monthly Return: {return_stats['mean_monthly_return']:.4f} ({return_stats['mean_monthly_return']*100:.2f}%)")
    print(f"- Std Monthly Return: {return_stats['std_monthly_return']:.4f} ({return_stats['std_monthly_return']*100:.2f}%)")
    print(f"- Min Monthly Return: {return_stats['min_monthly_return']:.4f} ({return_stats['min_monthly_return']*100:.2f}%)")
    print(f"- Max Monthly Return: {return_stats['max_monthly_return']:.4f} ({return_stats['max_monthly_return']*100:.2f}%)")
    print(f"- Total Observations: {return_stats['total_observations']:,}")
    
    # Use the most recent gold price as starting point
    initial_gold_price = historical_data['gold_eur_per_gram'].iloc[-1]
    print(f"- Current Gold Price: €{initial_gold_price:.2f}/gram")
    print()
    
    # Step 2: Monte Carlo Simulation
    print("Step 2: Running Monte Carlo Simulations")
    print("-" * 40)
    
    simulation = TavexGoldSimulation(
        buy_price_eur_per_gram=config['tavex_buy_price'],
        sell_price_eur_per_gram=config['tavex_sell_price'],
        monthly_grams=config['monthly_grams'],
        bonus_grams_per_year=config['bonus_grams_per_year']
    )
    
    # Run simulations for all periods
    all_results = simulation.run_multiple_periods(
        periods=config['simulation_periods'],
        initial_gold_price=initial_gold_price,
        monthly_return_mean=return_stats['mean_monthly_return'],
        monthly_return_std=return_stats['std_monthly_return'],
        num_simulations=config['num_simulations']
    )
    
    # Step 3: Analysis and Visualization
    print("\nStep 3: Generating Analysis and Visualizations")
    print("-" * 40)
    
    analysis = TavexAnalysis()
    
    # Create output directory
    output_dir = "simulation_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate summary table
    print("Creating summary table...")
    summary_table = analysis.create_summary_table(all_results)
    print("\nSUMMARY STATISTICS:")
    print("="*80)
    print(summary_table.to_string(index=False))
    
    # Save summary table
    summary_table.to_csv(f"{output_dir}/summary_statistics.csv", index=False)
    print(f"\nSummary table saved to {output_dir}/summary_statistics.csv")
    
    # Generate plots
    print("\nGenerating visualizations...")
    
    # Value distributions
    print("- Value distribution plots...")
    analysis.plot_value_distributions(all_results, f"{output_dir}/value_distributions.png")
    
    # ROI distributions
    print("- ROI distribution plots...")
    analysis.plot_roi_distributions(all_results, f"{output_dir}/roi_distributions.png")
    
    # Annualized returns
    print("- Annualized return plots...")
    analysis.plot_annualized_returns(all_results, f"{output_dir}/annualized_returns.png")
    
    # Break-even analysis
    print("- Break-even analysis...")
    break_even_df = analysis.plot_break_even_analysis(all_results, f"{output_dir}/break_even_analysis.png")
    break_even_df.to_csv(f"{output_dir}/break_even_analysis.csv", index=False)
    
    # Bonus gold impact analysis
    print("- Bonus gold impact analysis...")
    bonus_analysis_df = analysis.bonus_gold_impact_analysis(all_results)
    print("\nBONUS GOLD IMPACT ANALYSIS:")
    print("="*60)
    print(bonus_analysis_df.to_string(index=False))
    bonus_analysis_df.to_csv(f"{output_dir}/bonus_gold_impact.csv", index=False)
    
    # Step 4: Key Insights
    print("\nStep 4: Key Insights")
    print("-" * 40)
    
    # Calculate some key insights
    for months, results in all_results.items():
        years = months / 12
        df = results['results_df']
        stats = results['statistics']
        
        print(f"\n{int(years)}-Year Investment Period:")
        print(f"- Median Market Value: €{stats['market_value']['median']:,.0f}")
        print(f"- Median Tavex Sell Value: €{stats['tavex_sell_value']['median']:,.0f}")
        print(f"- Median Market ROI: {stats['roi']['median']*100:.1f}%")
        print(f"- Median Tavex ROI: {stats['tavex_roi']['median']*100:.1f}%")
        print(f"- Break-even probability (Market): {(df['roi'] >= 0).mean()*100:.1f}%")
        print(f"- Break-even probability (Tavex): {(df['tavex_roi'] >= 0).mean()*100:.1f}%")
        print(f"- Worst case (5th percentile) Market ROI: {stats['roi']['percentile_5']*100:.1f}%")
        print(f"- Best case (95th percentile) Market ROI: {stats['roi']['percentile_95']*100:.1f}%")
    
    print(f"\nAll results saved to '{output_dir}' directory.")
    print("\nSimulation completed successfully!")
    
    return all_results, summary_table, break_even_df, bonus_analysis_df

def run_quick_demo():
    """
    Run a quick demonstration with fewer simulations for testing.
    """
    print("Running Quick Demo (1000 simulations)...")
    
    # Override configuration for quick demo
    config = {
        'tavex_buy_price': 124.24,
        'tavex_sell_price': 111.97,
        'monthly_grams': 4.0,
        'bonus_grams_per_year': 4.0,
        'simulation_periods': [36, 60],  # Only 3 and 5 years
        'num_simulations': 1000,  # Reduced for quick demo
        'data_file': 'gold_historical_data_demo.csv'
    }
    
    # Use synthetic data for demo
    np.random.seed(42)
    dates = pd.date_range(start='2000-01-01', end='2024-01-01', freq='M')
    synthetic_returns = np.random.normal(0.005, 0.05, len(dates))
    synthetic_prices = [50.0]  # Starting price
    
    for ret in synthetic_returns[1:]:
        synthetic_prices.append(synthetic_prices[-1] * (1 + ret))
    
    historical_data = pd.DataFrame({
        'gold_eur_per_gram': synthetic_prices,
        'monthly_return': [0] + list(synthetic_returns[1:])
    }, index=dates)
    
    return_stats = {
        'mean_monthly_return': 0.005,
        'std_monthly_return': 0.05
    }
    
    initial_gold_price = synthetic_prices[-1]
    
    # Run simulation
    simulation = TavexGoldSimulation(
        buy_price_eur_per_gram=config['tavex_buy_price'],
        sell_price_eur_per_gram=config['tavex_sell_price'],
        monthly_grams=config['monthly_grams'],
        bonus_grams_per_year=config['bonus_grams_per_year']
    )
    
    all_results = simulation.run_multiple_periods(
        periods=config['simulation_periods'],
        initial_gold_price=initial_gold_price,
        monthly_return_mean=return_stats['mean_monthly_return'],
        monthly_return_std=return_stats['std_monthly_return'],
        num_simulations=config['num_simulations']
    )
    
    # Quick analysis
    analysis = TavexAnalysis()
    summary_table = analysis.create_summary_table(all_results)
    print("\nQuick Demo Results:")
    print(summary_table.to_string(index=False))
    
    return all_results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Run quick demo
        run_quick_demo()
    else:
        # Run full simulation
        try:
            main()
        except Exception as e:
            print(f"Error running simulation: {e}")
            print("Try running with 'python main.py demo' for a quick demonstration.")
