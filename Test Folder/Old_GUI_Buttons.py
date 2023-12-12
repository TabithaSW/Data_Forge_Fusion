# Original GUI Buttons
# Changed to drop down, so we won't use this file. Move to temp folder.


class GuiButtons:
    # Initialize attributes
    def __init__(self, master) -> None:
        self.master = master


        self.frame = tk.Frame(
            self.master,
            padx = 10,
            pady = 10,
            relief=tk.RIDGE,#border style
            bd=5, # borderwidth
            )
        self.frame.pack(expand=True, fill="both")


        # Bug Report Form button
        self.Bug_Report_Form = tk.Button(
            self.frame,
            text = "Report a Bug",
            command= self.open_bug_report_form,
            fg = "#2E8B57", #seagreen
            font =('Garamond',12, "bold"),
            pady = 10,
            padx = 10,
            cursor="hand2" # allows diff cursor over button, user knows to click
        )
        self.Bug_Report_Form.pack(side=tk.BOTTOM,expand=True,padx=10,pady=10)

        # file preview button
        self.left_merge = tk.Button(
            self.frame,
            text="Merge & Convert Files(s)",
            command=self.left_join,
            #bg="lightblue",
            fg = "#2E8B57", #seagreen
            font =('Garamond',12, "bold"),
            pady = 5,
            padx = 10,
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.left_merge.pack(side=tk.BOTTOM,expand=True,padx=10,pady=10)

        # Teradata button:
        self.connect_to_tera_button = tk.Button(
            self.frame,
            text = "Connect to Teradata",
            command= self.connect_to_tera,
            fg = "#2E8B57", #seagreen
            font =('Garamond',12, "bold"),
            pady = 5,
            padx = 10,
            cursor="hand2" # allows diff cursor over button, user knows to click
        )
        self.connect_to_tera_button.pack(side=tk.BOTTOM,expand=True,padx=10,pady=10)


        # Choose and convert button
        self.choose_file_button = tk.Button(
            self.frame,
            text="Choose File(s) for Conversion",
            command=self.choose_files,
            #bg="lightblue",
            fg = "#2E8B57", #seagreen
            font =('Garamond',12, "bold"),
            pady = 5,
            padx = 10,
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.choose_file_button.pack(side=tk.BOTTOM,expand=True,padx=10,pady=10)

        # file preview button
        self.preview_file_new = tk.Button(
            self.frame,
            text="Preview & Summary of Raw Data from Files(s)",
            command=self.file_preview,
            #bg="lightblue",
            fg = "#2E8B57", #seagreen
            font =('Garamond',12, "bold"),
            pady = 5,
            padx = 10,
            cursor="hand2" # allows diff cursor over button, user knows to click
            )
        self.preview_file_new.pack(side=tk.BOTTOM,expand=True,padx=10,pady=10)
