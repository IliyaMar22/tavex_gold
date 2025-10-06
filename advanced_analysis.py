"""
Advanced analysis module for Tavex gold simulation.
Includes additional features like inflation adjustment, scenario analysis, and risk metrics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class AdvancedTavexAnalysis:
    def __init__(self):
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
    def inflation_adjusted_analysis(self, all_results: Dict, inflation_rate: float = 0.02) -> Dict:
        """
        Calculate inflation-adjusted (real) returns.
        
        Args:
            all_results: Results from run_multiple_periods
            inflation_rate: Annual inflation rate (default 2%)
            
        Returns:
            dict: Inflation-adjusted results
        """
        inflation_adjusted_results = {}
        
        for months, results in all_results.items():
            years = months / 12
            df = results['results_df'].copy()
            
            # Calculate inflation factor
            inflation_factor = (1 + inflation_rate) ** years
            
            # Adjust values for inflation
            df['real_market_value'] = df['market_value'] / inflation_factor
            df['real_tavex_sell_value'] = df['tavex_sell_value'] / inflation_factor
            df['real_total_invested'] = df['total_invested'] / inflation_factor
            
            # Calculate real ROI
            df['real_roi'] = (df['real_market_value'] - df['real_total_invested']) / df['real_total_invested']
            df['real_tavex_roi'] = (df['real_tavex_sell_value'] - df['real_total_invested']) / df['real_total_invested']
            
            # Calculate real annualized returns
            df['real_annualized_return'] = (df['real_market_value'] / df['real_total_invested']) ** (1 / years) - 1
            df['real_tavex_annualized_return'] = (df['real_tavex_sell_value'] / df['real_total_invested']) ** (1 / years) - 1
            
            inflation_adjusted_results[months] = {
                'results_df': df,
                'inflation_rate': inflation_rate,
                'years': years
            }
        
        return inflation_adjusted_results
    
    def plot_inflation_comparison(self, nominal_results: Dict, real_results: Dict, save_path: str = None):
        """
        Compare nominal vs real returns.
        
        Args:
            nominal_results: Original results (nominal)
            real_results: Inflation-adjusted results
            save_path: Optional path to save the plot
        """
        periods = list(nominal_results.keys())
        n_periods = len(periods)
        
        fig, axes = plt.subplots(2, n_periods, figsize=(5*n_periods, 10))
        if n_periods == 1:
            axes = axes.reshape(2, 1)
        
        for i, months in enumerate(periods):
            years = months / 12
            nominal_df = nominal_results[months]['results_df']
            real_df = real_results[months]['results_df']
            
            # Market ROI comparison
            axes[0, i].hist(nominal_df['roi'] * 100, bins=50, alpha=0.6, 
                          label='Nominal', color=self.colors[0])
            axes[0, i].hist(real_df['real_roi'] * 100, bins=50, alpha=0.6, 
                          label='Real (Inflation-Adjusted)', color=self.colors[1])
            axes[0, i].set_title(f'Market ROI: Nominal vs Real\n{years:.0f} Years')
            axes[0, i].set_xlabel('ROI (%)')
            axes[0, i].set_ylabel('Frequency')
            axes[0, i].legend()
            axes[0, i].grid(True, alpha=0.3)
            
            # Tavex ROI comparison
            axes[1, i].hist(nominal_df['tavex_roi'] * 100, bins=50, alpha=0.6, 
                          label='Nominal', color=self.colors[0])
            axes[1, i].hist(real_df['real_tavex_roi'] * 100, bins=50, alpha=0.6, 
                          label='Real (Inflation-Adjusted)', color=self.colors[1])
            axes[1, i].set_title(f'Tavex ROI: Nominal vs Real\n{years:.0f} Years')
            axes[1, i].set_xlabel('ROI (%)')
            axes[1, i].set_ylabel('Frequency')
            axes[1, i].legend()
            axes[1, i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def scenario_analysis(self, all_results: Dict) -> Dict:
        """
        Perform scenario analysis (bull, base, bear markets).
        
        Args:
            all_results: Results from run_multiple_periods
            
        Returns:
            dict: Scenario analysis results
        """
        scenario_results = {}
        
        for months, results in all_results.items():
            years = months / 12
            df = results['results_df']
            
            # Define scenarios based on percentiles
            scenarios = {
                'Bear Market (5th percentile)': df['roi'].quantile(0.05),
                'Pessimistic (25th percentile)': df['roi'].quantile(0.25),
                'Base Case (50th percentile)': df['roi'].quantile(0.50),
                'Optimistic (75th percentile)': df['roi'].quantile(0.75),
                'Bull Market (95th percentile)': df['roi'].quantile(0.95)
            }
            
            # Calculate corresponding values
            scenario_values = {}
            for scenario, roi in scenarios.items():
                # Find the closest actual ROI
                closest_idx = (df['roi'] - roi).abs().idxmin()
                scenario_values[scenario] = {
                    'ROI': roi,
                    'Market Value': df.loc[closest_idx, 'market_value'],
                    'Tavex Sell Value': df.loc[closest_idx, 'tavex_sell_value'],
                    'Total Invested': df.loc[closest_idx, 'total_invested'],
                    'Total Grams': df.loc[closest_idx, 'total_grams'],
                    'Final Gold Price': df.loc[closest_idx, 'final_gold_price']
                }
            
            scenario_results[months] = {
                'years': years,
                'scenarios': scenario_values
            }
        
        return scenario_results
    
    def plot_scenario_analysis(self, scenario_results: Dict, save_path: str = None):
        """
        Plot scenario analysis results.
        
        Args:
            scenario_results: Results from scenario_analysis
            save_path: Optional path to save the plot
        """
        periods = list(scenario_results.keys())
        n_periods = len(periods)
        
        fig, axes = plt.subplots(1, n_periods, figsize=(6*n_periods, 6))
        if n_periods == 1:
            axes = [axes]
        
        for i, (months, results) in enumerate(scenario_results.items()):
            years = results['years']
            scenarios = results['scenarios']
            
            # Extract data for plotting
            scenario_names = list(scenarios.keys())
            roi_values = [scenarios[name]['ROI'] * 100 for name in scenario_names]
            market_values = [scenarios[name]['Market Value'] for name in scenario_names]
            
            # Create bar plot
            x_pos = np.arange(len(scenario_names))
            bars = axes[i].bar(x_pos, roi_values, color=self.colors[:len(scenario_names)])
            
            # Add value labels on bars
            for j, (bar, value) in enumerate(zip(bars, market_values)):
                height = bar.get_height()
                axes[i].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'€{value:,.0f}', ha='center', va='bottom', fontsize=8)
            
            axes[i].set_title(f'Scenario Analysis\n{years:.0f} Years')
            axes[i].set_xlabel('Market Scenario')
            axes[i].set_ylabel('ROI (%)')
            axes[i].set_xticks(x_pos)
            axes[i].set_xticklabels([name.split('(')[0].strip() for name in scenario_names], 
                                  rotation=45, ha='right')
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def risk_metrics_analysis(self, all_results: Dict) -> pd.DataFrame:
        """
        Calculate comprehensive risk metrics.
        
        Args:
            all_results: Results from run_multiple_periods
            
        Returns:
            pd.DataFrame: Risk metrics for each period
        """
        risk_metrics = []
        
        for months, results in all_results.items():
            years = months / 12
            df = results['results_df']
            
            # Calculate risk metrics
            market_roi = df['roi']
            tavex_roi = df['tavex_roi']
            
            # Value at Risk (VaR) - 5th percentile
            market_var_5 = market_roi.quantile(0.05)
            tavex_var_5 = tavex_roi.quantile(0.05)
            
            # Conditional Value at Risk (CVaR) - Expected shortfall
            market_cvar_5 = market_roi[market_roi <= market_var_5].mean()
            tavex_cvar_5 = tavex_roi[tavex_roi <= tavex_var_5].mean()
            
            # Maximum Drawdown (simplified - using min ROI as proxy)
            market_max_drawdown = market_roi.min()
            tavex_max_drawdown = tavex_roi.min()
            
            # Sharpe Ratio (simplified - using mean/std)
            market_sharpe = market_roi.mean() / market_roi.std() if market_roi.std() > 0 else 0
            tavex_sharpe = tavex_roi.mean() / tavex_roi.std() if tavex_roi.std() > 0 else 0
            
            # Downside Deviation (volatility of negative returns)
            market_downside = market_roi[market_roi < 0].std() if (market_roi < 0).any() else 0
            tavex_downside = tavex_roi[tavex_roi < 0].std() if (tavex_roi < 0).any() else 0
            
            # Probability of Loss
            market_prob_loss = (market_roi < 0).mean()
            tavex_prob_loss = (tavex_roi < 0).mean()
            
            risk_metrics.append({
                'Period (Years)': f"{years:.0f}",
                'Period (Months)': months,
                'Market VaR (5%)': f"{market_var_5*100:.2f}%",
                'Tavex VaR (5%)': f"{tavex_var_5*100:.2f}%",
                'Market CVaR (5%)': f"{market_cvar_5*100:.2f}%",
                'Tavex CVaR (5%)': f"{tavex_cvar_5*100:.2f}%",
                'Market Max Drawdown': f"{market_max_drawdown*100:.2f}%",
                'Tavex Max Drawdown': f"{tavex_max_drawdown*100:.2f}%",
                'Market Sharpe Ratio': f"{market_sharpe:.3f}",
                'Tavex Sharpe Ratio': f"{tavex_sharpe:.3f}",
                'Market Downside Dev': f"{market_downside*100:.2f}%",
                'Tavex Downside Dev': f"{tavex_downside*100:.2f}%",
                'Market Prob of Loss': f"{market_prob_loss*100:.1f}%",
                'Tavex Prob of Loss': f"{tavex_prob_loss*100:.1f}%"
            })
        
        return pd.DataFrame(risk_metrics)
    
    def plot_risk_heatmap(self, risk_metrics_df: pd.DataFrame, save_path: str = None):
        """
        Create a heatmap of risk metrics.
        
        Args:
            risk_metrics_df: DataFrame from risk_metrics_analysis
            save_path: Optional path to save the plot
        """
        # Select numeric columns for heatmap
        numeric_cols = ['Market VaR (5%)', 'Tavex VaR (5%)', 'Market CVaR (5%)', 'Tavex CVaR (5%)',
                       'Market Max Drawdown', 'Tavex Max Drawdown', 'Market Sharpe Ratio', 'Tavex Sharpe Ratio',
                       'Market Downside Dev', 'Tavex Downside Dev', 'Market Prob of Loss', 'Tavex Prob of Loss']
        
        # Convert percentage strings to numeric values
        heatmap_data = risk_metrics_df[numeric_cols].copy()
        for col in heatmap_data.columns:
            if '%' in col:
                heatmap_data[col] = heatmap_data[col].str.rstrip('%').astype(float)
            else:
                heatmap_data[col] = heatmap_data[col].astype(float)
        
        # Create heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data.T, 
                   annot=True, 
                   fmt='.2f', 
                   cmap='RdYlBu_r',
                   cbar_kws={'label': 'Risk Metric Value'})
        
        plt.title('Risk Metrics Heatmap by Investment Period')
        plt.xlabel('Investment Period (Years)')
        plt.ylabel('Risk Metrics')
        plt.xticks(ticks=range(len(risk_metrics_df)), 
                  labels=risk_metrics_df['Period (Years)'])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def sensitivity_analysis(self, base_results: Dict, 
                           price_scenarios: List[float] = [0.8, 0.9, 1.0, 1.1, 1.2],
                           save_path: str = None) -> Dict:
        """
        Perform sensitivity analysis on gold price scenarios.
        
        Args:
            base_results: Base simulation results
            price_scenarios: List of price multipliers (e.g., 0.8 = 20% lower prices)
            save_path: Optional path to save the plot
            
        Returns:
            dict: Sensitivity analysis results
        """
        sensitivity_results = {}
        
        for months, results in base_results.items():
            years = months / 12
            df = results['results_df'].copy()
            
            scenario_data = []
            for multiplier in price_scenarios:
                # Adjust final gold price
                adjusted_price = df['final_gold_price'] * multiplier
                
                # Recalculate values
                adjusted_market_value = df['total_grams'] * adjusted_price
                adjusted_tavex_value = df['total_grams'] * 111.97  # Tavex sell price unchanged
                
                # Recalculate ROI
                adjusted_roi = (adjusted_market_value - df['total_invested']) / df['total_invested']
                adjusted_tavex_roi = (adjusted_tavex_value - df['total_invested']) / df['total_invested']
                
                scenario_data.append({
                    'Price Multiplier': multiplier,
                    'Price Change (%)': (multiplier - 1) * 100,
                    'Median Market ROI (%)': adjusted_roi.median() * 100,
                    'Median Tavex ROI (%)': adjusted_tavex_roi.median() * 100,
                    'Median Market Value': adjusted_market_value.median(),
                    'Median Tavex Value': adjusted_tavex_value.median()
                })
            
            sensitivity_results[months] = {
                'years': years,
                'scenarios': pd.DataFrame(scenario_data)
            }
        
        # Plot sensitivity analysis
        if save_path:
            self.plot_sensitivity_analysis(sensitivity_results, save_path)
        
        return sensitivity_results
    
    def plot_sensitivity_analysis(self, sensitivity_results: Dict, save_path: str = None):
        """
        Plot sensitivity analysis results.
        
        Args:
            sensitivity_results: Results from sensitivity_analysis
            save_path: Optional path to save the plot
        """
        periods = list(sensitivity_results.keys())
        n_periods = len(periods)
        
        fig, axes = plt.subplots(1, n_periods, figsize=(6*n_periods, 6))
        if n_periods == 1:
            axes = [axes]
        
        for i, (months, results) in enumerate(sensitivity_results.items()):
            years = results['years']
            scenarios = results['scenarios']
            
            # Plot ROI vs price change
            axes[i].plot(scenarios['Price Change (%)'], scenarios['Median Market ROI (%)'], 
                        marker='o', linewidth=2, label='Market Value ROI', color=self.colors[0])
            axes[i].plot(scenarios['Price Change (%)'], scenarios['Median Tavex ROI (%)'], 
                        marker='s', linewidth=2, label='Tavex Sell ROI', color=self.colors[1])
            
            axes[i].set_title(f'Price Sensitivity Analysis\n{years:.0f} Years')
            axes[i].set_xlabel('Gold Price Change (%)')
            axes[i].set_ylabel('Median ROI (%)')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
            axes[i].axhline(y=0, color='red', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()

if __name__ == "__main__":
    # Example usage
    analysis = AdvancedTavexAnalysis()
    print("Advanced analysis module loaded successfully!")
