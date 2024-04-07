import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from utils import *

# TODO: generate config file, put it in the working directory

class Configurationv2:
    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):
        self.config_path = config_path
        self.cwd = load_config_as_dict(self.config_path)['BasicRunConfiguration']['cwdir']
        self.n_replicates = load_config_as_dict(self.config_path)['BasicRunConfiguration']['n_replicates']
        self.ref_path = load_config_as_dict(self.config_path)['GenomeElement']['ref_path']
        self.parent = parent
        self.tab_index = tab_index
        self.tab_parent = tab_parent
        self.tab_parent.add(parent, text=tab_title)
        if hide:
            self.tab_parent.tab(tab_index, state="disabled")
        # self.tab_parent.tab(tab_index, state="normal")

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 

        columns = ('Name', 'Column 2', 'Column 3', 'Column 4', 'Column 5')

        tree = ttk.Treeview(self.control_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        tree.tag_configure('evenrow', background='#F0F0F0')  # Light grey for odd rows
        tree.tag_configure('oddrow', background='white')  # White for even rows

        # Generate some data and insert into the treeview with alternating colors
        for i in range(1, len(columns) + 1):
            values = [f'Row {i} Value {j}' for j in range(1, 6)]
            # Use 'oddrow' tag for odd rows, 'evenrow' for even rows
            if i % 2 == 0:
                tree.insert('', 'end', values=values, tags=('evenrow',))
            else:
                tree.insert('', 'end', values=values, tags=('oddrow',))

        # Pack the treeview finally
        tree.pack(expand=True, fill='both')

        render_next_button(self.tab_index, self.tab_parent, self.parent)

#         
        


    def choose_directory(self):  
        chosen_directory = filedialog.askdirectory(title="Select a Directory")
        if chosen_directory:  
            self.cwd = chosen_directory
            self.diagnostic_label.config(text=f"Working Directory: {self.cwd}")  # Update the label with the new directory
            config = load_config_as_dict(self.config_path)
            config['BasicRunConfiguration']['cwdir'] = self.cwd
            save_config(self.config_path, config)
     
    def choose_ref_path(self):  
        filetypes = ( #don't need to check if its genome file: or use python package jaehee said
            ("Genome files", ("*.fasta", "*.fa", "*.gb", "*.gtf", "*.vcf", "*.bam", "*.sam", "*.fna")),
            ("All files", "*.*")
        )
        chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File", filetypes=filetypes)
        if chosen_file:  
            self.ref_path = chosen_file
            self.ref_path_label.config(text=f"Ref Path: {self.ref_path}") 
            config = load_config_as_dict(self.config_path)
            config['GenomeElement']['ref_path'] = self.ref_path
            save_config(self.config_path, config)

    def update_n_replicates(self):
        try:
            new_n_replicates = int(self.n_replicates_entry.get())  
            config = load_config_as_dict(self.config_path) 
            config['BasicRunConfiguration']['n_replicates'] = new_n_replicates 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "n_replicates changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for n_replicates.") 