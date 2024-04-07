
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from utils import *

class EpidemiologyModelv3:
    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):
        self.config_path = config_path

    # Epidemiology Model Configurations
        self.model = load_config_as_dict(self.config_path)['EpidemiologyModel']['model']

    # epoch changing
        self.n_epoch = load_config_as_dict(self.config_path)['EpidemiologyModel']['epoch_changing']['n_epoch']
        self.epoch_changing_generation = load_config_as_dict(self.config_path)['EpidemiologyModel']['epoch_changing']['epoch_changing_generation']
    # genetic_architecture
        self.transmissibility = load_config_as_dict(self.config_path)['EpidemiologyModel']['genetic_architecture']['transmissibility']
        self.cap_transmissibility = load_config_as_dict(self.config_path)['EpidemiologyModel']['genetic_architecture']['cap_transmissibility']
        self.drug_resistance = load_config_as_dict(self.config_path)['EpidemiologyModel']['genetic_architecture']['drug_resistance']
        self.cap_drugresist = load_config_as_dict(self.config_path)['EpidemiologyModel']['genetic_architecture']['cap_drugresist']

    # transition_rate
        self.S_IE_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['S_IE_rate']
        self.I_R_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['I_R_rate']
        self.R_S_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['R_S_rate']
        self.latency_prob = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['latency_prob']
        self.E_I_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['E_I_rate']
        self.I_E_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['I_E_rate']
        self.E_R_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['E_R_rate']
        self.sample_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['sample_rate']
        self.transition_rate_recovery_prob_after_sampling = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['recovery_prob_after_sampling']

    # massive_sampling
        self.event_num = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['event_num']
        self.generation = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['generation']
        self.sampling_prob = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['sampling_prob']
        self.massive_sampling_recovery_prob_after_sampling = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['recovery_prob_after_sampling']

        self.super_infection = load_config_as_dict(self.config_path)['EpidemiologyModel']['super_infection']

        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_parent.add(parent, text=tab_title)
        self.tab_index = tab_index
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")
        
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
        columns = ('Name', 'Column 2', 'Column 3', 'Column 4', 'Column 5')

        tree = ttk.Treeview(self.scrollable_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        tree.tag_configure('oddrow', background='white')  
        tree.tag_configure('evenrow', background='#F0F0F0')  
        
        for i in range(1, len(columns) + 1):
            values = [f'Row {i} Value {j}' for j in range(1, 6)]
            
            if i % 2 == 0:
                tree.insert('', 'end', values=values, tags=('evenrow',))
            else:
                tree.insert('', 'end', values=values, tags=('oddrow',))

        tree.pack(expand=True, fill='both')

        self.render_all()

        render_next_button(self.tab_index, self.tab_parent, self.parent)

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

    def render_model(self):
        """
        self.model = load_config_as_dict(self.config_path)['EpidemiologyModel']['model']
        """
        def update_model():
            prev_val = self.model
            self.model = self.model_var.get()
            config = load_config_as_dict(self.config_path)
            keys_path = ['EpidemiologyModel', 'model']
            update_nested_dict(config, keys_path, self.model)
            save_config(self.config_path, config)
            if prev_val != self.model:
                messagebox.showinfo("Success", "Model updated successfully")

        self.model_label = ttk.Label(self.scrollable_frame, text="model:")
        self.model_var = tk.StringVar(value=self.model)

        self.model_combobox = ttk.Combobox(
            self.scrollable_frame, textvariable=self.model_var, 
            values=["SIR", "SEIR"], state="readonly"
            )
        
        self.update_model_button = tk.Button(self.scrollable_frame, text="Update Method", command=update_model)
    
    def render_n_epoch(self):
        """
        self.n_epoch = load_config_as_dict(self.config_path)['EpidemiologyModel']['epoch_changing']['n_epoch']
        int
        """
        def update_n_epoch():
            try:
                prev_val = self.n_epoch
                self.n_epoch = int(float(self.n_epoch_entry.get()))
                config = load_config_as_dict(self.config_path)
                keys_path = ['EpidemiologyModel', 'epoch_changing', 'n_epoch']
                update_nested_dict(config, keys_path, self.n_epoch)
                save_config(self.config_path, config)
                if prev_val != self.n_epoch:
                    messagebox.showinfo("Success", "Updated successfully") 
            except ValueError:
                messagebox.showerror("Update Error", "Please enter a valid number.") 
            except Exception as e: 
                messagebox.showerror("Update Error", str(e))

        self.n_epoch_label = ttk.Label(self.scrollable_frame, text="n_epoch:")
        self.n_epoch_label
        self.n_epoch_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.n_epoch_entry.insert(0, self.n_epoch)  
        self.n_epoch_entry
        update_n_epoch_button = tk.Button(self.scrollable_frame, text="Update n_epoch", command=update_n_epoch)
        update_n_epoch_button
    
    def render_epoch_changing_generation(self):
        """
        self.epoch_changing_generation = load_config_as_dict(self.config_path)['EpidemiologyModel']['epoch_changing']['epoch_changing_generation']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'epoch_changing', 'epoch_changing_generation']
            update_list_int_params(self.epoch_changing_generation_entry, keys_path, self.config_path)

        self.epoch_changing_generation_label = ttk.Label(self.scrollable_frame, text="epoch_changing_generation:")
        self.epoch_changing_generation_label
        self.epoch_changing_generation_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.epoch_changing_generation_entry.insert(0, str(self.epoch_changing_generation))  
        self.epoch_changing_generation_entry
        self.update_epoch_changing_generation_button = tk.Button(self.scrollable_frame, text="Update epoch_changing_generation", command=update)
        self.update_epoch_changing_generation_button
    
    def render_transmissibility(self):
        """
        self.transmissibility = load_config_as_dict(self.config_path)['EpidemiologyModel']['genetic_architecture']['transmissibility']
        list of ints
        """
        def update():
            keys_path = ['EpidemiologyModel', 'genetic_architecture', 'transmissibility']
            update_list_int_params(self.transmissibility_entry, keys_path, self.config_path)

        self.transmissibility_label = ttk.Label(self.scrollable_frame, text="transmissibility:")
        self.transmissibility_label
        self.transmissibility_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.transmissibility_entry.insert(0, str(self.transmissibility))  
        self.transmissibility_entry
        self.update_transmissibility_button = tk.Button(self.scrollable_frame, text="Update transmissibility", command=update)
        self.update_transmissibility_button

    def render_cap_transmissibility(self):
        """
        self.cap_transmissibility = load_config_as_dict(self.config_path)['EpidemiologyModel']['genetic_architecture']['cap_transmissibility']
        """
        def update():
            keys_path = ['EpidemiologyModel', 'genetic_architecture', 'cap_transmissibility']
            update_list_int_params(self.cap_transmissibility_entry, keys_path, self.config_path)

        self.cap_transmissibility_label = ttk.Label(self.scrollable_frame, text="cap_transmissibility:")
        self.cap_transmissibility_label
        self.cap_transmissibility_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.cap_transmissibility_entry.insert(0, str(self.cap_transmissibility))  
        self.cap_transmissibility_entry
        self.update_cap_transmissibility_button = tk.Button(self.scrollable_frame, text="Update cap_transmissibility", command=update)
        self.update_cap_transmissibility_button

    def render_drug_resistance(self):
        """
        self.drug_resistance = load_config_as_dict(self.config_path)['EpidemiologyModel']['genetic_architecture']['drug_resistance']
        """
        def update():
            keys_path = ['EpidemiologyModel', 'genetic_architecture', 'drug_resistance']
            update_list_int_params(self.drug_resistance_entry, keys_path, self.config_path)

        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry
        self.update_drug_resistance_button = tk.Button(self.scrollable_frame, text="Update drug_resistance", command=update)
        self.update_drug_resistance_button    

    def render_cap_drugresist(self):
        """
        self.cap_drugresist = load_config_as_dict(self.config_path)['EpidemiologyModel']['genetic_architecture']['cap_drugresist']
        """
        def update():
            keys_path = ['EpidemiologyModel', 'genetic_architecture', 'cap_drugresist']
            update_list_int_params(self.cap_drugresist_entry, keys_path, self.config_path)
        self.cap_drugresist_label = ttk.Label(self.scrollable_frame, text="cap_drugresist:")
        self.cap_drugresist_label
        self.cap_drugresist_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.cap_drugresist_entry.insert(0, str(self.cap_drugresist))  
        self.cap_drugresist_entry
        self.update_cap_drugresist_button = tk.Button(self.scrollable_frame, text="Update cap_drugresist", command=update)
        self.update_cap_drugresist_button   
 
    def render_S_IE_rate(self):
        """
        self.S_IE_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['S_IE_rate']
        """
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'S_IE_rate']
            update_list_int_params(self.S_IE_rate_entry, keys_path, self.config_path)
        self.S_IE_rate_label = ttk.Label(self.scrollable_frame, text="S_IE_rate:")
        self.S_IE_rate_label
        self.S_IE_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.S_IE_rate_entry.insert(0, str(self.S_IE_rate))  
        self.S_IE_rate_entry
        self.update_S_IE_rate_button = tk.Button(self.scrollable_frame, text="Update S_IE_rate", command=update)
        self.update_S_IE_rate_button    

    def render_I_R_rate(self):
        """
        self.I_R_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['I_R_rate']
        """
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'I_R_rate']
            update_list_int_params(self.I_R_rate_entry, keys_path, self.config_path)
        self.I_R_rate_label = ttk.Label(self.scrollable_frame, text="I_R_rate:")
        self.I_R_rate_label
        self.I_R_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.I_R_rate_entry.insert(0, str(self.I_R_rate))  
        self.I_R_rate_entry
        self.update_I_R_rate_button = tk.Button(self.scrollable_frame, text="Update I_R_rate", command=update)
        self.update_I_R_rate_button  

    def render_R_S_rate(self):
        """
        self.R_S_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['R_S_rate']
        """
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'R_S_rate']
            update_list_int_params(self.R_S_rate_entry, keys_path, self.config_path)
        self.R_S_rate_label = ttk.Label(self.scrollable_frame, text="R_S_rate:")
        self.R_S_rate_label
        self.R_S_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.R_S_rate_entry.insert(0, str(self.R_S_rate))  
        self.R_S_rate_entry
        self.update_R_S_rate_button = tk.Button(self.scrollable_frame, text="Update R_S_rate", command=update)
        self.update_R_S_rate_button  

    def render_latency_prob(self):
        """
        self.latency_prob = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['latency_prob']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'latency_prob']
            update_list_int_params(self.latency_prob_entry, keys_path, self.config_path)
        self.latency_prob_label = ttk.Label(self.scrollable_frame, text="latency_prob:")
        self.latency_prob_label
        self.latency_prob_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.latency_prob_entry.insert(0, str(self.latency_prob))  
        self.latency_prob_entry
        self.update_latency_prob_button = tk.Button(self.scrollable_frame, text="Update latency_prob", command=update)
        self.update_latency_prob_button    

    def render_E_I_rate(self):
        """
        self.E_I_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['E_I_rate']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'E_I_rate']
            update_list_int_params(self.E_I_rate_entry, keys_path, self.config_path)
        self.E_I_rate_label = ttk.Label(self.scrollable_frame, text="E_I_rate:")
        self.E_I_rate_label
        self.E_I_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.E_I_rate_entry.insert(0, str(self.E_I_rate))  
        self.E_I_rate_entry
        self.update_E_I_rate_button = tk.Button(self.scrollable_frame, text="Update E_I_rate", command=update)
        self.update_E_I_rate_button 

    def render_I_E_rate(self):
        """
        self.I_E_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['I_E_rate']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'I_E_rate']
            update_list_int_params(self.I_E_rate_entry, keys_path, self.config_path)
        self.I_E_rate_label = ttk.Label(self.scrollable_frame, text="I_E_rate:")
        self.I_E_rate_label
        self.I_E_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.I_E_rate_entry.insert(0, str(self.I_E_rate))  
        self.I_E_rate_entry
        self.update_I_E_rate_button = tk.Button(self.scrollable_frame, text="Update I_E_rate", command=update)
        self.update_I_E_rate_button  

    def render_E_R_rate(self):
        """
        self.E_R_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['E_R_rate']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'E_R_rate']
            update_list_int_params(self.E_R_rate_entry, keys_path, self.config_path)
        self.E_R_rate_label = ttk.Label(self.scrollable_frame, text="E_R_rate:")
        self.E_R_rate_label
        self.E_R_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.E_R_rate_entry.insert(0, str(self.E_R_rate))  
        self.E_R_rate_entry
        self.update_E_R_rate_button = tk.Button(self.scrollable_frame, text="Update E_R_rate", command=update)
        self.update_E_R_rate_button   
        
    def render_sample_rate(self):
        """
        self.sample_rate = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['sample_rate']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'sample_rate']
            update_list_int_params(self.sample_rate_entry, keys_path, self.config_path)
        self.sample_rate_label = ttk.Label(self.scrollable_frame, text="sample_rate:")
        self.sample_rate_label
        self.sample_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.sample_rate_entry.insert(0, str(self.sample_rate))  
        self.sample_rate_entry
        self.update_sample_rate_button = tk.Button(self.scrollable_frame, text="Update sample_rate", command=update)
        self.update_sample_rate_button

    def render_transition_rate_recovery_prob_after_sampling(self):
        """
        self.transition_rate_recovery_prob_after_sampling = load_config_as_dict(self.config_path)['EpidemiologyModel']['transiton_rate']['recovery_prob_after_sampling']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'recovery_prob_after_sampling']
            update_list_int_params(self.transition_rate_recovery_prob_after_sampling_entry, keys_path, self.config_path)
        self.transition_rate_recovery_prob_after_sampling_label = ttk.Label(self.scrollable_frame, text="transition_rate_recovery_prob_after_sampling:")
        self.transition_rate_recovery_prob_after_sampling_label
        self.transition_rate_recovery_prob_after_sampling_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.transition_rate_recovery_prob_after_sampling_entry.insert(0, str(self.transition_rate_recovery_prob_after_sampling))  
        self.transition_rate_recovery_prob_after_sampling_entry
        self.update_transition_rate_recovery_prob_after_sampling_button = tk.Button(self.scrollable_frame, text="Update transition_rate_recovery_prob_after_sampling", command=update)
        self.update_transition_rate_recovery_prob_after_sampling_button

    def render_massive_sampling(self):
        """
        self.event_num = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['event_num']
        list of ints
        """
        def update():
            keys_path = ['EpidemiologyModel', 'massive_sampling', 'event_num']
            update_list_int_params(self.massive_sampling_entry, keys_path, self.config_path)
        self.massive_sampling_label = ttk.Label(self.scrollable_frame, text="massive_sampling:")
        self.massive_sampling_label
        self.massive_sampling_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.massive_sampling_entry.insert(0, self.event_num)  
        self.massive_sampling_entry
        update_massive_sampling_button = tk.Button(self.scrollable_frame, text="Update massive_sampling", command=update)
        update_massive_sampling_button    

    def render_massive_sampling_generation(self):
        """
        self.generation = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['generation']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'massive_sampling', 'generation']
            update_list_int_params(self.massive_sampling_generation_entry, keys_path, self.config_path)
        self.massive_sampling_generation_label = ttk.Label(self.scrollable_frame, text="massive_sampling_generation:")
        self.massive_sampling_generation_label
        self.massive_sampling_generation_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.massive_sampling_generation_entry.insert(0, str(self.generation))  
        self.massive_sampling_generation_entry
        self.update_massive_sampling_generation_button = tk.Button(self.scrollable_frame, text="Update massive_sampling_generation", command=update)
        self.update_massive_sampling_generation_button      
    def render_massive_sampling_probability(self):
        """
        self.sampling_prob = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['sampling_prob']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'massive_sampling', 'sampling_prob']
            update_list_int_params(self.massive_sampling_probability_entry, keys_path, self.config_path)
        self.massive_sampling_probability_label = ttk.Label(self.scrollable_frame, text="massive_sampling_probability:")
        self.massive_sampling_probability_label
        self.massive_sampling_probability_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.massive_sampling_probability_entry.insert(0, str(self.sampling_prob))  
        self.massive_sampling_probability_entry
        self.update_massive_sampling_probability_button = tk.Button(self.scrollable_frame, text="Update massive_sampling_probability", command=update)
        self.update_massive_sampling_probability_button   

    def render_massive_sampling_after_sampling(self):
        """
        self.massive_sampling_recovery_prob_after_sampling = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['recovery_prob_after_sampling']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'massive_sampling', 'recovery_prob_after_sampling']
            update_list_int_params(self.massive_sampling_after_sampling_entry, keys_path, self.config_path)
            
        self.massive_sampling_after_sampling_label = ttk.Label(self.scrollable_frame, text="massive_sampling_after_sampling:")
        self.massive_sampling_after_sampling_label
        self.massive_sampling_after_sampling_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.massive_sampling_after_sampling_entry.insert(0, str(self.massive_sampling_recovery_prob_after_sampling))  
        self.massive_sampling_after_sampling_entry
        self.update_massive_sampling_after_sampling_button = tk.Button(self.scrollable_frame, text="Update massive_sampling_after_sampling", command=update)
        self.update_massive_sampling_after_sampling_button      
    
    def render_super_infection(self):
        """
        self.super_infection = load_config_as_dict(self.config_path)['EpidemiologyModel']['super_infection']
        yes/no
        """
        def update():
            prev_val = self.super_infection
            self.super_infection = string_to_bool_mapping[self.super_infection_var.get()]
            config = load_config_as_dict(self.config_path)
            keys_path = ['EpidemiologyModel', 'super_infection']
            update_nested_dict(config, keys_path, self.super_infection)
            save_config(self.config_path, config)
            if prev_val != self.super_infection:
                messagebox.showinfo("Success", "Updated successfully") 

        self.super_infection_label = ttk.Label(self.scrollable_frame, text="super_infection:")
        self.super_infection_label
        self.super_infection_var = tk.StringVar(value=bool_to_string_mapping[self.super_infection])
        self.super_infection_combobox = ttk.Combobox(
            self.scrollable_frame, textvariable=self.super_infection_var, 
            values=["Yes", "No"], state="readonly"
            )
        
        self.super_infection_combobox
        self.update_super_infection_button = tk.Button(self.scrollable_frame, text="Update Method", command=update)
        self.update_super_infection_button
