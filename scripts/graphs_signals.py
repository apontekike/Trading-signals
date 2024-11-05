import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import json

# Step 1: Load the Excel data
# Define the path to your raw data file
data_file_raw = Path(__file__).resolve().parent.parent / "data" / "raw" 
data_file_signals = Path(__file__).resolve().parent.parent / "data" / "results" 

# Load your historical prices and signal data
prices = pd.read_csv(data_file_raw  / 'Historical_prices.xlsx',index_col=0)
signals = pd.read_csv(data_file_signals / 'Trading_signals.xlsx',index_col=0)
top = pd.read_csv(data_file_signals / 'Trades_with_positions.xlsx',index_col=0)


for ticker in top.index:
    signal = signals[ticker]
    price = prices[ticker]

    # Create a DataFrame for easier plotting
    df = pd.DataFrame({'Price': price, 'Signal': signal})

    df = df[100:]


    # Plot the price series
    plt.figure(figsize=(10, 6))
    plt.plot(df['Price'], label='Price', color='blue')

    # Add scatter plots for buy and sell signals
    buy_signals = df[df['Signal'] == 1]
    sell_signals = df[df['Signal'] == -1]

    plt.scatter(buy_signals.index, buy_signals['Price'], color='green', marker='^', label='Buy Signal', s=100)
    plt.scatter(sell_signals.index, sell_signals['Price'], color='red', marker='v', label='Sell Signal', s=100)

    # Customize the plot
    plt.title('Price Series with Buy and Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()