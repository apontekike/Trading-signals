import pandas as pd
from pathlib import Path
import numpy as np

# Step 1: Load the Excel data
# Define the path to your raw data file
data_file = Path(__file__).resolve().parent.parent / "data" / "raw" 

# Load the Excel file
prices = pd.read_csv(data_file / "Historical_prices.xlsx", index_col=0)

# Define EMA calculation function
def calculate_ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

# Initialize DataFrames for MACD, Signal, and Histogram
macd = pd.DataFrame(index=prices.index, columns=prices.columns)
signal = pd.DataFrame(index=prices.index, columns=prices.columns)

# Calculate MACD for each ticker
for ticker in prices.columns:
    # Step 2: Calculate 12-day and 26-day EMAs
    ema_12 = calculate_ema(prices[ticker], 12)
    ema_26 = calculate_ema(prices[ticker], 26)
    
    # Step 3: Calculate the MACD line
    macd[ticker] = ema_12 - ema_26
    
    # Step 4: Calculate the Signal line (9-day EMA of MACD line)
    signal[ticker] = calculate_ema(macd[ticker], 9)

data_file = Path(__file__).resolve().parent.parent / "data" / "signals" 

signal.to_csv(data_file / "macd_signal.xlsx")
macd.to_csv(data_file / "macd_value.xlsx")
