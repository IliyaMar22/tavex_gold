"""
Analysis and visualization module for Tavex gold simulation results.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TavexAnalysis:
    def __init__(self):
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
    def plot_value_distributions(self, all_results: Dict, save_path: str = None):
        """
        Plot histograms of end-value distributions for each period.
        
        Args:
            all_results: Results from run_multiple_periods
            save_path: Optional path to save the plot
        """
        periods = list(all_results.keys())
        n_periods = len(periods)
        
        fig, axes = plt.subplots(2, n_periods, figsize=(5*n_periods, 10))
        if n_periods == 1:
            axes = axes.reshape(2, 1)
        
        for i, (months, results) in enumerate(all_results.items()):
            years = months / 12
            df = results['results_df']
            
            # Market value distribution
            axes[0, i].hist(df['market_value'], bins=50, alpha=0.7, 
                          color=self.colors[i % len(self.colors)], edgecolor='black')
            axes[0, i].set_title(f'Market Value Distribution\n{years:.0f} Years ({months} months)')
            axes[0, i].set_xlabel('Final Market Value (EUR)')
            axes[0, i].set_ylabel('Frequency')
            axes[0, i].grid(True, alpha=0.3)
            
            # Tavex sell value distribution
            axes[1, i].hist(df['tavex_sell_value'], bins=50, alpha=0.7, 
                          color=self.colors[i % len(self.colors)], edgecolor='black')
            axes[1, i].set_title(f'Tavex Sell Value Distribution\n{years:.0f} Years ({months} months)')
            axes[1, i].set_xlabel('Final Tavex Sell Value (EUR)')
            axes[1, i].set_ylabel('Frequency')
            axes[1, i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def plot_roi_distributions(self, all_results: Dict, save_path: str = None):
        """
        Plot ROI distributions for each period.
        
        Args:
            all_results: Results from run_multiple_periods
            save_path: Optional path to save the plot
        """
        periods = list(all_results.keys())
        n_periods = len(periods)
        
        fig, axes = plt.subplots(1, n_periods, figsize=(5*n_periods, 6))
        if n_periods == 1:
            axes = [axes]
        
        for i, (months, results) in enumerate(all_results.items()):
            years = months / 12
            df = results['results_df']
            
            # Plot both market ROI and Tavex ROI
            axes[i].hist(df['roi'] * 100, bins=50, alpha=0.6, 
                        label='Market Value ROI', color=self.colors[0])
            axes[i].hist(df['tavex_roi'] * 100, bins=50, alpha=0.6, 
                        label='Tavex Sell ROI', color=self.colors[1])
            
            axes[i].set_title(f'ROI Distribution\n{years:.0f} Years ({months} months)')
            axes[i].set_xlabel('ROI (%)')
            axes[i].set_ylabel('Frequency')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def plot_annualized_returns(self, all_results: Dict, save_path: str = None):
        """
        Plot annualized return distributions.
        
        Args:
            all_results: Results from run_multiple_periods
            save_path: Optional path to save the plot
        """
        periods = list(all_results.keys())
        n_periods = len(periods)
        
        fig, axes = plt.subplots(1, n_periods, figsize=(5*n_periods, 6))
        if n_periods == 1:
            axes = [axes]
        
        for i, (months, results) in enumerate(all_results.items()):
            years = months / 12
            df = results['results_df']
            
            # Plot both market and Tavex annualized returns
            axes[i].hist(df['annualized_return'] * 100, bins=50, alpha=0.6, 
                        label='Market Value', color=self.colors[0])
            axes[i].hist(df['tavex_annualized_return'] * 100, bins=50, alpha=0.6, 
                        label='Tavex Sell', color=self.colors[1])
            
            axes[i].set_title(f'Annualized Returns\n{years:.0f} Years ({months} months)')
            axes[i].set_xlabel('Annualized Return (%)')
            axes[i].set_ylabel('Frequency')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def create_summary_table(self, all_results: Dict) -> pd.DataFrame:
        """
        Create a summary table with key statistics for each period.
        
        Args:
            all_results: Results from run_multiple_periods
            
        Returns:
            pd.DataFrame: Summary table
        """
        summary_data = []
        
        for months, results in all_results.items():
            years = months / 12
            stats = results['statistics']
            
            # Market value stats
            market_value = stats['market_value']
            market_roi = stats['roi']
            market_annualized = stats['annualized_return']
            
            # Tavex sell value stats
            tavex_value = stats['tavex_sell_value']
            tavex_roi = stats['tavex_roi']
            tavex_annualized = stats['tavex_annualized_return']
            
            summary_data.append({
                'Period (Years)': f"{years:.0f}",
                'Period (Months)': months,
                'Market Value - Median (EUR)': f"{market_value['median']:,.0f}",
                'Market Value - 5th %ile (EUR)': f"{market_value['percentile_5']:,.0f}",
                'Market Value - 95th %ile (EUR)': f"{market_value['percentile_95']:,.0f}",
                'Market ROI - Median (%)': f"{market_roi['median']*100:.1f}",
                'Market ROI - 5th %ile (%)': f"{market_roi['percentile_5']*100:.1f}",
                'Market ROI - 95th %ile (%)': f"{market_roi['percentile_95']*100:.1f}",
                'Tavex Sell - Median (EUR)': f"{tavex_value['median']:,.0f}",
                'Tavex ROI - Median (%)': f"{tavex_roi['median']*100:.1f}",
                'Market Annualized - Median (%)': f"{market_annualized['median']*100:.1f}",
                'Tavex Annualized - Median (%)': f"{tavex_annualized['median']*100:.1f}"
            })
        
        return pd.DataFrame(summary_data)
    
    def plot_break_even_analysis(self, all_results: Dict, save_path: str = None):
        """
        Analyze break-even scenarios.
        
        Args:
            all_results: Results from run_multiple_periods
            save_path: Optional path to save the plot
        """
        periods = list(all_results.keys())
        break_even_rates = []
        
        for months, results in all_results.items():
            years = months / 12
            df = results['results_df']
            
            # Calculate break-even rate (ROI >= 0)
            market_break_even = (df['roi'] >= 0).mean() * 100
            tavex_break_even = (df['tavex_roi'] >= 0).mean() * 100
            
            break_even_rates.append({
                'Years': years,
                'Market Value Break-even Rate (%)': market_break_even,
                'Tavex Sell Break-even Rate (%)': tavex_break_even
            })
        
        break_even_df = pd.DataFrame(break_even_rates)
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        ax.plot(break_even_df['Years'], break_even_df['Market Value Break-even Rate (%)'], 
                marker='o', linewidth=2, label='Market Value', color=self.colors[0])
        ax.plot(break_even_df['Years'], break_even_df['Tavex Sell Break-even Rate (%)'], 
                marker='s', linewidth=2, label='Tavex Sell', color=self.colors[1])
        
        ax.set_title('Break-even Analysis: Probability of Positive Returns')
        ax.set_xlabel('Investment Period (Years)')
        ax.set_ylabel('Break-even Rate (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)
        
        # Add horizontal line at 50%
        ax.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='50% Threshold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
        
        return break_even_df
    
    def bonus_gold_impact_analysis(self, all_results: Dict) -> pd.DataFrame:
        """
        Analyze the impact of bonus gold on returns.
        
        Args:
            all_results: Results from run_multiple_periods
            
        Returns:
            pd.DataFrame: Analysis of bonus gold impact
        """
        bonus_analysis = []
        
        for months, results in all_results.items():
            years = months / 12
            df = results['results_df']
            
            # Calculate bonus grams received
            total_bonus_grams = (months // 12) * 4  # 4 bonus grams per year
            
            # Calculate what the value would be without bonus
            # (total_grams - bonus_grams) * final_gold_price
            df['grams_without_bonus'] = df['total_grams'] - total_bonus_grams
            df['value_without_bonus'] = df['grams_without_bonus'] * df['final_gold_price']
            df['tavex_value_without_bonus'] = df['grams_without_bonus'] * 111.97  # Tavex sell price
            
            # Calculate ROI without bonus
            df['roi_without_bonus'] = (df['value_without_bonus'] - df['total_invested']) / df['total_invested']
            df['tavex_roi_without_bonus'] = (df['tavex_value_without_bonus'] - df['total_invested']) / df['total_invested']
            
            # Calculate bonus impact
            df['bonus_impact_roi'] = df['roi'] - df['roi_without_bonus']
            df['bonus_impact_tavex_roi'] = df['tavex_roi'] - df['tavex_roi_without_bonus']
            
            bonus_analysis.append({
                'Years': years,
                'Bonus Grams': total_bonus_grams,
                'Avg Bonus Impact on ROI (%)': df['bonus_impact_roi'].mean() * 100,
                'Avg Bonus Impact on Tavex ROI (%)': df['bonus_impact_tavex_roi'].mean() * 100,
                'Median Bonus Impact on ROI (%)': df['bonus_impact_roi'].median() * 100,
                'Median Bonus Impact on Tavex ROI (%)': df['bonus_impact_tavex_roi'].median() * 100
            })
        
        return pd.DataFrame(bonus_analysis)

if __name__ == "__main__":
    # Example usage
    analysis = TavexAnalysis()
    print("Analysis module loaded successfully!")
