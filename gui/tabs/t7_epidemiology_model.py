
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
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
        for i in range(4):  
            self.scrollable_frame.columnconfigure(i, weight=1)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        def configure_scroll_region(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        def configure_canvas_width(event):
            self.canvas.itemconfig(self.canvas_frame, width=event.width)
        
        self.scrollable_frame.bind("<Configure>", configure_scroll_region)
        self.canvas.bind("<Configure>", configure_canvas_width)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        


 

    def increment_frow(self, increment = True, by = 2):
        if increment:
            self.frow += by
        return self.frow

    def load_page(self):
        self.frow = 1
        hide = False
        to_renderer, to_derenderer = None, None
        
        self.render_slim_path_label(hide, column=1, columnspan=2, frow = self.increment_frow(increment = False))
        self.render_model(hide, column=0, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_n_epoch(hide, column=1, columnspan= 1, frow = self.increment_frow())
        # self.render_epoch_changing_generation(disabled = True)
        self.render_epoch_changing_generation(hide, column=0, columnspan= 3, frow = self.increment_frow(increment = False))
        self.render_title("Evolutionary Components Setting", hide, 0, frow = self.increment_frow(), columnspan=3)
        self.render_transmissibility(hide, column=0, columnspan=1, frow = self.increment_frow(by = 1))
        self.render_cap_transmissibility(hide, column=1, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_cap_drugresist(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_drug_resistance(hide, column=1, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_title("Transition Rates between Compartments", hide, 0, frow = self.increment_frow(), columnspan=3)

        self.render_S_IE_rate(hide, column=0, columnspan=1, frow = self.increment_frow(by = 1))
        self.render_latency_prob(hide, column=1, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_E_R_rate(hide, column=2, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_image(hide, image_path="assets/t7.png", desired_width=600, desired_height=300, column = 1, columnspan=2, frow = self.increment_frow())

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
        self.slim_path = self.config_dict['EpidemiologyModel']['slim_replicate_seed_file_path']
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
    
    def render_seir(self):
        seir_controls = GroupControls()
        self.render_latency_prob()
        self.render_E_I_rate()
        self.render_I_E_rate()
        self.render_E_R_rate()
        self.render_image()
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
    
    def render_slim_path_label(self, hide = True, column = None, frow = None, columnspan = 1):
        self.render_slim_path_text = "Slim Replicate Seed File Path"
        keys_path = ['EpidemiologyModel', 'slim_replicate_seed_file_path']
        component = EasyPathSelector(
            keys_path,
            self.config_path, 
            self.render_slim_path_text, 
            self.scrollable_frame, 
            column, hide, frow, columnspan
            )
        
        self.visible_components.add(component)
        return component
    
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

 
    def render_S_IE_rate(self, hide, column, columnspan, frow):
        text = "Transmission Rate β (list numerical)"
        keys_path = self.S_IE_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'S_IE_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component

    def render_I_R_rate(self, hide, column, columnspan, frow):
        text = "Active Recovery rate γ (list numerical)"
        keys_path = self.I_R_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'I_R_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component

    def render_R_S_rate(self, hide, column, columnspan, frow):
        text = "Immunity loss rate ω (list numerical)"
        keys_path = self.latency_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'R_S_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component

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

    def render_I_E_rate(self, hide, column, columnspan, frow):
        text = r'De-activation rate φ (list numerical)'
        keys_path = self.I_E_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'I_E_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
 

    def render_E_R_rate(self, hide, column, columnspan, frow):
        text = "Latent Recovery Rate τ (list numerical)"
        keys_path = self.E_R_rate_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'E_R_rate', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component 
    
    def render_image(self, hide, image_path, desired_width, desired_height, column, columnspan, frow):
        component = EasyImage(
            image_path, desired_width, 
            desired_height, hide, 
            self.scrollable_frame, frow, 
            column, columnspan, 
            rowspan=10
            )
        self.visible_components.add(component)
        return component
        
        
    def render_sample_rate(self, hide, column, columnspan, frow):
        text = r"Sample Rate ε (List Numerical)"
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
        text = r"Recovery Probability after Sampling δ (List Numerical)"
        keys_path = self.transition_rate_recovery_prob_after_sampling_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'recovery_prob_after_sampling', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component

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
