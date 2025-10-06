#!/bin/bash

# Tavex Gold Simulation Environment Setup Script
# This script sets up a virtual environment and installs all dependencies

echo "Setting up Tavex Gold Simulation Environment..."
echo "=============================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Verify installation
echo "Verifying installation..."
python -c "import pandas, numpy, matplotlib, scipy, yfinance, seaborn; print('All dependencies installed successfully!')"

echo ""
echo "Environment setup complete!"
echo "To activate the environment, run: source venv/bin/activate"
echo "To run the simulation, run: python main.py"
echo "To run the demo, run: python main.py demo"
