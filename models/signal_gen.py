import pandas as pd
from pathlib import Path
import numpy as np

# Step 1: Load the Excel data
# Define the path to your raw data file
data_file = Path(__file__).resolve().parent.parent / "data" / "raw" 
prices = pd.read_csv(data_file / "Historical_prices.xlsx", index_col=0)

data_file = Path(__file__).resolve().parent.parent / "data" / "signals" 
# Load all the data (assuming you have separate Excel files for each indicator)
macd = pd.read_csv(data_file / 'macd_value.xlsx', index_col=0)
signal = pd.read_csv(data_file /'macd_signal.xlsx', index_col=0)
obv = pd.read_csv(data_file /'OBV_stocks.xlsx', index_col=0)
momentum = pd.read_csv(data_file /'momentum.xlsx', index_col=0)

# Load Moving Averages
ma_short = pd.read_csv(data_file / 'MA_10p.xlsx' , index_col=0)  # Short-term MA
ma_medium = pd.read_csv(data_file / 'MA_20p.xlsx', index_col=0)  # Medium-term MA
ma_long = pd.read_csv(data_file / 'MA_50p.xlsx', index_col=0)  # Long-term MA

# Initialize a DataFrame for trading signals
trading_signals = pd.DataFrame(index=prices.index, columns=prices.columns)

# Define the trading strategy based on the indicators
for ticker in prices.columns:
    # Initialize with no signal
    trading_signals[ticker] = 0
    
    # Buy condition
    buy_condition = (
        (macd[ticker] > signal[ticker]) &               # MACD line above Signal line
        (momentum[ticker] > 0) &                        # Positive momentum
        (obv[ticker].diff() > 0) &                      # OBV is increasing
        (prices[ticker] > ma_short[ticker]) &          # Price above short-term MA
        (prices[ticker] > ma_medium[ticker]) &         # Price above medium-term MA
        (prices[ticker] > ma_long[ticker])             # Price above long-term MA
    )
    
    # Sell condition
    sell_condition = (
        (macd[ticker] < signal[ticker]) &               # MACD line below Signal line
        (momentum[ticker] < 0) &                        # Negative momentum
        (obv[ticker].diff() < 0) &                      # OBV is decreasing
        (prices[ticker] < ma_short[ticker]) &          # Price below short-term MA
        (prices[ticker] < ma_medium[ticker]) &         # Price below medium-term MA
        (prices[ticker] < ma_long[ticker])             # Price below long-term MA
    )
    
    # Apply signals
    trading_signals[ticker][buy_condition] = 1    # Buy signal
    trading_signals[ticker][sell_condition] = -1  # Sell signal

# Save the trading signals DataFrame to an Excel file
data_file = Path(__file__).resolve().parent.parent / "data" / "results"
trading_signals.to_csv(data_file / "Trading_signals.xlsx")

print("Trading signals have been generated and saved to Trading_signals.xlsx.")