#!/usr/bin/env python3

import asyncio
import json

async def generate_realistic_historical_data():
    """Generate realistic historical data based on gold market research"""
    import numpy as np
    from datetime import datetime, timedelta
    
    months = 300  # 25 years of data
    start_price = 10.5  # EUR per gram (circa 2000)
    prices = [start_price]
    dates = []
    returns = []

    # Real gold statistics from literature
    annual_drift = 0.075
    annual_vol = 0.16
    monthly_drift = annual_drift / 12
    monthly_vol = annual_vol / np.sqrt(12)
    mean_reversion_speed = 0.02
    long_term_mean = np.log(70)  # Long-term mean around 70 EUR/g

    start_date = datetime(2000, 1, 1)

    for i in range(months):
        date = start_date + timedelta(days=30 * i)
        dates.append(date.strftime("%Y-%m"))

        if i > 0:
            prev_price = prices[i - 1]
            log_price = np.log(prev_price)

            # Add mean reversion
            reversion = mean_reversion_speed * (long_term_mean - log_price)

            # Generate random return
            random_return = np.random.normal(0, 1)
            
            # Add occasional fat tail events
            fat_tail_event = np.random.choice([-0.15, 0, 0.15], p=[0.01, 0.98, 0.01])

            monthly_return = monthly_drift + reversion + monthly_vol * random_return + fat_tail_event
            new_price = prev_price * np.exp(monthly_return)
            
            # Ensure reasonable bounds
            new_price = max(20, min(500, new_price))
            prices.append(new_price)
            returns.append(monthly_return)

    # Calculate statistics
    returns_array = np.array(returns)
    mean_return = float(np.mean(returns_array))
    std_return = float(np.std(returns_array))
    skewness = float(np.mean(((returns_array - mean_return) / std_return) ** 3))
    kurtosis = float(np.mean(((returns_array - mean_return) / std_return) ** 4))

    return {
        "prices": prices,
        "dates": dates,
        "returns": returns,
        "statistics": {
            "mean_monthly_return": mean_return,
            "std_monthly_return": std_return,
            "annualized_return": (np.exp(mean_return * 12) - 1) * 100,
            "annualized_volatility": std_return * np.sqrt(12) * 100,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "current_price": prices[-1],
            "data_points": len(prices)
        }
    }

async def main():
    try:
        data = await generate_realistic_historical_data()
        print("Success!")
        print(f"Data points: {len(data['prices'])}")
        print(f"Statistics: {data['statistics']}")
        
        # Try to serialize to JSON
        json_str = json.dumps(data)
        print("JSON serialization successful!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
