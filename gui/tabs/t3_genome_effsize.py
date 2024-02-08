import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class GenomeEffSize:
    def __init__(self, parent, tab_parent, config_file):
        self.parent = parent
        self.tab_parent = tab_parent

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 

        diagnostic_label = ttk.Label(self.control_frame, text="Reference Genome")
        diagnostic_label.pack()

        choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        choose_file_button.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Effect Size Table")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["Customize", "Randomly Generate From GFF"], foreground="White")
        self.surname_combobox.pack()

        self.surname_combobox.bind("<<ComboboxSelected>>", self.on_combobox_change)

        self.dynamic_widgets = []

        # #if 1

        # diagnostic_label = ttk.Label(self.control_frame, text="Path To File")
        # diagnostic_label.pack()
        # choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        # choose_file_button.pack()


        # #if 2

        # diagnostic_label = ttk.Label(self.control_frame, text="Path To GFF")
        # diagnostic_label.pack()
        # choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        # choose_file_button.pack()

        # self.name_label = ttk.Label(self.control_frame, text="Number of Effect Size Groups")
        # self.name_label.pack()
        # self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        # self.name_entry.pack()

        # next_button = tk.Button(self.parent, text="Show")
        # next_button.pack()
        # # Show table 1

        # # Show Table 2

        next_button = tk.Button(self.parent, text="Normalize")
        next_button.pack()

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

    def choose_file(self):  # 
        filename = filedialog.askopenfilename(title="Select a file")
        print("Selected file:", filename)  # replace

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
        elif choice == "Randomly Generate From GFF":
            self.render_generate_from_gff()

    def render_customize_options(self):
        label = ttk.Label(self.control_frame, text="Path to File")
        label.pack()
        button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        button.pack()
        
        self.dynamic_widgets.extend([label, button])

    def render_generate_from_gff(self):

        label = ttk.Label(self.control_frame, text="Path to gff")
        label.pack()
        button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        button.pack()

        name_label = ttk.Label(self.control_frame, text="Number of Effect Size Groups")
        name_label.pack()
        name_entry = ttk.Entry(self.control_frame, foreground="White")
        name_entry.pack()

        self.dynamic_widgets.extend([label, button, name_label, name_entry])