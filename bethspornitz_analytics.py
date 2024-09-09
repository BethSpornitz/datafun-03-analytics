
''' 
This project focuses on developing proficiency in Git for version control, managing Python virtual environments, and handling various types of data. The project entails retrieving data from the web, processing it with suitable Python collections, and saving the processed data to files. 
 '''
# Standard library imports
import csv
import pathlib
import os
import json
import re
from collections import Counter

# External library imports (requires virtual environment)
import requests
import pandas as pd

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

##############################
# TXT
##############################

# Write data to a text file
def write_txt_file(folder_name, filename, data):
    folder_path = pathlib.Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    file_path = folder_path.joinpath(filename)
    with file_path.open('w', encoding='utf-8') as file:
        file.write(data)
        print(f"Text data saved to {file_path}")

# Fetch data from a text file
def fetch_and_write_txt_data(folder_name, filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        write_txt_file(folder_name, filename, response.text)
        return response.text
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

# Process and analyze text data
def process_txt_file(folder_name, filename, url):
    # Fetch the text data from the URL
    text_data = fetch_and_write_txt_data(folder_name, filename, url)
    
    if text_data:
        # Remove non-alphabetic characters and make lowercase
        clean_text = re.sub(r'[^A-Za-z\s]', '', text_data).lower()

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
        letter_count = sum(1 for char in text_data if char.isalpha())

        # Find the longest words
        longest_words = sorted(set(words), key=len, reverse=True)[:10]

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

        # Append longest words to the analysis
        analysis += "\nTop 10 Longest Words:\n"
        for word in longest_words:
            analysis += f"{word}\n"

        # Save the analysis to a file
        write_txt_file(folder_name, f"analysis_{filename}", analysis)

# Example usage for TXT
#process_txt_file('data-txt', 'data-txt.txt', 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt')



##############################
# Excel
##############################


import pathlib
import requests
import pandas as pd
import matplotlib.pyplot as plt

def write_excel_file(folder_name, filename, data):
    file_path = pathlib.Path(folder_name).joinpath(filename)
    try:
        folder_path = pathlib.Path(folder_name)
        folder_path.mkdir(parents=True, exist_ok=True)
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

def fetch_and_write_excel_file(folder_name, filename, url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        file_path = write_excel_file(folder_name, filename, response.content)
        return file_path
    except requests.RequestException as e:
        print(f"RequestException occurred while fetching data: {e}")
    except ValueError as e:
        print(f"ValueError occurred while processing response content: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching data: {e}")
    finally:
        print("Fetch operation attempted.")
    return None

def save_analysis_results_to_txt(folder_name, filename, analysis):
    folder_path = pathlib.Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path.joinpath(filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(analysis)
        print(f"Analysis results saved to {file_path}")

def process_excel_file(folder_name, filename, url, output_folder='data-excel'):
    # Fetch and write the Excel file
    file_path = fetch_and_write_excel_file(folder_name, filename, url)
    
    if file_path:
        try:
            # Determine the file extension and use the appropriate engine
            file_extension = pathlib.Path(file_path).suffix
            if file_extension == '.xlsx':
                engine = 'openpyxl'
            elif file_extension == '.xls':
                engine = 'xlrd'
            else:
                raise ValueError(f"Unsupported file extension: {file_extension}")
            
            # Load the Excel file into a pandas DataFrame
            df = pd.read_excel(file_path, engine=engine)
            
            # Inspect column names to identify valid columns
            print("\nColumn Names:\n")
            print(df.columns)

            # Create a text analysis report
            analysis = "\nData Preview:\n"
            analysis += df.head().to_string()  # Convert data preview to string
            
            analysis += "\n\nSummary Statistics:\n"
            analysis += df.describe().to_string()  # Convert summary stats to string

            # Check Missing Data
            analysis += "\n\nMissing Data:\n"
            analysis += df.isnull().sum().to_string()

            # Save the text report
            save_analysis_results_to_txt(output_folder, 'excel_analysis.txt', analysis)

            # Create output folder if it does not exist
            pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

            # Example: Plotting a histogram
            if 'c1' in df.columns:  # Ensure 'c1' column exists
                df['c1'].hist()  # Replace 'c1' with the appropriate column
                plt.savefig(f'{output_folder}/histogram.png')  # Save plot as an image
                plt.show()
            else:
                print("Column 'c1' does not exist in the DataFrame.")
        
        except Exception as e:
            print(f"An error occurred while analyzing the Excel data: {e}")
        finally:
            print("Analysis operation attempted.")

# Example usage
#process_excel_file('data-excel', 'data-excel.xls', 'https://github.com/bharathirajatut/sample-excel-dataset/raw/master/cattle.xls')

###########################
# CSV
###########################

def write_csv_file(folder_name, filename, data):
    file_path = pathlib.Path(folder_name).joinpath(filename)
    try:
        folder_path = pathlib.Path(folder_name)
        folder_path.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(data)
            print(f"CSV data saved to {file_path}")
    except IOError as e:
        print(f"IOError occurred while writing file: {e}")
    except OSError as e:
        print(f"OSError occurred while creating directories: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing file: {e}")
    finally:
        print("Write operation attempted.")
    return file_path  # Return the file path for further analysis

def fetch_and_write_csv_file(folder_name, filename, url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        file_path = write_csv_file(folder_name, filename, response.content)
        return file_path
    except requests.RequestException as e:
        print(f"RequestException occurred while fetching data: {e}")
    except ValueError as e:
        print(f"ValueError occurred while processing response content: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching data: {e}")
    finally:
        print("Fetch operation attempted.")
    return None

def save_analysis_results_to_txt(folder_name, filename, analysis):
    folder_path = pathlib.Path(folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path.joinpath(filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(analysis)
        print(f"Analysis results saved to {file_path}")

def process_csv_file(folder_name, filename, url, output_base_folder='data-csv'):
    # Fetch and write the CSV file
    file_path = fetch_and_write_csv_file(folder_name, filename, url)
    
    if file_path:
        try:
            # Load the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)
            
            # Inspect column names to identify valid columns
            print("\nColumn Names:\n")
            print(df.columns)
            
            # Create a unique folder for analysis based on the CSV file name (without extension)
            csv_base_name = pathlib.Path(filename).stem
            unique_output_folder = os.path.join(output_base_folder, csv_base_name)
            
            # Create a text analysis report
            analysis = "\nData Preview:\n"
            analysis += df.head().to_string()  # Convert data preview to string
            
            analysis += "\n\nSummary Statistics:\n"
            analysis += df.describe().to_string()  # Convert summary stats to string

            # Check for missing data
            analysis += "\n\nMissing Data:\n"
            analysis += df.isnull().sum().to_string()

            # Save the text report in the unique folder
            save_analysis_results_to_txt(unique_output_folder, 'csv_analysis.txt', analysis)

            # Create output folder if it does not exist
            pathlib.Path(unique_output_folder).mkdir(parents=True, exist_ok=True)

            # Example: Plotting a histogram for the first numeric column found
            numeric_columns = df.select_dtypes(include=['number']).columns
            if 'c1' in df.columns:
                df['c1'].hist()  # If 'c1' exists, use it
                plt.savefig(f'{unique_output_folder}/histogram.png')
                plt.show()
            elif len(numeric_columns) > 0:
                # If 'c1' doesn't exist, but there are other numeric columns, use the first one
                df[numeric_columns[0]].hist()
                plt.savefig(f'{unique_output_folder}/histogram.png')
                plt.show()
            else:
                print("No numeric columns available for plotting.")
        
        except Exception as e:
            print(f"An error occurred while analyzing the CSV data: {e}")
        finally:
            print("Analysis operation attempted.")

# Example usage
#process_csv_file('data-csv', 'data-csv.csv','https://raw.githubusercontent.com/MainakRepositor/Datasets/master/World%20Happiness%20Data/2020.csv')

################
# JSON
###############

def write_json_file(folder_path, filename, data):
    folder_path = pathlib.Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    file_path = folder_path.joinpath(filename)
    try:
        with file_path.open('w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"JSON data saved to {file_path}")
    except IOError as e:
        print(f"IOError occurred while writing file: {e}")
    except OSError as e:
        print(f"OSError occurred while creating directories: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing file: {e}")
    finally:
        print("Write operation attempted.")
    return file_path  # Return the file path for further analysis

def fetch_and_write_json_data(folder_path, filename, url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        json_data = response.json()  # Parse the JSON response content
        file_path = write_json_file(folder_path, filename, json_data)
        return file_path
    except requests.RequestException as e:
        print(f"RequestException occurred while fetching data: {e}")
    except ValueError as e:
        print(f"ValueError occurred while processing response content: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching data: {e}")
    finally:
        print("Fetch operation attempted.")
    return None

def save_simplified_data_to_file(folder_path, filename, data):
    folder_path = pathlib.Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path.joinpath(filename)
    try:
        with file_path.open('w', encoding='utf-8') as file:
            file.write("\n".join(data))
            print(f"Simplified data saved to {file_path}")
    except IOError as e:
        print(f"IOError occurred while writing file: {e}")
    except OSError as e:
        print(f"OSError occurred while creating directories: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing file: {e}")
    finally:
        print("Save operation attempted.")

def process_json_file(folder_path, filename, url, output_folder='data-json'):
    # Fetch and write the JSON file
    file_path = fetch_and_write_json_data(folder_path, filename, url)
    
    if file_path:
        try:
            # Load the JSON file into a Python dictionary
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            simplified_data = []

            # Example: Extracting information about astronauts in space
            if "people" in json_data:
                simplified_data.append("Astronauts currently in space:\n")
                for person in json_data["people"]:
                    name = person.get("name")
                    craft = person.get("craft")
                    simplified_data.append(f"- {name} aboard {craft}")

            # Example: Count the number of astronauts
            num_astronauts = len(json_data.get("people", []))
            simplified_data.append(f"\nTotal number of astronauts in space: {num_astronauts}")

            # Save the simplified output to a text file
            save_simplified_data_to_file(output_folder, 'simplified_data.txt', simplified_data)
        
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
        except Exception as e:
            print(f"An error occurred while processing the JSON data: {e}")
        finally:
            print("Analysis operation attempted.")

# Example usage
#process_json_file('data-json', 'data.json', 'http://api.open-notify.org/astros.json')


##############################
# Main function
##############################

def main():
     '''Main function to demonstrate module capabilities.''' 

    # URLs for data
txt_url = 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt'
csv_url = 'https://raw.githubusercontent.com/MainakRepositor/Datasets/master/World%20Happiness%20Data/2020.csv'
excel_url = 'https://github.com/bharathirajatut/sample-excel-dataset/raw/master/cattle.xls'
json_url = 'http://api.open-notify.org/astros.json'
princess_bride_url = 'https://www.evenmere.org/~bts/Random-Collected-Documents/princess_bride.html'
covid_url = 'https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv'

    # Folder names and filenames for data
txt_folder_name = 'data-txt'
csv_folder_name = 'data-csv'
excel_folder_name = 'data-excel'
json_folder_name = 'data-json'
princess_bride_folder_name = 'princess_bride-txt'
covid_folder_name = 'covid-csv'

txt_filename = 'data.txt'
csv_filename = 'data.csv'
excel_filename = 'data.xls'
json_filename = 'data.json'
princess_bride_filename = 'princess_bride.txt'
covid_filename = 'covid.csv'

# Process and analyze data
process_txt_file(txt_folder_name, txt_filename, txt_url)
process_csv_file(csv_folder_name, csv_filename, csv_url)
process_excel_file(excel_folder_name, excel_filename, excel_url)
process_json_file(json_folder_name,'data.json', json_url)
process_txt_file(princess_bride_folder_name, princess_bride_filename, princess_bride_url)
process_csv_file(covid_folder_name, covid_filename, covid_url)

#####################################
# Conditional Execution
#####################################

if __name__ == '__main__':
    main()