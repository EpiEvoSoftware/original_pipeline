
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class EpidemiologyModel:
    def __init__(self, parent, tab_parent, config_path):

        self.config_path = config_path

    # Epidemiology Model Configurations
        self.model = self.load_config_as_dict()['EpidemiologyModel']['model']

    # epoch changing
        self.n_epoch = self.load_config_as_dict()['EpidemiologyModel']['epoch_changing']['n_epoch']
        self.epoch_changing_generation = self.load_config_as_dict()['EpidemiologyModel']['epoch_changing']['epoch_changing_generation']
    # genetic_architecture
        self.transmissibility = self.load_config_as_dict()['EpidemiologyModel']['genetic_architecture']['transmissibility']
        self.cap_transmissibility = self.load_config_as_dict()['EpidemiologyModel']['genetic_architecture']['cap_transmissibility']
        self.drug_resistance = self.load_config_as_dict()['EpidemiologyModel']['genetic_architecture']['drug_resistance']
        self.cap_drugresist = self.load_config_as_dict()['EpidemiologyModel']['genetic_architecture']['cap_drugresist']

    # transition_rate
        self.S_IE_rate = self.load_config_as_dict()['EpidemiologyModel']['transiton_rate']['S_IE_rate']
        self.I_R_rate = self.load_config_as_dict()['EpidemiologyModel']['transiton_rate']['I_R_rate']
        self.R_S_rate = self.load_config_as_dict()['EpidemiologyModel']['transiton_rate']['R_S_rate']
        self.latency_prob = self.load_config_as_dict()['EpidemiologyModel']['transiton_rate']['latency_prob']
        self.E_I_rate = self.load_config_as_dict()['EpidemiologyModel']['transiton_rate']['E_I_rate']
        self.I_E_rate = self.load_config_as_dict()['EpidemiologyModel']['transiton_rate']['I_E_rate']
        self.E_R_rate = self.load_config_as_dict()['EpidemiologyModel']['transiton_rate']['E_R_rate']
        self.sample_rate = self.load_config_as_dict()['EpidemiologyModel']['transiton_rate']['sample_rate']
        self.transition_rate_recovery_prob_after_sampling = self.load_config_as_dict()['EpidemiologyModel']['transiton_rate']['recovery_prob_after_sampling']

    # massive_sampling
        self.event_num = self.load_config_as_dict()['EpidemiologyModel']['massive_sampling']['event_num']
        self.generation = self.load_config_as_dict()['EpidemiologyModel']['massive_sampling']['generation']
        self.sampling_prob = self.load_config_as_dict()['EpidemiologyModel']['massive_sampling']['sampling_prob']
        self.massive_sampling_recovery_prob_after_sampling = self.load_config_as_dict()['EpidemiologyModel']['massive_sampling']['recovery_prob_after_sampling']

        self.parent = parent
        self.tab_parent = tab_parent
        self.dynamic_widgets = []
        
        self.control_frame = ttk.Frame(self.parent)
        self.control_frame.pack(fill='both', expand=True)

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

        self.render_all()

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


    def render_all(self):
        self.render_model()
        self.render_n_epoch()
        self.render_epoch_changing_generation()
        self.render_transmissibility()
        
        self.render_cap_transmissibility()

        self.render_cap_drugresist()
            
        self.render_drug_resistance()
                
       
                
        self.render_S_IE_rate()
                
        self.render_I_R_rate()
                
        self.render_R_S_rate()
                
        self.render_latency_prob()
                
        self.render_E_I_rate()
                
        self.render_I_E_rate()
                
        self.render_E_R_rate()
                
        self.render_sample_rate()
                
        self.render_transition_rate_recovery_prob_after_sampling()
                
        self.render_massive_sampling()
                
        self.render_massive_sampling_generation()
                
        self.render_massive_sampling_probability()
                
        self.render_massive_sampling_after_sampling()
                
        
        self.render_super_infection()
          

    def update_generic(self):
        return
    
    def render_model(self):
        self.model_label = ttk.Label(self.scrollable_frame, text="model:")
        self.model_label.pack()
        self.model_var = tk.StringVar(value=self.model)
        self.model_combobox = ttk.Combobox(
            self.scrollable_frame, textvariable=self.model_var, 
            values=["SIR", "SEIR"], state="readonly"
            )
        self.model_combobox.pack()
        self.update_model_button = tk.Button(self.scrollable_frame, text="Update Method", command=self.update_generic)
        self.update_model_button.pack()
    
    def render_n_epoch(self):
        self.n_epoch_label = ttk.Label(self.scrollable_frame, text="n_epoch:")
        self.n_epoch_label.pack()
        self.n_epoch_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.n_epoch_entry.insert(0, self.n_epoch)  
        self.n_epoch_entry.pack()
        update_n_epoch_button = tk.Button(self.scrollable_frame, text="Update n_epoch", command=self.update_generic)
        update_n_epoch_button.pack()
    
    def render_epoch_changing_generation(self):
        self.epoch_changing_generation_label = ttk.Label(self.scrollable_frame, text="epoch_changing_generation:")
        self.epoch_changing_generation_label.pack()
        self.epoch_changing_generation_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.epoch_changing_generation_entry.insert(0, str(self.epoch_changing_generation))  
        self.epoch_changing_generation_entry.pack()
        self.update_epoch_changing_generation_button = tk.Button(self.scrollable_frame, text="Update epoch_changing_generation", command=self.update_generic)
        self.update_epoch_changing_generation_button.pack()
    
    def render_transmissibility(self):
        self.transmissibility_label = ttk.Label(self.scrollable_frame, text="transmissibility:")
        self.transmissibility_label.pack()
        self.transmissibility_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.transmissibility_entry.insert(0, str(self.transmissibility))  
        self.transmissibility_entry.pack()
        self.update_transmissibility_button = tk.Button(self.scrollable_frame, text="Update transmissibility", command=self.update_generic)
        self.update_transmissibility_button.pack()
    def render_cap_transmissibility(self):
        self.cap_transmissibility_label = ttk.Label(self.scrollable_frame, text="cap_transmissibility:")
        self.cap_transmissibility_label.pack()
        self.cap_transmissibility_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.cap_transmissibility_entry.insert(0, str(self.cap_transmissibility))  
        self.cap_transmissibility_entry.pack()
        self.update_cap_transmissibility_button = tk.Button(self.scrollable_frame, text="Update cap_transmissibility", command=self.update_generic)
        self.update_cap_transmissibility_button.pack()
    def render_cap_drugresist(self):
        self.cap_drugresist_label = ttk.Label(self.scrollable_frame, text="cap_drugresist:")
        self.cap_drugresist_label.pack()
        self.cap_drugresist_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.cap_drugresist_entry.insert(0, str(self.cap_drugresist))  
        self.cap_drugresist_entry.pack()
        self.update_cap_drugresist_button = tk.Button(self.scrollable_frame, text="Update cap_drugresist", command=self.update_generic)
        self.update_cap_drugresist_button.pack()   
    def render_drug_resistance(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
 
    def render_S_IE_rate(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
    def render_I_R_rate(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
    def render_R_S_rate(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
    def render_latency_prob(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
    def render_E_I_rate(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
    def render_I_E_rate(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
    def render_E_R_rate(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
    def render_sample_rate(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
    def render_transition_rate_recovery_prob_after_sampling(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()    
    def render_massive_sampling(self):
        self.massive_sampling_label = ttk.Label(self.scrollable_frame, text="massive_sampling:")
        self.massive_sampling_label.pack()
        self.massive_sampling_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.massive_sampling_entry.insert(0, self.event_num)  
        self.massive_sampling_entry.pack()
        update_massive_sampling_button = tk.Button(self.scrollable_frame, text="Update massive_sampling", command=self.update_generic)
        update_massive_sampling_button.pack()    
    def render_massive_sampling_generation(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()      
    def render_massive_sampling_probability(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()      
    def render_massive_sampling_after_sampling(self):
        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.pack()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.pack()
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=self.update_generic)
        self.update_drug_resistance_button.pack()      
    
    def render_super_infection(self):
        self.model_label = ttk.Label(self.scrollable_frame, text="model:")
        self.model_label.pack()
        self.model_var = tk.StringVar(value=self.model)
        self.model_combobox = ttk.Combobox(
            self.scrollable_frame, textvariable=self.model_var, 
            values=["Yes", "No"], state="readonly"
            )
        self.model_combobox.pack()
        self.update_model_button = tk.Button(self.scrollable_frame, text="Update Method", command=self.update_generic)
        self.update_model_button.pack()
