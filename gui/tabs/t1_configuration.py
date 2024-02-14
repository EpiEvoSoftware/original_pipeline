import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from tools import CreateToolTip

class Configuration:
    def __init__(self, parent, tab_parent, config_path):
        self.config_path = config_path
        self.cwd = self.load_config_as_dict()['BasicRunConfiguration']['cwdir']
        self.n_replicates = self.load_config_as_dict()['BasicRunConfiguration']['n_replicates']
        self.ref_path = self.load_config_as_dict()['GenomeElement']['ref_path']
        self.parent = parent
        self.tab_parent = tab_parent

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 

        diagnostic_label = ttk.Label(self.control_frame, text="Choose Working Directory")
        diagnostic_label.pack()
        choose_directory_button = tk.Button(self.control_frame, text="Choose Directory", command=self.choose_directory)
        choose_directory_button.pack()
        self.diagnostic_label = ttk.Label(self.control_frame, text="Current Working Directory: " + self.cwd)
        self.diagnostic_label.pack()

        self.n_replicates_label = ttk.Label(self.control_frame, text="n_replicates:")
        self.n_replicates_label.pack()
        self.n_replicates_entry = ttk.Entry(self.control_frame, foreground="black")
        self.n_replicates_entry.insert(0, self.n_replicates)  
        self.n_replicates_entry.pack()
        update_n_replicates_button = tk.Button(self.control_frame, text="Update n_replicates", command=self.update_n_replicates)
        update_n_replicates_button.pack()
        CreateToolTip(update_n_replicates_button, \
   'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, '
   'consectetur, adipisci velit. Neque porro quisquam est qui dolorem ipsum '
   'quia dolor sit amet, consectetur, adipisci velit. Neque porro quisquam '
   'est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.')

        
        ref_path_label = ttk.Label(self.control_frame, text="Choose Ref Path")
        ref_path_label.pack()
        choose_ref_path_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_ref_path)
        choose_ref_path_button.pack()
        self.ref_path_label = ttk.Label(self.control_frame, text="Current Ref Path: " + self.ref_path)
        self.ref_path_label.pack()

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()


    def go_to_next_tab(self):
        current_tab_index = self.tab_parent.index(self.tab_parent.select())
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.select(next_tab_index)

    def load_config_as_dict(self):
        with open(self.config_path, 'r') as file:
            return json.load(file)

    def save_config(self, config):
        with open(self.config_path, 'w') as file:
            json.dump(config, file, indent=4)

    def save_ref_path(self, config):
        with open(self.ref_path, 'w') as file:
            json.dump(config, file, indent=4)

    def choose_directory(self):  
        chosen_directory = filedialog.askdirectory(title="Select a Directory")
        if chosen_directory:  
            self.cwd = chosen_directory
            self.diagnostic_label.config(text=f"Working Directory: {self.cwd}")  # Update the label with the new directory
            config = self.load_config_as_dict()
            config['BasicRunConfiguration']['cwdir'] = self.cwd
            self.save_config(config)
     
    def choose_ref_path(self):  
        filetypes = ( #don't need to check if its genome file: or use python package jaehee said
            ("Genome files", ("*.fasta", "*.fa", "*.gb", "*.gtf", "*.vcf", "*.bam", "*.sam", "*.fna")),
            ("All files", "*.*")
        )
        chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File", filetypes=filetypes)
        if chosen_file:  
            self.ref_path = chosen_file
            self.ref_path_label.config(text=f"Ref Path: {self.ref_path}") 
            config = self.load_config_as_dict()
            config['GenomeElement']['ref_path'] = self.ref_path
            self.save_config(config)

    def update_n_replicates(self):
        try:
            new_n_replicates = int(self.n_replicates_entry.get())  
            config = self.load_config_as_dict() 
            config['BasicRunConfiguration']['n_replicates'] = new_n_replicates 
            self.save_config(config)  
            messagebox.showinfo("Update Successful", "n_replicates changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for n_replicates.") 