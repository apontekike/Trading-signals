import pandas as pd
from pathlib import Path

data_file = Path(__file__).resolve().parent.parent / "data" / "raw" 

# Load the Excel file
prices = pd.read_csv(data_file / "Historical_prices.xlsx", index_col=0)
volumes = pd.read_csv(data_file / "Historical_volume.xlsx", index_col=0)

# Step 2: Initialize an empty DataFrame for OBV with the same structure
obv = pd.DataFrame(index=prices.index, columns=prices.columns)

# Step 3: Calculate OBV for each ticker
for ticker in prices.columns:
    # Initialize the first OBV value to zero
    obv[ticker].iloc[0] = 0
    
    # Loop through each row to calculate OBV
    for i in range(1, len(prices)):
        if prices[ticker].iloc[i] > prices[ticker].iloc[i-1]:  # Price increased
            obv[ticker].iloc[i] = obv[ticker].iloc[i-1] + volumes[ticker].iloc[i]
        elif prices[ticker].iloc[i] < prices[ticker].iloc[i-1]:  # Price decreased
            obv[ticker].iloc[i] = obv[ticker].iloc[i-1] - volumes[ticker].iloc[i]
        else:  # Price unchanged
            obv[ticker].iloc[i] = obv[ticker].iloc[i-1]

data_file = Path(__file__).resolve().parent.parent / "data" / "signals" 
obv.to_csv(data_file / "OBV_stocks.xlsx")
