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

# Step 2: Calculate Daily Returns
daily_returns = prices.pct_change().fillna(0)  # Daily returns for each stock

# Step 3: Shift signals to align with the current day's returns
shifted_signals = signals.shift(1)  # Shift signals down by one day

# Calculate Strategy Returns
# Strategy returns are daily returns weighted by shifted signals (1, 0, -1)
strategy_returns = daily_returns * shifted_signals

# Step 4: Calculate Cumulative Returns for Each Stock
cumulative_returns = (1 + strategy_returns).cumprod() - 1  # Cumulative returns per stock

# Step 5: Rank Stocks by Final Cumulative Return
final_cumulative_returns = cumulative_returns.iloc[-1]  # Last row for each stock's final return
ranked_stocks = final_cumulative_returns.sort_values(ascending=False)

# Filter only stocks with positive final cumulative returns
positive_ranked_stocks = ranked_stocks[ranked_stocks > 0]

# Step 6: Calculate Aggregate Cumulative Return Across All Signals
aggregate_strategy_returns = strategy_returns.mean(axis=1)  # Mean return across all stocks each day
cumulative_aggregate_return = (1 + aggregate_strategy_returns).cumprod() - 1

if "__main__" == __name__:

    # Step 7: Plot Results
    plt.figure(figsize=(14, 7))

    # Plot individual top N stocks (e.g., top 5)
    top_n = 5
    for stock in ranked_stocks.index[:top_n]:  # Plot top 5 stocks by performance
        plt.plot(cumulative_returns[stock], label=stock)

    # Plot cumulative return of all trades
    plt.plot(cumulative_aggregate_return, label='Aggregate Strategy', color='black', linewidth=2)

    # Add plot details
    plt.title('Cumulative Returns of Top Stocks and Aggregate Strategy')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.show()

    # Step 8: Plot Distribution of Daily Strategy Returns
    plt.figure(figsize=(10, 5))
    sns.histplot(aggregate_strategy_returns, bins=50, kde=True)
    plt.title('Distribution of Daily Strategy Returns')
    plt.xlabel('Daily Return')
    plt.ylabel('Frequency')
    plt.show()

# Step 9: Identify Top 10 Stocks with Positive Returns and Calculate Their Combined Cumulative Return
top_10_positive_stocks = positive_ranked_stocks.index[:10]  # Get the top 10 positive stocks by cumulative return
top_10_strategy_returns = strategy_returns[top_10_positive_stocks].mean(axis=1)  # Average daily returns of the top 10 stocks
cumulative_top_10_return = (1 + top_10_strategy_returns).cumprod() - 1  # Cumulative return if only top 10 traded

# Step 9: Save All Positive-Return Stocks to CSV
positive_stocks_df = pd.DataFrame({
    "Stock": positive_ranked_stocks.index,
    "Cumulative Return": positive_ranked_stocks.values
})

# Save the positive-performing stocks and their returns to a CSV file
positive_stocks_df.to_csv(data_file_signals / "positive_performing_stocks.xlsx", index=False)

if "__main__" == __name__:
    
    print("Top 10 Positive Performing Stocks and their Cumulative Returns saved to CSV.")
    print("Cumulative Return if Only Top 10 Positive Stocks Were Traded:", cumulative_top_10_return[-1])

    # Plot cumulative return for the top 10 stocks
    plt.figure(figsize=(14, 7))
    plt.plot(cumulative_top_10_return, label='Top 10 Positive Stocks Strategy', color='purple', linewidth=2)
    plt.title('Cumulative Return of Top 10 Positive Performing Stocks Strategy')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.show()