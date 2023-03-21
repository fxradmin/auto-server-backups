import requests
import json
import os
from datetime import datetime, timedelta
import datetime
import sys
from dotenv import load_dotenv
import zipfile

load_dotenv('.env')
APP_ID = os.getenv('APP_ID')
APP_SECERET = os.getenv('APP_SECERET')
TENANT_ID = os.getenv('TENANT_ID')
TOKEN_ENDPOINT =f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
MS_GRAPH_SCOPE = os.getenv('MS_GRAPH_SCOPE')
userID = os.getenv('userID')
folderID= os.getenv('folderID')
filePath='/Users/derekfodekerodgers/Projects/auto-server-backups/wawoo'
fileName= os.path.basename(filePath) #this will c

#needed_directory = '/home/fxrracing/public_html/shopifyexports'
needed_directory = '/Users/derekfodekerodgers/Projects/auto-server-backups/wawoo'
def format_needed_files(needed_files):
    needed_files = str(needed_files)
    needed_files = needed_files.replace("[","")
    needed_files = needed_files.replace("]","")
    needed_files = needed_files.replace("'","")
    needed_files = needed_files.replace(", ",",")
    needed_files = needed_files.replace(","," \n")

    return needed_files
# Initialize the first zip file with a name
def zip_files():
	print("zip files accessed")
	# Define the directory path where your Excel files are located
	print("old directory",os.getcwd())
	os.chdir(needed_directory)
	print (os.getcwd())
	current_dir = os.getcwd()
	# Create a list of all the Excel files in the directory
	all_files = os.listdir(current_dir)
	# Initialize variables for tracking the total size of the zip file
	#print("all files",all_files)
	total_size = 0
	max_size = 1024 * 1024 * 640 # 300 MB
	zip_file_index = 1
	zipMonth = datetime.datetime.now().strftime("%B%Y")
	zip_file_name = f"filebackup_{zipMonth}_{zip_file_index}.zip"
	zip_file = zipfile.ZipFile(zip_file_name, "w")
	file_path = os.path.join(current_dir, zip_file_name)
	files_to_upload = []
	needed_files = []

	for file in all_files:
		date_created = datetime.datetime.fromtimestamp(os.path.getmtime(file))
		if file.endswith(".xlsx") :
			#and date_created.year < datetime.datetime.now().year-2 and date_created.month == datetime.datetime.now().month
			needed_files.append(file)
			excel_file_path = os.path.join(current_dir, file)
			zip_file.write(excel_file_path, file)
			os.remove(file)

			zip_info = zip_file.getinfo(file)
			file_size = zip_info.compress_size
			total_size += file_size

			if total_size >= max_size:
				try:
					with zip_file.open('log_file.txt', 'w') as log_file:
						log_file.write(f"Backup created on {datetime.datetime.now()}\n".encode())
						log_file.write(f"Backup contains the following files: {format_needed_files(needed_files)} ".encode())
					zip_file.close()
					print("total size",total_size)
					zip_file_index += 1
					zip_file_name = f"fileBackup_{zipMonth}_{zip_file_index}.zip"
					zip_file = zipfile.ZipFile(zip_file_name, "w")
					total_size = 0

				except Exception as e:
					print("error",e)
					pass
				finally:
					print("finally")
					#print("log data",needed_files)
					files_to_upload.append(zip_file_name)
					pass


	zip_file.close()		#print(needed_files)

	#print("files to upload",files_to_upload)
	return files_to_upload



def request_upload_url(token_response, fileName):
	print('request upload url accessed')
	#upload file function to upload a file to the onedrive
	#token_response = get_access_token()
	access_token = token_response['access_token']
	print('upload process accessed')
	url= f'https://graph.microsoft.com/v1.0/users/{userID}/drive/items/{folderID}:/{fileName}:/createUploadSession'
	payload = json.dumps({
  			"@microsoft.graph.conflictBehavior": "rename",
  			"description": "description",
  			"name": fileName
		})
	headers = {
  		'Authorization': 'Bearer ' + access_token,
  		'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	print(json.dumps(response.text))
	return response


def upload_request(response, filePath):
	print('upload request would have happened here')
	upload_url=response.json()['uploadUrl']
	with open(filePath, 'rb') as f:
			total_file_size = os.path.getsize(filePath)
			chunk_size = 2560000 # 2.5MB
			#1310720
			#alt_chunk_size = 655360 # 640KB
			chunk_number = total_file_size//chunk_size
			chunk_leftover = total_file_size - chunk_size * chunk_number
			i = 0
			while True:
				chunk_data = f.read(chunk_size)
				start_index = i*chunk_size
				end_index = start_index + chunk_size
				#If end of file, break
				if not chunk_data:
					break
				if i == chunk_number:
					end_index = start_index + chunk_leftover
				#Setting the header with the appropriate chunk data location in the file
				headers = {'Content-Length':'{}'.format(chunk_size),'Content-Range':'bytes {}-{}/{}'.format(start_index, end_index-1, total_file_size)}
				#Upload one chunk at a time
				chunk_data_upload = requests.put(upload_url, data=chunk_data, headers=headers)
				print(chunk_data_upload)
				print(chunk_data_upload.json())
				i = i + 1



def get_access_token():
	data = {
		'client_id': APP_ID,
		'client_secret': APP_SECERET,
		'scope': MS_GRAPH_SCOPE,
		'grant_type': 'client_credentials'
	}
	try:
		response = requests.post(TOKEN_ENDPOINT, data=data)
		response.raise_for_status()
		#print(response.json())
		print(response.raise_for_status())
		#need to save the token in a in json file
		with open('token.json', 'w') as f:
			json.dump(response.json(), f)
		token_response=response.json()
		print('get new token accesed')
		return token_response
	except requests.exceptions.HTTPError as err:
		print(f'Error:{err}')
		raise

#check if the token has expired

def check_token_expiration(token_response):
	time_til_expiration = token_response['expires_in']
	expiration_time = datetime.datetime.now() + timedelta(seconds=time_til_expiration)
	print(expiration_time)
	if expiration_time < datetime.datetime.now():
		os.remove('token.json')
		print('token has expired')
		new_token = get_access_token()
		return new_token
	else:
		#print('token is still valid')
		print('token check accesed')
		return token_response
		#save the token to cache

def token_exists():
	if os.path.exists('token.json'):
		#read the token from the file and check if it has expired
		print('token exists returned true')
		return True
	else:
		#error message
		print('token exists returned false')
		return False

def get_token_from_cache():
	print('get token from cache accessed')
	with open('token.json', 'r') as f:
		token = json.load(f)
	return token


def main():
	file_names = zip_files()
	print(file_names)
	for fileName in file_names:
		filePath = os.path.join('/Users/derekfodekerodgers/Projects/auto-server-backups/wawoo', fileName)
		if token_exists():
			token_response = get_token_from_cache()
			token_response = check_token_expiration(token_response)  # Update this line
			upload_url_response = request_upload_url(token_response, fileName)
			upload_request(upload_url_response, filePath)
			print(fileName)
			os.remove(fileName)
		else:
			token_response = get_access_token()
			upload_url_response = request_upload_url(token_response, fileName)
			upload_request(upload_url_response, filePath)
			print(fileName)
			os.remove(fileName)
if __name__ == '__main__':
	main()
	if (os.path.exists('token.json')):
		os.remove('token.json')
	sys.exit()

