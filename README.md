# OneDrive File Uploader

This script uploads multiple files to a OneDrive folder using the Microsoft Graph API. The script uses the `file_names` array to store the names of files to be uploaded. The script checks for an existing access token in a file named `token.json`. If the token is expired or doesn't exist, it requests a new token.

## Prerequisites

- Python 3.x
- Requests library: Install using `pip install requests`

## Configuration

Before running the script, you need to set up your OneDrive API credentials and other required variables. Replace the placeholder values in the following variables:

```python
APP_ID = ""
APP_SECERET = ""
TOKEN_ENDPOINT = ""
MS_GRAPH_SCOPE = ""
userID = ""
folderID = ""
```


## Functionality
- Uploads automatically generated backupfiles and uploads to a OneDrive folder (AAdmin)


## Usage
- make sure you have python 3.x installed
- Install the requests library using `pip install -r requirements.txt` or `pipenv install -r requirements.txt`
- Run the script using `python onedrive_uploader.py`
	
