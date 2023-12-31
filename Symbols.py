import csv
import datetime
import requests
import base64
from io import StringIO

def fetch_data():
    # Get the current date in DDMMYYYY format
    current_date = datetime.datetime.now().strftime('%d%m%Y')

    # Construct the Bhavcopy URL for the current date
    url = f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{current_date}.csv"

    try:
        # Fetch CSV data for the current date
        response = requests.get(url)
        response.raise_for_status()

        # Parse CSV data
        csv_data_array = list(csv.reader(StringIO(response.text)))

        # Extract data from the "SYMBOL" column
        symbols = [row[0] for row in csv_data_array[1:]]  # Assuming "SYMBOL" is in the first column

        # Save the symbols to a CSV file
        with open("Symbols.csv", "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["SYMBOL"])  # Write header
            csv_writer.writerows([[symbol] for symbol in symbols])

        print("Symbols saved to Symbols.csv for", current_date)

    except requests.exceptions.HTTPError as e:
        print(f"Error fetching data for {current_date}: {str(e)}")

        # If there is an error fetching the CSV for the current date, try the past 10 days
        for i in range(1, 11):
            past_date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%d%m%Y')
            past_url = f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{past_date}.csv"

            try:
                past_response = requests.get(past_url)
                past_response.raise_for_status()

                # Parse CSV data for the past date
                past_csv_data_array = list(csv.reader(StringIO(past_response.text)))

                # Extract data from the "SYMBOL" column
                symbols = [row[0] for row in past_csv_data_array[1:]]  # Assuming "SYMBOL" is in the first column

                # Save the symbols to a CSV file
                with open("Symbols.csv", "w", newline="") as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(["Symbol"])  # Write header
                    csv_writer.writerows([[symbol] for symbol in symbols])

                print("Symbols saved to Symbols.csv for", past_date)
                break  # Exit the loop if data is found for any past date

            except requests.exceptions.HTTPError as past_error:
                print(f"Error fetching data for {past_date}: {str(past_error)}")


# Call the function
fetch_data()

# GitHub credentials and repository information
github_user = "your_github_username"
github_token = "your_github_PAT"
repo_name = "NSE-Insider-Trading"
file_path = "Symbols.csv"

# GitHub API endpoints
base_url = f"https://api.github.com/repos/{github_user}/{repo_name}"
contents_url = f"{base_url}/contents/Symbols.csv"

# Read the contents of the file
with open(file_path, 'rb') as file:
    file_content = base64.b64encode(file.read()).decode('utf-8')

# Create a commit message
commit_message = "Update Symbols.csv"

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
