import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from backend import backend
from algorithm import algorithm

# Initialize the backend instance
tester = backend()

# Prompt user for the stock ticker manually
ticker = input("Please enter a stock ticker (e.g., AAPL, NVDA): ").upper()

# If no ticker is provided, default to AAPL
if not ticker:
    print("No stock ticker given, defaulting to AAPL")
    ticker = "AAPL"

# Initialize the algorithm with the provided or default ticker
algo = algorithm(ticker)

# Run the algorithm
tester.run(algo)

# Create a figure with a title based on the ticker
plt.figure(figsize=(10, 6), num="RSI Algorithm for " + ticker)

# Generate plots for volatility, returns, RSI, and portfolio performance
tester.calculateVol(algo)
tester.graphReturns(algo)
tester.graphRSI(algo)
tester.calculate_total_returns(algo)
tester.calculate_market_return(algo)
tester.risk_metrics(algo)

# Adjust layout and display the plots
plt.tight_layout()
plt.show()