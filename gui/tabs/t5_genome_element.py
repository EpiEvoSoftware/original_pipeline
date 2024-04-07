import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
from utils import *
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(os.path.dirname(current_dir), '../codes')
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
from genetic_effect_generator import *


class GenomeElement:
    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):

        self.init_val(config_path)
        self.init_tab(parent, tab_parent, tab_title, tab_index, hide)
        self.initial_load()

        render_next_button(self.tab_index, self.tab_parent, self.parent, self.global_update)

    def initial_load(self):
        self.render_all()
    
    def render_all(self):
        self.render_simulation_settings_title()
        self.render_use_genetic_model(None, None)

        self.init_user_input_group()
        self.init_num_traits_group()
        self.init_random_generate_group()
        self.init_global_group()

    def init_user_input_group(self):
        path_eff_size_table = self.render_path_eff_size_table()
        self.user_input_group_control = path_eff_size_table
        self.user_input_group_control.derender_itself()

    def init_num_traits_group(self):
        number_of_traits_title = self.render_number_of_traits_title()
        transmissibility = self.render_transmissibility()
        drug_resistance = self.render_drug_resistance()
        generate_genetic_architecture_method = self.render_generate_genetic_architecture_method()

        num_traits_group_control = [
            number_of_traits_title,
            transmissibility,
            drug_resistance,
            generate_genetic_architecture_method
        ]

        self.num_traits_group_control = GroupControls()
        for control in num_traits_group_control:
            self.num_traits_group_control.add(control)
        

    def init_random_generate_group(self):
        gff = self.render_gff()
        genes_num = self.render_genes_num()
        effsize_min = self.render_effsize_min()
        effsize_max = self.render_effsize_max()
        normalize = self.render_normalize()
        run_button = self.render_run_button()

        random_generate_group_control = [
            gff,
            genes_num,
            effsize_min,
            effsize_max,
            normalize,
            run_button
        ]    
        self.random_generate_group_control = GroupControls()
        for control in random_generate_group_control:
            self.random_generate_group_control.add(control)
        

    def init_global_group(self):
        self.global_group_control = GroupControls()
        self.global_group_control.add(self.random_generate_group_control)
        self.global_group_control.add(self.num_traits_group_control)
        self.global_group_control.add(self.user_input_group_control)
        
    
    def render_gff(self):
        keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', "gff"]
        config_path = self.config_path
        render_text = "Please provide the genome annotation in a gff-like format:"
        control_frame = self.control_frame
        column, frow = None, None
        component = EasyPathSelector(keys_path, config_path, render_text, control_frame, column, frow)
        self.to_update_components.add(component)
        return component

    def render_simulation_settings_title(self):
        self.render_simulation_settings_title_text = "Simulation Settings"
        self.number_of_traits_label = ttk.Label(self.control_frame, text=self.render_simulation_settings_title_text, style="Title.TLabel")
        self.number_of_traits_label.grid()
        
    def render_number_of_traits_title(self):
        column, frow = None, None
        self.render_number_of_traits_text = "Number of traits (Integer):"
        component = EasyLabel(self.render_number_of_traits_text, self.control_frame, column, frow)
        self.to_update_components.add(component)
        return component

    def render_transmissibility(self):
        keys_path = ['GenomeElement', 'traits_num', 'transmissibility']
        self.render_transmissibility_text = "Transmissibility"
        component = EasyEntry(keys_path, self.config_path, self.render_transmissibility_text, 'transmissibility', self.control_frame, None, None, 'integer')
        self.to_update_components.add(component)
        return component

    def render_drug_resistance(self):
        keys_path = ['GenomeElement', 'traits_num', 'drug_resistance']
        self.render_drug_resistance_text = "Drug-Resistance"
        column, frow = None, None
        component = EasyEntry(keys_path, self.config_path, self.render_drug_resistance_text, 'drug-resistance', self.control_frame, column, frow, 'integer')
        self.to_update_components.add(component)
        return component


    def render_generate_genetic_architecture_method(self, column = None, frow = None, to_rerender = None, to_derender = None):
        """
        generate_genetic_architecture_method
        self.generate_genetic_architecture_method = ['GenomeElement']['effect_size']['method']
        """
        keys_path = ["GenomeElement", "effect_size", "method"]                
        render_generate_genetic_architecture_method_text = "Method to Generate the Genetic Architecture"
        def comboboxselected(var):
            converted_var = render_to_val_generate_genetic_architecture_method.get(var.get(), "")
            no_validate_update_val(converted_var, self.config_path, keys_path)
            match converted_var:
                case "user_input":
                    if to_rerender is not None:
                        to_rerender()
                case "randomly_generate":
                    if to_derender is not None:
                        to_derender()
                case _:
                    raise ValueError("Invalid method specified")
        print("val_to_render_generate_genetic_architecture_method", val_to_render_generate_genetic_architecture_method)
        component =  EasyCombobox(keys_path, self.config_path, render_generate_genetic_architecture_method_text, 
                     self.control_frame, column, frow, 
                     generate_genetic_architecture_method_values, 
                     to_rerender, to_derender,
                     comboboxselected,
                     val_to_render_generate_genetic_architecture_method
                     )
        self.to_update_components.add(component)
    
        return component

    def render_genes_num(self):
        keys_path = ['GenomeElement','effect_size','randomly_generate','genes_num']
        render_text = "Number of Genomic Regions for each trait (list integer)"
        column, frow = None, None
        component =  EasyEntry(keys_path, self.config_path, render_text, "genes_num", self.control_frame, column, frow, "list")
        self.to_update_components.add(component)
        return component
        


    def render_use_genetic_model(self, to_rerender, to_derender):
        keys_path = ['GenomeElement', 'use_genetic_model']
        render_use_genetic_model_text = "Do you want to use genetic architecture for traits (transmissibility and/or Drug-resistance)?"
        column, frow = None, None
        component = EasyRadioButton(keys_path, self.config_path, render_use_genetic_model_text, "use_genetic_model", self.control_frame, column, frow, to_rerender, to_derender)
        self.to_update_components.add(component)
        return component
    
    def render_effsize_min(self):
        keys_path = ['GenomeElement','effect_size','randomly_generate','effsize_min']
        render_text = "Minimum Effect Size of each region for each trait (list numerical)"
        frow, column = None, None
        component = EasyEntry(keys_path, self.config_path, render_text, "effsize_min", self.control_frame, column, frow, "list")
        self.to_update_components.add(component)
        return component
        
        
    def render_effsize_max(self):
        keys_path = ['GenomeElement','effect_size','randomly_generate','effsize_max']
        render_text = "Maximum Effect Size of each region for each trait (list numerical)"
        column, frow = None, None
        component = EasyEntry(keys_path, self.config_path, render_text, "effsize_min", self.control_frame, column, frow, "list")
        self.to_update_components.add(component)
        return component
        
        

    def render_normalize(self):
        render_text = "Whether to Normalize randomly-selected effect sizes by the expected number of mutations?"
        keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', 'normalize']
        column, frow, = None, None
        component =  EasyRadioButton(keys_path, self.config_path, render_text, "normalize", self.control_frame, column, frow)
        self.to_update_components.add(component)
        return component
        
    def render_path_eff_size_table(self):
        render_generate_genetic_architecture_file_text = "Please provide the Genetic Architecture File in csv format:"
        keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', "gff"]
        config_path = self.config_path
        control_frame = self.control_frame
        column, frow = None, None
        filetype = (
            ("CSV files", "*.csv"),
            ("All files", "*.*")
            )
        component = EasyPathSelector(keys_path, config_path, render_generate_genetic_architecture_file_text, control_frame, column, frow, filetype)
        self.to_update_components.add(component)
        return component
        

    def render_run_button(self):
        def effect_size_generation():
            config = load_config_as_dict(self.config_path) 

            method = config['GenomeElement']['effect_size']['method']
            wk_dir = config["BasicRunConfiguration"]["cwdir"]
            n_gen = config["EvolutionModel"]["n_generation"]
            mut_rate = config["EvolutionModel"]["mut_rate"]
            trait_n = list(config['GenomeElement']['traits_num'].values())

            if method == "user_input":
                effsize_path = config['GenomeElement']['effect_size']['user_input']["path_effsize_table"]
            elif method == "randomly_generate":
                effsize_path = ""
                gff_in = config['GenomeElement']['effect_size']['randomly_generate']["gff"]
                causal_sizes = config['GenomeElement']['effect_size']['randomly_generate']['genes_num']
                es_lows = config['GenomeElement']['effect_size']['randomly_generate']['effsize_min']
                es_highs = config['GenomeElement']['effect_size']['randomly_generate']['effsize_max']
                norm_or_not = config['GenomeElement']['effect_size']['randomly_generate']['normalize']
            else:
                raise ValueError("Invalid method specified")
            
            run_effsize_generation(method, wk_dir, effsize_path=effsize_path, gff_in=gff_in, trait_n=trait_n, causal_sizes=causal_sizes, es_lows=es_lows, es_highs=es_highs, norm_or_not=norm_or_not, n_gen=n_gen, mut_rate=mut_rate)
            
            
        column, frow = None, None
        button_text = "Run Effect Size Generation"
        run_button_component = EasyButton(button_text, self.control_frame, column, frow, effect_size_generation)
        self.to_update_components.add(run_button_component)
        return run_button_component


    def init_tab(self, parent, tab_parent, tab_title, tab_index, hide):
        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_index = tab_index
        self.tab_parent.add(parent, text=tab_title)
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")
        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True)

    def global_update(self):
        users_validation_messages = []

        for component in self.to_update_components:
            component.update(users_validation_messages)

        match len(users_validation_messages):
            case 0:
                messagebox.showinfo("Update Successful", "Parameters Updated.")
                return 0
            case _:
                error_message_str = "\n\n".join(users_validation_messages)
                messagebox.showerror("Update Error", error_message_str)
                return 1
            

    def init_val(self, config_path):
        self.to_update_components = set()
        self.numtraits_group = set()
        self.random_generate_group = set()

        self.config_path = config_path
        self.config_dict = load_config_as_dict(self.config_path)
        self.use_genetic_model = self.config_dict['GenomeElement']['use_genetic_model']
        self.transmissibility = self.config_dict['GenomeElement']['traits_num']['transmissibility']
        self.drug_resistance = self.config_dict['GenomeElement']['traits_num']['drug_resistance']


        self.generate_genetic_architecture_method = self.config_dict['GenomeElement']['effect_size']['method']
        self.path_effsize_table = self.config_dict['GenomeElement']['effect_size']['user_input']["path_effsize_table"]
        self.gff = self.config_dict['GenomeElement']['effect_size']['randomly_generate']["gff"]
        self.genes_num = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['genes_num']
        self.effsize_min = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['effsize_min']
        self.effsize_max = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['effsize_max']
        self.normalize = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['normalize']