"""
Configuration file for Tavex Gold Subscription Monte Carlo Simulation.
Modify these parameters to customize the simulation behavior.
"""

# Tavex Pricing Configuration
TAVEX_CONFIG = {
    'buy_price_eur_per_gram': 124.24,      # Current Tavex buy price
    'sell_price_eur_per_gram': 111.97,     # Current Tavex sell price
    'monthly_grams': 4.0,                  # Grams purchased per month
    'bonus_grams_per_year': 4.0,           # Bonus grams received annually
}

# Simulation Configuration
SIMULATION_CONFIG = {
    'simulation_periods': [36, 60, 120],   # Months: 3, 5, 10 years
    'num_simulations': 10000,              # Number of Monte Carlo runs
    'random_seed': None,                   # Random seed for reproducibility (None for random)
}

# Data Configuration
DATA_CONFIG = {
    'start_date': '2000-01-01',            # Start date for historical data
    'end_date': None,                      # End date (None for today)
    'data_file': 'gold_historical_data.csv',  # File to save/load historical data
    'use_cached_data': True,               # Use cached data if available
}

# Analysis Configuration
ANALYSIS_CONFIG = {
    'inflation_rate': 0.02,                # Annual inflation rate for real returns
    'confidence_levels': [0.05, 0.25, 0.50, 0.75, 0.95],  # Percentiles to calculate
    'scenario_multipliers': [0.8, 0.9, 1.0, 1.1, 1.2],   # Price sensitivity analysis
}

# Output Configuration
OUTPUT_CONFIG = {
    'output_directory': 'simulation_results',
    'save_plots': True,                    # Save generated plots
    'plot_format': 'png',                  # Plot file format
    'plot_dpi': 300,                       # Plot resolution
    'save_detailed_results': True,         # Save detailed simulation results
}

# Risk Analysis Configuration
RISK_CONFIG = {
    'var_confidence': 0.05,                # Value at Risk confidence level
    'cvar_confidence': 0.05,               # Conditional VaR confidence level
    'max_drawdown_method': 'min_roi',      # Method for max drawdown calculation
}

# Visualization Configuration
VISUALIZATION_CONFIG = {
    'figure_size': (12, 8),                # Default figure size
    'color_palette': 'husl',               # Color palette for plots
    'style': 'seaborn-v0_8',              # Matplotlib style
    'font_size': 10,                       # Default font size
    'line_width': 2,                       # Default line width
    'alpha': 0.7,                          # Default transparency
}

# Advanced Features Configuration
ADVANCED_CONFIG = {
    'enable_inflation_analysis': True,     # Enable inflation-adjusted analysis
    'enable_scenario_analysis': True,      # Enable scenario analysis
    'enable_risk_metrics': True,          # Enable risk metrics calculation
    'enable_sensitivity_analysis': True,   # Enable sensitivity analysis
    'enable_bonus_impact_analysis': True,  # Enable bonus gold impact analysis
    'enable_break_even_analysis': True,    # Enable break-even analysis
}

# Validation Configuration
VALIDATION_CONFIG = {
    'min_simulations': 1000,               # Minimum number of simulations
    'max_simulations': 100000,             # Maximum number of simulations
    'min_period_months': 12,               # Minimum simulation period
    'max_period_months': 600,              # Maximum simulation period
    'validate_inputs': True,               # Validate input parameters
}

def validate_config():
    """
    Validate configuration parameters.
    
    Returns:
        bool: True if configuration is valid
    """
    errors = []
    
    # Validate Tavex configuration
    if TAVEX_CONFIG['buy_price_eur_per_gram'] <= 0:
        errors.append("Buy price must be positive")
    
    if TAVEX_CONFIG['sell_price_eur_per_gram'] <= 0:
        errors.append("Sell price must be positive")
    
    if TAVEX_CONFIG['buy_price_eur_per_gram'] <= TAVEX_CONFIG['sell_price_eur_per_gram']:
        errors.append("Buy price must be higher than sell price")
    
    if TAVEX_CONFIG['monthly_grams'] <= 0:
        errors.append("Monthly grams must be positive")
    
    if TAVEX_CONFIG['bonus_grams_per_year'] < 0:
        errors.append("Bonus grams cannot be negative")
    
    # Validate simulation configuration
    if SIMULATION_CONFIG['num_simulations'] < VALIDATION_CONFIG['min_simulations']:
        errors.append(f"Number of simulations must be at least {VALIDATION_CONFIG['min_simulations']}")
    
    if SIMULATION_CONFIG['num_simulations'] > VALIDATION_CONFIG['max_simulations']:
        errors.append(f"Number of simulations must be at most {VALIDATION_CONFIG['max_simulations']}")
    
    for period in SIMULATION_CONFIG['simulation_periods']:
        if period < VALIDATION_CONFIG['min_period_months']:
            errors.append(f"Simulation period {period} months is too short")
        if period > VALIDATION_CONFIG['max_period_months']:
            errors.append(f"Simulation period {period} months is too long")
    
    # Validate analysis configuration
    if not 0 <= ANALYSIS_CONFIG['inflation_rate'] <= 1:
        errors.append("Inflation rate must be between 0 and 1")
    
    for level in ANALYSIS_CONFIG['confidence_levels']:
        if not 0 <= level <= 1:
            errors.append(f"Confidence level {level} must be between 0 and 1")
    
    if errors:
        print("Configuration validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

def get_config_summary():
    """
    Get a summary of the current configuration.
    
    Returns:
        dict: Configuration summary
    """
    return {
        'tavex_pricing': TAVEX_CONFIG,
        'simulation_setup': SIMULATION_CONFIG,
        'data_settings': DATA_CONFIG,
        'analysis_options': ANALYSIS_CONFIG,
        'output_settings': OUTPUT_CONFIG,
        'risk_analysis': RISK_CONFIG,
        'visualization': VISUALIZATION_CONFIG,
        'advanced_features': ADVANCED_CONFIG,
        'validation': VALIDATION_CONFIG
    }

if __name__ == "__main__":
    # Validate configuration when run directly
    if validate_config():
        print("Configuration is valid!")
        
        # Print summary
        summary = get_config_summary()
        print("\nConfiguration Summary:")
        for category, settings in summary.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for key, value in settings.items():
                print(f"  {key}: {value}")
    else:
        print("Configuration validation failed!")
