import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import mplfinance as mpf
from polygon import RESTClient
import time
from yfinance.exceptions import YFRateLimitError
from dotenv import load_dotenv
import os

load_dotenv()

# ========== CONFIG ==========

API_KEY = os.getenv("POLYGON_API_KEY")
DEFAULT_TICKER = 'APP'
DEFAULT_PERIOD = '5d'
DEFAULT_INTERVAL = '1h'
MOVING_AVERAGE_LENGTH = 10

# ========== FETCHING FUNCTIONS ==========
def fetch_polygon_data(ticker: str, timespan: str, start_date: str, end_date: str) -> pd.DataFrame:
    client = RESTClient(api_key=API_KEY)
    aggs = client.get_aggs(ticker, 1, timespan, start_date, end_date)

    df = pd.DataFrame([{
        'Open': bar.open,
        'High': bar.high,
        'Low': bar.low,
        'Close': bar.close,
        'Volume': bar.volume,
        'Datetime': pd.to_datetime(bar.timestamp, unit='ms')
    } for bar in aggs])

    df.set_index('Datetime', inplace=True)
    return df

def add_moving_average(df: pd.DataFrame, window: int = MOVING_AVERAGE_LENGTH) -> pd.DataFrame:
    df['Moving_Average'] = df['Close'].rolling(window=window).mean()
    return df

# ========== PLOTTING FUNCTION ==========
def plot_stock_data(df: pd.DataFrame, ticker: str):
    add_plot = mpf.make_addplot(df['Moving_Average'], color='orange', width=1.5)

    color = mpf.make_marketcolors(up='g', down='r', wick="inherit", edge="inherit", volume='in')
    style = mpf.make_mpf_style(
        base_mpf_style='nightclouds',
        marketcolors=color,
        gridcolor='gray',
        gridstyle='--',
        y_on_right=True
    )

    mpf.plot(
        df,
        type='candle',
        style=style,
        ylabel='Price',
        volume=True,
        title=f"{ticker} Historical Data with Moving Average",
        show_nontrading=False,
        datetime_format='%Y-%m-%d %H:%M:%S',
        addplot=add_plot,
        xrotation=45
    )

# ========== MAIN SCRIPT ==========
if __name__ == "__main__":
    ticker = DEFAULT_TICKER
    timespan = 'hour'
    start_date = '2025-06-01'
    end_date = '2025-06-11'

    df = fetch_polygon_data(ticker, timespan, start_date, end_date)
    df = add_moving_average(df, MOVING_AVERAGE_LENGTH)
    plot_stock_data(df, ticker)



