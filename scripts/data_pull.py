from pathlib import Path
import yfinance as yf
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import os

def get_historical(tickers, start_date, end_date, interval="1d"):

    # Fetch the historical stock prices
    data = yf.download(tickers, start=start_date, end=end_date, interval=interval)['Adj Close']

    return data

def get_volume(tickers, start_date, end_date,interval="1d"):

    # Fetch the historical stock prices
    data = yf.download(tickers, start=start_date, end=end_date, interval=interval)['Volume']

    return data

def load_data(path,start_date,end_date,interval="1d"):

    df = pd.read_excel(path / "S&P500_tickers.xlsx")
    tickers = df['Symbol'].tolist()

    data = get_historical(tickers, start_date, end_date,interval=interval)
    data.to_csv(path / "Historical_prices.xlsx")

    data = get_volume(tickers, start_date, end_date, interval=interval)
    data.to_csv(path / "Historical_volume.xlsx")

if __name__ == "__main__":

    project_root = Path(__file__).resolve().parent.parent  # Goes up two levels to project-folder
    data_folder = project_root / "data" / "raw"

    start_date = (date.today() - relativedelta(days=60)).strftime("%Y-%m-%d")
    end_date = date.today().strftime("%Y-%m-%d")

    df = pd.read_excel(data_folder / "S&P500_tickers.xlsx")

    tickers = df['Symbol'].tolist()

    start_date = (date.today() - relativedelta(days=60)).strftime("%Y-%m-%d")
    end_date = date.today().strftime("%Y-%m-%d")

    data = get_historical(tickers, start_date, end_date, interval="1h")
    data.to_csv(data_folder / "Historical_prices.xlsx")

    data = get_volume(tickers, start_date, end_date, interval="1h")
    data.to_csv(data_folder / "Historical_volume.xlsx")

