import yfinance as yf
import pandas as pd

def fetch_options_data(ticker_symbol):
    # Fetch the stock data
    stock = yf.Ticker(ticker_symbol)
    
    # Get available expiration dates
    expiration_dates = stock.options
    if not expiration_dates:
        print(f"No options data available for {ticker_symbol}")
        return

    # Collect options data for each expiration date
    all_options_data = []
    for exp_date in expiration_dates:
        options_chain = stock.option_chain(exp_date)
        calls = options_chain.calls
        puts = options_chain.puts

        # Add expiration date to the data
        calls['type'] = 'call'
        calls['expirationDate'] = exp_date
        puts['type'] = 'put'
        puts['expirationDate'] = exp_date

        all_options_data.append(calls)
        all_options_data.append(puts)

    # Combine all options data into a single DataFrame
    options_data = pd.concat(all_options_data, ignore_index=True)
    return options_data

def display_historical_greeks(ticker_symbol):
    options_data = fetch_options_data(ticker_symbol)
    if options_data is None:
        return

    # Display relevant columns including Greeks if available
    greeks_columns = ['impliedVolatility', 'delta', 'gamma', 'theta', 'vega']
    available_columns = [col for col in greeks_columns if col in options_data.columns]

    if available_columns:
        print(options_data[['contractSymbol', 'type', 'expirationDate'] + available_columns])
    else:
        print("No Greeks data available for the options.")

if __name__ == "__main__":
    ticker = input("Enter the ticker symbol: ").strip().upper()
    display_historical_greeks(ticker)