# Standard library imports
import csv
import pathlib
import os
import json
import re
from collections import Counter

# External library imports (requires virtual environment)
import requests

# Ensure SSL certificates are handled properly
import requests.packages.urllib3.contrib.pyopenssl
requests.packages.urllib3.contrib.pyopenssl.inject_into_urllib3()

# Local module imports
import bethspornitz_project_setup

###############################
# Declare global variables
###############################

# Create a project path object
project_path = pathlib.Path.cwd()

# Create a project data path object
data_path = project_path.joinpath('data')

# Create the data path if it doesn't exist
data_path.mkdir(exist_ok=True)

###############################
# Create prefixed folders
###############################

def create_prefixed_folders(folder_list: list, prefix: str) -> None:
    for folder_name in folder_list:
        # Create the full folder name with prefix
        full_folder_name = f"{prefix}{folder_name}"
        # Create the directory
        os.makedirs(full_folder_name, exist_ok=True)
        # Print the confirmation message
        print(f"Created folder: {full_folder_name}")

# Call function to create folders using a prefix
folder_names = ['csv', 'excel', 'json', 'txt']
prefix = 'data-'
create_prefixed_folders(folder_names, prefix)

##############################
# TXT
##############################

def write_txt_file(folder_name, filename, data):
    folder_path = pathlib.Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    file_path = folder_path.joinpath(filename)
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)
        print(f"Text data saved to {file_path}")

def fetch_and_write_txt_data(folder_name, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        write_txt_file(folder_name, filename, response.text)
        return response.text
    else:
        print(f"Failed to fetch data: {response.status_code}")

def process_text_data(text):
    # Remove non-alphabetic characters and make lowercase
    text = re.sub(r'[^A-Za-z\s]', '', text).lower()

    # Split the text into words
    words = text.split()

    # Get word count and unique words using set
    word_count = len(words)
    unique_words = set(words)

    # Get frequency of each word
    word_freq = Counter(words)

    # Sort words by frequency
    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    return word_count, unique_words, sorted_word_freq

def analyze_text(folder_name, filename, url):
    # Fetch the text data from the URL
    text_data = fetch_and_write_txt_data(folder_name, filename, url)
    
    if text_data:
        # Process the text data
        word_count, unique_words, sorted_word_freq = process_text_data(text_data)

        # Prepare the analysis results
        analysis = (
            f"Total Word Count: {word_count}\n"
            f"Unique Words Count: {len(unique_words)}\n\n"
            "Top 10 Most Frequent Words:\n"
        )

        # Append top 10 words by frequency
        for word, freq in sorted_word_freq[:10]:
            analysis += f"{word}: {freq}\n"

        # Save the analysis to a file
        write_txt_file(folder_name, f"analysis_{filename}", analysis)

# Example usage
fetch_and_write_txt_data('data-txt', 'data-txt.txt', 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt')

# Example usage
analyze_text('data-txt', 'data-txt.txt', 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt')



##############################
# Excel
##############################

def write_excel_file(folder_name, filename, data):
    folder_path = pathlib.Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    file_path = folder_path.joinpath(filename)
    with open(file_path, 'wb') as file:
        file.write(data)
        print(f"Excel data saved to {file_path}")

def fetch_and_write_excel_data(folder_name, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        write_excel_file(folder_name, filename, response.content)
    else:
        print(f"Failed to fetch Excel data: {response.status_code}")

# Example usage
fetch_and_write_excel_data('data-excel', 'data-excel.xls', 'https://github.com/bharathirajatut/sample-excel-dataset/raw/master/cattle.xls')

############################
# CSV
###########################

def write_csv_file(folder_path, filename, data):
    folder_path = pathlib.Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    file_path = folder_path.joinpath(filename)
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)
        print(f"CSV data saved to {file_path}")

def fetch_and_write_csv_data(folder_path, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        write_csv_file(folder_path, filename, response.text)
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Example usage
fetch_and_write_csv_data('data-csv', 'data-csv.csv', 'https://raw.githubusercontent.com/MainakRepositor/Datasets/master/World%20Happiness%20Data/2020.csv')

################
# JSON
###############

def write_json_file(folder_path, filename, data):
    folder_path = pathlib.Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    file_path = folder_path.joinpath(filename)
    with file_path.open('w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"JSON data saved to {file_path}")

def fetch_and_write_json_data(folder_path, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()  # Parse the JSON response content
        write_json_file(folder_path, filename, json_data)
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Example usage
fetch_and_write_json_data(data_path, 'data.json', 'http://api.open-notify.org/astros.json')