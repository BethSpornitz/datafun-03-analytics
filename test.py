# Standard library imports
import csv
import pathlib
import os

# External library imports (requires virtual environment)
import requests

# Local module imports     
import bethspornitz_project_setup


###To try to bypass the SSL error
import requests
import requests.packages.urllib3.contrib.pyopenssl
requests.packages.urllib3.contrib.pyopenssl.inject_into_urllib3()

###############################
# Declare global variables
###############################

# Create a project path object
project_path = pathlib.Path.cwd()

# Create a project data path object
data_path = project_path.joinpath('data')

# Create the data path if it doesn't exist, otherwise do nothing
data_path.mkdir(exist_ok=True)


# Write function for txt file to be used in fetch_and_write
def write_txt_file(folder_name, filename, data):
    file_path = pathlib.Path(folder_name).joinpath(filename)
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)
        print(f"Text data saved to {file_path}")

def fetch_and_write_txt_data(folder_name, filename, url):
    # Fetch the data from the given URL
    response = requests.get(url)
    if response.status_code == 200:  
        write_txt_file(folder_name, filename, response.text)
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Example usage
#fetch_and_write_txt_data('data', 'example.txt', 'https://openlibrary.org/works/OL123456W/Romeo_and_Juliet')