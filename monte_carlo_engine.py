"""
Monte Carlo simulation engine for Tavex gold subscription investment strategy.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class TavexGoldSimulation:
    def __init__(self, 
                 buy_price_eur_per_gram: float = 124.24,
                 sell_price_eur_per_gram: float = 111.97,
                 monthly_grams: float = 4.0,
                 bonus_grams_per_year: float = 4.0):
        """
        Initialize the Tavex gold simulation.
        
        Args:
            buy_price_eur_per_gram: Tavex buy price per gram
            sell_price_eur_per_gram: Tavex sell price per gram  
            monthly_grams: Grams purchased per month
            bonus_grams_per_year: Bonus grams received annually
        """
        self.buy_price = buy_price_eur_per_gram
        self.sell_price = sell_price_eur_per_gram
        self.monthly_grams = monthly_grams
        self.bonus_grams_per_year = bonus_grams_per_year
        self.spread = (buy_price_eur_per_gram - sell_price_eur_per_gram) / buy_price_eur_per_gram
        
    def simulate_single_path(self, 
                           months: int, 
                           initial_gold_price: float,
                           monthly_return_mean: float,
                           monthly_return_std: float,
                           random_seed: int = None) -> Dict:
        """
        Simulate a single investment path.
        
        Args:
            months: Number of months to simulate
            initial_gold_price: Starting gold price per gram
            monthly_return_mean: Mean monthly return
            monthly_return_std: Standard deviation of monthly returns
            random_seed: Random seed for reproducibility
            
        Returns:
            dict: Simulation results
        """
        if random_seed is not None:
            np.random.seed(random_seed)
            
        # Initialize tracking variables
        current_gold_price = initial_gold_price
        total_grams = 0.0
        total_invested = 0.0
        monthly_data = []
        
        for month in range(months):
            # Buy gold at current Tavex price
            monthly_investment = self.monthly_grams * self.buy_price
            total_invested += monthly_investment
            total_grams += self.monthly_grams
            
            # Add bonus grams at the end of each year (every 12 months)
            if (month + 1) % 12 == 0:
                total_grams += self.bonus_grams_per_year
            
            # Simulate gold price movement for next month
            if month < months - 1:  # Don't simulate price for the last month
                # Generate random return from normal distribution
                random_return = np.random.normal(monthly_return_mean, monthly_return_std)
                current_gold_price *= (1 + random_return)
            
            # Store monthly data
            monthly_data.append({
                'month': month + 1,
                'gold_price': current_gold_price,
                'total_grams': total_grams,
                'total_invested': total_invested,
                'market_value': total_grams * current_gold_price,
                'tavex_sell_value': total_grams * self.sell_price
            })
        
        # Calculate final metrics
        final_market_value = total_grams * current_gold_price
        final_tavex_sell_value = total_grams * self.sell_price
        roi = (final_market_value - total_invested) / total_invested
        tavex_roi = (final_tavex_sell_value - total_invested) / total_invested
        
        # Annualized return
        years = months / 12
        annualized_return = (final_market_value / total_invested) ** (1 / years) - 1
        tavex_annualized_return = (final_tavex_sell_value / total_invested) ** (1 / years) - 1
        
        return {
            'months': months,
            'total_grams': total_grams,
            'total_invested': total_invested,
            'final_gold_price': current_gold_price,
            'market_value': final_market_value,
            'tavex_sell_value': final_tavex_sell_value,
            'roi': roi,
            'tavex_roi': tavex_roi,
            'annualized_return': annualized_return,
            'tavex_annualized_return': tavex_annualized_return,
            'monthly_data': monthly_data
        }
    
    def run_monte_carlo(self, 
                       months: int,
                       initial_gold_price: float,
                       monthly_return_mean: float,
                       monthly_return_std: float,
                       num_simulations: int = 10000) -> pd.DataFrame:
        """
        Run Monte Carlo simulation.
        
        Args:
            months: Number of months to simulate
            initial_gold_price: Starting gold price per gram
            monthly_return_mean: Mean monthly return
            monthly_return_std: Standard deviation of monthly returns
            num_simulations: Number of simulation runs
            
        Returns:
            pd.DataFrame: Results from all simulations
        """
        print(f"Running {num_simulations:,} Monte Carlo simulations for {months} months...")
        
        results = []
        
        for i in range(num_simulations):
            if (i + 1) % 1000 == 0:
                print(f"Completed {i + 1:,} simulations...")
                
            result = self.simulate_single_path(
                months=months,
                initial_gold_price=initial_gold_price,
                monthly_return_mean=monthly_return_mean,
                monthly_return_std=monthly_return_std,
                random_seed=None  # Use different seed for each simulation
            )
            
            # Store only the final results, not monthly data
            results.append({
                'simulation': i + 1,
                'months': result['months'],
                'total_grams': result['total_grams'],
                'total_invested': result['total_invested'],
                'final_gold_price': result['final_gold_price'],
                'market_value': result['market_value'],
                'tavex_sell_value': result['tavex_sell_value'],
                'roi': result['roi'],
                'tavex_roi': result['tavex_roi'],
                'annualized_return': result['annualized_return'],
                'tavex_annualized_return': result['tavex_annualized_return']
            })
        
        print("Monte Carlo simulation completed!")
        return pd.DataFrame(results)
    
    def calculate_statistics(self, results_df: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics from simulation results.
        
        Args:
            results_df: DataFrame with simulation results
            
        Returns:
            dict: Summary statistics
        """
        stats = {}
        
        for column in ['market_value', 'tavex_sell_value', 'roi', 'tavex_roi', 
                      'annualized_return', 'tavex_annualized_return']:
            if column in results_df.columns:
                data = results_df[column]
                stats[column] = {
                    'mean': data.mean(),
                    'median': data.median(),
                    'std': data.std(),
                    'min': data.min(),
                    'max': data.max(),
                    'percentile_5': data.quantile(0.05),
                    'percentile_25': data.quantile(0.25),
                    'percentile_75': data.quantile(0.75),
                    'percentile_95': data.quantile(0.95)
                }
        
        return stats
    
    def run_multiple_periods(self, 
                           periods: List[int],
                           initial_gold_price: float,
                           monthly_return_mean: float,
                           monthly_return_std: float,
                           num_simulations: int = 10000) -> Dict:
        """
        Run simulations for multiple time periods.
        
        Args:
            periods: List of months to simulate
            initial_gold_price: Starting gold price per gram
            monthly_return_mean: Mean monthly return
            monthly_return_std: Standard deviation of monthly returns
            num_simulations: Number of simulation runs per period
            
        Returns:
            dict: Results for each period
        """
        all_results = {}
        
        for months in periods:
            print(f"\n{'='*50}")
            print(f"Simulating {months} months ({months/12:.1f} years)")
            print(f"{'='*50}")
            
            results_df = self.run_monte_carlo(
                months=months,
                initial_gold_price=initial_gold_price,
                monthly_return_mean=monthly_return_mean,
                monthly_return_std=monthly_return_std,
                num_simulations=num_simulations
            )
            
            stats = self.calculate_statistics(results_df)
            
            all_results[months] = {
                'results_df': results_df,
                'statistics': stats
            }
        
        return all_results

if __name__ == "__main__":
    # Example usage
    simulation = TavexGoldSimulation()
    
    # Example parameters
    initial_price = 50.0  # EUR per gram
    monthly_return_mean = 0.005  # 0.5% monthly
    monthly_return_std = 0.05    # 5% monthly volatility
    
    # Run simulation for 36 months (3 years)
    results = simulation.run_monte_carlo(
        months=36,
        initial_gold_price=initial_price,
        monthly_return_mean=monthly_return_mean,
        monthly_return_std=monthly_return_std,
        num_simulations=1000
    )
    
    print("\nSimulation Results:")
    print(results[['total_grams', 'market_value', 'roi', 'annualized_return']].describe())
