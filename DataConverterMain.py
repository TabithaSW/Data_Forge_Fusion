# GUI library:
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import tkinter.scrolledtext as tkst
import teradatasql

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
        
        self.frame = tk.Frame(
            self.master,
            padx = 10,
            pady = 10,
            bg = "#FFE4CF", #Bisque
            relief=tk.RIDGE,#border style
            bd=5, # borderwidth
            )
        self.frame.pack(expand=True, fill="both")

        # GUI Label
        self.label = tk.Label(
            self.frame, 
            text = "File Type Convertor",
            font =('Garamond',20, "bold"),
            # bg="lightblue",
            fg = "#2E8B57", # SeaGreen
            )
        self.label.pack(pady=10)

        # We can make an image label with logo as well:
        # photo = tk.PhotoImage(file=' ')

        # GUI Buttons
        self.choose_file_button = tk.Button(
            self.frame,
            text="Choose File(s)",
            command=self.choose_files,
            bg="lightblue",
            fg = "#2E8B57", #seagreen
            font =('Garamond',12, "bold"),
            pady = 5,
            padx = 10,
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.choose_file_button.pack(padx=5)

        # GUI Loading bar
        self.progress = ttk.Progressbar(
            self.frame,
            length=200,
            mode="determinate",
            style="TProgressbar"
            )
        self.progress.pack(pady=5,padx = 5)

        # File information labels
        self.file_info_label = tk.Label(
            self.frame,
            bg = "#FFE4CF",
            text = " "
            )
        self.file_info_label.pack(side=tk.BOTTOM, expand=True)

        # Teradata button:
        self.connect_to_tera_button = tk.Button(
            self.frame,
            text = "Connect to Teradata",
            command= self.connect_to_tera
        )
        self.connect_to_tera_button.pack(side=tk.BOTTOM,expand=True,padx=10,pady=10)

    def choose_files(self):
        # Options for conversion:
        file_options = ["CSV", "JSON", "XML","csv","json","xml","excel","EXCEL"]

        # Temporary file name until user downloads coverted file and choose new name:
        new_file_name = "Converted_File"


        # What file does the user want to convert? Prompt the user to select a file from their PC.
        file_path = filedialog.askopenfilenames(title="Select File") # need to change to allow multiple files.

        # tuple to list format
        file_path = list(file_path)

        if file_path:
            # for each file in the chosen
            for i in file_path:

                # Check file type here with detect_file function, function checks type and converts to python dictionary:
                temp_data = Convert_Funcs.detect_file(i)

                # Once we know the current file type, let the user choose a conversion format using prompt_file_choice func.
                user_choice = Convert_Funcs.prompt_file_choice(file_path=i)
                self.show_file_info(i, user_choice) # display files chosen

                # if the data was processed correctly (into py dict) then we check what the user requested, despite upper or lower case for file type:
                if temp_data and user_choice.lower() in file_options:
                    
                    if user_choice.lower() == "csv":
                        self.show_loading_bar()
                        Convert_Funcs.write_csv_file(filename=new_file_name, data=temp_data)
                    elif user_choice.lower() == "xml":
                        self.show_loading_bar()
                        Convert_Funcs.write_xml_file(filename=new_file_name, data_list=temp_data)
                    elif user_choice.lower() == "json":
                        self.show_loading_bar()
                        Convert_Funcs.write_json_file(filename=new_file_name, data=temp_data)
                    elif user_choice.lower() == "excel":
                        self.show_loading_bar()
                        Convert_Funcs.write_to_excel(filename=new_file_name,datalist=temp_data)

                    # Complete loading bar
                    self.hide_loading_bar()

                # If the user picks something other than the three types initially:
                else:
                    warn = messagebox.askokcancel("No Valid File Format", icon="warning")
             # Does the user have more files they want to convert?
            response = messagebox.askyesno("Conversion Complete", "Conversion complete! Do you want to convert another file?")
            if not response:
                self.master.destroy()  # Close the application if the user chooses not to convert another file
        else:
            print("No file selected.")

    
    # Loading bar for when file conversions will complete, new addition.
    def show_loading_bar(self):
        self.progress["value"] = 0
        self.progress.start(10)  # Adjust the speed of the progress bar by changing the value passed to start

    def hide_loading_bar(self):
        self.progress.stop()
        self.progress["value"] = 100

    # Teradata connection abilities:
    def connect_to_tera(self):
        # connection details by user
        server = simpledialog.askstring("Teradata Connect","Enter Server:")
        username = simpledialog.askstring("Teradata Connect","Enter Username:")
        password = simpledialog.askstring("Teradata Connect","Enter Password:")
        output_file_path = simpledialog.askstring("Teradata Connect","OPTIONAL - Enter Output Path for File Save Location:")
        # query they want to pull
        user_query = simpledialog.askstring("SQL","Enter your Teradata Query in SQL Format:")
        # if uery entered,
        if user_query:
            #call the connection func in conert_funcs:
            query_res = Convert_Funcs.convert_teradata(username=username,server=server,password=password,query=user_query,output_path=output_file_path)
            self.show_file_info(query_res,"CSV")
            return query_res



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

