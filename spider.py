# when run , it will zip all the files in the current directory and upload send it to a webhook
import os
import sys
import zipfile
import smtplib
import time
import datetime
import requests

# Define the function to send email
def zip_files():
	current_dir = os.getcwd()
	all_files = os.listdir(current_dir)
	zip_file_name = "ServerBackup"+ '.zip'
	file_path = os.path.join(current_dir, zip_file_name)
	needed_files = []
	with zipfile.ZipFile(file_path, 'w') as zip:
		for file in all_files:
			#check if the file is a .xlsx file and if it was created in the current month
			date_created = datetime.datetime.fromtimestamp(os.path.getmtime(file))

			if file.endswith('.xlsx') and date_created.year < datetime.datetime.now().year and date_created.month == datetime.datetime.now().month:
				#append file name to a list called needed_files
				needed_files.append(file)
				print("Date and time",file,date_created)
				#print( "Date ",file,"was created:",date_created.year,date_created.month)
				zip.write(file)
				print('Added file: ' + file)
				print("...")
				#os.remove(file) - remove the file after it has been added to the zip file
		#create a .txt file with the date and time of the backup and add it to the zip file
		#datetimes = datetime.datetime.now()
		with zip.open('log_file.txt', 'w') as log_file:
			log_file.write(f"Backup created on {datetime.datetime.now()}\n".encode())
			log_file.write(f"Backup contains the following files: {needed_files}".encode())


	return zip_file_name

#define a function to upload the file to a webhook
def upload_file(zip_file_name):
	#upload the file to a webhook
	url = "https://hook.us1.make.com/t6ea9esx6e6xdwq14fmissri492livhs"
	with open(zip_file_name, 'rb') as f:

		r = requests.post(url, files={zip_file_name: f})

		return r.status_code

def main():


	# Get the email address and password
	#email = input('Enter your email address: ')
	#password = input('Enter your email password: ')

	zip_file_name = zip_files()
	#status_code = upload_file(zip_file_name)
	#print(status_code)
	#print where has the file been saved
	# Remove the zip file
	print(zip_file_name)
	#os.remove(zip_file_name)
	print('Done and file removed!')


#Call the main function

if __name__ == "__main__":
	main()

	sys.exit()
