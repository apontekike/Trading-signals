import pandas as pd
import numpy as np
from pathlib import Path
import yfinance as yf

def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    try:
        current_price = stock.history(period="1d")["Close"].iloc[-1]
        return current_price
    except IndexError:
        return None  # Return None if price is not available


# Example usage
ticker = "AAPL"  # Replace with your desired ticker symbol
current_price = get_current_price(ticker)
print(f"The current price of {ticker} is: ${current_price:.2f}")


# Define file paths
data_file_prices = Path(__file__).resolve().parent.parent / "data" / "raw" / 'Historical_prices.xlsx'
data_file_signals = Path(__file__).resolve().parent.parent / "data" / "results"

# Load data
signals_df = pd.read_csv(data_file_signals / 'Trading_signals.xlsx', index_col=0, parse_dates=True)
prices_df = pd.read_csv(data_file_prices, index_col=0, parse_dates=True)
stocks_df = pd.read_csv(data_file_signals / 'Trades.xlsx', index_col=0, parse_dates=True)

# Filter the data to use only the relevant stocks
prices_df = prices_df[stocks_df.index]
signals_df = signals_df[stocks_df.index]

# Calculate returns based on buy/sell signals
returns_data = {}
for ticker in signals_df.columns:
    ticker_signals = signals_df[ticker]
    ticker_prices = prices_df[ticker]
    returns = []
    start_price = None
    position = None
    
    for i in range(len(ticker_signals) - 1):
        # Long position: Buy signal (1) to Sell signal (-1)
        if ticker_signals[i] == 1 and position is None:
            start_price = ticker_prices[i]
            position = 'long'
        elif ticker_signals[i] == -1 and position == 'long' and start_price is not None:
            end_price = ticker_prices[i]
            returns.append((end_price - start_price) / start_price)
            start_price = None
            position = None
        
        # Short position: Sell signal (-1) to Buy signal (1)
        elif ticker_signals[i] == -1 and position is None:
            start_price = ticker_prices[i]
            position = 'short'
        elif ticker_signals[i] == 1 and position == 'short' and start_price is not None:
            end_price = ticker_prices[i]
            returns.append((start_price - end_price) / start_price)
            start_price = None
            position = None

    returns_data[ticker] = returns

# Convert returns data to a DataFrame and replace NaNs with 0
returns_df = pd.DataFrame({k: pd.Series(v) for k, v in returns_data.items()}).fillna(0)

# Calculate probability of a good signal
good_signal_prob = returns_df.apply(lambda x: np.mean(x > 0), axis=0)

# Calculate payout ratio: average profit / average absolute loss
average_profit = returns_df.apply(lambda x: x[x > 0].mean(), axis=0).fillna(0)
average_loss = returns_df.apply(lambda x: -x[x < 0].mean(), axis=0).fillna(0)  # Take absolute value of losses
payout_ratio = average_profit / average_loss
payout_ratio = payout_ratio.replace([np.inf, -np.inf], 0)  # Replace inf values if average_loss is 0

# Calculate Kelly fraction using probability and payout ratio
kelly_fraction = good_signal_prob - (1 - good_signal_prob) / payout_ratio
kelly_fraction = kelly_fraction.clip(lower=0)

# Combine Kelly fraction, good signal probability, and payout ratio into a single DataFrame
kelly_data = pd.DataFrame({
    'Kelly Fraction': kelly_fraction,
    'Probability of Good Signal': good_signal_prob,
    'Payout Ratio': payout_ratio
})

# Display the result with probabilities correctly shown
pd.options.display.float_format = '{:.4f}'.format
kelly_data_filtered = kelly_data[kelly_data['Kelly Fraction'] > 0]
trades = pd.merge(kelly_data_filtered, stocks_df, left_index=True, right_index=True, how='inner')

trades = trades.sort_values(by="Kelly Fraction", ascending=False)

trades["Capital Allocation"] = 1000000 * trades["Kelly Fraction"]

# Add a new column for current price
trades['Current Price'] = trades.index.map(get_current_price)

# Calculate the number of shares
trades['Shares to Buy'] = trades['Capital Allocation'] / trades['Current Price']

kelly_sum = trades['Kelly Fraction'].sum()

# Add the "Total" row with NaN in all columns except "Kelly fraction"
trades.loc['Total'] = [np.nan] * (len(trades.columns) - 1) + [kelly_sum]

print()
print()
print()
print(trades["Capital Allocation"].sum())
print()
print()
print()

trades.drop(columns=['Cumulative Return', 'Capital Allocation', 'Current Price'], inplace=True)

trades.to_csv(data_file_signals / "Trades_with_positions.xlsx")
