# Standard library imports
import csv
import pathlib
import os
import json
import re
from collections import Counter
import pandas as pd

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
        return None

def process_text_data(text):
    # Remove non-alphabetic characters and make lowercase
    clean_text = re.sub(r'[^A-Za-z\s]', '', text).lower()

    # Split the text into words
    words = clean_text.split()

    # Get word count and unique words using set
    word_count = len(words)
    unique_words = set(words)

    # Get frequency of each word
    word_freq = Counter(words)

    # Sort words by frequency
    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Count the total number of alphabetic characters (letters)
    letter_count = sum(1 for char in text if char.isalpha())

    return word_count, unique_words, sorted_word_freq, letter_count

def analyze_text(folder_name, filename, url):
    # Fetch the text data from the URL
    text_data = fetch_and_write_txt_data(folder_name, filename, url)
    
    if text_data:
        # Process the text data
        word_count, unique_words, sorted_word_freq, letter_count = process_text_data(text_data)

        # Prepare the analysis results
        analysis = (
            f"Total Word Count: {word_count}\n"
            f"Unique Words Count: {len(unique_words)}\n"
            f"Total Letter Count: {letter_count}\n\n"
            "Top 10 Most Frequent Words:\n"
        )

         # Append top 10 words by frequency
        for word, freq in sorted_word_freq[:10]:
            analysis += f"{word}: {freq}\n"

        # Save the analysis to a file
        write_txt_file(folder_name, f"analysis_{filename}", analysis)

# Example usage for TXT
fetch_and_write_txt_data('data-txt', 'data-txt.txt', 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt')
analyze_text('data-txt', 'data-txt.txt', 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt')