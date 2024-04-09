
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, PhotoImage
import json
import os
import sys
from PIL import Image, ImageTk
from utils import *
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(os.path.dirname(current_dir), '../codes')
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from seed_generator import *


# TODO: seed_size = len(seeded_host_id), validate
class SeedsConfiguration(TabBase):
    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):
        super().__init__(parent, tab_parent, config_path, tab_title, tab_index, hide)
        self.render_run_button()

    # def global_update(self):


    def init_val(self, config_path):
        self.config_path = config_path

        self.visible_components = set()

        self.frow_val = 0

        self.config_dict = load_config_as_dict(self.config_path)

        # SeedsConfiguration
        self.seed_size = self.config_dict['SeedsConfiguration']['seed_size']
        self.method = self.config_dict['SeedsConfiguration']['method']
        self.use_reference: bool = self.config_dict['SeedsConfiguration']['use_reference']

        # user_input
        self.path_seeds_vcf = self.config_dict['SeedsConfiguration']['user_input']['path_seeds_vcf']
        self.path_seeds_phylogeny = self.config_dict['SeedsConfiguration']['user_input']["path_seeds_phylogeny"]

        # SLiM_burnin_WF
        self.burn_in_Ne = self.config_dict['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_Ne']
        self.burn_in_generations_wf = self.config_dict['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_generations']
        self.burn_in_mutrate_wf = self.config_dict['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_mutrate']

        # SLiM_burnin_epi
        self.burn_in_generations_epi = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_generations']
        self.burn_in_mutrate_epi = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_mutrate']
        self.seeded_host_id = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']["seeded_host_id"]
        self.S_IE_rate = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']["S_IE_rate"]
        self.E_I_rate = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']["E_I_rate"]
        self.E_R_rate = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']["E_R_rate"]
        self.latency_prob = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']["latency_prob"]
        self.I_R_rate = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']['I_R_rate']
        self.I_E_rate = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']['I_E_rate']
        self.R_S_rate = self.config_dict['SeedsConfiguration']['SLiM_burnin_epi']['R_S_rate']
    
        
    def init_user_input_group(self, hide):
        tab_t = self.render_tab_title(hide, 5+3, 0, 3)
        path_seeds_vfc = self.render_path_seeds_vcf(hide, 5+3, 1, 1)
        path_seeds_phyl = self.render_path_seeds_phylogeny(hide, 12, 1, 1)
        grpctrs = GroupControls()
        grpctrs.add(tab_t)
        grpctrs.add(path_seeds_vfc)
        grpctrs.add(path_seeds_phyl)
        return grpctrs
    
    def init_wf_group(self, hide):
        """
        self.burn_in_Ne = self.config_dict['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_Ne']
        self.burn_in_generations_wf = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_generations']
        self.burn_in_mutrate_wf = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_mutrate']
        """
        wf_grpctrls = set()
        wf_grpctrls.add(self.render_tab_title(hide, 5+3, 0, 3))
        wf_grpctrls.add(self.render_burn_in_ne(hide, 1, 9))
        wf_grpctrls.add(self.render_burn_in_generations_wf(hide, 1, 11))
        wf_grpctrls.add(self.render_burn_in_mutrate_wf(hide, 1, 13))
        return wf_grpctrls
    
    def init_epi_group(self, hide):
        epi_grpctrls = set()
        epi_grpctrls.add(self.render_tab_title(False, 5+3, 0, 3))
        epi_grpctrls.add(self.render_burn_in_generations_epi(hide, 0, 6+3))
        epi_grpctrls.add(self.render_burn_in_mutrate_epi(hide, 1, 6+3))
        epi_grpctrls.add(self.render_seeded_host_id(hide, 2, 6+3))
        epi_grpctrls.add(self.render_S_IE_rate(hide, 0, 8+3))
        epi_grpctrls.add(self.render_E_I_rate(hide, 0, 10+3))
        epi_grpctrls.add(self.render_E_R_rate(hide, 2, 8+3))
        epi_grpctrls.add(self.render_latency_prob(hide, 1, 8+3))
        epi_grpctrls.add(self.render_I_R_rate(hide, 0, 16+3))
        epi_grpctrls.add(self.render_I_E_rate(hide, 0, 12+3))
        epi_grpctrls.add(self.render_R_S_rate(hide, 0, 14+3))
        epi_grpctrls.add(self.render_image("assets/t4.png", 700, 255, hide,
                          self.control_frame, frow=10+3,column=1,  
                          columnspan=2, rowspan=8))
        
        return epi_grpctrls


    def render_tab_title(self, hide = True, column = None, frow = None, columnspan = 1):
        # self.render_tab_title(user_input_components, 5+3, 0, 3)

        self.render_t4_title_text = "Burn-in Settings:"
        component = EasyTitle(
            self.render_t4_title_text,
            self.control_frame, column, frow, hide, columnspan
        )
        if not hide:
            self.visible_components.add(component)
        return component
    
    def render_seeds_size(self, hide, column, columnspan, frow):

        text = "Number of Seeding Pathogens (Integer)"
        keys_path = ['SeedsConfiguration', 'seed_size']
        component = EasyEntry(
            keys_path, self.config_path, 
            text, 'seeding_pathogens', 
            self.control_frame, column, frow, 'integer', hide, columnspan)

        if not hide:
            self.visible_components.add(component)
        return component

        self.seed_size_label = ttk.Label(self.control_frame, text=self.render_seeds_size_title, style="Bold.TLabel")
        self.seed_size_label.grid(row=1, column=1, columnspan= 3, sticky='w', pady=5)
        self.seed_size_entry = ttk.Entry(self.control_frame, foreground="black", width = 20)
        self.seed_size_entry.insert(0, self.seed_size)  
        self.seed_size_entry.grid(row=2, column=1, columnspan= 3, sticky='w', pady=5)

        self.render_seeds_size_components = []
        self.render_seeds_size_components.append(self.seed_size_label)
        self.render_seeds_size_components.append(self.seed_size_entry)

    def render_path_seeds_vcf(self, hide = True, column = None, frow = None, columnspan = 1):
        """
        self.path_seeds_vcf = load_config_as_dict(self.config_path)['SeedsConfiguration']['user_input']['path_seeds_vcf']
        """
        self.render_path_seeds_vcf_text = "The vcf file of the seeding pathogen sequences (VCF format)"
        keys_path = ['SeedsConfiguration', 'user_input', 'path_seeds_vcf']
        component = EasyPathSelector(
            keys_path,
            self.config_path, 
            self.render_path_seeds_vcf_text, 
            self.control_frame, 
            column, hide, frow, columnspan
            )
        
        if not hide:
            self.visible_components.add(component)
        return component
    

        def update():
            chosen_file = filedialog.askopenfilename(title="Select a File")
            if chosen_file:  
                self.path_seeds_vcf = chosen_file
                self.path_seeds_vcf_value_label.config(text=self.path_seeds_vcf) 
                config = load_config_as_dict(self.config_path)
                config['SeedsConfiguration']['user_input']['path_seeds_vcf'] = self.path_seeds_vcf
                save_config(self.config_path, config)

        self.render_path_seeds_vcf_text = "The vcf file of the seeding pathogen sequences (VCF format)"
        self.path_seeds_vcf_var = tk.StringVar(value=self.path_seeds_vcf)
        self.path_seeds_vcf_label = ttk.Label(self.control_frame, text=self.render_path_seeds_vcf_text, style = "Bold.TLabel")

        if self.path_seeds_vcf == "":
            self.path_seeds_vcf_value_label = ttk.Label(self.control_frame, text = "None selected", foreground="black")
        else:
            self.path_seeds_vcf_value_label = ttk.Label(self.control_frame, text = self.path_seeds_vcf, foreground="black")

        self.path_seeds_vcf_button = tk.Button(self.control_frame, text="Choose File", command=update)
        # self.delete_path_seeds_vcf_button = tk.Button(self.control_frame, text="Delete File", command=update)

        self.path_seeds_vcf_label.grid(row = 9, column = 1, sticky = 'w', pady = 5)
        self.path_seeds_vcf_value_label.grid(row=10, column=1, sticky='w', pady=5)
        self.path_seeds_vcf_button.grid(row=11, column=1, sticky='e', pady=5)
        # self.delete_path_seeds_vcf_button.grid(row=11, column=1, sticky='w', pady=5)

        components.add(self.path_seeds_vcf_label)
        components.add(self.path_seeds_vcf_value_label)
        components.add(self.path_seeds_vcf_button)
        # components.add(self.delete_path_seeds_vcf_button)



    def render_path_seeds_phylogeny(self, hide = True, column = None, frow = None, columnspan = 1):
        """
        self.path_seeds_phylogeny = load_config_as_dict(self.config_path)['SeedsConfiguration']['user_input']["path_seeds_phylogeny"]
        """

        text = "The phylogeny of the seeding sequences (nwk format, optional)"
        keys_path = ['SeedsConfiguration', 'user_input', 'path_seeds_vcf']
        component = EasyPathSelector(
            keys_path,
            self.config_path,
            text,
            self.control_frame, 
            column, hide, frow, columnspan
            )
        if not hide:
            self.visible_components.add(component)
        return component
    
        def update():
            chosen_file = filedialog.askopenfilename(title="Select a File")
            if chosen_file:  
                self.path_seeds_phylogeny = chosen_file
                self.path_seeds_phylogeny_value_label.config(text=self.path_seeds_phylogeny) 
                config = load_config_as_dict(self.config_path)
                config['SeedsConfiguration']['user_input']["path_seeds_phylogeny"] = self.path_seeds_phylogeny
                save_config(self.config_path, config)

        self.render_path_seeds_phylogeny_text = "The phylogeny of the seeding sequences (nwk format, optional)"
        self.path_seeds_phylogeny_var = tk.StringVar(value=self.path_seeds_phylogeny)
        self.path_seeds_phylogeny_label = ttk.Label(self.control_frame, text=self.render_path_seeds_phylogeny_text, style = "Bold.TLabel")

        if self.path_seeds_phylogeny == "":
            self.path_seeds_phylogeny_value_label = ttk.Label(self.control_frame, text = "None selected", foreground="black")
        else:
            self.path_seeds_phylogeny_value_label = ttk.Label(self.control_frame, text = self.path_seeds_phylogeny, foreground="black")

        self.path_seeds_phylogeny_button = tk.Button(self.control_frame, text="Choose File", command=update)
        # self.delete_path_seeds_phylogeny_button = tk.Button(self.control_frame, text="Delete File", command=update)

        self.path_seeds_phylogeny_label.grid(row = 12, column = 1, sticky = 'w', pady = 5)
        self.path_seeds_phylogeny_value_label.grid(row=13, column=1, sticky='w', pady=5)
        self.path_seeds_phylogeny_button.grid(row=14, column=1, sticky='e', pady=5)
        # self.delete_path_seeds_phylogeny_button.grid(row=11, column=1, sticky='w', pady=5)

        components.add(self.path_seeds_phylogeny_label)
        components.add(self.path_seeds_phylogeny_value_label)
        components.add(self.path_seeds_phylogeny_button)
        # components.add(self.delete_path_seeds_phylogeny_button)

    def render_use_reference(self, to_rerender, to_derender, hide = True, column = None, frow = None, columnspan = 1):
        keys_path = ['SeedsConfiguration', 'use_reference']
        text = "Do you want to use the same sequence (reference genome) as seeding sequences?"
        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)
            if var.get():
                self.use_genetic_model = True
                self.global_group_control.rerender_itself()

            else:
                self.use_genetic_model = False
                self.global_group_control.derender_itself()

        component = EasyRadioButton(
            keys_path, self.config_path, 
            text, "use_reference", 
            self.control_frame, column, 
            frow, hide, 
            to_rerender, to_derender,
            columnspan, radiobuttonselected
            )
        
        if not hide:
            self.visible_components.add(component)
        return component
        def update():
            keys_path = ['SeedsConfiguration', 'use_reference']
            no_validate_update(self.within_host_reproduction_var, self.config_path, keys_path)
            use_ref_local = get_dict_val(load_config_as_dict(self.config_path), keys_path)
            if use_ref_local:
                self.use_method_grid_configs = derender_components(self.use_method_components)
                self.user_input_grid_configs = derender_components(self.user_input_components)
                self.wf_grid_configs = derender_components(self.wf_components)
                self.epi_grid_configs = derender_components(self.epi_components)
            else:
                rerender_components(self.use_method_components, self.use_method_grid_configs)
                rerender_components(self.user_input_components, self.user_input_grid_configs)  
                keys_path = ['SeedsConfiguration', 'method']
                use_method_local = get_dict_val(load_config_as_dict(self.config_path), keys_path)
                match use_method_local:
                    case "user_input":
                        rerender_components(self.user_input_components, self.user_input_grid_configs)  
                    case "SLiM_burnin_WF":
                        rerender_components(self.wf_components, self.wf_grid_configs)    
                    case "SLiM_burnin_epi":
                        rerender_components(self.epi_components, self.epi_grid_configs)
            

        self.render_use_reference_text = "Do you want to use the same sequence (reference genome) as seeding sequences?"
        self.within_host_reproduction_var = tk.BooleanVar(value=self.use_reference)
        self.within_host_reproduction_label = ttk.Label(self.control_frame, text=self.render_use_reference_text, style = "Bold.TLabel")
        self.within_host_reproduction_label.grid(row = 3, column = 1, sticky = 'w', pady = 5)

        self.rb_true = ttk.Radiobutton(self.control_frame, text="Yes", variable=self.within_host_reproduction_var, value=True, command = update)
        self.rb_true.grid(row = 4, column = 1, columnspan= 3, sticky='w', pady=5)

        self.rb_false = ttk.Radiobutton(self.control_frame, text="No (Run the burn-in process or provide seeding sequences)", variable=self.within_host_reproduction_var, value=False, command = update)
        self.rb_false.grid(row = 5, column = 1, columnspan= 3, sticky='w', pady=5)

    def render_use_method(self, column = None, frow = None, to_rerender = None, to_derender = None, hide = True, width = 20, column_span = 20):
        text = 'Method to Generate Sequences of the Seeding Pathogens'
        keys_path = ['SeedsConfiguration', 'method']
        def comboboxselected(var, to_rerender, to_derender):
            converted_var = render_to_val_generate_genetic_architecture_method.get(var.get(), "")
            no_validate_update_val(converted_var, self.config_path, keys_path)
            match converted_var:
                case "user_input":
                    self.wf_grid_configs = derender_components(self.wf_components)
                    self.epi_grid_configs = derender_components(self.epi_components)
                    rerender_components(self.user_input_components, self.user_input_grid_configs)  
                case "SLiM_burnin_WF":
                    self.epi_grid_configs = derender_components(self.epi_components)
                    self.user_input_grid_configs = derender_components(self.user_input_components)
                    rerender_components(self.wf_components, self.wf_grid_configs)    
                case "SLiM_burnin_epi":
                    self.wf_grid_configs = derender_components(self.wf_components)
                    self.user_input_grid_configs = derender_components(self.user_input_components)
                    rerender_components(self.epi_components, self.epi_grid_configs)
                case _:
                    raise ValueError("Invalid method specified")
        component = EasyCombobox(keys_path, self.config_path, text, 
                    self.control_frame, column, frow, 
                    generate_genetic_architecture_method_values, 
                    to_rerender, to_derender,
                    comboboxselected,
                    hide,width, 
                    column_span,
                    val_to_render_generate_genetic_architecture_method)
        if not hide:
            self.visible_components.add(component)
    
        return component
        def update(event):
            keys_path = ['SeedsConfiguration', 'method']
            no_validate_update(self.use_method_var, self.config_path, keys_path, mapping = render_to_val_ui_wf_epi_mapping)
            match get_dict_val(load_config_as_dict(self.config_path), keys_path):
                case "user_input":
                    self.wf_grid_configs = derender_components(self.wf_components)
                    self.epi_grid_configs = derender_components(self.epi_components)
                    rerender_components(self.user_input_components, self.user_input_grid_configs)  
                case "SLiM_burnin_WF":
                    self.epi_grid_configs = derender_components(self.epi_components)
                    self.user_input_grid_configs = derender_components(self.user_input_components)
                    rerender_components(self.wf_components, self.wf_grid_configs)    
                case "SLiM_burnin_epi":
                    self.wf_grid_configs = derender_components(self.wf_components)
                    self.user_input_grid_configs = derender_components(self.user_input_components)
                    rerender_components(self.epi_components, self.epi_grid_configs)
        
        self.render_use_method_title = "Method to Generate Sequences of the Seeding Pathogens"
        self.use_method_label = ttk.Label(self.control_frame, text=self.render_use_method_title, style="Bold.TLabel")
        self.use_method_label.grid(row=6, column=1, columnspan= 3, sticky='w', pady=5)
        local_use_method_var = val_to_render_ui_wf_epi_mapping.get(self.method, "")
        self.use_method_var = tk.StringVar(value=local_use_method_var)
        combobox_vals = list(render_to_val_ui_wf_epi_mapping.keys())
        self.use_method_combobox = ttk.Combobox(
            self.control_frame, textvariable=self.use_method_var, 
            values=combobox_vals, state="readonly",
            width = 50
            )
        self.use_method_combobox.grid(row=7, column=1, columnspan= 3, sticky='w', pady=5)
        self.use_method_combobox.bind("<<ComboboxSelected>>", update)

        use_method_components = set()
        use_method_components.add(self.use_method_label)
        use_method_components.add(self.use_method_combobox)
        return use_method_components

    def render_burn_in_ne(self, hide = True, column = None, frow = None):
        columnspan = 1
        self.render_burn_in_ne_text= "Effective Population Size (Integer)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_WF','burn_in_Ne']
        
        component = EasyEntry(
            keys_path, self.config_path, 
            self.render_burn_in_ne_text, 'burn_in_ne', 
            self.control_frame, column, frow, 'integer', hide,
            columnspan
            )
        
        if not hide:
            self.visible_components.add(component)
        return component

        self.burn_in_Ne_label = ttk.Label(self.control_frame, text=self.render_burn_in_ne_text, style = "Bold.TLabel")
        self.burn_in_Ne_entry = ttk.Entry(self.control_frame, foreground="black")
        self.burn_in_Ne_entry.insert(0, self.burn_in_Ne)  
        # self.update_burn_in_Ne_button = tk.Button(self.control_frame, text="Update burn_in_Ne", command=self.update_burn_in_Ne)

        self.burn_in_Ne_label.grid(row = 9, column = 1, sticky='w', pady=5)
        self.burn_in_Ne_entry.grid(row = 10, column = 1, sticky='w', pady=5)
