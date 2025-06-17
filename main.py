import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
import numpy as np
import datetime
import mplfinance as mpf
from polygon import RESTClient
from options import fetch_options_data, display_historical_greeks
import requests
import json
import time
from yfinance.exceptions import YFRateLimitError


# Define the ticker symbol and the period for historical data
# y_ticker = 'AAPL' # Ticker fetched using yfinance API Example: 'AAPL' for Apple Inc.
p_ticker = 'AAPL' # Ticker fetched using polygon API Example: 'AAPL' for Apple Inc.
period = '5d' # Example: '1d', '5d', '1mo', '1y', etc.
interval = '1h' # Example: '1m', '2m', '5m', '15m', '30m', '60m', etc.

# Fetch the historical data from yfinance for the specified ticker and the specified period and interval
# stock = yf.Ticker(y_ticker)
# retries = 3
# for attempt in range(retries):
#     try:
# stock_history = stock.history(period=period, interval=interval)
#         break  # Exit the loop if the request is successful
#     except YFRateLimitError:
#         print(f"Rate limit hit. Retrying in 20 seconds... (Attempt {attempt + 1}/{retries})")
#         time.sleep(20)  # Wait for 20 seconds before retrying
# else:
#     print("Failed to fetch data after multiple attempts.")
# stock_history.index.name = 'Date'
# moving_average_length = 50  # In days, Example: 10, 50, 200, etc.
# stock_history['Moving_Average'] = stock_history['Close'].rolling(window=moving_average_length).mean()
# stock_history = stock_history[['Open', 'High', 'Low', 'Close', 'Volume', 'Moving_Average']]
# add_plot = mpf.make_addplot(stock_history['Moving_Average'], color='orange', width=1.5)

# Fetch the real-time data from polygon.io API
client = RESTClient(api_key="lNJCp_smwLaCbMGll6t7QtaINXX60v1y")
aggs = client.get_aggs(p_ticker, 1, 'hour', '2025-06-01', '2025-06-11')
print(aggs[1])
df = pd.DataFrame([{
    'Open': bar.open,
    'High': bar.high,
    'Low': bar.low,
    'Close': bar.close,
    'Volume': bar.volume,
    'Datetime': pd.to_datetime(bar.timestamp, unit='ms')
} for bar in aggs])
df.set_index('Datetime', inplace=True)

# Calculate moving average (optional)
moving_average_length = 10
df['Moving_Average'] = df['Close'].rolling(window=moving_average_length).mean()

# Prepare addplot for moving average
add_plot = mpf.make_addplot(df['Moving_Average'], color='orange', width=1.5)

# Customize plot style
color = mpf.make_marketcolors(up='g', down='r', wick="inherit", edge="inherit", volume='in')
style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=color, gridcolor='gray', gridstyle='--', y_on_right=True)

# Plot using mplfinance
mpf.plot(
    df,
    type='candle',
    style=style,
    ylabel='Price',
    volume=True,
    title="AAPL Historical Data with Moving Average",
    show_nontrading=False,
    datetime_format='%Y-%m-%d %H:%M:%S',
    addplot=add_plot,
    xrotation=45
)

# Plot data
# mpf.plot(stock_history, 
#          type='candle', 
#          style=style, 
#          ylabel='Price', 
#          volume=True, 
#          title=f"{y_ticker} Historical Data with {moving_average_length}-Period Moving Average", 
#          show_nontrading=False, 
#          datetime_format='%Y-%m-%d %H:%M:%S', 
#          addplot=add_plot,
#          xrotation=45)

#Options

# options_data = fetch_options_data(p_ticker) 
# print(options_data)
