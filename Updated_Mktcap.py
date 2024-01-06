from requests_html import HTMLSession
from datetime import timedelta
import os
import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf
import os
import logging
import requests
import time

def get_market_cap(symbol, session):
    # Construct the URL with the symbol
    url = f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}"
    
    # Open an HTML session with the URL
    response = session.get(url)
    
    # Add a delay to ensure the page is loaded before making the API call
    # time.sleep(5)
    
    # Make the API call
    api_url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}&section=trade_info"
    api_response = session.get(api_url)

    if api_response.status_code == 200:
        data = api_response.json()
        total_market_cap = data.get('marketDeptOrderBook', {}).get('tradeInfo', {}).get('totalMarketCap', None)
        return total_market_cap
    else:
        error_text = f"Request for symbol {symbol} failed with status code {api_response.status_code}"
        return None

# Read symbols from "Symbols.csv" file
symbols_df = pd.read_csv('Symbols.csv')

# Create an HTML session
session = HTMLSession()

# Fields to track
columns = ['symbol', 'market_cap']

# Create an empty DataFrame to store the results
mktcap_df = pd.DataFrame(columns=columns)

# Iterate through each symbol and fetch data
for index, row in symbols_df.iterrows():
    symbol = row['Symbol']
    market_cap = get_market_cap(symbol, session)

    if market_cap is not None:
        print(f"Market cap for {symbol}: {market_cap}")
        
        # Add a new row to the DataFrame
        mktcap_df = mktcap_df._append({'symbol': symbol, 'market_cap': market_cap}, ignore_index=True)
    else:
        print(f"Error fetching market cap for {symbol}")

# Save the DataFrame to a CSV file
mktcap_df.to_csv('mktcap.csv', index=False)

# Close the session at the end
session.close()
