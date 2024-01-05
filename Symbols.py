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
