# GUI library:
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import tkinter.scrolledtext as tkst

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
        self.master.title("File Convertor") # Application name

        # GUI Frame for widgets:
        
        self.frame = tk.Frame(self.master, padx = 10, pady = 10, bg = "lightgray",relief=tk.RAISED,bd=5)
        self.frame.pack(expand=True, fill="both")

        # GUI Label
        self.label = tk.Label(self.frame, text = "File Type Conversion", font =('Garamond',15),bg="lightblue")
        self.label.pack()

        # GUI Buttons
        self.choose_file_button = tk.Button(master, text="Choose File(s)", command=self.choose_files, bg="lightblue")
        self.choose_file_button.pack(pady=10, padx=10)

        # NEW ADDITION: Loading bar
        self.progress = ttk.Progressbar(self.frame, length=100, mode="determinate")
        self.progress.pack(pady=10)

        # NEW ADDITION: File information labels
        self.file_info_label = tk.Label(self.frame, text="", bg="lightgray")
        self.file_info_label.pack()

        # New addition
    
    def choose_files(self):
        # Options for conversion:
        file_options = ["CSV", "JSON", "XML","csv","json","xml"]
        # New file name:
        new_file_name = "Converted_File"

        # What file does the user want to convert? Prompt the user to select a file from their PC.
        file_path = filedialog.askopenfilename(title="Select File") # need to change to allow multiple files.

        if file_path:
            print("FILE PATH TEST", file_path)

            # Check file type here with detect_file function, function checks type and converts to python dictionary:
            temp_data = Convert_Funcs.detect_file(file_path)
            print("TEMP DATA TEST", temp_data)

            # Once we know the current file type, let the user choose a conversion format using prompt_file_choice func.
            user_choice = Convert_Funcs.prompt_file_choice(file_path=file_path)
            print("USER CHOICE TEST", user_choice)

            # if the data was processed correctly (into py dict) then we check what the user requested, despite upper or lower case for file type:
            if temp_data and user_choice.lower() in file_options:
                self.show_loading_bar()
                if user_choice.lower() == "csv":
                    Convert_Funcs.write_csv_file(filename=new_file_name, data=temp_data)
                elif user_choice.lower() == "xml":
                    Convert_Funcs.write_xml_file(filename=new_file_name, data_list=temp_data)
                elif user_choice.lower() == "json":
                    Convert_Funcs.write_json_file(filename=new_file_name, data=temp_data)

                # Complete loading bar and display file info.
                self.hide_loading_bar()
                self.show_file_info(file_path, user_choice)

                # Does the user have more files they want to convert?
                response = messagebox.askyesno("Conversion Complete", "Conversion complete! Do you want to convert another file?")
                if not response:
                    self.master.destroy()  # Close the application if the user chooses not to convert another file

            # If the user picks something other than the three types initially:
            else:
                warn = messagebox.askokcancel("Not A Valid File Format", icon="warning")
        else:
            print("No file selected.")

    
    # Loading bar for when file conversions will complete, new addition.
    def show_loading_bar(self):
        self.progress["value"] = 0
        self.progress.start(10)  # Adjust the speed of the progress bar by changing the value passed to start

    def hide_loading_bar(self):
        self.progress.stop()
        self.progress["value"] = 100


    # Allow users to double check the file they selected by viewing it'sname and type.
    def show_file_info(self, file_path, user_choice):
        #Take the current file name and whatever the user chooses to convert it to and display it under the progress bar.
        file_name = os.path.basename(file_path)
        self.file_info_label.config(text=f"Selected File: {file_name}\nConversion Type: {user_choice}", font=('Garamond', 12), bg="lightgray")
    

if __name__ == "__main__":
    root = tk.Tk()

    # Set the initial size of the main window
    root.geometry("400x300")  # Adjust the size as needed

    # Allow resizing both horizontally and vertically
    root.resizable(True, True)

    app = DataConverterApp(root)
    root.mainloop()


# TO BE ADDED:
# User options for file name.
# Batch processing, multiple files at once.
# File preview of before and after.
# Logging and error handling.
# Possible file customizations.
# File comparison highlight.
# Exporting the file elsewhere.
# Downloading multiple copies.
# File compression.
# Support for other formats.
