import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# MAIN Structure
class algorithm:
  
  # Initialize portfolio and cash
  portfolio = 0
  cash = 1000000
  
  # Set time period and ticker symbol
  start_date = "2021-12-13"
  end_date = datetime.today().strftime('%Y-%m-%d')
  SPY = "SPY"
  
  # Download market data for SPY
  market_ticker = yf.download(SPY, start_date, end_date, progress=False)
  
  # Initialize lists for technical indicators and trade history
  fourteen_day_ma = []  # Moving Average over 14 days
  trades = []           # List of executed trades
  RSI_vals = []         # RSI values
  return_vals = []      # Daily return values
  portfolio_vals = []   # Portfolio values
  
  # Counters and initial values
  RSI_day_count = 1
  prev_price = 0
  today_return = 0

  def __init__(self, tick):
    # Download data for the provided ticker symbol
    self.ticker_symbols = tick
    self.ticker = yf.download(self.ticker_symbols, self.start_date, self.end_date, progress=False)
    return # Base initialization

  # Function to execute a buy trade
  def buy(self, tick, day):
    price_on_day = self.ticker.loc[day]['Close']
    
    # Calculate amount of shares to buy with available cash
    buy_amt = self.cash / price_on_day
    self.portfolio += buy_amt
    self.cash -= (buy_amt * price_on_day)
    
    # Record trade data
    data = {"AAPL", buy_amt, day}
    self.trades.append(data)
  
  # Function to execute a sell trade
  def sell(self, tick, day):
    price_on_day = self.ticker.loc[day]['Close']
    
    # Sell entire portfolio holdings
    sell_amt = self.portfolio
    self.portfolio -= sell_amt
    self.cash += (sell_amt * price_on_day)
    
    # Record trade data
    data = {"AAPL", sell_amt, day}
    self.trades.append(data)
  
  # Calculate average gains from the 14-day moving average
  def calcualte_gain(self):
    total_gain = 0
    for i in self.fourteen_day_ma:
      if i > 0:
        total_gain += i  # sum gain magnitudes (was += 1, which counted up-days)
    
    if self.RSI_day_count > 14:
      self.RSI_day_count = 14  # Keep the day count at 14

    # Return average gain
    return (total_gain / self.RSI_day_count)

  # Calculate average losses from the 14-day moving average
  def calcualte_loss(self):
    total_loss = 0
    for i in self.fourteen_day_ma:
      if i < 0:
        total_loss += i
    
    if self.RSI_day_count > 14:
      self.RSI_day_count = 14  # Keep the day count at 14
    
    # Return average loss (absolute value)
    return -(total_loss / self.RSI_day_count)
  
  # Calculate the RSI value for the given day
  def RSI_val(self, day):
    # Append the daily return to the 14-day moving average list
    self.fourteen_day_ma.append(self.today_return - 1)

    # Maintain only 14 days of MA data
    if self.RSI_day_count >= 14:
        self.fourteen_day_ma.pop(0)
    
    # Average gain and average loss
    avg_gain = self.calcualte_gain()
    avg_loss = self.calcualte_loss()

    if avg_loss == 0:
        return 100  # RSI is 100 if there were no losses

    if avg_gain == 0:
        return 0  # RSI is 0 if there were no gains

    # Calculate RSI using average gain and loss
    return (100 - (100 / (1 + avg_gain / avg_loss)))
  
  # Get the current portfolio value for the given day
  def getCurrVal(self, day):
    price_on_day = self.ticker.loc[day]['Close']
    
    # Calculate total portfolio value (stocks + cash)
    portfolio_val = price_on_day * self.portfolio + self.cash
    return portfolio_val

  # Decide whether to buy, sell, or hold based on RSI
  def decide(self, tick, day):
    if self.RSI_day_count == 1:
      # Initialize on the first day, set previous price
      self.RSI_day_count += 1
      self.prev_price = self.ticker.loc[day]['Close']
      return

    # Calculate today's return based on price change
    self.today_return = self.ticker.loc[day]['Close'] / self.prev_price
    self.return_vals.append(self.today_return)
    
    self.ticker_symbols = tick
    RSI = self.RSI_val(day)  # Calculate RSI for the day
    self.RSI_vals.append(RSI)

    # Buy if RSI <= 30, Sell if RSI >= 70
    if RSI >= 70:
      self.sell("AAPL", day)
    elif RSI <= 30:
      self.buy("AAPL", day)
    
    # Update previous price for the next day
    self.prev_price = self.ticker.loc[day]['Close']
    self.RSI_day_count += 1

    # Update portfolio value for the day
    self.portfolio_vals.append(self.getCurrVal(day))
