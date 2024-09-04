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
import bethspornitz_attr

###############################
# Declare global variables
###############################

# Create a project path object
project_path = pathlib.Path.cwd()

# Create a project data path object
data_path = project_path.joinpath('data')

# Create the data path if it doesn't exist, otherwise do nothing
data_path.mkdir(exist_ok=True)


# Create a function to create prefixed folders by transforming a list of names and combining each with a prefix (e.g., "data-").
# Pass in a list of folder names
# Pass in a prefix (e.g. 'data-') to add to each

def create_prefixed_folders(folder_list: list, prefix: str) -> None:
    for folder_name in folder_list:
        # Create the full folder name with prefix
        full_folder_name = f"{prefix}_{folder_name}"
        # Create the directory
        os.makedirs(full_folder_name, exist_ok=True)
        # Print the confirmation message
        print(f"Created folder: {full_folder_name}")



 ##############################
 #txt
 ##############################

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

 ##############################
 #Excel
 ##############################
def write_excel_file(folder_name, filename, data):
    file_path = pathlib.Path(folder_name).joinpath(filename) # use pathlib to join paths
    with open(file_path, 'wb') as file:
        file.write(data)
        print(f"Excel data saved to {file_path}")

def fetch_and_write_excel_data(folder_name, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        write_excel_file(folder_name, filename, response.content)
    else:
        print(f"Failed to fetch Excel data: {response.status_code}")

#Example:  fetch_and_write_excel_data(data_path, 'cattle.xls','https://github.com/bharathirajatut/sample-excel-dataset/raw/master/cattle.xls')

############################
#CSV
###########################

def write_csv_file(folder_path, filename, data):
    file_path = pathlib.Path(folder_path).joinpath(filename)
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)
        print(f"CSV data saved to {file_path}")

def fetch_and_write_csv_data(folder_path, filename, url):
    # Fetch the data from the given URL
    response = requests.get(url)
    if response.status_code == 200:  
        write_csv_file(folder_path, filename, response.text)
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Example usage
#fetch_and_write_csv_data(data_path, 'data.csv', 'https://raw.githubusercontent.com/MainakRepositor/Datasets/master/World%20Happiness%20Data/2020.csv')

################
#JSON
###############

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

"""
#####################################
# Define a main() function for this module.
#####################################

def main():
    ''' Main function to demonstrate module capabilities. '''

 # Call function to create folders using a prefix
    folder_names = ['csv', 'excel', 'json', 'txt']
    prefix = 'data-'
    create_prefixed_folders(folder_names, prefix)


    print(f"Name: {yourname_attr.my_name_string}")

    txt_url = 'https://shakespeare.mit.edu/romeo_juliet/full.html'

    csv_url = 'https://raw.githubusercontent.com/MainakRepositor/Datasets/master/World%20Happiness%20Data/2020.csv' 

    excel_url = 'https://github.com/bharathirajatut/sample-excel-dataset/raw/master/cattle.xls' 
    
    json_url = 'http://api.open-notify.org/astros.json'

    txt_folder_name = 'data-txt'
    csv_folder_name = 'data-csv'
    excel_folder_name = 'data-excel' 
    json_folder_name = 'data-json' 

    txt_filename = 'data.txt'
    csv_filename = 'data.csv'
    excel_filename = 'data.xls' 
    json_filename = 'data.json' 

    fetch_and_write_txt_data(txt_folder_name, txt_filename, txt_url)
    fetch_and_write_csv_data(csv_folder_name, csv_filename,csv_url)
    fetch_and_write_excel_data(excel_folder_name, excel_filename,excel_url)
    fetch_and_write_json_data(json_folder_name, json_filename,json_url)

    process_txt_file(txt_folder_name,'data.txt', 'results_txt.txt')
    process_csv_file(csv_folder_name,'data.csv', 'results_csv.txt')
    process_excel_file(excel_folder_name,'data.xls', 'results_xls.txt')
    process_json_file(json_folder_name,'data.json', 'results_json.txt')

    # Find some data you care about. What format is it? How will you ingest the data?
    # What do you want to extract and write? What export format will you use?
    # Process at least TWO unique data sets and describe your work clearly.
    # Use the README.md and your code to showcase your ability to work with data."""
#####################################
# Conditional Execution
#####################################

if __name__ == '__main__':
    main()