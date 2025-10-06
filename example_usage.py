"""
Example usage script for Tavex Gold Subscription Monte Carlo Simulation.
This script demonstrates various ways to use the simulation tools.
"""

import pandas as pd
import numpy as np
from data_acquisition import GoldDataAcquisition
from monte_carlo_engine import TavexGoldSimulation
from analysis import TavexAnalysis
from advanced_analysis import AdvancedTavexAnalysis

def example_basic_simulation():
    """
    Example 1: Basic simulation with synthetic data
    """
    print("="*60)
    print("EXAMPLE 1: Basic Simulation with Synthetic Data")
    print("="*60)
    
    # Create synthetic historical data
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
    
    # Calculate return statistics
    return_stats = {
        'mean_monthly_return': 0.005,
        'std_monthly_return': 0.05
    }
    
    initial_gold_price = synthetic_prices[-1]
    
    # Run simulation
    simulation = TavexGoldSimulation()
    results = simulation.run_monte_carlo(
        months=36,  # 3 years
        initial_gold_price=initial_gold_price,
        monthly_return_mean=return_stats['mean_monthly_return'],
        monthly_return_std=return_stats['std_monthly_return'],
        num_simulations=1000  # Reduced for example
    )
    
    # Basic analysis
    print(f"Simulation completed with {len(results)} runs")
    print(f"Average final value: €{results['market_value'].mean():,.0f}")
    print(f"Average ROI: {results['roi'].mean()*100:.1f}%")
    print(f"Median ROI: {results['roi'].median()*100:.1f}%")
    print(f"Best case ROI: {results['roi'].max()*100:.1f}%")
    print(f"Worst case ROI: {results['roi'].min()*100:.1f}%")
    
    return results

def example_multiple_periods():
    """
    Example 2: Multiple time periods simulation
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Multiple Time Periods Simulation")
    print("="*60)
    
    # Use synthetic data for consistency
    np.random.seed(42)
    dates = pd.date_range(start='2000-01-01', end='2024-01-01', freq='M')
    synthetic_returns = np.random.normal(0.005, 0.05, len(dates))
    synthetic_prices = [50.0]
    
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
    
    # Run multiple periods
    simulation = TavexGoldSimulation()
    all_results = simulation.run_multiple_periods(
        periods=[36, 60, 120],  # 3, 5, 10 years
        initial_gold_price=initial_gold_price,
        monthly_return_mean=return_stats['mean_monthly_return'],
        monthly_return_std=return_stats['std_monthly_return'],
        num_simulations=1000
    )
    
    # Analysis
    analysis = TavexAnalysis()
    summary_table = analysis.create_summary_table(all_results)
    
    print("Summary Statistics:")
    print(summary_table.to_string(index=False))
    
    return all_results

def example_advanced_analysis():
    """
    Example 3: Advanced analysis features
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Advanced Analysis Features")
    print("="*60)
    
    # Get results from previous example
    all_results = example_multiple_periods()
    
    # Advanced analysis
    advanced_analysis = AdvancedTavexAnalysis()
    
    # Inflation-adjusted analysis
    print("\nInflation-Adjusted Analysis (2% annual inflation):")
    real_results = advanced_analysis.inflation_adjusted_analysis(all_results, inflation_rate=0.02)
    
    # Risk metrics
    print("\nRisk Metrics Analysis:")
    risk_metrics = advanced_analysis.risk_metrics_analysis(all_results)
    print(risk_metrics.to_string(index=False))
    
    # Scenario analysis
    print("\nScenario Analysis:")
    scenario_results = advanced_analysis.scenario_analysis(all_results)
    
    for months, results in scenario_results.items():
        years = results['years']
        print(f"\n{years:.0f}-Year Investment Scenarios:")
        for scenario, data in results['scenarios'].items():
            print(f"  {scenario}: {data['ROI']*100:.1f}% ROI, €{data['Market Value']:,.0f} value")
    
    return all_results, real_results, risk_metrics, scenario_results

