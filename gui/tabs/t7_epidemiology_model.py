
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from utils import *

class EpidemiologyModel(TabBase):
    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):
        super().__init__(parent, tab_parent, config_path, tab_title, tab_index, hide)

    def init_tab(self, parent, tab_parent, tab_title, tab_index, hide):
        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_index = tab_index
        self.tab_parent.add(parent, text=tab_title)
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")
        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(padx=10, pady=10)
        
        # Modified part for scrolling
            # Testings
        self.canvas = tk.Canvas(self.control_frame)
        self.scrollbar = ttk.Scrollbar(self.control_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set, width=1300, height=700)
        
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


 

    def increment_frow(self, increment = True, by = 2):
        if increment:
            self.frow += by
        return self.frow

    def load_page(self):
        self.frow = 1
        hide = False
        to_renderer, to_derenderer = None, None
        self.render_model(hide, column=0, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_n_epoch(hide, column=1, columnspan= 1, frow = self.increment_frow(increment = False))
        # self.render_epoch_changing_generation(disabled = True)
        self.render_epoch_changing_generation(hide, column=0, columnspan= 3, frow = self.increment_frow())
        self.render_title("Evolutionary Components Setting", hide, 0, frow = self.increment_frow(), columnspan=3)
        self.render_transmissibility(hide, column=0, columnspan=1, frow = self.increment_frow(by = 1))
        self.render_cap_transmissibility(hide, column=2, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_cap_drugresist(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_drug_resistance(hide, column=2, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_title("Transition Rates between Compartments", hide, 0, frow = self.increment_frow(), columnspan=3)

        self.render_S_IE_rate(hide, column=0, columnspan=1, frow = self.increment_frow(by = 1))
        self.render_latency_prob(hide, column=1, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_E_R_rate(hide, column=2, columnspan=1, frow = self.increment_frow(increment = False))

        self.render_E_I_rate(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_I_E_rate(hide, column=0, columnspan=1, frow = self.increment_frow())

        self.render_I_R_rate(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_R_S_rate(hide, column=0, columnspan=1, frow = self.increment_frow())
        
        self.render_sample_rate(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_transition_rate_recovery_prob_after_sampling(hide, column=0, columnspan=1, frow = self.increment_frow())

        self.render_title("Massive Sampling Events", hide, 0, frow = self.increment_frow(), columnspan=3)

        self.render_massive_sampling(hide, column=0, columnspan=1, frow = self.increment_frow(by = 1))
        self.render_massive_sampling_generation(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_massive_sampling_probability(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_massive_sampling_after_sampling(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_super_infection(to_renderer, to_derenderer, hide, column=0, columnspan=1, frow = self.increment_frow())

    def init_val(self, config_path):
        self.config_path = config_path
        self.config_dict = load_config_as_dict(self.config_path)

        self.model = self.config_dict['EpidemiologyModel']['model']
        self.model_keys_path = ['EpidemiologyModel','model']
    
        self.n_epoch = self.config_dict['EpidemiologyModel']['epoch_changing']['n_epoch']
        self.n_epoch_keys_path = ['EpidemiologyModel','epoch_changing','n_epoch']
        self.epoch_changing_generation = self.config_dict['EpidemiologyModel']['epoch_changing']['epoch_changing_generation']
        self.epoch_changing_generation_keys_path = ['EpidemiologyModel','epoch_changing','epoch_changing_generation']
        self.transmissibility = self.config_dict['EpidemiologyModel']['genetic_architecture']['transmissibility']
        self.transmissibility_keys_path = ['EpidemiologyModel','genetic_architecture','transmissibility']
        self.cap_transmissibility = self.config_dict['EpidemiologyModel']['genetic_architecture']['cap_transmissibility']
        self.cap_transmissibility_keys_path = ['EpidemiologyModel','genetic_architecture','cap_transmissibility']
        self.drug_resistance = self.config_dict['EpidemiologyModel']['genetic_architecture']['drug_resistance']
        self.drug_resistance_keys_path = ['EpidemiologyModel','genetic_architecture','drug_resistance']
        self.cap_drugresist = self.config_dict['EpidemiologyModel']['genetic_architecture']['cap_drugresist']
        self.cap_drugresist_keys_path = ['EpidemiologyModel','genetic_architecture','cap_drugresist']
        self.S_IE_rate = self.config_dict['EpidemiologyModel']['transiton_rate']['S_IE_rate']
        self.S_IE_rate_keys_path = ['EpidemiologyModel','transiton_rate','S_IE_rate']
        self.I_R_rate = self.config_dict['EpidemiologyModel']['transiton_rate']['I_R_rate']
        self.I_R_rate_keys_path = ['EpidemiologyModel','transiton_rate','I_R_rate']
        self.R_S_rate = self.config_dict['EpidemiologyModel']['transiton_rate']['R_S_rate']
        self.R_S_rate_keys_path = ['EpidemiologyModel','transiton_rate','R_S_rate']
        self.latency_prob = self.config_dict['EpidemiologyModel']['transiton_rate']['latency_prob']
        self.latency_prob_keys_path = ['EpidemiologyModel','transiton_rate','latency_prob']
        self.E_I_rate = self.config_dict['EpidemiologyModel']['transiton_rate']['E_I_rate']
        self.E_I_rate_keys_path = ['EpidemiologyModel','transiton_rate','E_I_rate']
        self.I_E_rate = self.config_dict['EpidemiologyModel']['transiton_rate']['I_E_rate']
        self.I_E_rate_keys_path = ['EpidemiologyModel','transiton_rate','I_E_rate']
        self.E_R_rate = self.config_dict['EpidemiologyModel']['transiton_rate']['E_R_rate']
        self.E_R_rate_keys_path = ['EpidemiologyModel','transiton_rate','E_R_rate']
        self.sample_rate = self.config_dict['EpidemiologyModel']['transiton_rate']['sample_rate']
        self.sample_rate_keys_path = ['EpidemiologyModel','transiton_rate','sample_rate']
        self.transition_rate_recovery_prob_after_sampling = self.config_dict['EpidemiologyModel']['transiton_rate']['recovery_prob_after_sampling']
        self.transition_rate_recovery_prob_after_sampling_keys_path = ['EpidemiologyModel','transiton_rate','recovery_prob_after_sampling']

        self.event_num = self.config_dict['EpidemiologyModel']['massive_sampling']['event_num']
        self.event_num_keys_path = ['EpidemiologyModel','massive_sampling','event_num']
        self.generation = self.config_dict['EpidemiologyModel']['massive_sampling']['generation']
        self.generation_keys_path = ['EpidemiologyModel','massive_sampling','generation']
        self.sampling_prob = self.config_dict['EpidemiologyModel']['massive_sampling']['sampling_prob']
        self.sampling_prob_keys_path = ['EpidemiologyModel','massive_sampling','sampling_prob']
        self.massive_sampling_recovery_prob_after_sampling = self.config_dict['EpidemiologyModel']['massive_sampling']['recovery_prob_after_sampling']
        self.massive_sampling_recovery_prob_after_sampling_keys_path = ['EpidemiologyModel','massive_sampling','recovery_prob_after_sampling']
        self.super_infection = self.config_dict['EpidemiologyModel']['super_infection']
        self.super_infection_keys_path = ['EpidemiologyModel','super_infection']



    def render_model(self, hide, column, columnspan, frow):
        text = "Compartmental Model"
        keys_path = self.model_keys_path
        width = 50

        component = EasyCombobox(
            keys_path, self.config_path, 
            text,  
            self.scrollable_frame, column, frow, ["SIR", "SEIR"], None,None, None, hide, width , columnspan)

        self.visible_components.add(component)
        return component
        # """
        # self.model = load_config_as_dict(self.config_path)['EpidemiologyModel']['model']
        # """
        # def update_model():
        #     prev_val = self.model
        #     self.model = self.model_var.get()
        #     config = load_config_as_dict(self.config_path)
        #     keys_path = ['EpidemiologyModel', 'model']
        #     update_nested_dict(config, keys_path, self.model)
        #     save_config(self.config_path, config)
        #     if prev_val != self.model:
        #         messagebox.showinfo("Success", "Model updated successfully")
        # text = "Compartmental Model"
        # component = EasyCombobox(
        #     # self.model_keys_path,
        #     # self.config_path, text, 
        #     # self.control_frame, column, frow,
        #     # ["SIR", "SEIR"],
        #     # )
        # )
        # self.model_label = ttk.Label(self.scrollable_frame, text=self.render_model_text).grid()
        
        # self.model_var = tk.StringVar(value=get_dict_val(self.config_dict, self.model_keys_path))

        # self.model_combobox = ttk.Combobox(
        #     self.scrollable_frame, textvariable=self.model_var, 
        #     values=["SIR", "SEIR"], state="readonly"
        #     ).grid()
        
        # self.update_model_button = tk.Button(self.scrollable_frame, text="Update Method", command=update_model).grid()
    
    def render_seir(self):
        seir_controls = GroupControls()
        self.render_latency_prob()
        self.render_E_I_rate()
        self.render_I_E_rate()
        self.render_E_R_rate()
        return seir_controls
    
    def render_n_epoch(self, hide, column, columnspan, frow):
        text = "Number of Epochs (Integer)"
        keys_path = self.n_epoch_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'n_epoch', 
            self.scrollable_frame, column, frow, 'integer', hide, columnspan
            )

        self.visible_components.add(component)
        return component
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
        self.render_n_epoch_text = "Number of Epochs (Integer)"
        self.n_epoch_label = ttk.Label(self.scrollable_frame, text=self.render_n_epoch_text)
        self.n_epoch_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.n_epoch_entry.insert(0, self.n_epoch)  
        self.n_epoch_label.grid()
        self.n_epoch_entry.grid()
        # update_n_epoch_button = tk.Button(self.scrollable_frame, text="Update n_epoch", command=update_n_epoch)
        # update_n_epoch_button.grid()
    
    def render_epoch_changing_generation(self, hide, column, columnspan, frow):
        text = "On which generation(s) should the simulation go to the next epoch (List integer)"
        keys_path = self.epoch_changing_generation_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'epoch_changing_generation', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'epoch_changing', 'epoch_changing_generation']
            update_list_int_params(self.epoch_changing_generation_entry, keys_path, self.config_path)

        self.render_epoch_changing_generation_text = "On which generation(s) should the simulation go to the next epoch  (List integer)"
        self.epoch_changing_generation_label = ttk.Label(self.scrollable_frame, text=self.render_epoch_changing_generation_text)
        self.epoch_changing_generation_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.epoch_changing_generation_entry.insert(0, str(self.epoch_changing_generation))  
        self.epoch_changing_generation_label.grid()
        self.epoch_changing_generation_entry.grid()
        # self.update_epoch_changing_generation_button = tk.Button(self.scrollable_frame, text="Update epoch_changing_generation", command=update)
        # self.update_epoch_changing_generation_button.grid()
        if disabled:
            self.epoch_changing_generation_label.configure(state="disabled")
            self.epoch_changing_generation_entry.configure(foreground='light grey', state="disabled")
        else:
            self.epoch_changing_generation_entry.configure(state="normal")
            self.epoch_changing_generation_label.configure(foreground='black', state="normal")    
    
    def render_title(self, text, hide = True, column = None, frow = None, columnspan = 1):
        # self.render_tab_title(user_input_components, 5+3, 0, 3)
        component = EasyTitle(
            text,
            self.scrollable_frame, column, frow, hide, columnspan
        )
        self.visible_components.add(component)
        return component

    def render_transmissibility(self, hide, column, columnspan, frow):
        text = "Which transmissibility trait to use for each epoch (List integer)"
        keys_path = self.transmissibility_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'transmissibility', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'genetic_architecture', 'transmissibility']
            update_list_int_params(self.transmissibility_entry, keys_path, self.config_path)

        self.render_transmissibility_text = "Which transmissibility trait to use for each epoch (List integer)" 
        self.transmissibility_label = ttk.Label(self.scrollable_frame, text=self.render_transmissibility_text)
        self.transmissibility_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.transmissibility_entry.insert(0, str(self.transmissibility))  
        self.transmissibility_label.grid()
        self.transmissibility_entry.grid()
        

    def render_cap_transmissibility(self, hide, column, columnspan, frow):
        text = "The maximum transmissibility for each epoch (List Numerical)"
        keys_path = self.cap_transmissibility_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'cap_transmissibility', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'genetic_architecture', 'cap_transmissibility']
            update_list_int_params(self.cap_transmissibility_entry, keys_path, self.config_path)

        self.cap_transmissibility_label = ttk.Label(self.scrollable_frame, text="cap_transmissibility:")
        self.cap_transmissibility_label.grid()
        self.cap_transmissibility_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.cap_transmissibility_entry.insert(0, str(self.cap_transmissibility))  
        self.cap_transmissibility_entry.grid()

    def render_drug_resistance(self, hide, column, columnspan, frow):
        text = "Which drug-resistance trait to use for each epoch (List Integer)"
        keys_path = self.drug_resistance_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'drug_resistance', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'genetic_architecture', 'drug_resistance']
            update_list_int_params(self.drug_resistance_entry, keys_path, self.config_path)

        self.drug_resistance_label = ttk.Label(self.scrollable_frame, text="drug_resistance:")
        self.drug_resistance_label.grid()
        self.drug_resistance_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.drug_resistance_entry.insert(0, str(self.drug_resistance))  
        self.drug_resistance_entry.grid()

    def render_cap_drugresist(self, hide, column, columnspan, frow):
        text = "The maximum drug-resistance for each epoch (List Numerical)"
        keys_path = self.cap_drugresist_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'cap_drugresist', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'genetic_architecture', 'cap_drugresist']
            update_list_int_params(self.cap_drugresist_entry, keys_path, self.config_path)
        self.cap_drugresist_label = ttk.Label(self.scrollable_frame, text="cap_drugresist:")
        self.cap_drugresist_label.grid()
        self.cap_drugresist_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.cap_drugresist_entry.insert(0, str(self.cap_drugresist))  
        self.cap_drugresist_entry.grid()
        self.update_cap_drugresist_button = tk.Button(self.scrollable_frame, text="Update cap_drugresist", command=update)
        self.update_cap_drugresist_button.grid()   
 
    def render_S_IE_rate(self, hide, column, columnspan, frow):
        text = "Transmission Rate beta (list numerical)"
        keys_path = self.S_IE_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'S_IE_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'S_IE_rate']
            update_list_int_params(self.S_IE_rate_entry, keys_path, self.config_path)
        self.S_IE_rate_label = ttk.Label(self.scrollable_frame, text="S_IE_rate:")
        self.S_IE_rate_label.grid()
        self.S_IE_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.S_IE_rate_entry.insert(0, str(self.S_IE_rate))  
        self.S_IE_rate_entry.grid()
        self.update_S_IE_rate_button = tk.Button(self.scrollable_frame, text="Update S_IE_rate", command=update)
        self.update_S_IE_rate_button.grid()    

    def render_I_R_rate(self, hide, column, columnspan, frow):
        text = "Active Recovery rate gamma (list numerical)"
        keys_path = self.I_R_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'I_R_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'I_R_rate']
            update_list_int_params(self.I_R_rate_entry, keys_path, self.config_path)
        self.I_R_rate_label = ttk.Label(self.scrollable_frame, text="I_R_rate:")
        self.I_R_rate_label.grid()
        self.I_R_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.I_R_rate_entry.insert(0, str(self.I_R_rate))  
        self.I_R_rate_entry.grid()
        self.update_I_R_rate_button = tk.Button(self.scrollable_frame, text="Update I_R_rate", command=update)
        self.update_I_R_rate_button.grid()  

    def render_R_S_rate(self, hide, column, columnspan, frow):
        text = "Immunity loss rate \u03C9 (list numerical)"
        keys_path = self.latency_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'R_S_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'R_S_rate']
            update_list_int_params(self.R_S_rate_entry, keys_path, self.config_path)
        self.R_S_rate_label = ttk.Label(self.scrollable_frame, text="R_S_rate:")
        self.R_S_rate_label.grid()
        self.R_S_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.R_S_rate_entry.insert(0, str(self.R_S_rate))  
        self.R_S_rate_entry.grid()
        self.update_R_S_rate_button = tk.Button(self.scrollable_frame, text="Update R_S_rate", command=update)
        self.update_R_S_rate_button.grid()  

    def render_latency_prob(self, hide, column, columnspan, frow):
        text = "Latency Probability p (list numerical)"
        keys_path = self.latency_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'latency_prob', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'latency_prob']
            update_list_int_params(self.latency_prob_entry, keys_path, self.config_path)
        self.latency_prob_label = ttk.Label(self.scrollable_frame, text="latency_prob:")
        self.latency_prob_label.grid()
        self.latency_prob_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.latency_prob_entry.insert(0, str(self.latency_prob))  
        self.latency_prob_entry.grid()
        self.update_latency_prob_button = tk.Button(self.scrollable_frame, text="Update latency_prob", command=update)
        self.update_latency_prob_button.grid()    
        components.add(self.latency_prob_label)
        components.add(self.latency_prob_entry)

    def render_E_I_rate(self, hide, column, columnspan, frow):
        text = "Activation rate v (list numerical)"
        keys_path = self.E_I_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'E_I_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'E_I_rate']
            update_list_int_params(self.E_I_rate_entry, keys_path, self.config_path)
        self.E_I_rate_label = ttk.Label(self.scrollable_frame, text="E_I_rate:")
        self.E_I_rate_label.grid()
        self.E_I_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.E_I_rate_entry.insert(0, str(self.E_I_rate))  
        self.E_I_rate_entry.grid()
        self.update_E_I_rate_button = tk.Button(self.scrollable_frame, text="Update E_I_rate", command=update)
        self.update_E_I_rate_button.grid() 

    def render_I_E_rate(self, hide, column, columnspan, frow):
        text = "De-activation rate \phi (list numerical)"
        keys_path = self.I_E_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'I_E_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'I_E_rate']
            update_list_int_params(self.I_E_rate_entry, keys_path, self.config_path)
        self.I_E_rate_label = ttk.Label(self.scrollable_frame, text="I_E_rate:")
        self.I_E_rate_label.grid()
        self.I_E_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.I_E_rate_entry.insert(0, str(self.I_E_rate))  
        self.I_E_rate_entry.grid()
        self.update_I_E_rate_button = tk.Button(self.scrollable_frame, text="Update I_E_rate", command=update)
        self.update_I_E_rate_button.grid()  

    def render_E_R_rate(self, hide, column, columnspan, frow):
        text = "Latent Recovery Rate \tau (list numerical)"
        keys_path = self.E_R_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'E_R_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'E_R_rate']
            update_list_int_params(self.E_R_rate_entry, keys_path, self.config_path)
        self.E_R_rate_label = ttk.Label(self.scrollable_frame, text="E_R_rate:")
        self.E_R_rate_label.grid()
        self.E_R_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.E_R_rate_entry.insert(0, str(self.E_R_rate))  
        self.E_R_rate_entry.grid()
        self.update_E_R_rate_button = tk.Button(self.scrollable_frame, text="Update E_R_rate", command=update)
        self.update_E_R_rate_button.grid()   
        
    def render_sample_rate(self, hide, column, columnspan, frow):
        text = "Sample Rate \epsilon (List Numerical)"
        keys_path = self.sample_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'sample_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'sample_rate']
            update_list_int_params(self.sample_rate_entry, keys_path, self.config_path)
        self.sample_rate_label = ttk.Label(self.scrollable_frame, text="sample_rate:")
        self.sample_rate_label.grid()
        self.sample_rate_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.sample_rate_entry.insert(0, str(self.sample_rate))  
        self.sample_rate_entry.grid()
        self.update_sample_rate_button = tk.Button(self.scrollable_frame, text="Update sample_rate", command=update)
        self.update_sample_rate_button.grid()

    def render_transition_rate_recovery_prob_after_sampling(self, hide, column, columnspan, frow):
        text = "Recovery Probability after Sampling \delta (List Numerical)"
        keys_path = self.transition_rate_recovery_prob_after_sampling_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'recovery_prob_after_sampling', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'transiton_rate', 'recovery_prob_after_sampling']
            update_list_int_params(self.transition_rate_recovery_prob_after_sampling_entry, keys_path, self.config_path)
        self.transition_rate_recovery_prob_after_sampling_label = ttk.Label(self.scrollable_frame, text="transition_rate_recovery_prob_after_sampling:")
        self.transition_rate_recovery_prob_after_sampling_label.grid()
        self.transition_rate_recovery_prob_after_sampling_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.transition_rate_recovery_prob_after_sampling_entry.insert(0, str(self.transition_rate_recovery_prob_after_sampling))  
        self.transition_rate_recovery_prob_after_sampling_entry.grid()
        self.update_transition_rate_recovery_prob_after_sampling_button = tk.Button(self.scrollable_frame, text="Update transition_rate_recovery_prob_after_sampling", command=update)
        self.update_transition_rate_recovery_prob_after_sampling_button.grid()

    def render_massive_sampling(self, hide, column, columnspan, frow):
        text = "How many massive sampling events will be simulated (Integer)"
        keys_path = self.event_num_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'event_num', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'massive_sampling', 'event_num']
            update_list_int_params(self.massive_sampling_entry, keys_path, self.config_path)
        self.massive_sampling_label = ttk.Label(self.scrollable_frame, text="massive_sampling:")
        self.massive_sampling_label.grid()
        self.massive_sampling_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.massive_sampling_entry.insert(0, self.event_num)  
        self.massive_sampling_entry.grid()
        update_massive_sampling_button = tk.Button(self.scrollable_frame, text="Update massive_sampling", command=update)
        update_massive_sampling_button.grid()    

    def render_massive_sampling_generation(self, hide, column, columnspan, frow):
        text = "In which generation (s) will the massive sampling events be simulated (List integer)"
        keys_path = self.generation_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'massive_sampling_generation', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        """
        self.generation = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['generation']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'massive_sampling', 'generation']
            update_list_int_params(self.massive_sampling_generation_entry, keys_path, self.config_path)
        self.massive_sampling_generation_label = ttk.Label(self.scrollable_frame, text="massive_sampling_generation:")
        self.massive_sampling_generation_label.grid()
        self.massive_sampling_generation_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.massive_sampling_generation_entry.insert(0, str(self.generation))  
        self.massive_sampling_generation_entry.grid()
        self.update_massive_sampling_generation_button = tk.Button(self.scrollable_frame, text="Update massive_sampling_generation", command=update)
        self.update_massive_sampling_generation_button.grid()      
    def render_massive_sampling_probability(self, hide, column, columnspan, frow):
        text = "Probability of being sampled for every pathogen genome in each massive sample event (List Numerical)"
        keys_path = self.sampling_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'sampling_prob', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        """
        self.sampling_prob = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['sampling_prob']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'massive_sampling', 'sampling_prob']
            update_list_int_params(self.massive_sampling_probability_entry, keys_path, self.config_path)
        self.massive_sampling_probability_label = ttk.Label(self.scrollable_frame, text="massive_sampling_probability:")
        self.massive_sampling_probability_label.grid()
        self.massive_sampling_probability_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.massive_sampling_probability_entry.insert(0, str(self.sampling_prob))  
        self.massive_sampling_probability_entry.grid()
        self.update_massive_sampling_probability_button = tk.Button(self.scrollable_frame, text="Update massive_sampling_probability", command=update)
        self.update_massive_sampling_probability_button.grid()   

    def render_massive_sampling_after_sampling(self, hide, column, columnspan, frow):
        text = "Probability of Recovering Once Sampled in each Massive Sampling Event (List Numerical)"
        keys_path = self.massive_sampling_recovery_prob_after_sampling_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'recovery_prob_after_sampling', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        """
        self.massive_sampling_recovery_prob_after_sampling = load_config_as_dict(self.config_path)['EpidemiologyModel']['massive_sampling']['recovery_prob_after_sampling']
        list of floats
        """
        def update():
            keys_path = ['EpidemiologyModel', 'massive_sampling', 'recovery_prob_after_sampling']
            update_list_int_params(self.massive_sampling_after_sampling_entry, keys_path, self.config_path)
            
        self.massive_sampling_after_sampling_label = ttk.Label(self.scrollable_frame, text="massive_sampling_after_sampling:")
        self.massive_sampling_after_sampling_label.grid()
        self.massive_sampling_after_sampling_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.massive_sampling_after_sampling_entry.insert(0, str(self.massive_sampling_recovery_prob_after_sampling))  
        self.massive_sampling_after_sampling_entry.grid()
        self.update_massive_sampling_after_sampling_button = tk.Button(self.scrollable_frame, text="Update massive_sampling_after_sampling", command=update)
        self.update_massive_sampling_after_sampling_button.grid()      
    
    def render_super_infection(self, to_rerender, to_derender, hide = True, column = None, frow = None, columnspan = 1):
        keys_path = self.super_infection_keys_path
        text = "Do you want to enable super-infection events?"
        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)

        component = EasyRadioButton(
            keys_path, self.config_path, 
            text, "use_reference", 
            self.scrollable_frame, column, 
            frow, hide, 
            to_rerender, to_derender,
            columnspan, radiobuttonselected
            )
        
        self.visible_components.add(component)
        return component
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
        self.super_infection_label.grid()
        self.super_infection_var = tk.StringVar(value=bool_to_string_mapping[self.super_infection])
        self.super_infection_combobox = ttk.Combobox(
            self.scrollable_frame, textvariable=self.super_infection_var, 
            values=["Yes", "No"], state="readonly"
            )
        
        self.super_infection_combobox.grid()
        self.update_super_infection_button = tk.Button(self.scrollable_frame, text="Update Method", command=update)
        self.update_super_infection_button.grid()
