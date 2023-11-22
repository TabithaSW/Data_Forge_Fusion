
import Convert_Funcs
# basic data manipulation libraries
import pandas as pd
import numpy as np

# File conversion libraries:
import xml.etree.ElementTree as ET
import json
import csv
import operator
import os

#GUI Stuff
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


# Writes to a JSON File Format
def write_json_file(filename, data):
    """
    Writes JSON files. Similar to write_csv_file.
    """
    with open(filename, 'w') as file:
        json_new = json.dumps(data)
        file.write(json_new)


# Reads in a CSV File
def read_csv_file(filename):
    # Dictionary Object to store data:
    data = []
    # Open CSV File:
    with open(filename, 'r') as file:
        # Pull data from CSV:
        reader = csv.DictReader(file)
        # Loop through file records,
        for row in reader:
            data.append(row)
    return data

        
file_path = filedialog.askopenfilename(title = "Select File") 
test = Convert_Funcs.detect_file(file_path)
print(test)
temp = read_csv_file('crime.csv')
print(temp[0:5])
#write_json_file(temp)