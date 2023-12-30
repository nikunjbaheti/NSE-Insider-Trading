import subprocess
import os
from datetime import datetime
import schedule
import time

def run_script(script_name):
    print(f"Running {script_name}...")
    subprocess.run(["python", script_name])

def get_market_cap():
    # Define the logic for getting market cap
    # You need to implement this function according to your requirements
    pass

def main():
    scripts_to_run = ["Run Scripts.py", "StkData.py", "Updated_Mktcap.py", "promoter_pledge.py", "insider_trading_data.py"]

    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Script started at {current_time}")

    # Run each script one by one
    for script in scripts_to_run:
        run_script(script)

    print("All scripts completed.")

if __name__ == "__main__":
    main()

# Schedule the job to run every day at 12 AM
schedule.every().day.at("12:00").do(get_market_cap)

while True:
    schedule.run_pending()
    time.sleep(1)
