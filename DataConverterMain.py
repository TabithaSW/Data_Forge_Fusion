# GUI library:
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import tkinter.scrolledtext as tkst
import teradatasql

# Basic math and file operations libraries:
import numpy as np
import pandas as pd
import os

#plots
import matplotlib.pyplot as plt
import seaborn as sns

# Import the read/write functions
import Convert_Funcs

# duplication check libraries
import json
import csv

# bug report packages
import webbrowser


class DataConverterApp:
    # Initialize attributes
    def __init__(self, master) -> None:
        self.master = master

        # GUI Title: 
        self.master.title("Data Foundry - Forge Analytics") # Application name

        # Load the logo image
        self.logo_image = tk.PhotoImage(file="Forge.png")  # Ensure 'logo.png' is the correct path
        # Resize the logo image (adjust the subsample values as needed to fit your GUI)
        self.logo_image = self.logo_image.subsample(4, 4)  # Example: subsample to 1/3 of the original size

        # Display the logo - adjust 'side' to tk.LEFT for top left positioning
        self.logo_label = tk.Label(self.master, image=self.logo_image)
        self.logo_label.pack(side=tk.LEFT, pady=10, padx=10, anchor='ne')

        # Display the logo text below the logo image
        #self.logo_text = tk.Label(self.master, text="File Types: CSV, EXCEL, PARQUET, JSON, XML")
        #self.logo_text.pack(side=tk.LEFT, pady=10, padx=10, anchor='ne')


        # design changes for tabs and app
        # Create an instance of ttk style
        s = ttk.Style()
        s.theme_use('default')
        s.configure('TNotebook.Tab', background="#7A7585")
        s.map("TNotebook", background= [("selected", "#7D99AD")])

        # lets make this tabular, new design:
        MainTabs = ttk.Notebook(self.master)

        self.progress = ttk.Progressbar(
            self.master,
            length=450,
            mode="determinate",
            style="TProgressbar"
            )
        self.progress.pack(side = tk.TOP,pady=5,padx = 5)

        Conversion_Tasks = ttk.Frame(MainTabs) 
        self.conversion_tab = Conversion_Tasks
        Analytic_Tasks = ttk.Frame(MainTabs)
        self.analysis_tab = Analytic_Tasks
        Connections = ttk.Frame(MainTabs)
        self.connect_tab = Connections
        Report_Settings = ttk.Frame(MainTabs)
        self.report_tab = Report_Settings

        MainTabs.add(Conversion_Tasks, text ='Conversion') 
        MainTabs.add(Analytic_Tasks, text ='Analytic Options') 
        MainTabs.add(Connections, text ='Connections') 
        MainTabs.add(Report_Settings, text ='Settings & Reports') 
        MainTabs.pack(expand = 1, fill ="both")      


        # Style the buttons:
        button_style = {'font': ('Helvetica', 10), 'pady': 3, 'padx': 5}  

        # Bug Report Form button
        self.Bug_Report_Form = tk.Button(
            self.report_tab,
            text = "Report a Bug",
            command= self.open_bug_report_form,
            **button_style,
            cursor="hand2" # allows diff cursor over button, user knows to click
        )
        self.Bug_Report_Form.pack(side=tk.TOP, anchor='w', padx=10, pady=5)

        # plot_analysis for creating custom plots from your data!
        self.Plot_Tool = tk.Button(
            self.analysis_tab,
            text = "Custom Plot Creation",
            command= self.plot_analysis,
            **button_style,
            cursor="hand2" # allows diff cursor over button, user knows to click
        )
        self.Plot_Tool.pack(side=tk.TOP, anchor='w', padx=10, pady=5)

        # Data summary label
        self.summary_label1 = tk.Label(
            self.conversion_tab,
            text = "",
            bg= 'lightgrey',
            font =('Helvetica', 10)
            )
        self.summary_label1.pack(side=tk.BOTTOM, expand=True)

        # Data summary label for other tab
        self.summary_label = tk.Label(
            self.analysis_tab,
            bg= 'lightgrey',
            text = "",
            font =('Helvetica', 10)
            )
        self.summary_label.pack(side=tk.BOTTOM, expand=True)

        # file merge button
        self.left_merge = tk.Button(
            self.analysis_tab,
            text="Merge & Convert Files(s)",
            command=self.left_join,
            #bg="lightblue",
            # fg = "#2E8B57", #seagreen
            **button_style,  # Apply the common button style
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.left_merge.pack(side=tk.TOP, anchor='w', padx=10, pady=5)

         # Duplicate Detection button (NEW)
        self.duplicate_detection_btn = tk.Button(
            self.analysis_tab,
            text="Duplicate Detection",
            command=self.duplicate_detection,
            **button_style,  # Apply the common button style
            cursor="hand2"  # allows different cursor over button, user knows to click
        )
        self.duplicate_detection_btn.pack(side=tk.TOP, anchor='w', padx=10, pady=5)

        # Teradata button:
        self.connect_to_tera_button = tk.Button(
            self.connect_tab,
            text = "Connect to Teradata",
            command= self.connect_to_tera,
            **button_style,  # Apply the common button style
            cursor="hand2" # allows diff cursor over button, user knows to click
        )
        self.connect_to_tera_button.pack(side=tk.TOP, anchor='w', padx=10, pady=5)


        # Choose and convert button
        self.choose_file_button = tk.Button(
            self.conversion_tab,
            text="Choose File(s) for Conversion",
            command=self.choose_files,
            #bg="lightblue",
            **button_style,  # Apply the common button style
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.choose_file_button.pack(side=tk.TOP, anchor='w', padx=10, pady=5)

        # Compress file
        self.compress_file_btn = tk.Button(
            self.conversion_tab,
            text="Compress File",
            command=self.compress,
            #bg="lightblue",
            **button_style,  # Apply the common button style
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.compress_file_btn.pack(side=tk.TOP, anchor='w', padx=10, pady=5)

        # file preview button
        self.preview_file_new = tk.Button(
            self.conversion_tab,
            text="Preview & Summary of Files(s)",
            command=self.file_preview,
            #bg="lightblue",
            **button_style,  # Apply the common button style
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.preview_file_new.pack(side=tk.TOP, anchor='w', padx=10, pady=5)

        # 2nd file preview button
        self.preview_file_new = tk.Button(
            self.analysis_tab,
            text="Preview & Summary of Files(s)",
            command=self.file_preview,
            #bg="lightblue",
            **button_style,  # Apply the common button style
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.preview_file_new.pack(side=tk.TOP, anchor='w', padx=10, pady=5)


        # File information labels
        self.file_info_label = tk.Label(
            self.conversion_tab,
            text = " ",
            bg= 'lightgrey',
            font =('Helvetica', 10)
            )
        self.file_info_label.pack(side=tk.BOTTOM, expand=True)

        # 2nd File information labels secondary tab version
        self.file_info_label1 = tk.Label(
            self.analysis_tab,
            bg= 'lightgrey',
            text = " ",
            font =('Helvetica', 10)
            )
        self.file_info_label1.pack(side=tk.BOTTOM, expand=True)

    
        # end progress bar
        # Repack progress bar at the end or at the desired location
        self.progress.pack_forget()  # Remove the current packing
        self.progress.pack(side=tk.LEFT, pady=3, padx=3)
        

    def choose_files(self):
        # Options for conversion:
        file_options = ["CSV", "JSON", "XML","csv","json","xml","excel","EXCEL","PARQUET","parquet"]

        # Temporary file name until user downloads coverted file and choose new name:
        new_file_name = "Converted_File"


        # What file does the user want to convert? Prompt the user to select a file from their PC.
        file_path = filedialog.askopenfilenames(title="Select File",filetypes=(("CSV","*.csv"),("JSON",'*.json'),
                                                                               ("XML","*.xml"),("Excel","*.xlsx"),
                                                                               ("Parquet File", ".parquet"))) 

        # tuple to list format
        file_path = list(file_path)

        if file_path:
            # for each file in the chosen
            for i in file_path:

                # Check file type here with detect_file function, function checks type and converts to python dictionary:
                temp_data = Convert_Funcs.detect_file(i)


                """
                # Need to fix:
                update summary label
                self.summary_data(temp_data)
                messagebox.showinfo(title="File Summary",message="File Summary Content Appears In Main Window")
                
                
                """
                

                # Once we know the current file type, let the user choose a conversion format using prompt_file_choice func.
                user_choice = Convert_Funcs.prompt_file_choice(file_path=i)
                self.show_file_info(i, user_choice) # display files chosen

                # if the data was processed correctly (into py dict) then we check what the user requested, despite upper or lower case for file type:
                if temp_data and user_choice.lower() in file_options:

                    # display data preview:
                    df_preview = pd.DataFrame(temp_data) # all my read functions convert to py dict first prior to file change.

                    # TRTYING TO IMPLEMENT COLUMN SORT:

                    # Create a dictionary to keep track of the sorting order for each column
                    sort_orders = {col: "ascending" for col in df_preview.columns}

                    def toggle_sort(column):
                        # Access sort_orders with nonlocal keyword to modify it within this nested function
                        nonlocal sort_orders

                        # Determine the next sorting order
                        next_order = "descending" if sort_orders[column] == "ascending" else "ascending"
                        
                        # Sort the DataFrame based on the column and order
                        sorted_df = df_preview.sort_values(by=column, ascending=(next_order == "ascending"))
                        
                        # Update the Treeview with sorted data
                        for row in prev_widget.get_children():
                            prev_widget.delete(row)
                        for index, row in sorted_df.iterrows():
                            prev_widget.insert("", tk.END, values=list(row))
                        
                        # Update the sorting order for the next click
                        sort_orders[column] = next_order




                    # create new tkinter window for preview:
                    prev_window = tk.Toplevel(self.master)
                    prev_window.title("File Content Preview as DataFrame")
                    prev_window.geometry("500x500")

                    # decided to add scrollbar so we're going from frame to widget (tree) first
                    frame_2 = ttk.Frame(prev_window)
                    frame_2.pack(expand=True,fill="both")

                    #create widget for top level window (widget is a pandas df preiew)
                    prev_widget = ttk.Treeview(frame_2,show="headings") #treeview allows hierarchical collection of items, like a table.
                    prev_widget["columns"] = list(df_preview.columns) # each col in df = 1 col in widget treeview


                    # Configure the columns and headings in the Treeview, and assign the sorting function to the heading command
                    for col in df_preview.columns:
                        col_str = str(col)  # Convert column name to string to prevent errors with non-string types
                        prev_widget.column(col_str, anchor="w")
                        prev_widget.heading(col_str, text=col_str.capitalize(), anchor="w",
                                            command=lambda c=col_str: toggle_sort(c))
                        
                    """
                    Old code:
                    for col in df_preview.columns:
                        prev_widget.column(col, anchor="w")
                        prev_widget.heading(col, text=col.capitalize(), anchor="w",
                                            command=lambda c=col: toggle_sort(c))
                    """

                    # create scrollbar instance
                    my_scroll = ttk.Scrollbar(frame_2,orient="vertical",command=prev_widget.yview )
                    my_scroll.pack(side="right",fill="y")

                    horiz_scroll = ttk.Scrollbar(frame_2, orient = "horizontal", command = prev_widget.xview)
                    horiz_scroll.pack(side = "bottom",fill = "x")

                    prev_widget.configure(yscrollcommand=my_scroll.set)
                    prev_widget.configure(xscrollcommand = horiz_scroll.set)
                    

                    # Insert to widget
                    # Insert the initial unsorted data into the Treeview
                    for i, row in df_preview.iterrows():
                        if i >= 1000:  # Limit to 1000 rows
                            break
                        prev_widget.insert("", "end", values=list(row)) 
                    #insert into the widget, creates new row in widget each iter

                    # display widget
                    prev_widget.pack(expand=True,fill="both")

                    # allow user to close out the preview
                    close_widg = tk.Button(prev_widget, text="Close Data Preview",command=prev_window.destroy)
                    close_widg.pack(side="bottom",pady=10) 

                    
                    if user_choice.lower() == "csv":
                        self.show_loading_bar()
                        Convert_Funcs.write_csv_file(data=temp_data)

                    elif user_choice.lower() == "xml":
                        self.show_loading_bar()
                        Convert_Funcs.write_xml_file(data_list=temp_data)

                    elif user_choice.lower() == "json":
                        self.show_loading_bar()
                        Convert_Funcs.write_json_file(data=temp_data)

                    elif user_choice.lower() == "excel":
                        self.show_loading_bar()
                        Convert_Funcs.write_excel_file(datalist=temp_data)
                    
                    elif user_choice.lower() == "parquet":
                        self.show_loading_bar()
                        Convert_Funcs.write_parquet_file(data=temp_data)

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
    
    def left_join(self):
        # What files does the user want to join
        file_path = filedialog.askopenfilenames(title="Select File",filetypes=(("CSV","*.csv"),("JSON",'*.json'),
                                                                               ("XML","*.xml"),("Excel","*.xlsx"),
                                                                               ("Parquet File", ".parquet")))

        # tuple to list format
        file_path = list(file_path)

        # convert both to python dict
        data1 = Convert_Funcs.detect_file(file_path[0])
        data2 = Convert_Funcs.detect_file(file_path[1])

        Convert_Funcs.file_merge(data1,data2)

        return
    
    # Loading bar for when file conversions will complete, new addition.
    def show_loading_bar(self):
        self.progress["value"] = 0
        self.progress.start(10)  # Adjust the speed of the progress bar by changing the value passed to start

    def hide_loading_bar(self):
        self.progress.stop()
        self.progress["value"] = 100

    def sort_by_column(self, col, reverse):
        """Sort treeview content by given column."""
        l = [(self.prev_widget.set(k, col), k) for k in self.prev_widget.get_children('')]
        l.sort(reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.prev_widget.move(k, '', index)

        # Reverse sort next time
        self.sort_order[col] = "descending" if self.sort_order[col] == "ascending" else "ascending"


    # adding file preview, no conversion required:
    def file_preview(self):
        # What file does the user want to convert? Prompt the user to select a file from their PC.
        file_path = filedialog.askopenfilenames(title="Select Single File for Preview",filetypes=(("CSV","*.csv"),("JSON",'*.json'),
                                                                               ("XML","*.xml"),("Excel","*.xlsx"),("Parquet File", ".parquet")))
        file_path = list(file_path) #convert from tuple
        raw_data = Convert_Funcs.detect_file(file_path[0])

        #update summary label
        self.summary_data(raw_data)
        messagebox.showinfo(title="File Summary",message="File Summary Content Appears In Main Window")


        Convert_Funcs.display_teradata_preview(raw_data)
        return
    
    def compress(self):
        # What file does the user want to convert? Prompt the user to select a file from their PC.
        file_path = filedialog.askopenfilenames(title="Select File for Compression",filetypes=(("CSV","*.csv"),("JSON",'*.json'),
                                                                               ("XML","*.xml"),("Excel","*.xlsx"),("Parquet File", ".parquet")))
        test_comp = Convert_Funcs.compress_file(input_filepath=file_path) # should print if working
        response = messagebox.askyesno("Compress File", "Would you like to compress another file or continue using application?")
        if not response:
            self.master.destroy()  # Close the application if the user chooses not to convert another file
        return

    
    def open_bug_report_form(self):
        response = messagebox.askyesno(title="Bug Report Form",message="The Bug Report Form requires WIFI and Google sign in. Would you like to proceed?")
        if response:
            form_link = 'https://docs.google.com/forms/d/e/1FAIpQLSenWSnSEtqWfIO900PvIJawnd0Tx3k8OLrGBcDnMnAK-Xdqfg/viewform?usp=sf_link'
            webbrowser.open(form_link)
        return
    
    def plot_analysis(self):
        file_path = filedialog.askopenfilenames(title="Select Single File for Preview",filetypes=(("CSV","*.csv"),("JSON",'*.json'),
                                                                               ("XML","*.xml"),("Excel","*.xlsx"),("Parquet File", ".parquet")))
        file_path = list(file_path) #convert from tuple
        raw_data = Convert_Funcs.detect_file(file_path[0]) # creates the raw data 
        df_preview = pd.DataFrame(raw_data) # turn it into a pd dataframe

        # Setting up a new Tkinter window for plot configuration
        plot_config_window = tk.Toplevel(self.master)
        plot_config_window.title("Plot Configuration")

        # Variable for storing the plot type selection
        plot_type_var = tk.StringVar(value="bar")

        # Radio buttons for selecting the plot type
        plot_types = [("Bar", "bar"), ("Scatter", "scatter"), ("Violin", "violin")]
        tk.Label(plot_config_window, text="Select plot type:").pack(anchor='w')
        for text, mode in plot_types:
            tk.Radiobutton(plot_config_window, text=text, variable=plot_type_var, value=mode,
                   font=('Helvetica', 14), indicatoron=0, width=20, height=2, background='lightblue').pack(anchor='w', pady=5)

        # Combobox for selecting the X and Y columns
        tk.Label(plot_config_window, text="Select X column:").pack(anchor='w')
        x_column = ttk.Combobox(plot_config_window, values=list(df_preview.columns))
        x_column.pack(fill='x', expand=True)

        tk.Label(plot_config_window, text="Select Y column:").pack(anchor='w')
        y_column = ttk.Combobox(plot_config_window, values=list(df_preview.columns))
        y_column.pack(fill='x', expand=True)

        # Function to handle plot creation
        def on_create_plot():
            if plot_type_var.get() in ['scatter', 'violin'] and (not x_column.get() or not y_column.get()):
                tk.messagebox.showerror("Error", "Please select both X and Y columns for scatter and violin plots.")
                return
            Convert_Funcs.create_plot(df_preview, x_column.get(), y_column.get(), plot_type_var.get())  # Assuming 'create_plot' can handle these params
            plot_config_window.destroy()

        # Button to create the plot
        tk.Button(plot_config_window, text="Create Plot", command=on_create_plot).pack(pady=10)

        return  # The plotting function itself should handle plot display/save
        


    def summary_data(self,data):
        print("DATA TEST",data[0:3])
        total_rows = len(data)
        total_cols = len(data[0]) if data else 0
        missing_vals = sum(1 for row in data if any(str(value).strip()== '' or str(value) == "" for value in row.values()))
        has_null_vals = sum(1 for row in data if any(value is None or pd.isna(value) for value in row.values()))
        question_mark_vals = sum(1 for row in data if any(str(value).strip() == '*' or str(value).strip() == '?' for value in row.values()))

        s_text = (
            f"DATA SUMMARY: \n"
            f"Total Rows:   {total_rows}\n"
            f"Total Columns:   {total_cols}\n"
            f"Missing or Empty Values:   {missing_vals}\n"
            f"Null Values:   {has_null_vals}\n"
            #f"Values with ? or *:   {total_rows}\n"

        )
        self.summary_label.config(text=s_text,font=('Helvetica', 10), bg="lightgray")
        self.summary_label1.config(text=s_text,font=('Helvetica', 10), bg="lightgray")

    # password hidden entry func for teradata
    def hide_input(self,title, prompt):
        return simpledialog.askstring(title,prompt,show = "*")

    # Teradata connection abilities:
    def connect_to_tera(self):

        # connection details by user
        server = simpledialog.askstring("Teradata Connect","Enter Server:")
        username = simpledialog.askstring("Teradata Connect","Enter Username:")
        password = self.hide_input("Teradata Connect","Enter Password:")
        output_file_path = simpledialog.askstring("Teradata Connect","OPTIONAL - Enter Output Path for File Save Location:")
        # query they want to pull
        user_query = simpledialog.askstring("SQL","Enter your Teradata Query in SQL Format:")
        # if uery entered,
        if user_query:
            #call the connection func in conert_funcs:
            query_res = Convert_Funcs.convert_teradata(username=username,server=server,password=password,query=user_query,
                                                       output_path=output_file_path)
            
            # display file info
            self.show_file_info(query_res,"CSV")

            # Use read func and then do the summary using the converted csv.
            summary_data = Convert_Funcs.read_csv_file(query_res)
            self.summary_data(data = summary_data)
            
            response = messagebox.askyesno("Query Complete", "Query complete! Would you like to convert a file or submit another query?")
            if not response:
                self.master.destroy()  # Close the application if the user chooses not to convert another file
            return query_res


    def duplicate_detection(self):
        # Prompt the user to select a file
        file_path = filedialog.askopenfilename(title="Select File for Duplicate Detection", 
                                            filetypes=[("CSV", "*.csv"), ("JSON", "*.json"), ("XML", "*.xml"), ("Excel", "*.xlsx"), ("Parquet File", "*.parquet")])
        
        if not file_path:
            return

        # Detect file type and read data
        data = Convert_Funcs.detect_file(file_path)
        
        # Create a DataFrame
        df = pd.DataFrame(data)

        # Convert nested structures to string for detection if necessary
        df = df.applymap(lambda x: json.dumps(x) if isinstance(x, dict) else x)

        # Detect duplicates
        duplicates = df[df.duplicated()]

        if not duplicates.empty:
            duplicates_window = tk.Toplevel(self.master)
            duplicates_window.title("Duplicate Records")

            frame = ttk.Frame(duplicates_window)
            frame.pack(expand=True, fill="both")

            tree = ttk.Treeview(frame, columns=list(duplicates.columns), show="headings")
            for col in duplicates.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='w')

            for _, row in duplicates.iterrows():
                tree.insert("", "end", values=list(row))

            tree.pack(expand=True, fill="both")

            remove_duplicates_btn = tk.Button(duplicates_window, text="Remove Duplicates", command=lambda: self.remove_duplicates(df, duplicates, duplicates_window))
            remove_duplicates_btn.pack(side="bottom", pady=10)

        else:
            messagebox.showinfo("Duplicate Detection", "No duplicate records found.")

    def remove_duplicates(self, df, duplicates, window):
        df.drop_duplicates(inplace=True)
        messagebox.showinfo("Duplicate Detection", "Duplicate records removed.")
        window.destroy()




    # Allow users to double check the file they selected by viewing it'sname and type.
    def show_file_info(self, file_path, user_choice):
        #Take the current file name and whatever the user chooses to convert it to and display it under the progress bar.
        file_name = os.path.basename(file_path)
        self.file_info_label1.config(text=f"Selected File: {file_name}\nConversion Type: {user_choice}", font=('Garamond', 12), bg="lightgray")
        self.file_info_label.config(text=f"Selected File: {file_name}\nConversion Type: {user_choice}", font=('Garamond', 12), bg="lightgray")
    

if __name__ == "__main__":
    root = tk.Tk()

    # Set the initial size of the main window
    root.geometry("500x500")  # Adjust the size as needed

    # Allow resizing both horizontally and vertically
    root.resizable(True, True)

    root.title("Data Forge Fusion")

    root.configure(bg="#7D99AD")


    app = DataConverterApp(root)
    root.mainloop()