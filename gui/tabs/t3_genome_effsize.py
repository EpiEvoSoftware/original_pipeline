import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class GenomeEffSize:
    def __init__(self, parent, tab_parent, config_file):
        self.parent = parent
        self.tab_parent = tab_parent

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True)  # Pack the frame

        diagnostic_label = ttk.Label(self.control_frame, text="Reference Genome")
        diagnostic_label.pack()

        choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        choose_file_button.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Effect Size Table")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["Customize", "Randomly Generate From GFF"], foreground="White")
        self.surname_combobox.pack()

        diagnostic_label = ttk.Label(self.control_frame, text="Path To File")
        diagnostic_label.pack()
        choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        choose_file_button.pack()

        diagnostic_label = ttk.Label(self.control_frame, text="Path To GFF")
        diagnostic_label.pack()
        choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        choose_file_button.pack()

        self.name_label = ttk.Label(self.control_frame, text="Number of Effect Size Groups")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        next_button = tk.Button(self.parent, text="Show")
        next_button.pack()
        # Show table 1

        # Show Table 2

        next_button = tk.Button(self.parent, text="Normalize")
        next_button.pack()

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

    def choose_file(self):  # Added self parameter
        filename = filedialog.askopenfilename(title="Select a file")
        print("Selected file:", filename)  # You can replace this with your own logic

    def go_to_next_tab(self):
        current_tab_index = self.tab_parent.index(self.tab_parent.select())
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.select(next_tab_index)