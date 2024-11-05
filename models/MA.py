import pandas as pd
from pathlib import Path
import numpy as np

# Step 1: Load the Excel data
# Define the path to your raw data file
data_file = Path(__file__).resolve().parent.parent / "data" / "raw" 
# Load the Excel file
df = pd.read_csv(data_file / "Historical_prices.xlsx", index_col=0)

# Step 2: Calculate moving averages
moving_average_10 = df.rolling(window=10).mean()  # 10-day moving average
moving_average_20 = df.rolling(window=20).mean()  # 20-day moving average
moving_average_50 = df.rolling(window=50).mean()  # 50-day moving average

data_file = Path(__file__).resolve().parent.parent / "data" / "signals" 


moving_average_10.to_csv(data_file / 'MA_10p.xlsx')
moving_average_20.to_csv(data_file / 'MA_20p.xlsx')
moving_average_50.to_csv(data_file / 'MA_50p.xlsx')

