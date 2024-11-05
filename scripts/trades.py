from pathlib import Path
import yfinance as yf
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import os
import json

# Get the path to the data directory from the current script location
project_root = Path(__file__).resolve().parent.parent  # Goes up two levels to project-folder
data_folder = project_root / "data" / "results"

signals = pd.read_csv(data_folder / "Trading_signals.xlsx")
signals = signals.tail(1)
signals = signals.T
stocks = pd.read_csv(data_folder / "positive_performing_stocks.xlsx",index_col=0)

signals = signals.rename_axis(stocks.index.name)
signals = signals[1:]
signals.columns = ['Signal']

trades = stocks.join(signals, how='inner')
trades = trades.loc[~(trades == 0).all(axis=1)]

trades = trades[trades['Signal'] != 0]

trades.to_csv(data_folder / "Trades.xlsx")





