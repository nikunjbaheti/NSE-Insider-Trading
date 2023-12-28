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
import base64
import schedule
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

# GitHub credentials and repository information
github_user = "nikunjbaheti"
github_token = "Your_Github_PAT"
repo_name = "NSE-Insider-Trading"
file_path = "mktcap.csv"

# GitHub API endpoints
base_url = f"https://api.github.com/repos/{github_user}/{repo_name}"
contents_url = f"{base_url}/contents/insider.csv"

# Read the contents of the file
with open(file_path, 'rb') as file:
    file_content = base64.b64encode(file.read()).decode('utf-8')

# Create a commit message
commit_message = "Update insider.csv"

# Check if the file exists on the repository
response = requests.get(contents_url, auth=(github_user, github_token))
if response.status_code == 200:
    # If the file exists, update it
    sha = response.json()['sha']
    payload = {
        "message": commit_message,
        "content": file_content,
        "sha": sha
    }
    update_response = requests.put(contents_url, json=payload, auth=(github_user, github_token))
    print(update_response.text)
elif response.status_code == 404:
    # If the file doesn't exist, create it
    payload = {
        "message": commit_message,
        "content": file_content
    }
    create_response = requests.put(contents_url, json=payload, auth=(github_user, github_token))
    print(create_response.text)
else:
    print(f"Failed to check file existence. Status code: {response.status_code}")

# Schedule the job to run every day at 12 AM
schedule.every().day.at("12:00").do(get_market_cap)

while True:
    schedule.run_pending()
    time.sleep(1)
