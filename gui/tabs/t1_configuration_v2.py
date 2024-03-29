import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from tools import *

# TODO: generate config file, put it in the working directory

class Configurationv2:
    def __init__(self, parent, tab_parent, config_path):
        self.config_path = config_path
        self.cwd = load_config_as_dict(self.config_path)['BasicRunConfiguration']['cwdir']
        self.n_replicates = load_config_as_dict(self.config_path)['BasicRunConfiguration']['n_replicates']
        self.ref_path = load_config_as_dict(self.config_path)['GenomeElement']['ref_path']
        self.parent = parent
        self.tab_parent = tab_parent

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

#         self.control_frame = ttk.Frame(self.parent, width=300)
#         diagnostic_label = ttk.Label(self.control_frame, text="Choose Working Directory")
#         diagnostic_label.pack()
#         choose_directory_button = tk.Button(self.control_frame, text="Choose Directory", command=self.choose_directory)
#         choose_directory_button.pack()
#         self.diagnostic_label = ttk.Label(self.control_frame, text="Current Working Directory: " + self.cwd)
#         self.diagnostic_label.pack()

#         self.n_replicates_label = ttk.Label(self.control_frame, text="n_replicates:")
#         self.n_replicates_label.pack()
#         self.n_replicates_entry = ttk.Entry(self.control_frame, foreground="black")
#         self.n_replicates_entry.insert(0, self.n_replicates)  
#         self.n_replicates_entry.pack()
#         update_n_replicates_button = tk.Button(self.control_frame, text="Update n_replicates", command=self.update_n_replicates)
#         update_n_replicates_button.pack()
#         CreateToolTip(update_n_replicates_button, \
#    'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, '
#    'consectetur, adipisci velit. Neque porro quisquam est qui dolorem ipsum '
#    'quia dolor sit amet, consectetur, adipisci velit. Neque porro quisquam '
#    'est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.')

        
#         ref_path_label = ttk.Label(self.control_frame, text="Choose Ref Path")
#         ref_path_label.pack()
#         choose_ref_path_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_ref_path)
#         choose_ref_path_button.pack()
#         self.ref_path_label = ttk.Label(self.control_frame, text="Current Ref Path: " + self.ref_path)
#         self.ref_path_label.pack()

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab, state = "disabled")
        next_button.pack()
        next_button.configure(state="normal")


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