# no east
        components.add(self.burn_in_Ne_label)
        components.add(self.burn_in_Ne_entry)

    def render_burn_in_generations_wf(self, hide = True, column = None, frow = None):
        
        columnspan = 1
        self.render_burn_in_generations_wf_text = "Number of Burn-in Generations (Integer)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_WF', 'burn_in_generations']
        component = EasyEntry(keys_path, self.config_path, self.render_burn_in_generations_wf_text, 'burn_in_generations_wf', self.control_frame, column, frow, 'integer', hide, columnspan)
        if not hide:
            self.visible_components.add(component)
        return component

    def render_burn_in_mutrate_wf(self, hide = True, column = None, frow = None):
        columnspan = 1
        self.render_burn_in_mutrate_wf_text = "Burn-in Mutation Rate (Numerical)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_WF', 'burn_in_mutrate']
        component = EasyEntry(keys_path, self.config_path, 
                              self.render_burn_in_generations_wf_text, 
                              'burn_in_mutrate', self.control_frame, column, 
                              frow, 'integer', hide, columnspan=columnspan
                              )
        if not hide:
            self.visible_components.add(component)
        return component

        self.burn_in_mutrate_wf_label = ttk.Label(self.control_frame, text=self.render_burn_in_mutrate_wf_text, style = "Bold.TLabel")
        self.burn_in_mutrate_wf_entry = ttk.Entry(self.control_frame, foreground="black")
        self.burn_in_mutrate_wf_entry.insert(0, self.burn_in_mutrate_wf)  
        
        self.burn_in_mutrate_wf_label.grid(row = 13, column = 1, sticky='w', pady=5)
        self.burn_in_mutrate_wf_entry.grid(row = 14, column = 1, sticky='w', pady=5)
        # self.update_burn_in_mutrate_wf_button = tk.Button(self.control_frame, text="Update burn_in_mutrate_wf", command=self.update_burn_in_mutrate_wf)
        # self.update_burn_in_mutrate_wf_button.grid()

        components.add(self.burn_in_mutrate_wf_label)
        components.add(self.burn_in_mutrate_wf_entry)

    # startofepi
    def render_burn_in_generations_epi(self, hide = True, column = None, frow = None):
        self.render_burn_in_generations_epi_text = "Number of Burn-in Generations (Integer)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', 'burn_in_generations']
        
        component = EasyEntry(keys_path, self.config_path, self.render_burn_in_generations_epi_text, 'burn_in_generations_epi', self.control_frame, column, frow, 'integer', hide, 1)
        if not hide:
            self.visible_components.add(component)
        return component

        self.burn_in_generations_epi_label = ttk.Label(self.control_frame, text=self.render_burn_in_generations_epi_text, style="Bold.TLabel")
        self.burn_in_generations_epi_entry = ttk.Entry(self.control_frame, foreground="black")
        self.burn_in_generations_epi_entry.insert(0, self.burn_in_generations_epi)  

        self.burn_in_generations_epi_label.grid(row=6+3, column=0, sticky='w', pady=5)
        self.burn_in_generations_epi_entry.grid(row=7+3, column=0, sticky='w', pady=5)

        # self.render_burn_in_generations_epi_components = []
        epi_components.add(self.burn_in_generations_epi_label)
        epi_components.add(self.burn_in_generations_epi_entry)

        # self.update_burn_in_generations_epi_button = tk.Button(self.control_frame, text="Update burn_in_generations", command=self.update_burn_in_generations_epi)
        # self.update_burn_in_generations_epi_button.grid()

        # self.t4_title.grid(row=7, column=0, sticky='w', pady=5)

    def render_burn_in_mutrate_epi(self, hide = True, column = None, frow = None):

        self.render_burn_in_mutrate_epi_text = "Burn-in Mutation Rate (Numerical)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', 'burn_in_mutrate']
        component = EasyEntry(keys_path, self.config_path, self.render_burn_in_mutrate_epi_text, 'burn_in_mutrate', self.control_frame, column, frow, 'integer', hide, 1)
        if not hide:
            self.visible_components.add(component)
        return component

        self.burn_in_mutrate_epi_label = ttk.Label(self.control_frame, text=self.render_burn_in_mutrate_epi_text, style="Bold.TLabel")
        self.burn_in_mutrate_epi_entry = ttk.Entry(self.control_frame, foreground="black")
        self.burn_in_mutrate_epi_entry.insert(0, self.burn_in_mutrate_epi)

        self.burn_in_mutrate_epi_label.grid(row=6+3, column=1, sticky='w', pady=5)
        self.burn_in_mutrate_epi_entry.grid(row=7+3, column=1, sticky='w', pady=5)

        # self.render_burn_in_mutrate_epi_components = []
        epi_components.add(self.burn_in_mutrate_epi_label)
        epi_components.add(self.burn_in_mutrate_epi_entry)
        # self.update_burn_in_mutrate_epi_button = tk.Button(self.control_frame, text="Update burn_in_mutrate_epi", command=self.update_burn_in_mutrate_epi)
        # self.update_burn_in_mutrate_epi_button.grid()

    def render_seeded_host_id(self, hide = True, column = None, frow = None):
        self.render_seeded_host_id_text = "Seeded Host (Patient 0) ID(s) (integer)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', "seeded_host_id"]
        component = EasyEntry(keys_path, self.config_path, self.render_seeded_host_id_text, 'seeded_host_id', self.control_frame, column, frow, 'list', hide, columnspan=1)
        if not hide:
            self.visible_components.add(component)
        return component


        self.seeded_host_id_label = ttk.Label(self.control_frame, text=self.render_seeded_host_id_text, style="Bold.TLabel")
        self.seeded_host_id_entry = ttk.Entry(self.control_frame, foreground="black")
        self.seeded_host_id_entry.insert(0, str(self.seeded_host_id))  

        self.seeded_host_id_label.grid(row=6+3, column=2, sticky='w', pady=5)
        self.seeded_host_id_entry.grid(row=7+3, column=2, sticky='w', pady=5)

        # self.render_seeded_host_id_components = []
        epi_components.add(self.seeded_host_id_label)
        epi_components.add(self.seeded_host_id_entry)
        # self.update_seeded_host_id_button = tk.Button(self.control_frame, text="Update seeded_host_id", command=self.update_seeded_host_id)
        # self.update_seeded_host_id_button.grid()

    def render_S_IE_rate(self, hide = True, column = None, frow = None):

        self.render_S_IE_rate_text = "Transmission Rate \u03B2 (Numerical)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', "S_IE_rate"]
        component = EasyEntry(keys_path, self.config_path, self.render_S_IE_rate_text,'S_IE_rate', self.control_frame, column, frow, 'integer', hide, 1)
        if not hide:
            self.visible_components.add(component)
        return component

        self.S_IE_rate_label = ttk.Label(self.control_frame, text=self.render_S_IE_rate_text, style="Bold.TLabel")
        self.S_IE_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.S_IE_rate_entry.insert(0, self.S_IE_rate)  

        self.S_IE_rate_label.grid(row=8+3, column=0, sticky='w', pady=5)
        self.S_IE_rate_entry.grid(row=9+3, column=0, sticky='w', pady=5)

        # self.render_S_IE_rate_components = []
        epi_components.add(self.S_IE_rate_label)
        epi_components.add(self.S_IE_rate_entry)

    def render_E_R_rate(self, hide = True, column = None, frow = None):
        
        self.render_E_R_rate_text = "Latent Recovery Rate \u03C4 (Numerical)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', "E_R_rate"]
        component = EasyEntry(keys_path, self.config_path, self.render_E_R_rate_text, 'E_R_rate', self.control_frame, column, frow, 'integer', hide, 1)
        if not hide:
            self.visible_components.add(component)
        return component

        self.E_R_rate_label = ttk.Label(self.control_frame, text=self.render_E_R_rate_text, style="Bold.TLabel")
        self.E_R_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.E_R_rate_entry.insert(0, self.E_R_rate)  

        self.E_R_rate_label.grid(row=8+3, column=2, sticky='w', pady=5)
        self.E_R_rate_entry.grid(row=9+3, column=2, sticky='w', pady=5)

        # self.render_E_R_rate_components = []
        epi_components.add(self.E_R_rate_label)
        epi_components.add(self.E_R_rate_entry)
    
    def render_latency_prob(self, hide = True, column = None, frow = None):
        self.render_latency_prob_text = "Latency Probability p (Numerical)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', "latency_prob"]
        component = EasyEntry(keys_path, self.config_path, self.render_latency_prob_text, 'latency_prob', self.control_frame, column, frow, 'integer', hide, 1)
        if not hide:
            self.visible_components.add(component)
        return component

        self.latency_prob_label = ttk.Label(self.control_frame, text=self.render_latency_prob_text, style="Bold.TLabel")
        self.latency_prob_entry = ttk.Entry(self.control_frame, foreground="black")
        self.latency_prob_entry.insert(0, self.latency_prob)  

        self.latency_prob_label.grid(row=8+3, column=1, sticky='w', pady=5)
        self.latency_prob_entry.grid(row=9+3, column=1, sticky='w', pady=5)
        
        # self.render_latency_prob_components = []
        epi_components.add(self.latency_prob_label)
        epi_components.add(self.latency_prob_entry)

               
    def render_E_I_rate(self, hide = True, column = None, frow = None):

        self.render_E_I_rate_text = "Activation Rate v (Numerical)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', "E_I_rate"]
        component = EasyEntry(keys_path, self.config_path, self.render_E_I_rate_text, 'E_I_rate', self.control_frame, column, frow, 'integer', hide, 1)
        if not hide:
            self.visible_components.add(component)
        return component

        self.E_I_rate_label = ttk.Label(self.control_frame, text=self.render_E_I_rate_text, style="Bold.TLabel")
        self.E_I_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.E_I_rate_entry.insert(0, self.E_I_rate)  

        self.E_I_rate_label.grid(row=10+3, column=0, sticky='w', pady=5)
        self.E_I_rate_entry.grid(row=11+3, column=0, sticky='w', pady=5)

        epi_components.add(self.E_I_rate_label)
        epi_components.add(self.E_I_rate_entry)
        
    
    def render_I_E_rate(self, hide = True, column = None, frow = None):
        self.render_I_E_rate_text = "De-activaton Rate \u03C6 (numerical)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', 'I_E_rate']
        component = EasyEntry(
            keys_path, self.config_path, self.render_I_E_rate_text, 'I_E_rate', self.control_frame, column, frow, 'integer', hide, 
            columnspan=1)
        if not hide:
            self.visible_components.add(component)
        return component
        self.I_E_rate_label = ttk.Label(self.control_frame, text=self.render_I_E_rate_text, style="Bold.TLabel")



        self.I_E_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.I_E_rate_entry.insert(0, self.I_E_rate)  

        self.I_E_rate_label.grid(row=12+3, column=0, sticky='w', pady=5)
        self.I_E_rate_entry.grid(row=13+3, column=0, sticky='w', pady=5)

        # self.render_I_E_rate_components = []
        epi_components.add(self.I_E_rate_label)
        epi_components.add(self.I_E_rate_entry)
    
    def render_R_S_rate(self, hide = True, column = None, frow = None):
        self.render_R_S_rate_text = "Immunity Loss Rate \u03C9 (numerical)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', 'R_S_rate']
        component = EasyEntry(
            keys_path, self.config_path, self.render_R_S_rate_text, 'R_S_rate', self.control_frame, column, frow, 'integer', hide,
            columnspan=1
            )
        if not hide:
            self.visible_components.add(component)
        return component
        keys_path = []
        component = EasyEntry(
            keys_path, self.config_path, self.render_burn_in_mutrate_epi_text, 'burn_in_generations', self.control_frame, column, frow, 'integer', hide
            )
        if not hide:
            self.visible_components.add(component)
        self.R_S_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.R_S_rate_entry.insert(0, self.R_S_rate)  
        
        self.R_S_rate_label.grid(row=14+3, column=0, sticky='w', pady=5)
        self.R_S_rate_entry.grid(row=15+3, column=0, sticky='w', pady=5)

        # self.render_R_S_rate_components = []
        epi_components.add(self.R_S_rate_label)
        epi_components.add(self.R_S_rate_entry)

    def render_I_R_rate(self, hide = True, column = None, frow = None):
        self.render_I_R_rate_text = "Active Recovery Rate \u03B3 (numerical)"
        keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', 'I_R_rate']
        component = EasyEntry(
            keys_path, self.config_path, self.render_I_R_rate_text, 'burn_in_generations', self.control_frame, column, frow, 'integer', hide,
            columnspan=1
        )
        if not hide:
            self.visible_components.add(component)
        return component
        self.I_R_rate_label = ttk.Label(self.control_frame, text=self.render_I_R_rate_text, style="Bold.TLabel")

        self.I_R_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.I_R_rate_entry.insert(0, self.I_R_rate)  

        self.I_R_rate_label.grid(row=16+3, column=0, sticky='w', pady=5)
        self.I_R_rate_entry.grid(row=17+3, column=0, sticky='w', pady=5)

        # self.render_I_R_rate_components = []
        epi_components.add(self.I_R_rate_label)
        epi_components.add(self.I_R_rate_entry)

    def render_image(self, image_path, desired_width, desired_height, hide, control_frame, frow, column, columnspan, rowspan):
        component = EasyImage(
            image_path, desired_width, 
            desired_height, hide, 
            control_frame, frow, 
            column, columnspan, 
            rowspan
            )
        if not hide:
            self.visible_components.add(component)       
            # image_label.grid(column=1, row=10+3, columnspan=2, rowspan=8, sticky="nsew")
            # if not hide:
            #     self.visible_components.add(image_label)                    
    
    
    # def update_use_method(self, event):
    #     new_use_method = self.use_method_var.get()
    #     if new_use_method in ["user_input", "SLiM_burnin_WF", "SLiM_burnin_epi"]: 
    #         config = load_config_as_dict(self.config_path)
    #         config['SeedsConfiguration']['method'] = new_use_method
    #         save_config(self.config_path, config)
    #         messagebox.showinfo("Update Successful", "Method Updated.")

    #         if new_use_method == "user_input":
    #             if not hasattr(self, 'path_seeds_vcf_label'):  # create the label if it doesn't exist
    #                 # Hide other labels if initialized
    #                 self.hide_elements()
    #                 # 

    #                 # Labels Creating
    #                 # self.render_path_seeds_vcf()
    #             else:
    #                 # Hide other labels if initialized
    #                 self.hide_elements()
    #                 #

    #                 # show the label if it was previously created
    #                 self.path_seeds_vcf_label.grid()
    #                 self.choose_path_seeds_vcf_button.grid()
    #                 self.path_seeds_vcf_indicator.grid()
                    

    #         elif new_use_method == "SLiM_burnin_WF":
    #             if not hasattr(self, 'burn_in_Ne_label'):  # create the label if it doesn't exist
    #                 # Hide other labels if initialized
    #                 self.hide_elements()
    #                 # 

    #                 # burn_in_Ne, burn_in_generations_wf, burn_in_mutrate_wf
    #                 self.render_burn_in_ne()

    #                 # burn_in_generations_wf
    #                 self.render_burn_in_generations_wf()

    #                 # burn_in_mutrate_wf
    #                 self.render_burn_in_mutrate_wf()

    #             else: # Show the label if it was previously created
    #                 # Hide other labels if initialized
    #                 self.hide_elements()
    #                 # 

    #                 # Show Labels
    #                 self.burn_in_Ne_label.grid()
    #                 self.burn_in_Ne_entry.grid()
    #                 self.update_burn_in_Ne_button.grid()

    #                 self.burn_in_generations_wf_label.grid()
    #                 self.burn_in_generations_wf_entry.grid()
    #                 self.update_burn_in_generations_wf_button.grid()

    #                 self.burn_in_mutrate_wf_label.grid()
    #                 self.burn_in_mutrate_wf_entry.grid()
    #                 self.update_burn_in_mutrate_wf_button.grid()
                    

    #         elif new_use_method == "SLiM_burnin_epi":
    #             if not hasattr(self, 'burn_in_generations_epi_label'):  # create the label if it doesn't exist
    #                 self.hide_elements()
                    
    #                 # self.burn_in_generations_epi = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_generations']
    #                 self.render_burn_in_generations_epi()

    #                 # self.burn_in_mutrate_epi = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_mutrate']
    #                 self.render_burn_in_mutrate_epi()

    #                 # 

    #                 # self.seeded_host_id = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["seeded_host_id"]
    #                 self.render_seeded_host_id()

    #                 # 

    #                 # self.S_IE_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["S_IE_rate"]
    #                 self.render_S_IE_rate()

    #                 # 

    #                 # self.E_I_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["E_I_rate"]
    #                 self.render_E_I_rate()

    #                 # 

    #                 # self.E_R_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["E_R_rate"]
    #                 self.render_E_R_rate()

    #                 # self.latency_prob = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']["latency_prob"]
    #                 self.render_latency_prob()
 

    #                 # self.I_R_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi', 'I_R_rate']
    #                 self.render_I_R_rate()

    #                 # self.I_E_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['I_E_rate']
    #                 self.render_I_E_rate()
                    

    #                 # self.R_S_rate = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_epi']['R_S_rate']
    #                 self.render_R_S_rate()
                    

    #             else:
    #                 self.hide_elements()
    #                 # show the label if it was previously created
    #                 self.burn_in_generations_epi_label.grid()
    #                 self.burn_in_generations_epi_entry.grid()
    #                 self.update_burn_in_generations_epi_button.grid()

    #                 self.burn_in_mutrate_epi_label.grid()
    #                 self.burn_in_mutrate_epi_entry.grid()
    #                 self.update_burn_in_mutrate_epi_button.grid()
                    
    #                 self.seeded_host_id_label.grid()
    #                 self.seeded_host_id_entry.grid()
    #                 self.update_seeded_host_id_button.grid()
                    
    #                 self.S_IE_rate_label.grid()
    #                 self.S_IE_rate_entry.grid()
    #                 self.update_S_IE_rate_button.grid()
                    
    #                 self.E_I_rate_label.grid()
    #                 self.E_I_rate_entry.grid()
    #                 self.update_E_I_rate_button.grid()
                    
    #                 self.E_R_rate_label.grid()
    #                 self.E_R_rate_entry.grid()
    #                 self.update_E_R_rate_button.grid()
                    
    #                 self.latency_prob_label.grid()
    #                 self.latency_prob_entry.grid()
    #                 self.update_latency_prob_button.grid()
                    
    #                 self.I_R_rate_label.grid()
    #                 self.I_R_rate_entry.grid()
    #                 self.update_I_R_rate_button.grid()
                    
    #                 self.I_E_rate_label.grid()
    #                 self.I_E_rate_entry.grid()
    #                 self.update_I_E_rate_button.grid()
                    
    #                 self.R_S_rate_label.grid()
    #                 self.R_S_rate_entry.grid()
    #                 self.update_R_S_rate_button.grid()

    #         self.render_run_button()
    #         messagebox.showinfo("Update Successful", "method changed.")
    #     else:
    #         messagebox.showerror("Update Error", "Please enter a valid entry for method.")

    # def choose_network_path(self):  
    #     chosen_path = filedialog.askdirectory(title="Select a Directory")
    #     if chosen_path:  
    #         self.network_path = chosen_path
    #         self.network_path_label = ttk.Label(self.control_frame, text="Current Network Path: " + self.network_path)
    #         self.network_path_label.grid()
    #         self.network_path_label.config(text=f"Path Network: {self.network_path}") 
    #         config = load_config_as_dict(self.config_path)
    #         config['SeedsConfiguration']['user_input']["path_network"] = self.network_path
    #         save_config(self.config_path, config)
    
    # def choose_and_update_path_seeds_vcf(self):  
    #     filetypes = ( #don't need to check if its genome file: or use python package jaehee said
    #         ("Genome files", ("*.fasta", "*.fa", "*.gb", "*.gtf", "*.vcf", "*.bam", "*.sam", "*.fna")),
    #         ("All files", "*.*")
    #     )
    #     chosen_file = filedialog.askopenfilename(title="Select a path_seeds_vcf", filetypes=filetypes)
    #     if chosen_file:  
    #         self.path_seeds_vcf = chosen_file
    #         self.path_seeds_vcf_indicator.config(text=f"choose_path_seeds_vcf: {self.path_seeds_vcf}") 
    #         config = load_config_as_dict(self.config_path)
    #         config['SeedsConfiguration']['user_input']['path_seeds_vcf'] = self.path_seeds_vcf
    #         save_config(self.config_path, config)


    # def update_seed_size(self):
    #     try:
    #         new_seed_size = int(float(self.seed_size_entry.get()))  
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['seed_size'] = new_seed_size 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "seed_size changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid integer for seed_size.") 

    # def update_burn_in_Ne(self):
    #     try:
    #         new_burn_in_Ne = int(float(self.burn_in_Ne_entry.get()))
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_Ne'] = new_burn_in_Ne 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "burn_in_Ne changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid integer for burn_in_Ne.") 
    
    # def update_burn_in_generations_wf(self):
    #     try:
    #         new_burn_in_generations_wf = int(float(self.burn_in_generations_wf_entry.get()))
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_generations'] = new_burn_in_generations_wf 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "burn_in_generations_wf changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid integer for burn_in_generations_wf.") 


    # def update_burn_in_mutrate_wf(self):
    #     try:
    #         new_burn_in_mutrate_wf = float(self.burn_in_mutrate_wf_entry.get())  
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_mutrate'] = new_burn_in_mutrate_wf 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "burn_in_mutrate_wf changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid integer for burn_in_mutrate_wf.") 

    # def update_burn_in_generations_epi(self):
    #     try:
    #         new_burn_in_generations_epi = int(float(self.burn_in_generations_epi_entry.get()))
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_generations'] = new_burn_in_generations_epi
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "burn_in_generations changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid integer for burn_in_generations.") 

    # def update_burn_in_mutrate_epi(self):
    #     try:
    #         new_burn_in_mutrate_epi = float(self.burn_in_mutrate_epi_entry.get())  
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_epi']['burn_in_generations'] = new_burn_in_mutrate_epi 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "burn_in_mutrate_epi changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid float for burn_in_mutrate_epi.") 

    # def update_seeded_host_id(self):
    #     keys_path = ['SeedsConfiguration', 'SLiM_burnin_epi', 'seeded_host_id']
    #     update_list_int_params(self.seeded_host_id_entry, keys_path, self.config_path)
        
    # def update_S_IE_rate(self):
    #     try:
    #         new_S_IE_rate = float(self.S_IE_rate_entry.get())  
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_epi']['S_IE_rate'] = new_S_IE_rate 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "S_IE_rate changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid float for S_IE_rate.") 
    #     except Exception as e: # General error handling (e.g., file operation failures)
    #         messagebox.showerror("Update Error", str(e))    

    # def update_E_I_rate(self):
    #     try:
    #         new_E_I_rate = float(self.E_I_rate_entry.get())  
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_epi']['E_I_rate'] = new_E_I_rate 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "E_I_rate changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid float for E_I_rate.") 
    #     except Exception as e: # General error handling (e.g., file operation failures)
    #         messagebox.showerror("Update Error", str(e))    

    # def update_E_R_rate(self):
    #     try:
    #         new_E_R_rate = float(self.E_R_rate_entry.get())  
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_epi']['E_R_rate'] = new_E_R_rate 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "E_R_rate changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid float for E_R_rate.") 
    #     except Exception as e: # General error handling (e.g., file operation failures)
    #         messagebox.showerror("Update Error", str(e))    

    # def update_latency_prob(self):
    #     try:
    #         new_latency_prob = int(float(self.latency_prob_entry.get()))
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_epi']['latency_prob'] = new_latency_prob 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "latency_prob changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid float for latency_prob.") 
    #     except Exception as e: # General error handling (e.g., file operation failures)
    #         messagebox.showerror("Update Error", str(e))    

    # def update_I_R_rate(self):
    #     try:
    #         new_I_R_rate = float(self.I_R_rate_entry.get())  
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_epi']['I_R_rate'] = new_I_R_rate 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "I_R_rate changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid float for I_R_rate.") 
    #     except Exception as e: # General error handling (e.g., file operation failures)
    #         messagebox.showerror("Update Error", str(e))    

    # def update_I_E_rate(self):
    #     try:
    #         new_I_E_rate = float(self.I_E_rate_entry.get())  
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_epi']['I_E_rate'] = new_I_E_rate 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "I_E_rate changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid float for I_E_rate.") 
    #     except Exception as e: # General error handling (e.g., file operation failures)
    #         messagebox.showerror("Update Error", str(e))    

    # def update_R_S_rate(self):
    #     try:
    #         new_R_S_rate = float(self.R_S_rate_entry.get())  
    #         config = load_config_as_dict(self.config_path) 
    #         config['SeedsConfiguration']['SLiM_burnin_epi']['R_S_rate'] = new_R_S_rate 
    #         save_config(self.config_path, config)  
    #         messagebox.showinfo("Update Successful", "R_S_rate changed.")  
    #     except ValueError:
    #         messagebox.showerror("Update Error", "Please enter a valid float for R_S_rate.") 
    #     except Exception as e: # General error handling (e.g., file operation failures)
    #         messagebox.showerror("Update Error", str(e))

    # def hide_elements(self):
    #     if hasattr(self, 'path_seeds_vcf_label'):
    #         # new_use_method == "SLiM_burnin_WF":
    #         self.path_seeds_vcf_label.pack_forget()
    #         self.choose_path_seeds_vcf_button.pack_forget()
    #         self.path_seeds_vcf_indicator.pack_forget()
    #         # 
    #     if hasattr(self, 'burn_in_Ne_label'):
    #         # new_use_method == "SLiM_burnin_WF":
    #         self.burn_in_Ne_label.pack_forget()
    #         self.burn_in_Ne_entry.pack_forget()
    #         self.update_burn_in_Ne_button.pack_forget()

    #         self.burn_in_generations_wf_label.pack_forget()
    #         self.burn_in_generations_wf_entry.pack_forget()
    #         self.update_burn_in_generations_wf_button.pack_forget()

    #         self.burn_in_mutrate_wf_label.pack_forget()
    #         self.burn_in_mutrate_wf_entry.pack_forget()
    #         self.update_burn_in_mutrate_wf_button.pack_forget()
    #         # 

    #     if hasattr(self, 'burn_in_generations_epi_label'):
    #         # new_use_method == "SLiM_burnin_epi":
    #         self.burn_in_generations_epi_label.pack_forget()
    #         self.burn_in_generations_epi_entry.pack_forget()
    #         self.update_burn_in_generations_epi_button.pack_forget()

    #         self.burn_in_mutrate_epi_label.pack_forget()
    #         self.burn_in_mutrate_epi_entry.pack_forget()
    #         self.update_burn_in_mutrate_epi_button.pack_forget()
            
    #         self.seeded_host_id_label.pack_forget()
    #         self.seeded_host_id_entry.pack_forget()
    #         self.update_seeded_host_id_button.pack_forget()
            
    #         self.S_IE_rate_label.pack_forget()
    #         self.S_IE_rate_entry.pack_forget()
    #         self.update_S_IE_rate_button.pack_forget()
            
    #         self.E_I_rate_label.pack_forget()
    #         self.E_I_rate_entry.pack_forget()
    #         self.update_E_I_rate_button.pack_forget()
            
    #         self.E_R_rate_label.pack_forget()
    #         self.E_R_rate_entry.pack_forget()
    #         self.update_E_R_rate_button.pack_forget()
            
    #         self.latency_prob_label.pack_forget()
    #         self.latency_prob_entry.pack_forget()
    #         self.update_latency_prob_button.pack_forget()
            
    #         self.I_R_rate_label.pack_forget()
    #         self.I_R_rate_entry.pack_forget()
    #         self.update_I_R_rate_button.pack_forget()
            
    #         self.I_E_rate_label.pack_forget()
    #         self.I_E_rate_entry.pack_forget()
    #         self.update_I_E_rate_button.pack_forget()
            
    #         self.R_S_rate_label.pack_forget()
    #         self.R_S_rate_entry.pack_forget()
    #         self.update_R_S_rate_button.pack_forget()

            
    def render_run_button(self):
        def seed_generation():
            config = load_config_as_dict(self.config_path)
            cwdir = config["BasicRunConfiguration"]["cwdir"]
            seed_size = config["SeedsConfiguration"]["seed_size"]
            method = config["SeedsConfiguration"]["method"]
            ref_path = get_dict_val(config, ["GenomeElement", "ref_path"])

            try: 
                if method == "SLiM_burnin_WF":
                    Ne = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_Ne"]
                    n_gen = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_generations"]
                    mu = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_mutrate"]
                    error = run_seed_generation(method=method, wk_dir=cwdir, seed_size=seed_size, Ne=Ne,
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
                    
                    error = run_seed_generation(method=method, wk_dir=cwdir, seed_size=seed_size, mu=mu, n_gen=n_gen, 
                                seeded_host_id=seeded_host_id, S_IE_rate=S_IE_rate, E_I_rate=E_I_rate,
                                E_R_rate=E_R_rate, latency_prob=latency_prob, I_R_rate=I_R_rate, 
                                I_E_rate=I_E_rate, R_S_rate=R_S_rate, host_size=host_size, ref_path=ref_path)

                elif method == "user_input":
                    path_seeds_vcf = config["SeedsConfiguration"]["user_input"]["path_seeds_vcf"]
                    path_seeds_phylogeny = config["SeedsConfiguration"]["user_input"]["path_seeds_phylogeny"]
                    error = run_seed_generation(method=method, wk_dir=cwdir, seed_size=seed_size, seed_vcf=path_seeds_vcf, 
                                        path_seeds_phylogeny=path_seeds_phylogeny)
                
                if error is not None:
                    raise Exception(error)
                
            except Exception as e:
                    messagebox.showerror("Seed Generation Error", str(e))
                    

        self.run_seed_generation_button = tk.Button(self.control_frame, text="Run Seed Generation", command=seed_generation)
        self.run_seed_generation_button.grid()



    def load_page(self):
        hide = False
        to_renderer, to_derenderer = None, None
        self.render_seeds_size(hide, column=1, columnspan= 3, frow = 1)

        self.render_use_reference(to_renderer, to_derenderer, hide, column = 1, frow = 4, columnspan= 3)
        self.render_use_method(column=1, frow=6, to_rerender=to_renderer, to_derender=to_derenderer, hide=hide, column_span= 3 )
        self.user_input_group_controls = self.init_user_input_group(hide)
        self.wf_group_controls = self.init_wf_group(hide)
        self.epi_group_controls = self.init_epi_group(hide)
             
        # if not self.use_reference:
        #     rerender_components(self.use_method_components, self.use_method_grid_configs)

        # self.user_input_components = self.init_user_input_group()
        # self.user_input_grid_configs = derender_components(self.user_input_components)

        # self.wf_components = self.init_wf_group()
        # self.wf_grid_configs = derender_components(self.wf_components)

        # self.epi_components = self.init_epi_group()
        # self.epi_grid_configs = derender_components(self.epi_components)

        # match self.method:
        #     case "user_input":
        #         rerender_components(self.user_input_components, self.user_input_grid_configs)  
        #     case "SLiM_burnin_WF":
        #         rerender_components(self.wf_components, self.wf_grid_configs)    
        #     case "SLiM_burnin_epi":
        #         rerender_components(self.epi_components, self.epi_grid_configs)
