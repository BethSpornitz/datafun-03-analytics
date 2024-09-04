# Standard library imports
import csv
import pathlib
import os
import json

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

def write_json_file(folder_path, filename, data):
    file_path = pathlib.Path(folder_path).joinpath(filename)
    with file_path.open('w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"JSON data saved to {file_path}")

def fetch_and_write_json_data(folder_path, filename, url):
    # Fetch the data from the given URL
    response = requests.get(url)
    if response.status_code == 200:  
        json_data = response.json()  # Parse the JSON response content
        write_json_file(folder_path, filename, json_data)
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Example usage
fetch_and_write_json_data(data_path, 'data.json', 'http://api.open-notify.org/astros.json')