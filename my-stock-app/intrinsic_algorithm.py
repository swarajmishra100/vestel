import yfinance as yf
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Author: Ken Fukutomi, 2025
class Intrinsic:

    start_date = "2021-12-13"
    end_date = datetime.today().strftime('%Y-%m-%d')
    market_ticker = yf.download("SPY", start_date, end_date, progress=False)

    # Initialize Pandas dataframe
    def __init__(self, tick):
        self.ticker_symbols = tick
        self.ticker = yf.download(self.ticker_symbols, self.start_date, self.end_date, progress=False)

        # Create a DataFrame with Date, High, and Low prices
        self.df = pd.DataFrame({
            "Date": self.ticker.index,
            "High": self.ticker['High'],
            "Low": self.ticker['Low'],
            "Open": self.ticker['Open'],
            "Close": self.ticker['Close'],
            "Volume": self.ticker['Volume'],
            "Adj Close": self.ticker['Adj Close']
        })

    # Return the current dataframe
    def get_data(self):
        return self.df
    
    # Returns the datatype of the dataframe
    def print_dtype(self):
        for columns in self.df.columns:
            print(f'{columns} : {self.df[columns].dtype}')
    
    # Return the specific datatype of column
    def get_dtype(self, param):
        if param not in self.df.columns:
            return "Does not exist."
        else:
            return (self.df[param].dtype)
    
    # Simple Plot, [ALL]
    def simple_plot(self):
      columns_to_plot = [col for col in self.df.columns if col != "Date"]
      num_cols = len(columns_to_plot)

      fig, axes = plt.subplots(nrows=num_cols, ncols=1, figsize=(8,6 * num_cols))
      for i, column in enumerate(columns_to_plot):
        ax = axes[i] if num_cols > 1 else axes
        self.df.plot(x='Date', y=column, ax=ax)
        ax.set_title(f"{column} over Time")
        ax.set_xlabel('Date')
        ax.set_ylabel(column)
      
      plt.tight_layout()
      plt.grid(True)
      plt.show()



# Example usage
if __name__ == "__main__":
    stock = Intrinsic("AAPL")  # You can input the ticker symbol you need
    stock_data = stock.get_data()
    stock.simple_plot()