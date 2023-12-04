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

#GUI Stuff
# GUI library:
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import tkinter.scrolledtext as tkst

def write_excel_file(datalist,filepath):
    # allow users to choose filename
    filename = os.path.basename(filepath)
    custom_name = filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel File",".xlsx")])

    # create excel template workbook
    workbook = openpyxl.Workbook()

    # headers 
    headers = list(datalist[0].keys())
    sheet.append(headers)

    for dict_ in datalist:
        sheet.append([dict_[header] forheader in headers])
    workbook.save(custom_name)

# NEW FORMAT, EXCEL (simplified using pandas func):
def write_to_excel(filename, datalist):
    filename = os.path.basename(filename)
    custom_name = filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel File",".xlsx")])
    # Convert to DF using pandas from pythion dict
    df = pd.DataFrame(data = datalist)
    df = (df.T) # Transform
    df.to_excel(excel_writer=custom_name,sheet_name=filename)