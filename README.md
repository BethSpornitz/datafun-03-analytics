# Working with Data

## Overview

Project 3 focuses on developing proficiency in Git for version control, managing Python virtual environments, and handling various types of data. The project entails retrieving data from the web, processing it with suitable Python collections, and saving the processed data to files.

## Features

- Retrieving data from the web
- Handling different data types
- Save extracted data to data files including CSV or JSON files

## Installation

Requires installation of:  
requests  
pandas  
matplotlib  
openpyxl  
xlrd

## Clone the Repository

git clone https://github.com/BethSpornitz/datafun-03-analytics

## Usage

The project contains functions to process various file types and save both the data and analysis results.

Individual Functions
Each file type (TXT, CSV, Excel, JSON) is processed with dedicated functions:

process_txt_file(): Fetches, cleans, and analyzes text data.  
process_csv_file(): Retrieves CSV data, analyzes numeric columns, and generates histograms.  
process_excel_file(): Fetches Excel files, processes numeric columns, and provides summary statistics.  
process_json_file(): Fetches and processes JSON data.

## Create Project Virtual Environment

On Windows, create a project virtual environment in the .venv folder.

```shell

py -m venv .venv
.venv\Scripts\Activate
py -m pip install -r requirements.txt

```

## Git add and commit

```shell
git add .
git commit -m "add .gitignore, cmds to readme"
git push origin main
```
