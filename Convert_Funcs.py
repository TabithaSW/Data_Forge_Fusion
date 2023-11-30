
# basic data manipulation libraries
import pandas as pd
import numpy as np
import teradatasql

# File conversion libraries:
import xml.etree.ElementTree as ET
import json
import csv
import operator
import os

#GUI Stuff
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

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

# Writes to a CSV File Format
def write_csv_file(filename, data):
    """
    Takes a filename (to be writen to) and a data object 
    (created by one of the read_*_file functions). 
    Writes the data in the CSV format.
    """
    filename = None
    if not filename:
        filename = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV File",".csv")])
    # Generate instance of new file to write:
    with open(filename, "w", newline="") as outfile:
        # Pass CSV file and dictionary keys as column headers:
        writer = csv.DictWriter(outfile, fieldnames=data[0].keys())

        writer.writeheader()

        for entry in data:
            writer.writerow(entry)

# Reads in a JSON File
def read_json_file(filename):
    """
    Similar to read_csv_file, except works for JSON files.
    """
    with open(filename) as json_file:
        data = json.load(json_file)
    return [data]

# Writes to a JSON File Format
def write_json_file(filename, data):
    """
    Writes JSON files. Similar to write_csv_file.
    """
    filename = None
    if not filename:
        filename = filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("JSON File",".json")])
    with open(filename, 'w') as file:
        json_new = json.dumps(data)
        file.write(json_new)

# Reads an XML file
def read_xml_file(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data_list = []
    for record in root:
        record_dict = {}
        for column in record:
            record_dict.update({column.tag: column.text})
        data_list.append(record_dict)
    return data_list

# Writes to an XML File:
def write_xml_file(filename,data_list):
    filename = None
    if not filename:
        filename = filedialog.asksaveasfilename(defaultextension=".xml",filetypes=[("XML File",".xml")])

    # there should be a single "data" node,
    root = ET.Element("data")
    for record in data_list:
        # with as many record nodes as needed
        record_node = ET.SubElement(root, "record")
        for column, value in record.items():
            # in each record is column node with text content for that record
            column_node = ET.SubElement(record_node, column)
            column_node.text = value
    tree = ET.ElementTree(root)
    tree.write(filename)

def detect_file(file_path):
        # When user is prompted to choose a file, we need to ensure it is correctly identified before conversion.
        x, file_extension = os.path.splitext(file_path.lower()) # X is root, rest is the extension, x is throwaway var.

        if file_extension == ".csv":
            return read_csv_file(file_path)
        elif file_extension == ".xml":
            return read_xml_file(file_path)
        elif file_extension == ".xlsx":
            return read_excel_file(file_path)
        else:
            return read_json_file(file_path)
        
def prompt_file_choice(file_path):
        file_options = ["CSV", "JSON", "XML","csv","json","xml","excel","EXCEL"]
        file_name = os.path.basename(file_path)
        user_choice = simpledialog.askstring(f"{file_name} Conversion Options","CSV, JSON, EXCEL, or XML?",initialvalue=file_options[0])
        if user_choice.lower() in [option.lower() for option in file_options]:
            return user_choice
        else:
            messagebox.showwarning("Conversion Cancelled")

# NEW FORMAT, EXCEL (simplified using pandas func):
def write_to_excel(filename, datalist):
    filename = os.path.basename(filename)
    custom_name = filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel File",".xlsx")])
    # Convert to DF using pandas from pythion dict
    df = pd.DataFrame(data = datalist,index = [0])
    df = (df.T) # Transform
    df.to_excel(excel_writer=custom_name,sheet_name=filename)

def read_excel_file(filename):
    extract = pd.read_excel(filename)
    data = extract.to_dict()
    return data 

# Lets do some DBMS stuff that made go hand in hand with file conversion.
# Teradata to start:
def convert_teradata(server, username, password, query,output_path = None):
    #allow user to enter query
    try:
        # assign connection object
        with teradatasql.connect(host = server, user=username,password=password) as conn:
            # cursor to execute queries
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall() # store query results
        # lets convert this file format first,
        csv_filename = "Teradata_Result.csv"
        if output_path:
            csv_filename = os.path.join(output_path, csv_filename)
        with open(csv_filename,'w',newline='') as f:
            csv_write = csv.writer(f)
            # if header:
            if cur.description:
                csv_write.writerow([col[0] for col in cur.description])
            # complete write 
            csv_write.writerows(result)
        return csv_filename
    # if user enters illegible query, produce error by teradata.
    except teradatasql.Error as error_:
        return f"Error: {error_}"



