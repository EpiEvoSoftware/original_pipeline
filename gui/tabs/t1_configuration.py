import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from tools import *


# TODO: generate config file, put it in the working directory

class Configuration:
    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):
        self.config_path = config_path
        self.cwd = load_config_as_dict(self.config_path)['BasicRunConfiguration']['cwdir']
        self.n_replicates = load_config_as_dict(self.config_path)['BasicRunConfiguration']['n_replicates']
        self.ref_path = load_config_as_dict(self.config_path)['GenomeElement']['ref_path']
        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_index = tab_index

        self.tab_parent.add(self.parent, text=tab_title)
        # self.tab_parent.tab(tab_index, state="disabled")
        # self.tab_parent.tab(tab_index, state="normal")

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 
        self.control_frame.grid_columnconfigure(0, weight=1)
        

        self.render_working_directory()

        self.render_n_replicates()

        self.render_ref_path_label()

        render_next_button(self.tab_index, self.tab_parent, self.parent)
        

    def render_working_directory(self):
        def diagnostic_label_title():
            title = "Choose Working Directory"
            self.diagnostic_label_title = ttk.Label(self.control_frame, text=title)
            self.diagnostic_label_title.pack() #grid(row = 0, column = 0, sticky = 'W', pady = 2)

        def choose_directory_button():
            choose_directory_button = tk.Button(self.control_frame, text="Choose Directory", command=self.choose_directory)
            # choose_directory_button.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
            choose_directory_button.pack()

        def diagnostic_label():
            self.cwd = "/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff"
            self.diagnostic_label = ttk.Label(self.control_frame, text="Current Working Directory: " + self.cwd, background="black")
            self.diagnostic_label.pack()# grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        self.test = tk.StringVar(value = "bi-allele")
        self.trans_type_combobox = ttk.Combobox(self.control_frame, foreground = "black", width = 23, textvariable=self.test, values=["bi-allele", "additive", "/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff"], state="disabled").pack() #grid(row=3, column=0, sticky='ew', padx=5, pady=5)

        diagnostic_label_title()
        choose_directory_button()
        diagnostic_label()
        # self.diagnostic_label_title = ttk.Label(self.control_frame, text="Choose Working Directory")
        # self.diagnostic_label_title.pack()
        # choose_directory_button = tk.Button(self.control_frame, text="Choose Directory", command=self.choose_directory)
        # choose_directory_button.pack()
        # self.diagnostic_label = ttk.Label(self.control_frame, text="Current Working Directory: " + self.cwd)
        # self.diagnostic_label.pack()

    def render_n_replicates(self):
        self.n_replicates_label = ttk.Label(self.control_frame, text="n_replicates:").pack(side='left')
        # self.n_replicates_label.pack() #grid(row=3, column=1, sticky='ew', padx=5, pady=5)
        self.n_replicates_entry = ttk.Entry(self.control_frame, foreground="black", width = 80)
        # self.n_replicates_entry.insert(0, self.n_replicates)
        self.n_replicates_entry.insert(0, "/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff")
        # self.n_replicates_entry.delete(0, tk.END)
        self.n_replicates_entry.configure(state="disabled")
        self.n_replicates_entry.configure(state="normal")
        # self.n_replicates_entry.insert(0, 'new_text')
        new_width = len('/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff')
        self.n_replicates_entry.config(width=new_width)
        self.n_replicates_entry.configure(state="disabled")
        CreateToolTip(self.n_replicates_entry, \
   '/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff')
        self.n_replicates_entry.pack(side='right') #grid(row=4, column=0, sticky='ew', padx=5, pady=5)
        update_n_replicates_button = tk.Button(self.control_frame, text="Update n_replicates", command=self.update_n_replicates)
        update_n_replicates_button.pack() #grid(row=5, column=0, sticky='ew', padx=5, pady=5)
        # self.n_replicates_label = ttk.Label(self.control_frame, text="n_replicates:")
        # self.n_replicates_label.pack()
        # self.n_replicates_entry = ttk.Entry(self.control_frame, foreground="black")
        # self.n_replicates_entry.insert(0, self.n_replicates)  
        # self.n_replicates_entry.pack()
        # update_n_replicates_button = tk.Button(self.control_frame, text="Update n_replicates", command=self.update_n_replicates)
        # update_n_replicates_button.pack()

        CreateToolTip(update_n_replicates_button, \
   'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, '
   'consectetur, adipisci velit. Neque porro quisquam est qui dolorem ipsum '
   'quia dolor sit amet, consectetur, adipisci velit. Neque porro quisquam '
   'est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.')
        
    def render_ref_path_label(self):
        ref_path_label = ttk.Label(self.control_frame, text="Choose Ref Path")
        ref_path_label.pack() #grid(row=6, column=0, sticky='ew', padx=5, pady=5)
        choose_ref_path_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_ref_path)
        choose_ref_path_button.pack() #grid(row=7, column=0, sticky='ew', padx=5, pady=5)
        self.ref_path_label = ttk.Label(self.control_frame, text="Current Ref Path: " + self.ref_path)
        self.ref_path_label.pack() #grid(row=8, column=0, sticky='ew', padx=5, pady=5)
        # ref_path_label = ttk.Label(self.control_frame, text="Choose Ref Path")
        # ref_path_label.pack()
        # choose_ref_path_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_ref_path)
        # choose_ref_path_button.pack()
        # self.ref_path_label = ttk.Label(self.control_frame, text="Current Ref Path: " + self.ref_path)
        # self.ref_path_label.pack()


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
            new_n_replicates = int(float(self.n_replicates_entry.get()))
            # int() doesn't process scientific notation for strings, but float() does
            config = load_config_as_dict(self.config_path) 
            config['BasicRunConfiguration']['n_replicates'] = new_n_replicates 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "n_replicates changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for n_replicates.") 
