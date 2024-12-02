# Hypothetical "backend"
import yfinance as yf
import pandas as pd
import numpy as np
from algorithm import algorithm
import matplotlib.pyplot as plt

class backend:
  
  data = {"Ticker": [],
          "Amount": [],
          "Date": []}
  portfolio_value = []

  def __init__(self) -> None:
    pass

  def run(self, algo):
    for day in algo.ticker.index:
      algo.decide("AAPL", day)
      self.portfolio_value.append(algo.getCurrVal(day))

  def graphReturns(self, algorithm):
    df = pd.DataFrame(algorithm.portfolio_vals)
    plt.subplot(2,2,1)
    plt.plot(df.index, df[0], label="Close Price", color="blue")
    plt.title('Portflio values ')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
  
  def graphRSI(self, algorithm): 
    df = pd.DataFrame(algorithm.RSI_vals)

    plt.subplot(2,2,2)
    plt.plot(df.index, df[0], label='Close Price', color='blue')
    plt.title('RSI Values')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)     

  def calculateVol(self, algorithm):
    df = pd.DataFrame(algorithm.portfolio_vals)
    returns = df.pct_change()
    vols = (returns.std())

    plt.subplot(2,2,3)
    plt.plot(df.index, returns, label='Close Price', color='blue')
    plt.title('Daily Returns')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)

  def calculate_total_returns(self, algorithm):
    total_returns = []
    total=1

    df = pd.DataFrame(algorithm.portfolio_vals)
    returns = df.pct_change()
    returns = returns.dropna()

    for day_return in returns[0]:
      total = total * (1 + day_return)
      total_returns.append(total)

    df2 = pd.DataFrame(total_returns)

    plt.subplot(2,2,4)
    plt.plot(df2.index, df2[0], label="Close Price", color="blue")
    plt.title('Normalized Returns')
    plt.xlabel('Date')
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
  
  def calculate_market_return(self, algorithm):
    start_val = algorithm.market_ticker.iloc[0]["Close"]
    end_val = algorithm.market_ticker.iloc[-1]["Close"]
    market_return = ((end_val / start_val) - 1)*100
    print(f"Market Return Over Time Period: {np.round(market_return, 2)}%")
    
    start_val = algorithm.portfolio_vals[0]
    end_val = algorithm.portfolio_vals[-1]
    our_return = ((end_val / start_val) - 1)*100
    print(f"Our Return Over Time Period: {np.round(our_return, 2)}%")
    print(f"Performance compared to Market: {np.round(our_return - market_return, 2)}%")