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
    file_path = pathlib.Path(folder_name).joinpath(filename)
    try:
        folder_path = pathlib.Path(folder_name)
        folder_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        
        # Attempt to open and write the file
        with open(file_path, 'wb') as file:
            file.write(data)
            print(f"Excel data saved to {file_path}")
    except IOError as e:
        print(f"IOError occurred while writing file: {e}")
    except OSError as e:
        print(f"OSError occurred while creating directories: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing file: {e}")
    finally:
        print("Write operation attempted.")
    
    return file_path  # Return the file path for further analysis

def fetch_and_write_excel_data(folder_name, filename, url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        
        # Attempt to write the fetched data to a file
        file_path = write_excel_file(folder_name, filename, response.content)
        
        # Perform data analysis after saving the file
        analyze_excel_data(file_path)
        
    except requests.RequestException as e:
        print(f"RequestException occurred while fetching data: {e}")
    except ValueError as e:
        print(f"ValueError occurred while processing response content: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching data: {e}")
    finally:
        print("Fetch operation attempted.")

def analyze_excel_data(file_path):
    try:
        # Load the Excel file into a pandas DataFrame using xlrd for .xls files - must pip install xlrd
        df = pd.read_excel(file_path, engine='xlrd')
        
        # Display basic info about the data
        print("\nData Preview:")
        print(df.head())  # Show the first 5 rows of the data
        
        print("\nSummary Statistics:")
        print(df.describe())  # Show summary statistics for numerical columns
        
        # Perform any additional analysis here
        
    except Exception as e:
        print(f"An error occurred while analyzing the Excel data: {e}")

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
        process_csv_data(folder_path, filename)  # Process data after saving
    else:
        print(f"Failed to fetch data: {response.status_code}")

def process_csv_data(folder_path, filename):
    # Load the CSV data using pandas
    file_path = pathlib.Path(folder_path).joinpath(filename)
    df = pd.read_csv(file_path)
    
    # Perform basic analysis
    insights = []

    # Example: Data Preview and Summary Statistics
    insights.append("Data Preview:\n")
    insights.append(df.head().to_string())  # Add first few rows

    insights.append("\n\nSummary Statistics:\n")
    insights.append(df.describe().to_string())  # Add summary stats for numeric columns

    # Example: Analyzing specific column (e.g., Happiness Score)
    if 'Happiness Score' in df.columns:
        avg_happiness = df['Happiness Score'].mean()
        insights.append(f"\n\nAverage Happiness Score: {avg_happiness:.2f}")

    # Add more analysis as needed (e.g., top countries by happiness score, correlations, etc.)

    # Save insights to a text file
    save_insights_to_file(folder_path, 'insights.txt', insights)

def save_insights_to_file(folder_path, filename, insights):
    file_path = pathlib.Path(folder_path).joinpath(filename)
    with file_path.open('w', encoding='utf-8') as file:
        file.write("\n".join(insights))
    print(f"Insights saved to {file_path}")

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
        process_json_data(json_data)  # Process the JSON data after saving
    else:
        print(f"Failed to fetch data: {response.status_code}")

def process_json_data(json_data):
    # Extract relevant data and present it in a readable format
    simplified_data = []

    # Example: Extracting information about astronauts in space
    if "people" in json_data:
        simplified_data.append("Astronauts currently in space:\n")
        for person in json_data["people"]:
            name = person.get("name")
            craft = person.get("craft")
            simplified_data.append(f"- {name} aboard {craft}")
    
    # Add additional analysis as needed (e.g., other parts of the JSON)

    # Save the simplified output to a text file
    save_simplified_data_to_file('data-json', 'simplified_data.txt', simplified_data)

def save_simplified_data_to_file(folder_path, filename, data):
    folder_path = pathlib.Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path.joinpath(filename)
    with file_path.open('w', encoding='utf-8') as file:
        file.write("\n".join(data))
    print(f"Simplified data saved to {file_path}")

# Example usage
fetch_and_write_json_data('data-json', 'data.json', 'http://api.open-notify.org/astros.json')