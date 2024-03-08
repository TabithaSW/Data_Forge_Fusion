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

# bug report packages
import webbrowser


class DataConverterApp:
    # Initialize attributes
    def __init__(self, master) -> None:
        self.master = master

        # GUI Title: 
        self.master.title("File Convertor") # Application name

        # lets make this tabular, new design:
        MainTabs = ttk.Notebook(self.master)

        self.progress = ttk.Progressbar(
            self.master,
            length=200,
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

        # Data summary label
        self.summary_label = tk.Label(
            self.conversion_tab,
            font =('Helvetica', 10)
            )
        self.summary_label.pack(side=tk.BOTTOM, expand=True)

        # Data summary label for other tab
        self.summary_label = tk.Label(
            self.analysis_tab,
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

        # file preview button
        self.preview_file_new = tk.Button(
            self.conversion_tab,
            text="Preview & Summary of Raw Data from Files(s)",
            command=self.file_preview,
            #bg="lightblue",
            **button_style,  # Apply the common button style
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.preview_file_new.pack(side=tk.TOP, anchor='w', padx=10, pady=5)

        # 2nd file preview button
        self.preview_file_new = tk.Button(
            self.analysis_tab,
            text="Preview & Summary of Raw Data from Files(s)",
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
            font =('Helvetica', 10)
            )
        self.file_info_label.pack(side=tk.BOTTOM, expand=True)

        # 2nd File information labels secondary tab version
        self.file_info_label = tk.Label(
            self.analysis_tab,
            text = " ",
            font =('Helvetica', 10)
            )
        self.file_info_label.pack(side=tk.BOTTOM, expand=True)

    
        # end progress bar
        # Repack progress bar at the end or at the desired location
        self.progress.pack_forget()  # Remove the current packing
        self.progress.pack(side=tk.BOTTOM, pady=5, padx=5)
        

    def choose_files(self):
        # Options for conversion:
        file_options = ["CSV", "JSON", "XML","csv","json","xml","excel","EXCEL"]

        # Temporary file name until user downloads coverted file and choose new name:
        new_file_name = "Converted_File"


        # What file does the user want to convert? Prompt the user to select a file from their PC.
        file_path = filedialog.askopenfilenames(title="Select File",filetypes=(("CSV","*.csv"),("JSON",'*.json'),
                                                                               ("XML","*.xml"),("Excel","*.xlsx"))) 

        # tuple to list format
        file_path = list(file_path)

        if file_path:
            # for each file in the chosen
            for i in file_path:

                # Check file type here with detect_file function, function checks type and converts to python dictionary:
                temp_data = Convert_Funcs.detect_file(i)
                #update summary label
                self.summary_data(temp_data)
                messagebox.showinfo(title="File Summary",message="File Summary Content Appears In Main Window")

                # Once we know the current file type, let the user choose a conversion format using prompt_file_choice func.
                user_choice = Convert_Funcs.prompt_file_choice(file_path=i)
                self.show_file_info(i, user_choice) # display files chosen

                # if the data was processed correctly (into py dict) then we check what the user requested, despite upper or lower case for file type:
                if temp_data and user_choice.lower() in file_options:

                    # display data preview:
                    df_preview = pd.DataFrame(temp_data) # all my read functions convert to py dict first prior to file change.

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

                    # setup the df for previewing, configure display of the cols:
                    for col in df_preview.columns:
                        prev_widget.column(col, anchor="w")
                        prev_widget.heading(col, text=col,anchor="w")

                    # create scrollbar instance
                    my_scroll = ttk.Scrollbar(frame_2,orient="vertical",command=prev_widget.yview )
                    my_scroll.pack(side="right",fill="y")

                    horiz_scroll = ttk.Scrollbar(frame_2, orient = "horizontal", command = prev_widget.xview)
                    horiz_scroll.pack(side = "bottom",fill = "x")

                    prev_widget.configure(yscrollcommand=my_scroll.set)
                    prev_widget.configure(xscrollcommand = horiz_scroll.set)
                    

                    # Insert to widget
                    for i, (data, row) in enumerate(df_preview.iterrows()): # for each row of data
                        if i >= 1000: # preview ends at 1000 rows
                            break
                        prev_widget.insert("",data,values=list(row)) #insert into the widget, creates new row in widget each iter

                    # display widget
                    prev_widget.pack(expand=True,fill="both")

                    # allow user to close out the preview
                    close_widg = tk.Button(prev_widget, text="Close Data Preview",command=prev_window.destroy)
                    close_widg.pack(side="bottom",pady=10) 

                    
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
                        Convert_Funcs.write_excel_file(filepath=new_file_name,datalist=temp_data)

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
                                                                               ("XML","*.xml"),("Excel","*.xlsx")))

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

    # adding file preview, no conversion required:
    def file_preview(self):
        # What file does the user want to convert? Prompt the user to select a file from their PC.
        file_path = filedialog.askopenfilenames(title="Select Single File for Preview",filetypes=(("CSV","*.csv"),("JSON",'*.json'),
                                                                               ("XML","*.xml"),("Excel","*.xlsx")))
        file_path = list(file_path) #convert from tuple
        raw_data = Convert_Funcs.detect_file(file_path[0])

        #update summary label
        self.summary_data(raw_data)
        messagebox.showinfo(title="File Summary",message="File Summary Content Appears In Main Window")


        Convert_Funcs.display_teradata_preview(raw_data)
        return
    
    def open_bug_report_form(self):
        response = messagebox.askyesno(title="Bug Report Form",message="The Bug Report Form requires WIFI and Google sign in. Would you like to proceed?")
        if response:
            form_link = 'https://docs.google.com/forms/d/e/1FAIpQLSenWSnSEtqWfIO900PvIJawnd0Tx3k8OLrGBcDnMnAK-Xdqfg/viewform?usp=sf_link'
            webbrowser.open(form_link)
        return


    def summary_data(self,data):
        #print("DATA TEST",data)
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
        self.summary_label.config(text=s_text,font=('Garamond', 12), bg="lightgray")

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


    # Allow users to double check the file they selected by viewing it'sname and type.
    def show_file_info(self, file_path, user_choice):
        #Take the current file name and whatever the user chooses to convert it to and display it under the progress bar.
        file_name = os.path.basename(file_path)
        self.file_info_label.config(text=f"Selected File: {file_name}\nConversion Type: {user_choice}", font=('Garamond', 12), bg="lightgray")
    

if __name__ == "__main__":
    root = tk.Tk()

    # Set the initial size of the main window
    root.geometry("400x400")  # Adjust the size as needed

    # Allow resizing both horizontally and vertically
    root.resizable(True, True)

    root.title("File Conversion Application")

    app = DataConverterApp(root)
    root.mainloop()