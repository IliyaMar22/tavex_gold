"""
Simple test script to verify the Monte Carlo simulation logic without external dependencies.
"""

import random
import math

def simple_monte_carlo_test():
    """
    Simple test of the Monte Carlo simulation logic.
    """
    print("="*50)
    print("SIMPLE MONTE CARLO TEST")
    print("="*50)
    
    # Configuration
    buy_price = 124.24
    sell_price = 111.97
    monthly_grams = 4.0
    bonus_grams_per_year = 4.0
    months = 36  # 3 years
    num_simulations = 1000
    
    # Simulation parameters
    initial_gold_price = 50.0
    monthly_return_mean = 0.005  # 0.5% monthly
    monthly_return_std = 0.05    # 5% monthly volatility
    
    print(f"Configuration:")
    print(f"- Buy Price: €{buy_price:.2f}/gram")
    print(f"- Sell Price: €{sell_price:.2f}/gram")
    print(f"- Monthly Purchase: {monthly_grams} grams")
    print(f"- Bonus Gold: {bonus_grams_per_year} grams/year")
    print(f"- Simulation Period: {months} months ({months/12:.0f} years)")
    print(f"- Number of Simulations: {num_simulations:,}")
    print()
    
    # Run simulations
    results = []
    
    for sim in range(num_simulations):
        if (sim + 1) % 200 == 0:
            print(f"Completed {sim + 1:,} simulations...")
        
        # Initialize simulation
        current_gold_price = initial_gold_price
        total_grams = 0.0
        total_invested = 0.0
        
        # Simulate each month
        for month in range(months):
            # Buy gold
            monthly_investment = monthly_grams * buy_price
            total_invested += monthly_investment
            total_grams += monthly_grams
            
            # Add bonus grams at end of year
            if (month + 1) % 12 == 0:
                total_grams += bonus_grams_per_year
            
            # Simulate gold price movement (except for last month)
            if month < months - 1:
                # Generate random return
                random_return = random.gauss(monthly_return_mean, monthly_return_std)
                current_gold_price *= (1 + random_return)
        
        # Calculate final values
        market_value = total_grams * current_gold_price
        tavex_sell_value = total_grams * sell_price
        roi = (market_value - total_invested) / total_invested
        tavex_roi = (tavex_sell_value - total_invested) / total_invested
        
        results.append({
            'total_grams': total_grams,
            'total_invested': total_invested,
            'market_value': market_value,
            'tavex_sell_value': tavex_sell_value,
            'roi': roi,
            'tavex_roi': tavex_roi
        })
    
    # Calculate statistics
    market_values = [r['market_value'] for r in results]
    rois = [r['roi'] for r in results]
    tavex_rois = [r['tavex_roi'] for r in results]
    total_grams_list = [r['total_grams'] for r in results]
    
    # Sort for percentiles
    market_values.sort()
    rois.sort()
    tavex_rois.sort()
    
    print("\nSimulation Results:")
    print("="*30)
    
    # Market value statistics
    print(f"Market Value (EUR):")
    print(f"  Mean: €{sum(market_values)/len(market_values):,.0f}")
    print(f"  Median: €{market_values[len(market_values)//2]:,.0f}")
    print(f"  5th percentile: €{market_values[int(len(market_values)*0.05)]:,.0f}")
    print(f"  95th percentile: €{market_values[int(len(market_values)*0.95)]:,.0f}")
    
    # ROI statistics
    print(f"\nMarket ROI (%):")
    print(f"  Mean: {sum(rois)/len(rois)*100:.1f}%")
    print(f"  Median: {rois[len(rois)//2]*100:.1f}%")
    print(f"  5th percentile: {rois[int(len(rois)*0.05)]*100:.1f}%")
    print(f"  95th percentile: {rois[int(len(rois)*0.95)]*100:.1f}%")
    
    # Tavex ROI statistics
    print(f"\nTavex Sell ROI (%):")
    print(f"  Mean: {sum(tavex_rois)/len(tavex_rois)*100:.1f}%")
    print(f"  Median: {tavex_rois[len(tavex_rois)//2]*100:.1f}%")
    print(f"  5th percentile: {tavex_rois[int(len(tavex_rois)*0.05)]*100:.1f}%")
    print(f"  95th percentile: {tavex_rois[int(len(tavex_rois)*0.95)]*100:.1f}%")
    
    # Break-even analysis
    break_even_market = sum(1 for roi in rois if roi >= 0) / len(rois) * 100
    break_even_tavex = sum(1 for roi in tavex_rois if roi >= 0) / len(tavex_rois) * 100
    
    print(f"\nBreak-even Analysis:")
    print(f"  Market Value: {break_even_market:.1f}% of simulations profitable")
    print(f"  Tavex Sell: {break_even_tavex:.1f}% of simulations profitable")
    
    # Bonus gold analysis
    expected_grams = months * monthly_grams + (months // 12) * bonus_grams_per_year
    actual_grams = sum(total_grams_list) / len(total_grams_list)
    
    print(f"\nGold Accumulation:")
    print(f"  Expected total grams: {expected_grams:.1f}")
    print(f"  Average actual grams: {actual_grams:.1f}")
    print(f"  Bonus grams received: {(months // 12) * bonus_grams_per_year:.1f}")
    
    # Spread impact
    spread_impact = (sum(tavex_rois)/len(tavex_rois) - sum(rois)/len(rois)) * 100
    print(f"\nSpread Impact:")
    print(f"  Average ROI difference (Market vs Tavex): {spread_impact:.1f} percentage points")
    
    return results

def test_bonus_gold_impact():
    """
    Test the impact of bonus gold on returns.
    """
    print("\n" + "="*50)
    print("BONUS GOLD IMPACT TEST")
    print("="*50)
    
    # Run simulation with and without bonus
    configs = [
        ("With Bonus", 4.0),  # 4 bonus grams per year
        ("Without Bonus", 0.0)  # No bonus
    ]
    
    for name, bonus_grams in configs:
        print(f"\n{name} Configuration:")
        
        # Simple simulation
        buy_price = 124.24
        monthly_grams = 4.0
        months = 36
        initial_price = 50.0
        
        # Run 1000 simulations
        rois = []
        for _ in range(1000):
            current_price = initial_price
            total_grams = 0.0
            total_invested = 0.0
            
            for month in range(months):
                # Buy gold
                total_invested += monthly_grams * buy_price
                total_grams += monthly_grams
                
                # Add bonus at end of year
                if (month + 1) % 12 == 0:
                    total_grams += bonus_grams
                
                # Simulate price movement
                if month < months - 1:
                    random_return = random.gauss(0.005, 0.05)
                    current_price *= (1 + random_return)
            
            # Calculate ROI
            final_value = total_grams * current_price
            roi = (final_value - total_invested) / total_invested
            rois.append(roi)
        
        avg_roi = sum(rois) / len(rois) * 100
        median_roi = sorted(rois)[len(rois)//2] * 100
        
        print(f"  Average ROI: {avg_roi:.1f}%")
        print(f"  Median ROI: {median_roi:.1f}%")
        print(f"  Total grams: {months * monthly_grams + (months // 12) * bonus_grams:.1f}")

if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    
    # Run tests
    results = simple_monte_carlo_test()
    test_bonus_gold_impact()
    
    print("\n" + "="*50)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*50)
