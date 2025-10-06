"""
Data acquisition module for historical gold prices in EUR.
Uses yfinance to fetch historical gold price data and convert to EUR.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class GoldDataAcquisition:
    def __init__(self):
        self.gold_ticker = "GC=F"  # Gold futures
        self.eur_usd_ticker = "EURUSD=X"  # EUR/USD exchange rate
        
    def fetch_historical_data(self, start_date="2000-01-01", end_date=None):
        """
        Fetch historical gold prices and convert to EUR.
        
        Args:
            start_date (str): Start date for data (YYYY-MM-DD)
            end_date (str): End date for data (YYYY-MM-DD), defaults to today
            
        Returns:
            pd.DataFrame: Historical gold prices in EUR per gram
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        print(f"Fetching gold data from {start_date} to {end_date}...")
        
        # Fetch gold prices in USD
        gold_data = yf.download(self.gold_ticker, start=start_date, end=end_date, progress=False)
        
        # Fetch EUR/USD exchange rates
        eur_usd_data = yf.download(self.eur_usd_ticker, start=start_date, end=end_date, progress=False)
        
        if gold_data.empty or eur_usd_data.empty:
            raise ValueError("Failed to fetch historical data")
            
        # Convert gold prices from USD per troy ounce to EUR per gram
        # 1 troy ounce = 31.1034768 grams
        troy_ounce_to_grams = 31.1034768
        
        # Align the data by date
        aligned_data = pd.DataFrame(index=gold_data.index)
        aligned_data['gold_usd_per_oz'] = gold_data['Close']
        aligned_data['eur_usd_rate'] = eur_usd_data['Close']
        
        # Convert to EUR per gram
        aligned_data['gold_eur_per_gram'] = (
            aligned_data['gold_usd_per_oz'] / 
            aligned_data['eur_usd_rate'] / 
            troy_ounce_to_grams
        )
        
        # Calculate monthly returns
        aligned_data['monthly_return'] = aligned_data['gold_eur_per_gram'].pct_change()
        
        # Remove NaN values
        aligned_data = aligned_data.dropna()
        
        print(f"Successfully fetched {len(aligned_data)} data points")
        print(f"Date range: {aligned_data.index[0].strftime('%Y-%m-%d')} to {aligned_data.index[-1].strftime('%Y-%m-%d')}")
        
        return aligned_data[['gold_eur_per_gram', 'monthly_return']]
    
    def get_return_statistics(self, data):
        """
        Calculate return statistics for Monte Carlo simulation.
        
        Args:
            data (pd.DataFrame): Historical data with monthly_return column
            
        Returns:
            dict: Statistics including mean, std, and other metrics
        """
        returns = data['monthly_return'].dropna()
        
        stats = {
            'mean_monthly_return': returns.mean(),
            'std_monthly_return': returns.std(),
            'min_monthly_return': returns.min(),
            'max_monthly_return': returns.max(),
            'skewness': returns.skew(),
            'kurtosis': returns.kurtosis(),
            'total_observations': len(returns)
        }
        
        return stats
    
    def save_data(self, data, filename="gold_historical_data.csv"):
        """Save historical data to CSV file."""
        data.to_csv(filename)
        print(f"Data saved to {filename}")
    
    def load_data(self, filename="gold_historical_data.csv"):
        """Load historical data from CSV file."""
        data = pd.read_csv(filename, index_col=0, parse_dates=True)
        print(f"Data loaded from {filename}")
        return data

if __name__ == "__main__":
    # Example usage
    acquisition = GoldDataAcquisition()
    
    # Fetch data
    data = acquisition.fetch_historical_data()
    
    # Get statistics
    stats = acquisition.get_return_statistics(data)
    print("\nReturn Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value:.6f}")
    
    # Save data
    acquisition.save_data(data)
