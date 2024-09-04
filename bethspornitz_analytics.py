''' 
This project focuses on developing proficiency in Git for version control, managing Python virtual environments, and handling various types of data. The project entails retrieving data from the web, processing it with suitable Python collections, and saving the processed data to files. 
 '''

# Standard library imports
import csv
import pathlib 
import os

# External library imports (requires virtual environment)
import requests  

# Local module imports     
import bethspornitz_project_setup
import utils_bethspornitz

def fetch_and_write_txt_data(folder_name, filename, url):
    # Fetch the data from the given URL
    response = requests.get(url)
    
    if response.status_code == 200:
       
        write_txt_file(folder_name, filename, data)
     
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Example usage
# fetch_and_write_txt_data('data', 'example.txt', 'https://example.com/data.txt')

#### Write function
def write_txt_file(folder_name, filename, data):
    file_path = pathlib.Path(folder_name).join_path(filename)
    with file_path.open('w') as file:
        file.write(data)
        print(f"Text data saved to {file_path}")