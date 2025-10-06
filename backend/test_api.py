#!/usr/bin/env python3

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing API endpoints...")
    
    # Test health
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test historical data
    try:
        response = requests.get(f"{base_url}/gold/historical")
        print(f"Historical data: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Data points: {len(data.get('prices', []))}")
            print(f"Statistics: {data.get('statistics', {})}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Historical data failed: {e}")
    
    # Test simulation
    try:
        response = requests.post(f"{base_url}/simulate", json={
            "num_simulations": 100,
            "periods": [36]
        })
        print(f"Simulation: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Results keys: {list(data.get('results', {}).keys())}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Simulation failed: {e}")

if __name__ == "__main__":
    test_api()