def example_custom_parameters():
    """
    Example 4: Custom parameters and configuration
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Parameters")
    print("="*60)
    
    # Custom Tavex parameters
    custom_simulation = TavexGoldSimulation(
        buy_price_eur_per_gram=130.0,      # Higher buy price
        sell_price_eur_per_gram=115.0,     # Higher sell price
        monthly_grams=5.0,                 # More grams per month
        bonus_grams_per_year=5.0           # More bonus grams
    )
    
    print("Custom Configuration:")
    print(f"- Buy Price: €{custom_simulation.buy_price:.2f}/gram")
    print(f"- Sell Price: €{custom_simulation.sell_price:.2f}/gram")
    print(f"- Monthly Purchase: {custom_simulation.monthly_grams} grams")
    print(f"- Bonus Gold: {custom_simulation.bonus_grams_per_year} grams/year")
    print(f"- Spread: {custom_simulation.spread*100:.1f}%")
    
    # Run simulation with custom parameters
    results = custom_simulation.run_monte_carlo(
        months=60,  # 5 years
        initial_gold_price=50.0,
        monthly_return_mean=0.005,
        monthly_return_std=0.05,
        num_simulations=1000
    )
    
    print(f"\nCustom Simulation Results (5 years):")
    print(f"- Average final value: €{results['market_value'].mean():,.0f}")
    print(f"- Average ROI: {results['roi'].mean()*100:.1f}%")
    print(f"- Total grams accumulated: {results['total_grams'].mean():.1f}")
    print(f"- Total invested: €{results['total_invested'].mean():,.0f}")
    
    return results

def example_comparison_analysis():
    """
    Example 5: Compare different investment strategies
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Strategy Comparison")
    print("="*60)
    
    # Standard Tavex strategy
    standard_sim = TavexGoldSimulation(
        buy_price_eur_per_gram=124.24,
        sell_price_eur_per_gram=111.97,
        monthly_grams=4.0,
        bonus_grams_per_year=4.0
    )
    
    # No-bonus strategy (for comparison)
    no_bonus_sim = TavexGoldSimulation(
        buy_price_eur_per_gram=124.24,
        sell_price_eur_per_gram=111.97,
        monthly_grams=4.0,
        bonus_grams_per_year=0.0  # No bonus
    )
    
    # Run both simulations
    standard_results = standard_sim.run_monte_carlo(
        months=60,
        initial_gold_price=50.0,
        monthly_return_mean=0.005,
        monthly_return_std=0.05,
        num_simulations=1000
    )
    
    no_bonus_results = no_bonus_sim.run_monte_carlo(
        months=60,
        initial_gold_price=50.0,
        monthly_return_mean=0.005,
        monthly_return_std=0.05,
        num_simulations=1000
    )
    
    # Compare results
    print("Strategy Comparison (5 years):")
    print(f"{'Metric':<25} {'Standard':<15} {'No Bonus':<15} {'Difference':<15}")
    print("-" * 70)
    
    metrics = [
        ('Average ROI (%)', standard_results['roi'].mean()*100, no_bonus_results['roi'].mean()*100),
        ('Median ROI (%)', standard_results['roi'].median()*100, no_bonus_results['roi'].median()*100),
        ('Average Value (€)', standard_results['market_value'].mean(), no_bonus_results['market_value'].mean()),
        ('Total Grams', standard_results['total_grams'].mean(), no_bonus_results['total_grams'].mean()),
        ('Break-even Rate (%)', (standard_results['roi'] >= 0).mean()*100, (no_bonus_results['roi'] >= 0).mean()*100)
    ]
    
    for metric, standard, no_bonus in metrics:
        diff = standard - no_bonus
        print(f"{metric:<25} {standard:<15.1f} {no_bonus:<15.1f} {diff:<15.1f}")
    
    return standard_results, no_bonus_results

def main():
    """
    Run all examples
    """
    print("TAVEX GOLD SIMULATION - EXAMPLE USAGE")
    print("="*60)
    
    try:
        # Run examples
        example_basic_simulation()
        example_multiple_periods()
        example_advanced_analysis()
        example_custom_parameters()
        example_comparison_analysis()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
