from requests_html import HTMLSession
from datetime import timedelta
import os
import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf
import os
import requests
import time

def get_stock_data(symbol, session):
    # Construct the URL with the symbol
    url = f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}"
    
    # Open an HTML session with the URL
    response = session.get(url)
    
    # Add a delay to ensure the page is loaded before making the API call
    # time.sleep(5)
    
    # Make the API call
    api_url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    api_response = session.get(api_url)

    if api_response.status_code == 200:
        data = api_response.json()
        basic_industry = data.get('industryInfo', {}).get('basicIndustry', None)
        industry = data.get('industryInfo', {}).get('industry', None)
        macro = data.get('industryInfo', {}).get('macro', None)
        sector = data.get('industryInfo', {}).get('sector', None)
        
        return basic_industry, industry, macro, sector  # Correct indentation here
    else:
        error_text = f"Request for symbol {symbol} failed with status code {api_response.status_code}"
        return None

# Read symbols from "Symbols.csv" file
symbols_df = pd.read_csv('Symbols.csv')

print(df.head())

# Create an HTML session
session = HTMLSession()

# Fields to track
columns = ['symbol', 'basic_industry','macro', 'sector']

# Create an empty DataFrame to store the results
mktcap_df = pd.DataFrame(columns=columns)

# Iterate through each symbol and fetch data
for index, row in symbols_df.iterrows():
    symbol = row['symbol']
    industry_data = get_stock_data(symbol, session)

    if industry_data is not None:
        basic_industry, industry, macro, sector = industry_data  # Unpack the tuple

        print(f"Stock data for {symbol}: {industry_data}")

        # Add a new row to the DataFrame
        mktcap_df = mktcap_df._append({'symbol': symbol, 'basic_industry': basic_industry, 'industry': industry, 'macro': macro, 'sector': sector}, ignore_index=True)
    else:
        print(f"Error fetching market cap for {symbol}")

# Save the DataFrame to a CSV file
mktcap_df.to_csv('stkdata.csv', index=False)

# Close the session at the end
session.close()
