import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from tools import *


# TODO add line breaks to path rendering if too long, add None selected if path is empty

class Configurationv3:
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
        # self.control_frame.pack(fill='both', expand=True) 
        self.control_frame.pack(padx=10, pady=10)
        # self.control_frame.columnconfigure(0, minsize=80, weight = 0)
        # self.control_frame.grid_columnconfigure(0, minsize = 100, weight=1, pad = 100)
        # parent_widget.columnconfigure(column_index, minsize=min_width, weight=weight)

        # tree = ttk.Treeview(self.control_frame).grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.render_working_directory()
        self.render_ref_path_label()

        self.render_n_replicates()

                # self.control_frame.columnconfigure(0, minsize=80, weight = 0)

        render_next_button(self.tab_index, self.tab_parent, self.parent)
        

    def render_working_directory(self):
        def diagnostic_label_title():
            title = "Choose Working Directory"
            self.diagnostic_label_title = ttk.Label(self.control_frame, text=title)
            self.diagnostic_label_title.grid(row = 0, column = 0, sticky = 'W', pady = 2)

        def choose_directory_button():
            choose_directory_button = tk.Button(self.control_frame, text="Choose Directory", command=self.choose_directory)
            choose_directory_button.grid(row=2, column=0, sticky='e')


        # def diagnostic_label():
        #     # self.cwd = "/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff"
        #     self.diagnostic_label = ttk.Label(self.control_frame, text="Current Working Directory: " + self.cwd, background="black")
        #     self.diagnostic_label.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        # self.test = tk.StringVar(value = "bi-allele")
        # self.trans_type_combobox = ttk.Combobox(self.control_frame, foreground = "black", width = 23, textvariable=self.test, values=["bi-allele", "additive", "/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff"], state="disabled").grid(row=3, column=0, sticky='ew', padx=5, pady=5)

        # diagnostic_label_title()
        choose_directory_button()
        # diagnostic_label()

    def render_n_replicates(self):
        
        self.working_directory_label = ttk.Label(self.control_frame, text="Working Directory:", style="Bold.TLabel")
        self.working_directory_label.grid(row=0, column=0, pady=5, sticky='w')
        
        # self.n_replicates_label.grid(row=3, column=1, sticky='ew', padx=5, pady=5)
        if self.cwd == "":
            self.user_working_directory_label = ttk.Label(self.control_frame, text = "None Selected", foreground="black", width = minwidth)
        else:
            self.user_working_directory_label = ttk.Label(self.control_frame, text = self.cwd, foreground="black", width = minwidth)

        # self.n_replicates_entry.insert(0, self.n_replicates)
        # self.n_replicates_entry.insert(0, "/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff")
        # self.n_replicates_entry.delete(0, tk.END)
        # self.n_replicates_entry.configure(state="disabled")
        # self.n_replicates_entry.configure(state="normal")
        # self.n_replicates_entry.insert(0, 'new_text')
        new_width = len('/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff')
        # self.n_replicates_entry.config(width=new_width)
        # self.n_replicates_entry.configure(state="disabled")
        # self.n_replicates_entry.grid(row=4, column=0, sticky='ew', padx=5, pady=5)
        self.user_working_directory_label.grid(row=1, column=0, pady=5, sticky='w')
#         CreateToolTip(self.n_replicates_entry, \
#    '/Users/vivianzhao/Desktop/TB_software/tb-software/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.overlap.gff')
        update_n_replicates_button = tk.Button(self.control_frame, text="Update n_replicates", command=self.update_n_replicates)







        # update_n_replicates_button.grid(row=5, column=0, sticky='ew', padx=5, pady=5)
        self.n_replicates_label = ttk.Label(self.control_frame, text="Number of Simulation Replicates", style="Bold.TLabel")
        self.n_replicates_label2 = ttk.Label(self.control_frame, text="(Integer):")
        self.n_replicates_label.grid(row=7, column=0, sticky='w', pady=5)
        self.n_replicates_label2.grid(row=7, column=0, sticky='w', pady=5, padx=215)
        # self.n_replicates_label.pack()
        self.n_replicates_entry = ttk.Entry(self.control_frame, foreground="black", width = 20)
        self.n_replicates_entry.grid(row=8, column=0, sticky='w', pady=5)
        self.n_replicates_entry.insert(0, self.n_replicates)  
        # self.n_replicates_entry.pack()
        # update_n_replicates_button = tk.Button(self.control_frame, text="Update n_replicates", command=self.update_n_replicates)
        # update_n_replicates_button.pack()

        CreateToolTip(update_n_replicates_button, \
   'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, '
   'consectetur, adipisci velit. Neque porro quisquam est qui dolorem ipsum '
   'quia dolor sit amet, consectetur, adipisci velit. Neque porro quisquam '
   'est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.')
        
    def render_ref_path_label(self):
        ref_path_label = ttk.Label(self.control_frame, text="Pathogen Reference Genome File", style="Bold.TLabel")
        ref_path_label.grid(row=4, column=0, sticky='ew', pady=5)
        ref_path_label = ttk.Label(self.control_frame, text="(FASTA Format):")
        ref_path_label.grid(row=4, column=0, sticky='ew', pady=5, padx=220)
        # self.n_replicates_entry23 = ttk.Label(self.control_frame, text = self.ref_path, foreground="black", width = minwidth)
        if self.ref_path == "":
            self.ref_path_label = ttk.Label(self.control_frame, text = "None selected", foreground="black", width = minwidth)
        else:
            self.ref_path_label = ttk.Label(self.control_frame, text = self.ref_path, foreground="black", width = minwidth)




        self.ref_path_label.grid(row=5, column=0, pady=5, sticky='w')

        # choose_directory_button = tk.Button(self.control_frame, text="Choose Directory", command=self.choose_directory)
        # choose_directory_button.grid(row=2, column=0, sticky='e')
        choose_ref_path_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_ref_path)
        choose_ref_path_button.grid(row=6, column=0, sticky='e', pady=5)

        # self.ref_path_label = ttk.Label(self.control_frame, text="Current Ref Path: " + self.ref_path)
        # self.ref_path_label.grid(row=9, column=0, sticky='ew', padx=5, pady=5)
        
        # ref_path_label = ttk.Label(self.control_frame, text="Choose Ref Path")
        # ref_path_label.pack()
        # choose_ref_path_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_ref_path)
        # choose_ref_path_button.pack()
        # self.ref_path_label = ttk.Label(self.control_frame, text="Current Ref Path: " + self.ref_path)
        # self.ref_path_label.pack()


    def choose_directory(self):  
        chosen_directory = filedialog.askdirectory(title="Select a Directory")
        if chosen_directory:  
            self.cwd = chosen_directory
            self.user_working_directory_label.config(text=f"{self.cwd}")  # Update the label with the new directory
            config = load_config_as_dict(self.config_path)
            config['BasicRunConfiguration']['cwdir'] = self.cwd
            save_config(self.config_path, config)
     
    def choose_ref_path(self):  
        filetypes = ( #don't need to check if its genome file: or use python package jaehee said
            ("Genome files", ("*.fasta", "*.fa", "*.gb", "*.gtf", "*.vcf", "*.bam", "*.sam", "*.fna")),
            ("All files", "*.*")
        )
        # chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File", filetypes=filetypes)
        chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File")
        if chosen_file:  
            self.ref_path = chosen_file
            self.ref_path_label.config(text=self.ref_path) 
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
