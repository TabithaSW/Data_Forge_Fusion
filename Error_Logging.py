# GUI library:
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import tkinter.scrolledtext as tkst

# Basic math and file operations libraries:
import numpy as np
import pandas as pd
import os

# bug reporting
import logging


class BugReport:
    def __init__(self, master): 
        self.master = master 
        self.master.title("Bug Report Feature")

        self.desc_label = tk.Label(master, text = "Bug Description Form")
        self.desc_label.pack()

        # allow user to enter bug issue: The Entry widget allows you to enter a single-line text.
        self.desc_text = tk.Entry(master, width=50)
        self.desc_text.pack()

        # allow user to attach evidence of bug issue so issue can be resolved.
        self.attach_label = tk.Label(master,"Attach File/Photo:")
        self.attach_label.pack()

        # buttons for attaching and submitting the bug report with text/file/photo 
        self.attach_butt = tk.Button(master,text="Attach:",command=self.attach_file)
        self.attach_butt.pack()

        self.submit_butt = tk.Button(master, text="Submit Bug Report",command=self.submit_bug_report)
        self.submit_butt.pack()
    
    def attach_file(self):
        file_path = filedialog.askopenfilenames(title="Attach a File or Image for Bug Evidence (optional):")
        pass

    def submit_bug_report(self):
        bug_desc = self.desc_text.get() # pull the bug text input from user
        self.logging_rep(bug_desc) # call logging here so we can get the error info
        
        messagebox.showinfo("Bug Report Successfully Submitted","Thank you for reporting the issue, we will look into fixing it ASAP!")
        self.master.destroy() # end report form, close out
        pass

    def logging_rep(self, description):
        logging.basicConfig(filename="bug_reports.log",level=logging.ERROR) #specify name and log type
        logging.error(f"Bug Description: {description}")
        