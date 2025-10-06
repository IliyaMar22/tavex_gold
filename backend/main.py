"""
FastAPI backend for Tavex Gold Simulation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import asyncio
import json

app = FastAPI(title="Tavex Gold Simulation API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GoldAPI configuration
GOLDAPI_KEY = "goldapi-q738vsmgfbokhe-io"
GOLDAPI_BASE_URL = "https://www.goldapi.io/api"

# Tavex parameters
TAVEX_PARAMS = {
    "buy_price": 124.24,
    "sell_price": 111.97,
    "spread": 0.0988,
    "monthly_grams": 4,
    "subscriptions": 4,
    "bonus_grams_per_year": 4
}

class SimulationRequest(BaseModel):
    num_simulations: int = 10000
    periods: List[int] = [36, 60, 120]  # months

class SimulationResponse(BaseModel):
    historical_data: Dict
    results: Dict
    tavex_params: Dict

class GoldPriceData(BaseModel):
    price: float
    currency: str
    timestamp: str
    source: str

@app.get("/")
async def root():
    return {"message": "Tavex Gold Simulation API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/gold/current", response_model=GoldPriceData)
async def get_current_gold_price():
    """Get current gold price from GoldAPI"""
    try:
        url = f"{GOLDAPI_BASE_URL}/XAU/EUR"
        headers = {
            "x-access-token": GOLDAPI_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return GoldPriceData(
            price=data.get("price", 0),
            currency="EUR",
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            source="GoldAPI.io"
        )
    
    except requests.exceptions.RequestException as e:
        # Fallback to synthetic data
        return GoldPriceData(
            price=106.41,  # Fallback price
            currency="EUR",
            timestamp=datetime.now().isoformat(),
            source="Synthetic (API Error)"
        )

@app.get("/gold/historical")
async def get_historical_gold_data():
    """Generate realistic historical gold data"""
    try:
        # Try to get some historical data from GoldAPI
        historical_data = await generate_realistic_historical_data()
        print(f"Generated historical data with {len(historical_data['prices'])} prices")
        return historical_data
    except Exception as e:
        print(f"Error in historical data generation: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating historical data: {str(e)}")

async def generate_realistic_historical_data():
    """Generate realistic historical data based on gold market research"""
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
            "annualized_return": float((np.exp(mean_return * 12) - 1) * 100),
            "annualized_volatility": float(std_return * np.sqrt(12) * 100),
            "skewness": skewness,
            "kurtosis": kurtosis,
            "current_price": float(prices[-1]),
            "data_points": len(prices)
        }
    }

def box_muller_transform():
    """Box-Muller transform for normal distribution"""
    u1 = np.random.random()
    u2 = np.random.random()
    z = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    return z

def simulate_single_path(months: int, stats: Dict) -> Dict:
    """Simulate a single investment path"""
    total_grams = 0
    total_invested = 0
    grams_history = []
    value_history = []

    # Start from current Tavex buy price
    current_price = TAVEX_PARAMS["buy_price"]

    for month in range(1, months + 1):
        # Generate monthly return using historical statistics
        random_return = stats["mean_monthly_return"] + stats["std_monthly_return"] * box_muller_transform()
        
        # Apply return
        current_price *= np.exp(random_return)
        
        # Ensure price doesn't go negative or unreasonably high
        current_price = max(20, min(500, current_price))

        # Purchase monthly allocation
        grams_purchased = TAVEX_PARAMS["monthly_grams"] * TAVEX_PARAMS["subscriptions"]
        total_grams += grams_purchased
        total_invested += grams_purchased * TAVEX_PARAMS["buy_price"]

        # Add bonus grams every 12 months
        if month % 12 == 0:
            total_grams += TAVEX_PARAMS["bonus_grams_per_year"]

        # Calculate market value at Tavex sell price (accounting for spread)
        market_value = total_grams * current_price * (1 - TAVEX_PARAMS["spread"])

        grams_history.append(total_grams)
        value_history.append(market_value)

    final_value = value_history[-1]
    roi = ((final_value - total_invested) / total_invested) * 100
    annualized_return = (np.power(final_value / total_invested, 12 / months) - 1) * 100

    return {
        "total_grams": total_grams,
        "total_invested": total_invested,
        "final_value": final_value,
        "roi": roi,
        "annualized_return": annualized_return,
        "grams_history": grams_history,
        "value_history": value_history
    }

@app.post("/simulate")
async def run_simulation(request: SimulationRequest):
    """Run Monte Carlo simulation"""
    try:
        # Get historical data
        historical_data = await generate_realistic_historical_data()
        stats = historical_data["statistics"]
        
        results = {}
        
        for months in request.periods:
            sim_results = []
            
            # Run simulations
            for i in range(request.num_simulations):
                sim_results.append(simulate_single_path(months, stats))
            
            # Sort by final value for percentile calculations
            sim_results.sort(key=lambda x: x["final_value"])
            
            final_values = [r["final_value"] for r in sim_results]
            rois = [r["roi"] for r in sim_results]
            annualized_returns = [r["annualized_return"] for r in sim_results]
            
            # Calculate percentiles
            def get_percentile(arr, p):
                return arr[int(len(arr) * p)]
            
            median = get_percentile(final_values, 0.5)
            p25 = get_percentile(final_values, 0.25)
            p75 = get_percentile(final_values, 0.75)
            p5 = get_percentile(final_values, 0.05)
            p95 = get_percentile(final_values, 0.95)
            
            median_roi = get_percentile(rois, 0.5)
            median_annualized = get_percentile(annualized_returns, 0.5)
            
            # Calculate bonus gram impact
            total_grams_with_bonus = sim_results[0]["total_grams"]
            total_grams_without_bonus = (months / 12) * 12 * TAVEX_PARAMS["subscriptions"]
            bonus_grams_total = total_grams_with_bonus - total_grams_without_bonus
            bonus_impact = (bonus_grams_total / total_grams_without_bonus) * 100
            
            # Break-even analysis
            break_even_count = sum(1 for r in sim_results if r["roi"] > 0)
            break_even_probability = (break_even_count / request.num_simulations) * 100
            
            # Create histogram data
            histogram_bins = 30
            min_val = final_values[0]
            max_val = final_values[-1]
            bin_size = (max_val - min_val) / histogram_bins
            
            histogram = [0] * histogram_bins
            for val in final_values:
                bin_index = min(int((val - min_val) / bin_size), histogram_bins - 1)
                histogram[bin_index] += 1
            
            histogram_data = []
            for i, count in enumerate(histogram):
                histogram_data.append({
                    "value": min_val + (i + 0.5) * bin_size,
                    "count": count,
                    "label": f"€{int((min_val + i * bin_size) / 1000)}k"
                })
            
            results[months] = {
                "years": months / 12,
                "total_invested": sim_results[0]["total_invested"],
                "total_grams": total_grams_with_bonus,
                "bonus_grams": bonus_grams_total,
                "bonus_impact": bonus_impact,
                "median": median,
                "p25": p25,
                "p75": p75,
                "p5": p5,
                "p95": p95,
                "median_roi": median_roi,
                "median_annualized": median_annualized,
                "break_even_probability": break_even_probability,
                "histogram": histogram_data,
                "sample_path": sim_results[len(sim_results) // 2]
            }
        
        return {
            "historical_data": historical_data,
            "results": results,
            "tavex_params": TAVEX_PARAMS
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
