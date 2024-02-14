import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox

class Seeds:
    def __init__(self, parent, tab_parent, config_path):
        self.parent = parent
        self.tab_parent = tab_parent
        self.dynamic_widgets = []

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True)

        diagnostic_label = ttk.Label(self.control_frame, text="Working Directory")
        diagnostic_label.pack()
        choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        choose_file_button.pack()

        self.name_label = ttk.Label(self.control_frame, text="Seeds Size")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Seeds VCF File")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["Customize", "SLiM Burn-In"], foreground="White")
        self.surname_combobox.pack()

        self.surname_combobox.bind("<<ComboboxSelected>>", self.on_combobox_change)

        self.dynamic_widgets = []

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

    def choose_file(self):  
        filename = filedialog.askopenfilename(title="Select a file")
        print("Selected file:", filename) 

    def go_to_next_tab(self):
        current_tab_index = self.tab_parent.index(self.tab_parent.select())
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.select(next_tab_index)

    def on_combobox_change(self, event):
        """
        Clear previously displayed widgets
        Check the combobox value and render appropriate UI elements
        """
        for widget in self.dynamic_widgets:
            widget.destroy()
        self.dynamic_widgets.clear()

        choice = self.surname_combobox.get()
        if choice == "Customize":
            self.render_customize_options()
        elif choice == "SLiM Burn-In":
            self.render_slim_burn_in_options()

    def render_customize_options(self):
        labels = ["Path to Seed", "Path to Seed Phylogeny"]
        for label_text in labels:
            label = ttk.Label(self.control_frame, text=label_text)
            label.pack()
            button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
            button.pack()
            
            self.dynamic_widgets.extend([label, button])

    def render_slim_burn_in_options(self):
        entries = ["Burn-In Ne", "Burn-In Input Rate", "Generations, Run", "Scaling Factor"]
        for entry_text in entries:
            label = ttk.Label(self.control_frame, text=entry_text)
            label.pack()
            entry = ttk.Entry(self.control_frame, foreground="White")
            entry.pack()
            
            self.dynamic_widgets.extend([label, entry])
