import tkinter as tk
from tkinter import ttk, Menu, Scrollbar, font
from kenneth import Kenneth


class SystemInfoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the icon
        self.iconbitmap('img/icon.ico')

        # Grab all the system specs
        self.specs = Kenneth()

        # Set the title so everyone knows this is Kenneth
        self.title("Kenneth")

        # This barely works
        self.configure(background='green')

        # Paned window setup
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg='gray')
        self.paned_window.configure(background='green')
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left frame (Pane)
        self.left_frame = ttk.Frame(self.paned_window, width=300)
        self.paned_window.add(self.left_frame, stretch="never")

        # Right frame (Pane)
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, stretch="always")

        # Left column - List of hardware types
        self.hardware_list = ttk.Treeview(self.left_frame, selectmode='browse')
        self.hardware_list.pack(expand=True, fill='both')

        # Inserting categories and assigning the resulting data to them
        self.categories = {
            "Overview": "overview",
            "CPU": 'cpu',
            "RAM": 'ram',
            "Motherboard": 'motherboard',
            "HDD": 'disk',
            "GPU": 'gpu',
            "Monitor": 'monitors',
            "OS": 'os'
        }

        self.show_all_var = tk.BooleanVar(value=False)  # Default to False

        # Add everything to the hardware list
        for category in self.categories.keys():
            self.hardware_list.insert('', 'end', iid=category, text=category)

        # Binding the selection event
        self.hardware_list.bind("<<TreeviewSelect>>", self.on_select)

        # Right column - Summary with Scrollbar
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, stretch="always")

        # Use a monospaced font for better alignment
        self.custom_font = font.Font(family="Consolas", size=10)

        # Summary text
        self.summary_text = tk.Text(self.right_frame, wrap='word', font=self.custom_font, bg='#25ff00')
        self.summary_text.pack(side=tk.LEFT, expand=True, fill='both')

        # Gotta have scrollbars
        self.scrollbar = Scrollbar(self.right_frame, command=self.summary_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        # Set the background color
        self.summary_text.config(yscrollcommand=self.scrollbar.set, bg='#25ff00')

        # Menu setup
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        # File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save")
        self.file_menu.add_command(label="Print")
        self.file_menu.add_command(label="Exit")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # View menu
        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Options")
        self.view_menu.add_command(label="Refresh")
        self.view_menu.add_checkbutton(label="Show all", onvalue=True, offvalue=False, variable=self.show_all_var)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # Help menu
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

    def on_select(self, event):

        # Get the category
        selected_item = self.hardware_list.selection()[0]
        # bits = selected_item.split("}} {{")
        # print(len(bits))

        # Update the text column
        self.update_summary(selected_item)

    def update_summary(self, text):

        # Get the device name to use in specs from the selected device in the dropdown
        # This is basically translating the user friendly text to the text that lives in the dict
        devname = self.categories[text]

        # See if we should show all the information or just a bit of the important stuff
        show_all = self.show_all_var.get()

        # Surely there's a better way to do this
        if show_all:
            data = self.specs.devices[devname]['text']
        else:
            data = self.specs.devices[devname]['text_minimal']

        # Clear the text
        self.summary_text.delete(1.0, "end")

        # Set the font
        self.summary_text.configure(font=self.custom_font)

        # Dump the text into the window
        self.summary_text.insert("end", data)


# Example usage
app = SystemInfoApp()
app.mainloop()
