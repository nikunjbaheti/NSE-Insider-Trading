import requests
import base64

# GitHub credentials and repository information
github_user = "your_user_id"
github_token = "your_api_key"
repo_name = "NSE-Insider-Trading"
file_path = r"F:\Share\DONT DELETE OR TOUCH\Desktop\New folder\NSE-Insider-Trading-master\insider.csv"

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
