
# basic data manipulation libraries
import pandas as pd
import numpy as np
import teradatasql

# File conversion libraries:
import xml.etree.ElementTree as ET
import json
import csv
import openpyxl
import operator
import os
import dask.dataframe as dd

#GUI Stuff
# GUI library:
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import tkinter.scrolledtext as tkst

# Need some small funcs from main py
import DataConverterMain

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
        #print("FILE PATH TES:",file_path)
        # When user is prompted to choose a file, we need to ensure it is correctly identified before conversion.
        x, file_extension = os.path.splitext(file_path) # X is root, rest is the extension, x is throwaway var.

        #print(file_extension,"FILE EX TEST")

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

# NEW FORMAT, EXCEL:
def write_excel_file(datalist,filepath):
    # allow users to choose filename
    filename = os.path.basename(filepath)
    custom_name = filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel File",".xlsx")])

    # create excel template workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    
    # headers 
    headers = list(datalist[0].keys())
    sheet.append(headers)

    for dict_ in datalist:
        sheet.append([dict_[header] for header in headers])
    workbook.save(custom_name)

# changed to using openpyxl because of pandas limit
def read_excel_file(file_path):
    # excel files are workbooks compirsed of individual sheets of data
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]

    datalist = [] #all my read funcs convert to a python list of dictionaries.
    # start at second row, pass header.
    for row in sheet.iter_rows(min_row = 2, values_only = True):
        row_dict = dict(zip(headers,row)) # need to zip headers if multiple sheets
        datalist.append(row_dict)
    return datalist

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
                cols = [col[0] for col in cur.description]
                result = cur.fetchall() # store query results

        display_teradata_preview(query_result=result,headers=cols)

        # lets convert this file format first,
        csv_filename = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV File",".csv")])
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

# Teradata preview:
def display_teradata_preview(query_result,headers=None):
    # preview window
    df_prev = pd.DataFrame(query_result)

    prev_window = tk.Toplevel()
    prev_window.title("Result Preview")
    prev_window.geometry("500x500")

    frame = ttk.Frame(prev_window)
    frame.pack(expand=True,fill="both")

    tree = ttk.Treeview(frame, show ="headings")
    tree["columns"] = list(df_prev.columns)

    for col in df_prev.columns:
        tree.column(col, anchor = "w")
        tree.heading(col, text = col, anchor = "w")

    scrollb = ttk.Scrollbar(frame, orient = "vertical", command = tree.yview)
    scrollb.pack(side = "right", fill = "y")

    horiz_scroll = ttk.Scrollbar(frame, orient = "horizontal", command = tree.xview)
    horiz_scroll.pack(side = "bottom",fill = "x")

    tree.configure(yscrollcommand = scrollb.set)
    tree.configure(xscrollcommand = horiz_scroll.set)

    for i, (data, row) in enumerate(df_prev.iterrows()): # for each row of data
        if i >= 1000: # preview ends at 1000 rows
            break
        tree.insert("",data,values=list(row)) #insert into the widget, creates new row in widget each iter

    tree.pack(expand=True,fill = "both")

    close_b = tk.Button(prev_window, text = "Close Preview",command = prev_window.destroy)
    close_b.pack(side = "bottom",pady=10)
    return

# joining files together and converting func
def file_merge(data1,data2):
    # pandas take the already converted files and put into df format 
    df1 = dd.from_pandas(pd.DataFrame(data1), npartitions=1)
    df2 = dd.from_pandas(pd.DataFrame(data2), npartitions=1)

    print("DATAFRAME TEST",df1)

    # merge files
    merge_dfs = dd.merge(df1,df2,how="left",on=list(set(df1.columns) & set(df2.columns)))

    # let user choose format and name post merge
    output_type = simpledialog.askstring("Output File Type","Choose Output File Type (CSV, JSON, XML, EXCEL):")
    name = filedialog.asksaveasfilename(defaultextension=f".{output_type.lower()}",
                                        filetypes=[(f"{output_type} File",f".{output_type.lower()}")])
    
    # check file type to compute the change from the merged filetye
    # can use my write funcs with this merge df from dask, need to use dask funcs
    if output_type.lower() == "csv":
        merge_dfs.compute().to_csv(name,index = False)
    elif output_type.lower() == "xml":
        merge_dfs.compute().to_xml(name,index = False)
    elif output_type.lower() == "json":
        merge_dfs.compute().to_json(name,orient = 'records',lines = True) # same to json as my own func result
    elif output_type.lower() == "excel":
        merge_dfs.compute().to_excel(name,index = False)
    else:
        warn = messagebox.askokcancel("No Valid File Format", icon="warning")
    return name
