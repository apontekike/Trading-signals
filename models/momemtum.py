import pandas as pd
from pathlib import Path
import numpy as np

# Define the path to your raw data file
data_file = Path(__file__).resolve().parent.parent / "data" / "raw" 

# Load the Excel file
df = pd.read_csv(data_file / "Historical_prices.xlsx", index_col=0)

# Initialize a new DataFrame to hold results
results = pd.DataFrame(index=df.index)

# Iterate over each column (stock ticker)
n = 20
for ticker in df.columns:
    #Calculate 20-day momentum
    momentum = (df[ticker] - df[ticker].shift(n)) / df[ticker].shift(n)

    #Calculate positive and negative days
    positive_days = df[ticker].diff().gt(0).rolling(window=n).sum()
    negative_days = df[ticker].diff().lt(0).rolling(window=n).sum()

    #Calculate percentages
    percent_positive = positive_days / n
    percent_negative = negative_days / n

    #Calculate the result: momentum * (percent_positive - percent_negative)
    result = np.where(
        momentum > 0,
        momentum * (percent_positive - percent_negative),
        momentum * (percent_negative - percent_positive)
    )

    # Store the result in the results DataFrame
    results[ticker] = momentum

data_file = Path(__file__).resolve().parent.parent / "data" / "signals" 
results = results.iloc[n:]


#Save the results to a new Excel file (optional)
results.to_csv(data_file / 'momentum.xlsx')

