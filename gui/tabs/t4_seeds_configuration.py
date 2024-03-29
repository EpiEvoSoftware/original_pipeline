
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
from tools import *
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(os.path.dirname(current_dir), '../codes')
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from seed_generator import *


# TODO: seed_size = len(seeded_host_id), validate
class SeedsConfiguration:
    def __init__(self, parent, tab_parent, config_path):

        self.config_path = config_path

        # SeedsConfiguration
        self.seed_size = load_config_as_dict(self.config_path)['SeedsConfiguration']['seed_size']
        self.method = load_config_as_dict(self.config_path)['SeedsConfiguration']['method']

        # user_input
        self.path_seeds_vcf = load_config_as_dict(self.config_path)['SeedsConfiguration']['user_input']['path_seeds_vcf']
        self.path_seeds_phylogeny = load_config_as_dict(self.config_path)['SeedsConfiguration']['user_input']["path_seeds_phylogeny"]

        # SLiM_burnin_WF
        self.burn_in_Ne = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_Ne']
        self.burn_in_generations_wf = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_generations']
        self.burn_in_mutrate_wf = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_mutrate']

        # SLiM_burnin_epi
        self.burn_in_generations_epi = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_generations']
        self.burn_in_mutrate_epi = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_mutrate']
        self.seeded_host_id = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["seeded_host_id"]
        self.S_IE_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["S_IE_rate"]
        self.E_I_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["E_I_rate"]
        self.E_R_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["E_R_rate"]
        self.latency_prob = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["latency_prob"]
        self.I_R_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['I_R_rate']
        self.I_E_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['I_E_rate']
        self.R_S_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['R_S_rate']

        self.parent = parent
        self.tab_parent = tab_parent
        self.dynamic_widgets = []
        
        self.control_frame = ttk.Frame(self.parent)
        self.control_frame.pack(fill='both', expand=True)


        # Modified part for scrolling
            # Testings
        self.canvas = tk.Canvas(self.control_frame)
        self.scrollbar = ttk.Scrollbar(self.control_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        def configure_scroll_region(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        def configure_canvas_width(event):
            self.canvas.itemconfig(self.canvas_frame, width=event.width)
        
        self.scrollable_frame.bind("<Configure>", configure_scroll_region)
        self.canvas.bind("<Configure>", configure_canvas_width)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
            # Testing End
        # 




        # seed_size:
        self.seed_size_label = ttk.Label(self.scrollable_frame, text="seed_size:")
        self.seed_size_label.pack()
        self.seed_size_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.seed_size_entry.insert(0, self.seed_size)  
        self.seed_size_entry.pack()
        update_seed_size_button = tk.Button(self.scrollable_frame, text="Update seed_size", command=self.update_seed_size)
        update_seed_size_button.pack()
        # end of seed_size

        # Method:
        self.use_method_label = ttk.Label(self.scrollable_frame, text="method:")
        self.use_method_label.pack()
        self.use_method_var = tk.StringVar(value=self.method)
        self.use_method_combobox = ttk.Combobox(
            self.scrollable_frame, textvariable=self.use_method_var, 
            values=["user_input", "SLiM_burnin_WF", "SLiM_burnin_epi"], state="readonly"
            )
        self.use_method_combobox.pack()
        update_use_method_button = tk.Button(self.scrollable_frame, text="Update Method", command=self.update_use_method)
        update_use_method_button.pack()

        if self.method == "user_input":
            return
            self.method_label = ttk.Label(self.control_frame, text="method:")
            self.method_label.pack()
            self.method_var = tk.StringVar()
            self.method_combobox = ttk.Combobox(self.control_frame, textvariable=self.method_var, values=["randomly generate", "user_input"], state="readonly")
            self.method_combobox.pack()
            self.update_method_button = tk.Button(self.control_frame, text="Update method", command=self.update_method)
            self.update_method_button.pack()
        elif self.method == "SLiM_burnin_WF":
            return
        elif self.method == "SLiM_burnin_epi":
            return
        # End of Method



        # Next Button
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

    def update_use_method(self):
        new_use_method = self.use_method_var.get()
        if new_use_method in ["user_input", "SLiM_burnin_WF", "SLiM_burnin_epi"]: 
            config = load_config_as_dict(self.config_path)
            config['SeedsConfiguration']['method'] = new_use_method
            save_config(self.config_path, config)

            if new_use_method == "user_input":
                if not hasattr(self, 'path_seeds_vcf_label'):  # create the label if it doesn't exist
                    # Hide other labels if initialized
                    self.hide_elements()
                    # 

                    # Labels Creating
                    self.path_seeds_vcf_label = ttk.Label(self.scrollable_frame, text="Choose path_seeds_vcf")
                    self.path_seeds_vcf_label.pack()
                    self.choose_path_seeds_vcf_button = tk.Button(self.scrollable_frame, text="Choose path_seeds_vcf", command=self.choose_and_update_path_seeds_vcf)
                    self.choose_path_seeds_vcf_button.pack()
                    self.path_seeds_vcf_indicator = ttk.Label(self.scrollable_frame, text="Current path_seeds_vcf: " + self.path_seeds_vcf)
                    self.path_seeds_vcf_indicator.pack()
                else:
                    # Hide other labels if initialized
                    self.hide_elements()
                    #

                    # show the label if it was previously created
                    self.path_seeds_vcf_label.pack()
                    self.choose_path_seeds_vcf_button.pack()
                    self.path_seeds_vcf_indicator.pack()
                    

            elif new_use_method == "SLiM_burnin_WF":
                if not hasattr(self, 'burn_in_Ne_label'):  # create the label if it doesn't exist
                    # Hide other labels if initialized
                    self.hide_elements()
                    # 

                    # burn_in_Ne, burn_in_generations_wf, burn_in_mutrate_wf
                    self.burn_in_Ne_label = ttk.Label(self.scrollable_frame, text="burn_in_Ne:")
                    self.burn_in_Ne_label.pack()
                    self.burn_in_Ne_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.burn_in_Ne_entry.insert(0, self.burn_in_Ne)  
                    self.burn_in_Ne_entry.pack()
                    self.update_burn_in_Ne_button = tk.Button(self.scrollable_frame, text="Update burn_in_Ne", command=self.update_burn_in_Ne)
                    self.update_burn_in_Ne_button.pack()

                    # burn_in_generations_wf
                    self.burn_in_generations_wf_label = ttk.Label(self.scrollable_frame, text="burn_in_generations_wf:")
                    self.burn_in_generations_wf_label.pack()
                    self.burn_in_generations_wf_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.burn_in_generations_wf_entry.insert(0, self.burn_in_generations_wf)  
                    self.burn_in_generations_wf_entry.pack()
                    self.update_burn_in_generations_wf_button = tk.Button(self.scrollable_frame, text="Update burn_in_generations_wf", command=self.update_burn_in_generations_wf)
                    self.update_burn_in_generations_wf_button.pack()

                    # burn_in_mutrate_wf
                    self.burn_in_mutrate_wf_label = ttk.Label(self.scrollable_frame, text="burn_in_mutrate_wf:")
                    self.burn_in_mutrate_wf_label.pack()
                    self.burn_in_mutrate_wf_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.burn_in_mutrate_wf_entry.insert(0, self.burn_in_mutrate_wf)  
                    self.burn_in_mutrate_wf_entry.pack()
                    self.update_burn_in_mutrate_wf_button = tk.Button(self.scrollable_frame, text="Update burn_in_mutrate_wf", command=self.update_burn_in_mutrate_wf)
                    self.update_burn_in_mutrate_wf_button.pack()
                else: # Show the label if it was previously created
                    # Hide other labels if initialized
                    self.hide_elements()
                    # 

                    # Show Labels
                    self.burn_in_Ne_label.pack()
                    self.burn_in_Ne_entry.pack()
                    self.update_burn_in_Ne_button.pack()

                    self.burn_in_generations_wf_label.pack()
                    self.burn_in_generations_wf_entry.pack()
                    self.update_burn_in_generations_wf_button.pack()

                    self.burn_in_mutrate_wf_label.pack()
                    self.burn_in_mutrate_wf_entry.pack()
                    self.update_burn_in_mutrate_wf_button.pack()
                    

            elif new_use_method == "SLiM_burnin_epi":
                if not hasattr(self, 'burn_in_generations_epi_label'):  # create the label if it doesn't exist
                    self.hide_elements()
                    
                    # self.burn_in_generations_epi = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_generations']
                    self.burn_in_generations_epi_label = ttk.Label(self.scrollable_frame, text="burn_in_generations:")
                    self.burn_in_generations_epi_label.pack()
                    self.burn_in_generations_epi_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.burn_in_generations_epi_entry.insert(0, self.burn_in_generations_epi)  
                    self.burn_in_generations_epi_entry.pack()
                    self.update_burn_in_generations_epi_button = tk.Button(self.scrollable_frame, text="Update burn_in_generations", command=self.update_burn_in_generations_epi)
                    self.update_burn_in_generations_epi_button.pack()
                    # 

                    # self.burn_in_mutrate_epi = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_mutrate']
                    self.burn_in_mutrate_epi_label = ttk.Label(self.scrollable_frame, text="burn_in_mutrate_epi:")
                    self.burn_in_mutrate_epi_label.pack()
                    self.burn_in_mutrate_epi_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.burn_in_mutrate_epi_entry.insert(0, self.burn_in_mutrate_epi)  
                    self.burn_in_mutrate_epi_entry.pack()
                    self.update_burn_in_mutrate_epi_button = tk.Button(self.scrollable_frame, text="Update burn_in_mutrate_epi", command=self.update_burn_in_mutrate_epi)
                    self.update_burn_in_mutrate_epi_button.pack()
                    # 

                    # self.seeded_host_id = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["seeded_host_id"]
                    self.seeded_host_id_label = ttk.Label(self.scrollable_frame, text="seeded_host_id:")
                    self.seeded_host_id_label.pack()
                    self.seeded_host_id_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.seeded_host_id_entry.insert(0, str(self.seeded_host_id))  
                    self.seeded_host_id_entry.pack()
                    self.update_seeded_host_id_button = tk.Button(self.scrollable_frame, text="Update seeded_host_id", command=self.update_seeded_host_id)
                    self.update_seeded_host_id_button.pack()
                    # 

                    # self.S_IE_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["S_IE_rate"]
                    self.S_IE_rate_label = ttk.Label(self.scrollable_frame, text="S_IE_rate:")
                    self.S_IE_rate_label.pack()
                    self.S_IE_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.S_IE_rate_entry.insert(0, self.S_IE_rate)  
                    self.S_IE_rate_entry.pack()
                    self.update_S_IE_rate_button = tk.Button(self.scrollable_frame, text="Update S_IE_rate", command=self.update_S_IE_rate)
                    self.update_S_IE_rate_button.pack()
                    # 

                    # self.E_I_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["E_I_rate"]
                    self.E_I_rate_label = ttk.Label(self.scrollable_frame, text="E_I_rate:")
                    self.E_I_rate_label.pack()
                    self.E_I_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.E_I_rate_entry.insert(0, self.E_I_rate)  
                    self.E_I_rate_entry.pack()
                    self.update_E_I_rate_button = tk.Button(self.scrollable_frame, text="Update E_I_rate", command=self.update_E_I_rate)
                    self.update_E_I_rate_button.pack()
                    # 

                    # self.E_R_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["E_R_rate"]
                    self.E_R_rate_label = ttk.Label(self.scrollable_frame, text="E_R_rate:")
                    self.E_R_rate_label.pack()
                    self.E_R_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.E_R_rate_entry.insert(0, self.E_R_rate)  
                    self.E_R_rate_entry.pack()
                    self.update_E_R_rate_button = tk.Button(self.scrollable_frame, text="Update E_R_rate", command=self.update_E_R_rate)
                    self.update_E_R_rate_button.pack()
                    # 

                    # self.latency_prob = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["latency_prob"]
                    self.latency_prob_label = ttk.Label(self.scrollable_frame, text="latency_prob:")
                    self.latency_prob_label.pack()
                    self.latency_prob_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.latency_prob_entry.insert(0, self.latency_prob)  
                    self.latency_prob_entry.pack()
                    self.update_latency_prob_button = tk.Button(self.scrollable_frame, text="Update latency_prob", command=self.update_latency_prob)
                    self.update_latency_prob_button.pack()
                    #                     

                    # self.I_R_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['I_R_rate']
                    self.I_R_rate_label = ttk.Label(self.scrollable_frame, text="I_R_rate:")
                    self.I_R_rate_label.pack()
                    self.I_R_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.I_R_rate_entry.insert(0, self.I_R_rate)  
                    self.I_R_rate_entry.pack()
                    self.update_I_R_rate_button = tk.Button(self.scrollable_frame, text="Update I_R_rate", command=self.update_I_R_rate)
                    self.update_I_R_rate_button.pack()
                    # 

                    # self.I_E_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['I_E_rate']
                    self.I_E_rate_label = ttk.Label(self.scrollable_frame, text="I_E_rate:")
                    self.I_E_rate_label.pack()
                    self.I_E_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.I_E_rate_entry.insert(0, self.I_E_rate)  
                    self.I_E_rate_entry.pack()
                    self.update_I_E_rate_button = tk.Button(self.scrollable_frame, text="Update I_E_rate", command=self.update_I_E_rate)
                    self.update_I_E_rate_button.pack()
                    # 

                    # self.R_S_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['R_S_rate']
                    self.R_S_rate_label = ttk.Label(self.scrollable_frame, text="R_S_rate:")
                    self.R_S_rate_label.pack()
                    self.R_S_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.R_S_rate_entry.insert(0, self.R_S_rate)  
                    self.R_S_rate_entry.pack()
                    self.update_R_S_rate_button = tk.Button(self.scrollable_frame, text="Update R_S_rate", command=self.update_R_S_rate)
                    self.update_R_S_rate_button.pack()
                    # 

                else:
                    self.hide_elements()
                    # show the label if it was previously created
                    self.burn_in_generations_epi_label.pack()
                    self.burn_in_generations_epi_entry.pack()
                    self.update_burn_in_generations_epi_button.pack()

                    self.burn_in_mutrate_epi_label.pack()
                    self.burn_in_mutrate_epi_entry.pack()
                    self.update_burn_in_mutrate_epi_button.pack()
                    
                    self.seeded_host_id_label.pack()
                    self.seeded_host_id_entry.pack()
                    self.update_seeded_host_id_button.pack()
                    
                    self.S_IE_rate_label.pack()
                    self.S_IE_rate_entry.pack()
                    self.update_S_IE_rate_button.pack()
                    
                    self.E_I_rate_label.pack()
                    self.E_I_rate_entry.pack()
                    self.update_E_I_rate_button.pack()
                    
                    self.E_R_rate_label.pack()
                    self.E_R_rate_entry.pack()
                    self.update_E_R_rate_button.pack()
                    
                    self.latency_prob_label.pack()
                    self.latency_prob_entry.pack()
                    self.update_latency_prob_button.pack()
                    
                    self.I_R_rate_label.pack()
                    self.I_R_rate_entry.pack()
                    self.update_I_R_rate_button.pack()
                    
                    self.I_E_rate_label.pack()
                    self.I_E_rate_entry.pack()
                    self.update_I_E_rate_button.pack()
                    
                    self.R_S_rate_label.pack()
                    self.R_S_rate_entry.pack()
                    self.update_R_S_rate_button.pack()

            self.render_run_button()
            messagebox.showinfo("Update Successful", "method changed.")
        else:
            messagebox.showerror("Update Error", "Please enter a valid entry for method.")

    def choose_network_path(self):  
        chosen_path = filedialog.askdirectory(title="Select a Directory")
        if chosen_path:  
            self.network_path = chosen_path
            self.network_path_label = ttk.Label(self.scrollable_frame, text="Current Network Path: " + self.network_path)
            self.network_path_label.pack()
            self.network_path_label.config(text=f"Path Network: {self.network_path}") 
            config = load_config_as_dict(self.config_path)
            config['SeedsConfiguration']['user_input']["path_network"] = self.network_path
            save_config(self.config_path, config)
    
    def choose_and_update_path_seeds_vcf(self):  
        filetypes = ( #don't need to check if its genome file: or use python package jaehee said
            ("Genome files", ("*.fasta", "*.fa", "*.gb", "*.gtf", "*.vcf", "*.bam", "*.sam", "*.fna")),
            ("All files", "*.*")
        )
        chosen_file = filedialog.askopenfilename(title="Select a path_seeds_vcf", filetypes=filetypes)
        if chosen_file:  
            self.path_seeds_vcf = chosen_file
            self.path_seeds_vcf_indicator.config(text=f"choose_path_seeds_vcf: {self.path_seeds_vcf}") 
            config = load_config_as_dict(self.config_path)
            config['SeedsConfiguration']['user_input']['path_seeds_vcf'] = self.path_seeds_vcf
            save_config(self.config_path, config)


    def update_seed_size(self):
        try:
            new_seed_size = int(float(self.seed_size_entry.get()))  
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['seed_size'] = new_seed_size 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "seed_size changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for seed_size.") 

    def update_burn_in_Ne(self):
        try:
            new_burn_in_Ne = int(float(self.burn_in_Ne_entry.get()))
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_Ne'] = new_burn_in_Ne 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "burn_in_Ne changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for burn_in_Ne.") 
    
    def update_burn_in_generations_wf(self):
        try:
            new_burn_in_generations_wf = int(float(self.burn_in_generations_wf_entry.get()))
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_generations'] = new_burn_in_generations_wf 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "burn_in_generations_wf changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for burn_in_generations_wf.") 


    def update_burn_in_mutrate_wf(self):
        try:
            new_burn_in_mutrate_wf = float(self.burn_in_mutrate_wf_entry.get())  
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_mutrate'] = new_burn_in_mutrate_wf 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "burn_in_mutrate_wf changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for burn_in_mutrate_wf.") 



    # EPI
    def update_burn_in_generations_epi(self):
        try:
            new_burn_in_generations_epi = int(float(self.burn_in_generations_epi_entry.get()))
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_generations'] = new_burn_in_generations_epi
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "burn_in_generations changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for burn_in_generations.") 

    def update_burn_in_mutrate_epi(self):
        try:
            new_burn_in_mutrate_epi = float(self.burn_in_mutrate_epi_entry.get())  
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_generations'] = new_burn_in_mutrate_epi 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "burn_in_mutrate_epi changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid float for burn_in_mutrate_epi.") 

    def update_seeded_host_id(self):
        try:
            new_seeded_host_id = self.seeded_host_id_entry.get().strip()
            cleaned_input = new_seeded_host_id.strip("[]").strip()
            
            if cleaned_input == "":
                parsed_new_seeded_host_id = []
            elif cleaned_input.isdigit():
                parsed_new_seeded_host_id = [int(float(cleaned_input))]
            elif "," in new_seeded_host_id:
                parsed_new_seeded_host_id = [int(float(item.strip())) for item in cleaned_input.split(',')]
            else:
                raise ValueError("Invalid input format.")
                    

            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['seeded_host_id'] = parsed_new_seeded_host_id
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "burn_in_generations changed.")  
        except ValueError: # This catches cases where conversion to integer fails
            messagebox.showerror("Update Error", "Please enter a valid list of integers for seeded_host_id, separated by commas.")
        except Exception as e: # General error handling (e.g., file operation failures)
            messagebox.showerror("Update Error", str(e))           

    def update_S_IE_rate(self):
        try:
            new_S_IE_rate = float(self.S_IE_rate_entry.get())  
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['S_IE_rate'] = new_S_IE_rate 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "S_IE_rate changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid float for S_IE_rate.") 
        except Exception as e: # General error handling (e.g., file operation failures)
            messagebox.showerror("Update Error", str(e))    

    def update_E_I_rate(self):
        try:
            new_E_I_rate = float(self.E_I_rate_entry.get())  
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['E_I_rate'] = new_E_I_rate 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "E_I_rate changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid float for E_I_rate.") 
        except Exception as e: # General error handling (e.g., file operation failures)
            messagebox.showerror("Update Error", str(e))    

    def update_E_R_rate(self):
        try:
            new_E_R_rate = float(self.E_R_rate_entry.get())  
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['E_R_rate'] = new_E_R_rate 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "E_R_rate changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid float for E_R_rate.") 
        except Exception as e: # General error handling (e.g., file operation failures)
            messagebox.showerror("Update Error", str(e))    

    def update_latency_prob(self):
        try:
            new_latency_prob = int(float(self.latency_prob_entry.get()))
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['latency_prob'] = new_latency_prob 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "latency_prob changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid float for latency_prob.") 
        except Exception as e: # General error handling (e.g., file operation failures)
            messagebox.showerror("Update Error", str(e))    

    def update_I_R_rate(self):
        try:
            new_I_R_rate = float(self.I_R_rate_entry.get())  
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['I_R_rate'] = new_I_R_rate 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "I_R_rate changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid float for I_R_rate.") 
        except Exception as e: # General error handling (e.g., file operation failures)
            messagebox.showerror("Update Error", str(e))    

    def update_I_E_rate(self):
        try:
            new_I_E_rate = float(self.I_E_rate_entry.get())  
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['I_E_rate'] = new_I_E_rate 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "I_E_rate changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid float for I_E_rate.") 
        except Exception as e: # General error handling (e.g., file operation failures)
            messagebox.showerror("Update Error", str(e))    

    def update_R_S_rate(self):
        try:
            new_R_S_rate = float(self.R_S_rate_entry.get())  
            config = load_config_as_dict(self.config_path) 
            config['SeedsConfiguration']['SLiM_burnin_epi']['R_S_rate'] = new_R_S_rate 
            save_config(self.config_path, config)  
            messagebox.showinfo("Update Successful", "R_S_rate changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid float for R_S_rate.") 
        except Exception as e: # General error handling (e.g., file operation failures)
            messagebox.showerror("Update Error", str(e))                
    def hide_elements(self):
        if hasattr(self, 'path_seeds_vcf_label'):
            # new_use_method == "SLiM_burnin_WF":
            self.path_seeds_vcf_label.pack_forget()
            self.choose_path_seeds_vcf_button.pack_forget()
            self.path_seeds_vcf_indicator.pack_forget()
            # 
        if hasattr(self, 'burn_in_Ne_label'):
            # new_use_method == "SLiM_burnin_WF":
            self.burn_in_Ne_label.pack_forget()
            self.burn_in_Ne_entry.pack_forget()
            self.update_burn_in_Ne_button.pack_forget()

            self.burn_in_generations_wf_label.pack_forget()
            self.burn_in_generations_wf_entry.pack_forget()
            self.update_burn_in_generations_wf_button.pack_forget()

            self.burn_in_mutrate_wf_label.pack_forget()
            self.burn_in_mutrate_wf_entry.pack_forget()
            self.update_burn_in_mutrate_wf_button.pack_forget()
            # 

        if hasattr(self, 'burn_in_generations_epi_label'):
            # new_use_method == "SLiM_burnin_epi":
            self.burn_in_generations_epi_label.pack_forget()
            self.burn_in_generations_epi_entry.pack_forget()
            self.update_burn_in_generations_epi_button.pack_forget()

            self.burn_in_mutrate_epi_label.pack_forget()
            self.burn_in_mutrate_epi_entry.pack_forget()
            self.update_burn_in_mutrate_epi_button.pack_forget()
            
            self.seeded_host_id_label.pack_forget()
            self.seeded_host_id_entry.pack_forget()
            self.update_seeded_host_id_button.pack_forget()
            
            self.S_IE_rate_label.pack_forget()
            self.S_IE_rate_entry.pack_forget()
            self.update_S_IE_rate_button.pack_forget()
            
            self.E_I_rate_label.pack_forget()
            self.E_I_rate_entry.pack_forget()
            self.update_E_I_rate_button.pack_forget()
            
            self.E_R_rate_label.pack_forget()
            self.E_R_rate_entry.pack_forget()
            self.update_E_R_rate_button.pack_forget()
            
            self.latency_prob_label.pack_forget()
            self.latency_prob_entry.pack_forget()
            self.update_latency_prob_button.pack_forget()
            
            self.I_R_rate_label.pack_forget()
            self.I_R_rate_entry.pack_forget()
            self.update_I_R_rate_button.pack_forget()
            
            self.I_E_rate_label.pack_forget()
            self.I_E_rate_entry.pack_forget()
            self.update_I_E_rate_button.pack_forget()
            
            self.R_S_rate_label.pack_forget()
            self.R_S_rate_entry.pack_forget()
            self.update_R_S_rate_button.pack_forget()
    def render_run_button(self):
        def seed_generation():
            config = load_config_as_dict(self.config_path)
            cwdir = config["BasicRunConfiguration"]["cwdir"]
            seed_size = config["SeedsConfiguration"]["seed_size"]
            method = config["SeedsConfiguration"]["method"]
            ref_path = "/Users/vivianzhao/Desktop/TB_software/TB_software_new/original_pipeline/test/data/TB/GCF_000195955.2_ASM19595v2_genomic.fna"
            
            if method == "SLiM_burnin_WF":
                Ne = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_Ne"]
                n_gen = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_generations"]
                mu = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_mutrate"]
                run_seed_generation(method=method, wk_dir=cwdir, seed_size=seed_size, Ne=Ne,
                                    mu=mu, n_gen=n_gen, ref_path=ref_path)
            elif method == "SLiM_burnin_epi":
                n_gen = config["SeedsConfiguration"]["SLiM_burnin_epi"]["burn_in_generations"]
                mu = config["SeedsConfiguration"]["SLiM_burnin_epi"]["burn_in_mutrate"]
                seeded_host_id = config["SeedsConfiguration"]["SLiM_burnin_epi"]["seeded_host_id"]
                S_IE_rate = config["SeedsConfiguration"]["SLiM_burnin_epi"]["S_IE_rate"]
                E_I_rate = config["SeedsConfiguration"]["SLiM_burnin_epi"]["E_I_rate"]
                E_R_rate = config["SeedsConfiguration"]["SLiM_burnin_epi"]["E_R_rate"]
                latency_prob = config["SeedsConfiguration"]["SLiM_burnin_epi"]["latency_prob"]
                I_R_rate = config["SeedsConfiguration"]["SLiM_burnin_epi"]["I_R_rate"]
                I_E_rate = config["SeedsConfiguration"]["SLiM_burnin_epi"]["I_E_rate"]
                R_S_rate = config["SeedsConfiguration"]["SLiM_burnin_epi"]["R_S_rate"]
                host_size = config["NetworkModelParameters"]["host_size"]
                
                run_seed_generation(method=method, wk_dir=cwdir, seed_size=seed_size, mu=mu, n_gen=n_gen, 
                            seeded_host_id=seeded_host_id, S_IE_rate=S_IE_rate, E_I_rate=E_I_rate,
                            E_R_rate=E_R_rate, latency_prob=latency_prob, I_R_rate=I_R_rate, 
                            I_E_rate=I_E_rate, R_S_rate=R_S_rate, host_size=host_size, ref_path=ref_path)

            elif method == "user_input":
                path_seeds_vcf = config["SeedsConfiguration"]["user_input"]["path_seeds_vcf"]
                path_seeds_phylogeny = config["SeedsConfiguration"]["user_input"]["path_seeds_phylogeny"]
                run_seed_generation(method=method, wk_dir=cwdir, seed_size=seed_size, seed_vcf=path_seeds_vcf, 
                                    path_seeds_phylogeny=path_seeds_phylogeny)

        self.run_seed_generation_button = tk.Button(self.scrollable_frame, text="Run Seed Generation", command=seed_generation)
        self.run_seed_generation_button.pack()
