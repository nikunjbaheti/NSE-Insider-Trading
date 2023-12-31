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

def get_data():
    # Create a session
    session = HTMLSession()

    # Define the headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.nseindia.com/",
    }

    # Set the headers
    session.headers.update(headers)

    # Get the main page first to start a session and set any necessary cookies
    main_page = session.get("https://www.nseindia.com/companies-listing/corporate-filings-pledged-data")

    url = f"https://www.nseindia.com/api/corporate-pledgedata?index=equities"
    response = session.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        error_text = f"Request failed with status code {response.status_code}"
        return error_text

logging.basicConfig(filename="data_update.log", format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Fields to track
columns = ['company_name', 'total_promoter_holding_pct', 'promoter_shares_encumbered', 'promoter_shares_encumbered_pct']

pledge_file_path = 'pledge.csv'

# Read the CSV file
pledge_df = pd.read_csv('pledge.csv')  # load csv file

# Delete existing data in the pledge.csv file
pledge_df = pd.DataFrame(columns=columns)
pledge_df.to_csv(pledge_file_path, index=False)

data = get_data()  # fetch data obtained from API

if type(data) == str:
    # there was some error and we couldn't fetch data from the API
    logger.info('error fetching data')
else:
    logger.info('data fetched')
    
    # Fill the dataframe with the insider trades from the day
    pledge_data = data['data']
    
    # we will fill this dataframe every day
    day_df = pd.DataFrame(columns=columns)
    
    # Iterate through insider data
    for i in range(len(pledge_data)):
        trade_data = pledge_data[i]
        #date = datetime.strptime(trade_data['date'], '%d-%b-%Y %H:%M')

        company_name = trade_data['comName']
        
        total_promoter_holding_pct = trade_data['percPromoterHolding']
        
        promoter_shares_encumbered = trade_data['totPromoterShares']
        
        promoter_shares_encumbered_pct = trade_data['percPromoterShares']

        # Add missing columns with default values or adjust the number of elements in the row
        row = [
            company_name, total_promoter_holding_pct, promoter_shares_encumbered, promoter_shares_encumbered_pct
        ]

        # Make sure the length of the row matches the length of the columns
        day_df.loc[len(day_df.index)] = row
        
        # Specify the columns for checking duplicates
        duplicate_check_columns = ['company_name', 'total_promoter_holding_pct', 'promoter_shares_encumbered', 'promoter_shares_encumbered_pct']

        # Create a pandas Series for the current row
        current_row = pd.Series(row, index=columns)

        # Check if the current row is a duplicate based on specified columns
        is_duplicate = day_df.duplicated(subset=duplicate_check_columns, keep='first').any()

        # If the row is not a duplicate, add it to the dataframe
        if not is_duplicate:
            day_df.loc[len(day_df.index)] = row

# Post-processing of the dataframe
logger.info(f'entries added: {len(day_df)}')
pledge_df = pd.concat([day_df, pledge_df], ignore_index=True)

# Save the DataFrame to the CSV file
pledge_df.to_csv(pledge_file_path, index=False)

# GitHub credentials and repository information
github_user = "your_github_username"
github_token = "your_github_PAT"
repo_name = "NSE-Insider-Trading"
file_path = "pledge.csv"

# GitHub API endpoints
base_url = f"https://api.github.com/repos/{github_user}/{repo_name}"
contents_url = f"{base_url}/contents/pledge.csv"

# Read the contents of the file
with open(file_path, 'rb') as file:
    file_content = base64.b64encode(file.read()).decode('utf-8')

# Create a commit message
commit_message = "Update pledge.csv"

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



