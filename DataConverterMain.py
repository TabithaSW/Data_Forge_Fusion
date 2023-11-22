# GUI library:
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Basic math and file operations libraries:
import numpy as np
import pandas as pd
import os

# Import the read/write functions
import Convert_Funcs


class DataConverterApp:
    # Initialize attributes
    def __init__(self, master) -> None:
        self.master = master

        # GUI Title: 
        self.master.title("Data File Convertor") # Application name

        # GUI Frame for widgets:
        
        self.frame = tk.Frame(self.master, padx = 10, pady = 10, bg = "lightgray")
        self.frame.pack()

        # GUI Label
        self.label = tk.Label(self.frame, text = "Data File Type Converter", font =('Garamond',15),bg="lightblue")
        self.label.pack()

        # GUI Buttons
        self.choose_file_button = tk.Button(master, text = "Choose a File",command = self.choose_file, bg = "lightblue")
        self.choose_file_button.pack(pady = 10, padx = 10)

    
    def choose_file(self):
        # Options for conversion:
        file_options = ["CSV","JSON","XML"]

        # What file does the user want to convert? Prompt user to select a file from their PC.

        file_path = filedialog.askopenfilename(title = "Select File") 
        # print("FILE PATH TEST",file_path)
        
        # Check file type here with detect_file function, function checks type and converts to python dictionary:
        temp_data = Convert_Funcs.detect_file(file_path)
        # print("TEMP DATA TEST",temp_data[0:5])

        # Once we know the current file type, let the user choose a conversion format using prmpt_file_choice func.
        user_choice = Convert_Funcs.prompt_file_choice(file_path=file_path)
        # print("USER CHOICE TEST",user_choice)
        
        if temp_data:
            if user_choice in file_options:
                if user_choice == "CSV":
                    Convert_Funcs.write_csv_file(filename = file_path,data=temp_data)
                elif user_choice == "XML":
                    Convert_Funcs.write_xml_file(filename = file_path,data=temp_data)
                elif user_choice == "JSON":
                    Convert_Funcs.write_json_file(filename = file_path,data=temp_data)
                # If the user picks something other than the three types:
            else:
                warn = messagebox.askokcancel("Not A Valid File Format",icon = "warning")
    

if __name__ == "__main__":
    root = tk.Tk()
    app = DataConverterApp(root)
    root.mainloop()