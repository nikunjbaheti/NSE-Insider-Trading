# NSE Insider Trading Data Updater

This Python script fetches insider trading data from the NSE India API, processes the data, and updates it in a CSV file named `insider.csv`. The script also pushes the updated CSV file to a GitHub repository for version control.

# Dependencies

Make sure you have the following Python libraries installed:

- requests_html
- pandas
- numpy
- yfinance

You can install them using:

```bash
pip install requests_html pandas numpy yfinance

## Usage

1. Clone the repository:

```bash
git clone https://github.com/nikunjbaheti/NSE-Insider-Trading.git
```

2. Navigate to the project directory:

```bash
cd NSE-Insider-Trading
```

3. Run the script:

```bash
python script_name.py
```

Replace `script_name.py` with the actual name of your Python script.

# Configuration

Make sure to configure the following parameters in the script:

- `github_user`: Your GitHub username.
- `github_token`: Your GitHub personal access token.
- `repo_name`: The name of your GitHub repository.
- `file_path`: The path to the insider.csv file in your GitHub repository.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Remember to replace `script_name.py` with the actual name of your Python script, and update the configuration parameters accordingly.
