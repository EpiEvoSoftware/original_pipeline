import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox

class Seeds:
    def __init__(self, parent, tab_parent, config_file):
        self.parent = parent
        self.tab_parent = tab_parent

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True)  # Pack the frame



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

        vcf = ttk.Label(self.control_frame, text="Path to Seed")
        vcf.pack()
        choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        choose_file_button.pack()

        vcf = ttk.Label(self.control_frame, text="Path to Seed Phylogeny")
        vcf.pack()
        choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        choose_file_button.pack()

        self.name_label = ttk.Label(self.control_frame, text="Burn-In Ne")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.name_label = ttk.Label(self.control_frame, text="Burn-In Input Rate")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.name_label = ttk.Label(self.control_frame, text="Generations, Run")

        self.name_label = ttk.Label(self.control_frame, text="Scaling Factor")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

        # self.table = ttk.Treeview(self.control_frame, columns=('id', 't1', 't2', 'host_id'), show='headings')
        # You may need to pack or grid the table as well depending on your layout requirements

    def choose_file(self):  # Added self parameter
        filename = filedialog.askopenfilename(title="Select a file")
        print("Selected file:", filename)  # replace

    def go_to_next_tab(self):
        current_tab_index = self.tab_parent.index(self.tab_parent.select())
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.select(next_tab_index)