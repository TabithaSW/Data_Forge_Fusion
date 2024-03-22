# Original GUI Buttons
# Changed to drop down, so we won't use this file. Move to temp folder.

import tkinter as tk

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

        # lets make a menu/dropdown containing all the buttons instead of individual ones
        menu_drop = tk.Menu(self.frame,tearoff=0, font=('Garamond',12,'bold'))#fg='#2E8B57')
        master.config(menu = menu_drop)
        file_menu = tk.Menu(menu_drop, tearoff=0,font=('Garamond',12,'bold'))#fg='#2E8B57') #
        menu_drop.add_cascade(label = "Application Options: ",menu=file_menu,font=('Garamond',12,'bold'))

        # all buttons so far and commands
        file_menu.add_command(label="Preview & Summary of Raw Data from Files(s)",command=self.file_preview)
        file_menu.add_command(label="Choose File(s) for Conversion",command=self.choose_files)
        file_menu.add_command(label="Connect to Teradata",command = self.connect_to_tera)
        file_menu.add_command(label="Report a Bug",command=self.open_bug_report_form)
        file_menu.add_command(label="Merge & Convert Files",command=self.left_join)
