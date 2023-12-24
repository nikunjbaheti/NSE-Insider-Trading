import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from requests.auth import HTTPBasicAuth
import os

# Replace with your GitHub username and personal access token
GITHUB_USERNAME = "your_username"
GITHUB_TOKEN = "your_personal_access_token"

# Set the repository name and file name
REPO_NAME = "NSE Insider Trading"
FILE_NAME = "data.csv"

# Function to push the file to GitHub
def push_to_github(repo_name, file_name, file_content):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_name}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": "Add data.csv",
        "content": file_content
    }

    response = requests.put(url, json=data, headers=headers, auth=HTTPBasicAuth(GITHUB_USERNAME, GITHUB_TOKEN))

    if response.status_code == 200:
        print("File uploaded to GitHub successfully.")
    else:
        print(f"Failed to upload file to GitHub. Status code: {response.status_code}")
        print(response.text)

# Set up the WebDriver
driver = webdriver.Chrome()

try:
    # Open the website
    driver.get("https://www.nseindia.com/companies-listing/corporate-filings-insider-trading")

    # Click on the "3M" button
    three_m_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='3M']")))
    three_m_button.click()

    # Wait for 2 minutes
    time.sleep(120)

    # Click on the "Download(.csv)" button
    download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Download(.csv)']")))
    download_button.click()

    # Wait for the download to complete (adjust the sleep time if needed)
    time.sleep(10)

    # Read the downloaded CSV file
    with open(FILE_NAME, 'r') as file:
        file_content = file.read()

    # Push the file to GitHub
    push_to_github(REPO_NAME, FILE_NAME, file_content)

finally:
    # Close the WebDriver
    driver.quit()

# Clean up: Remove the local CSV file after pushing to GitHub
os.remove(FILE_NAME)
