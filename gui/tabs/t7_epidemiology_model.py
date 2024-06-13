
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import platform
from utils import *




class EpidemiologyModel(TabBase):
    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):
        super().__init__(parent, tab_parent, config_path, tab_title, tab_index, hide)

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
        self.S_IE_prob = self.config_dict['EpidemiologyModel']['transition_prob']['S_IE_prob']
        self.S_IE_prob_keys_path = ['EpidemiologyModel','transition_prob','S_IE_prob']
        self.I_R_prob = self.config_dict['EpidemiologyModel']['transition_prob']['I_R_prob']
        self.I_R_prob_keys_path = ['EpidemiologyModel','transition_prob','I_R_prob']
        self.R_S_prob = self.config_dict['EpidemiologyModel']['transition_prob']['R_S_prob']
        self.R_S_prob_keys_path = ['EpidemiologyModel','transition_prob','R_S_prob']
        self.latency_prob = self.config_dict['EpidemiologyModel']['transition_prob']['latency_prob']
        self.latency_prob_keys_path = ['EpidemiologyModel','transition_prob','latency_prob']
        self.E_I_prob = self.config_dict['EpidemiologyModel']['transition_prob']['E_I_prob']
        self.E_I_prob_keys_path = ['EpidemiologyModel','transition_prob','E_I_prob']
        self.I_E_prob = self.config_dict['EpidemiologyModel']['transition_prob']['I_E_prob']
        self.I_E_prob_keys_path = ['EpidemiologyModel','transition_prob','I_E_prob']
        self.E_R_prob = self.config_dict['EpidemiologyModel']['transition_prob']['E_R_prob']
        self.E_R_prob_keys_path = ['EpidemiologyModel','transition_prob','E_R_prob']
        self.sample_prob = self.config_dict['EpidemiologyModel']['transition_prob']['sample_prob']
        self.sample_prob_keys_path = ['EpidemiologyModel','transition_prob','sample_prob']
        self.transition_prob_recovery_prob_after_sampling = self.config_dict['EpidemiologyModel']['transition_prob']['recovery_prob_after_sampling']
        self.transition_prob_recovery_prob_after_sampling_keys_path = ['EpidemiologyModel','transition_prob','recovery_prob_after_sampling']

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
        
        def configure_frame(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        def configure_canvas(event):
            self.canvas.itemconfig(self.canvas_frame, width=event.width)
        
        def _bound_to_mousewheel(event):
            if platform.system() == 'Linux':
                self.canvas.bind_all("<Button-4>", _on_mousewheel)
                self.canvas.bind_all("<Button-5>", _on_mousewheel)
            else:
                self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbound_to_mousewheel(event):
            if platform.system() == 'Linux':
                self.canvas.unbind_all("<Button-4>")
                self.canvas.unbind_all("<Button-5>")
            else:
                self.canvas.unbind_all("<MouseWheel>")

        def _on_mousewheel(event):
            if platform.system() == 'Windows':
                self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
            elif platform.system() == 'Darwin':
                self.canvas.yview_scroll(int(-1 * (event.delta)), "units")
            else:
                if event.num == 4:
                    self.canvas.yview_scroll( -1, "units" )
                elif event.num == 5:
                    self.canvas.yview_scroll( 1, "units" ) 
        
        self.scrollable_frame.bind("<Configure>", configure_frame)
        self.canvas.bind("<Configure>", configure_canvas)
        self.scrollable_frame.bind('<Enter>', _bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', _unbound_to_mousewheel)
        
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

        self.SEIR_only_entries = set()

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
        self.render_title("Transition Probabilities between Compartments", hide, 0, frow = self.increment_frow(), columnspan=3)

        self.render_S_IE_prob(hide, column=0, columnspan=1, frow = self.increment_frow(by = 1))
        self.render_latency_prob(hide, column=1, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_E_R_prob(hide, column=2, columnspan=1, frow = self.increment_frow(increment = False))
        self.render_image(hide, image_path="assets/t7.png", desired_width=600, desired_height=300, column = 1, columnspan=2, frow = self.increment_frow())

        self.render_E_I_prob(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_I_E_prob(hide, column=0, columnspan=1, frow = self.increment_frow())

        self.render_I_R_prob(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_R_S_prob(hide, column=0, columnspan=1, frow = self.increment_frow())
        
        self.render_sample_prob(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_transition_prob_recovery_prob_after_sampling(hide, column=0, columnspan=1, frow = self.increment_frow())

        self.render_title("Massive Sampling Events", hide, 0, frow = self.increment_frow(), columnspan=3)

        self.render_massive_sampling(hide, column=0, columnspan=1, frow = self.increment_frow(by = 1))
        self.render_massive_sampling_generation(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_massive_sampling_probability(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_massive_sampling_after_sampling(hide, column=0, columnspan=1, frow = self.increment_frow())
        self.render_super_infection(to_renderer, to_derenderer, hide, column=0, columnspan=1, frow = self.increment_frow())

    def render_model(self, hide, column, columnspan, frow):
        def update(e):
            config = load_config_as_dict(self.config_path)
            config['EpidemiologyModel']['model'] = model_var.get()
            save_config(self.config_path, config)

            #toggle sir/seir entries
            if model_var.get() == "SIR":
                for entry in self.SEIR_only_entries:
                    entry.config(state='disabled', foreground='light grey')
                    # entry.grid_remove()
            elif model_var.get() == "SEIR":
                for entry in self.SEIR_only_entries:
                    entry.config(state='normal', foreground='black')
                    # entry.grid()
        
        model_label = ttk.Label(self.scrollable_frame, text="Compartmental Model", style="Bold.TLabel")
        model_var = tk.StringVar(value=load_config_as_dict(self.config_path)['EpidemiologyModel']['model'])
        model_combobox = ttk.Combobox(
            self.scrollable_frame,
            textvariable=model_var,
            values=["SIR", "SEIR"],
            state="readonly",
        )
        model_combobox.bind("<<ComboboxSelected>>", update)

        model_label.grid(row=frow, column=column, columnspan=columnspan, sticky="w", pady=5)
        model_combobox.grid(row=frow + 1, column=column, columnspan=columnspan, sticky="w", pady=5)
    
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

 
    def render_S_IE_prob(self, hide, column, columnspan, frow):
        text = "Transmission Prob. β (list numerical)"
        keys_path = self.S_IE_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'S_IE_prob', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component

    def render_I_R_prob(self, hide, column, columnspan, frow):
        text = "Active Recovery Prob. γ (list numerical)"
        keys_path = self.I_R_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'I_R_prob', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component

    def render_R_S_prob(self, hide, column, columnspan, frow):
        text = "Immunity Loss Prob. ω (list numerical)"
        keys_path = self.latency_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'R_S_prob', 
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
        self.SEIR_only_entries.add(component.entry)
        return component
      
    def render_E_I_prob(self, hide, column, columnspan, frow):
        text = "Activation Prob. v (list numerical)"
        keys_path = self.E_I_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'E_I_prob', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        self.SEIR_only_entries.add(component.entry)
        return component 

    def render_I_E_prob(self, hide, column, columnspan, frow):
        text = r'De-activation Prob. φ (list numerical)'
        keys_path = self.I_E_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'I_E_prob', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        self.SEIR_only_entries.add(component.entry)
        return component
 

    def render_E_R_prob(self, hide, column, columnspan, frow):
        text = "Latent Recovery Prob. τ \n(list numerical)"
        keys_path = self.E_R_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'E_R_prob', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        self.SEIR_only_entries.add(component.entry)
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
        
        
    def render_sample_prob(self, hide, column, columnspan, frow):
        text = r"Sample Prob. ε (List Numerical)"
        keys_path = self.sample_prob_keys_path
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'sample_prob', 
            self.scrollable_frame, column, frow, 'list', hide, columnspan
            )

        self.visible_components.add(component)
        return component
        def update():
            keys_path = ['EpidemiologyModel', 'transition_prob', 'sample_prob']
            update_list_int_params(self.sample_prob_entry, keys_path, self.config_path)
        self.sample_prob_label = ttk.Label(self.scrollable_frame, text="sample_prob:")
        self.sample_prob_label.grid()
        self.sample_prob_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.sample_prob_entry.insert(0, str(self.sample_prob))  
        self.sample_prob_entry.grid()
        self.update_sample_prob_button = tk.Button(self.scrollable_frame, text="Update sample_prob", command=update)
        self.update_sample_prob_button.grid()

    def render_transition_prob_recovery_prob_after_sampling(self, hide, column, columnspan, frow):
        text = r"Recovery Probability after Sampling δ (List Numerical)"
        keys_path = self.transition_prob_recovery_prob_after_sampling_keys_path
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
