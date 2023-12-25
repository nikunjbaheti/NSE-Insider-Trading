import subprocess
import time
import os

def run_script(script_name, script_directory):
    try:
        script_path = os.path.join(script_directory, script_name)
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

def main():
    script_directory = r"F:\Share\DONT DELETE OR TOUCH\Desktop\New folder\NSE-Insider-Trading-master"
    script_names = ["get_trading_data.py", "insider_trading_data.py", "combine_trade_data.py", "Github.py"]

    for script_name in script_names:
        run_script(script_name, script_directory)
        print(f"Waiting for 20 seconds before running the next script...")
        time.sleep(20)  # Wait for 2 minutes (120 seconds)

if __name__ == "__main__":
    main()
