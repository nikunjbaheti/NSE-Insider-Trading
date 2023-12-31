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

# Create an HTML session
session = HTMLSession()

# Fields to track
columns = ['symbol', 'basic_industry','macro', 'sector']

# Create an empty DataFrame to store the results
mktcap_df = pd.DataFrame(columns=columns)

# Iterate through each symbol and fetch data
for index, row in symbols_df.iterrows():
    symbol = row['Symbol']
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

# GitHub credentials and repository information
github_user = "your_github_username"
github_token = "your_github_PAT"
repo_name = "NSE-Insider-Trading"
file_path = "stkdata.csv"

# GitHub API endpoints
base_url = f"https://api.github.com/repos/{github_user}/{repo_name}"
contents_url = f"{base_url}/contents/stkdata.csv"

# Read the contents of the file
with open(file_path, 'rb') as file:
    file_content = base64.b64encode(file.read()).decode('utf-8')

# Create a commit message
commit_message = "Update stkdata.csv"

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



