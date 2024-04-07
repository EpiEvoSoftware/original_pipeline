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
        # self.render_use_genetic_model(None, None)
        
        return
        self.render_genetic_architecture_group()
        self.render_num_traits_group(self.use_genetic_model)
        self.render_user_input(False)
        self.render_gff()
        self.render_number_of_traits()
        self.render_number_of_traits_title()
        self.render_transmissibility()
        self.render_drug_resistance()
        self.render_generate_genetic_architecture_method()
        self.render_genes_num()
        self.render_randomly_generate()
        self.render_run_button()
    
    def render_all(self):
        self.render_simulation_settings_title()
        self.render_use_genetic_model(None, None)

        self.init_user_input_group()
        self.init_num_traits_group()
        self.init_random_generate_group()
        self.init_global_group()

        # to_derender_generate_genetic_architecture_method = GroupControls()
        # to_derender_generate_genetic_architecture_method.add(self.user_input_group_control)
        # to_derender_generate_genetic_architecture_method.add(self.random_generate_group_control)
        # generate_genetic_architecture_method_comp = self.render_generate_genetic_architecture_method(
        #     to_rerender=to_derender_generate_genetic_architecture_method.rerender_itself, 
        #     to_derender=to_derender_generate_genetic_architecture_method.derender_itself
        #     )
        # generate_genetic_architecture_method_comp.derender_itself()


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
        # self.num_traits_group_control.derender_itself()

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
        # self.random_generate_group_control.derender_itself()

    def init_global_group(self):
        self.global_group_control = GroupControls()
        self.global_group_control.add(self.random_generate_group_control)
        self.global_group_control.add(self.num_traits_group_control)
        self.global_group_control.add(self.user_input_group_control)
        # self.global_group_control.derender_itself()
    
    def render_genetic_architecture_group(self):
        """
        first render group for yes/no forms
        """
        to_rerender, to_derender = None, None
        # feed in groups of all controls
        use_genetic_model_component = self.render_use_genetic_model(to_rerender, to_derender)
        return use_genetic_model_component

    def render_num_traits_group(self, show):
        """
        second render group
        """
        transmissibility_component = self.render_transmissibility()
        drug_resistance_component = self.render_drug_resistance()
        render_generate_genetic_architecture_method_component = self.render_generate_genetic_architecture_method()

        if show:
            transmissibility_component.rerender_itself()
            drug_resistance_component.rerender_itself()
            render_generate_genetic_architecture_method_component.rerender_itself()
        else:
            transmissibility_component.derender_itself()
            drug_resistance_component.derender_itself()
            render_generate_genetic_architecture_method_component.derender_itself()

    
    def render_user_input(self, hide):
        """
        second render group, answered yes to method & 'user input' to genetic arch
        """
        # render all, derender, collect controls
        if hide:
            # controls rerender all
            return
        else:
            # controls dereneder all 
            return
        user_input_group_controls = {} 
        return user_input_group_controls
    
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
        
        # self.to_update_components.add(self.number_of_traits_label)

    def render_number_of_traits_title(self):
        column, frow = None, None
        self.render_number_of_traits_text = "Number of traits (Integer):"
        component = EasyLabel(self.render_number_of_traits_text, self.control_frame, column, frow)
        self.to_update_components.add(component)
        return component
# 
    def render_transmissibility(self):
        keys_path = ['GenomeElement', 'traits_num', 'transmissibility']
        self.render_transmissibility_text = "Transmissibility"
        component = EasyEntry(keys_path, self.config_path, self.render_transmissibility_text, 'transmissibility', self.control_frame, None, None, 'integer')
        self.to_update_components.add(component)
        return component
        # self.transmissibility_label = ttk.Label(self.control_frame, text=self.render_transmissibility_text, style = "Bold.TLabel")
        self.transmissibility_label = ttk.Label(self.control_frame, text=self.render_transmissibility_text, style = "Bold.TLabel")
        self.transmissibility_entry = ttk.Entry(self.control_frame, foreground="black")
        self.transmissibility_entry.insert(0, self.transmissibility)

        self.transmissibility_entry.grid()
        self.transmissibility_label.grid()
        # components.add(self.transmissibility, self.transmissibility_entry)

    def render_drug_resistance(self):
        keys_path = ['GenomeElement', 'traits_num', 'drug_resistance']
        self.render_drug_resistance_text = "Drug-Resistance"
        column, frow = None, None
        component = EasyEntry(keys_path, self.config_path, self.render_drug_resistance_text, 'drug-resistance', self.control_frame, column, frow, 'integer')
        self.to_update_components.add(component)
        return component
    
        self.drug_resistance_label = ttk.Label(self.control_frame, text=self.render_drug_resistance_text, style = "Bold.TLabel")
        self.drug_resistance_entry = ttk.Entry(self.control_frame, foreground="black")
        self.drug_resistance_entry.insert(0, self.drug_resistance)

        self.drug_resistance_entry.grid()
        self.drug_resistance_label.grid()
    
    def render_generate_genetic_architecture_file(self):
        render_generate_genetic_architecture_file_text = "Please provide the Genetic Architecture File in csv format:"
        keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', "gff"]
        config_path = self.config_path
        render_text = "Please provide the genome annotation in a gff-like format:"
        control_frame = self.control_frame
        column, frow = None, None
        component = EasyPathSelector(keys_path, config_path, render_text, control_frame, column, frow)
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
                # self.generate_genetic_architecture_method_combobox = ttk.Combobox(self.control_frame, textvariable=self.generate_genetic_architecture_method_var, values=generate_genetic_architecture_method_values, state="readonly")

        return component
        def update(event):
            """
            Updates the self.traits_num value in the params file
            """
            keys_path = ['GenomeElement', 'effect_size', 'method']
            converted_generate_genetic_architecture_method_var = render_to_val_generate_genetic_architecture_method.get(self.generate_genetic_architecture_method_var.get(), "")
            no_validate_update_val(converted_generate_genetic_architecture_method_var, self.config_path, keys_path)
            return
            try:
                if new_generate_genetic_architecture_method == "user_input":
                    self.hide_elements_update_methods()
                    self.render_path_eff_size_table()
                    # if not hasattr(self, 'path_network_label'):  
                    #     self.render_path_eff_size_table()
                    # else:
                    #     # break, show the label if it was previously created
                    #     self.path_network_label.grid()
                    #     self.choose_path_network_button.grid()
                    #     self.chosen_path_network_label.grid()

                elif new_generate_genetic_architecture_method == "randomly_generate":
                    self.hide_elements_update_methods()
                    self.render_rg_options()
            except ValueError:
                messagebox.showerror("Update Error", "Invalid Input.") 


        self.render_generate_genetic_architecture_method_text = "Method to Generate the Genetic Architecture"
        self.generate_genetic_architecture_method_label = ttk.Label(self.control_frame, text=self.render_generate_genetic_architecture_method_text, style = "Bold.TLabel")
        local_generate_genetic_architecture_method_var = val_to_render_generate_genetic_architecture_method.get(self.generate_genetic_architecture_method, "")
        self.generate_genetic_architecture_method_var = tk.StringVar(value=local_generate_genetic_architecture_method_var)
        self.generate_genetic_architecture_method_combobox = ttk.Combobox(self.control_frame, textvariable=self.generate_genetic_architecture_method_var, values=generate_genetic_architecture_method_values, state="readonly")
        self.generate_genetic_architecture_method_combobox.bind("<<ComboboxSelected>>", update)

        self.generate_genetic_architecture_method_label.grid()
        self.generate_genetic_architecture_method_combobox.grid()

    def render_genes_num(self):
        keys_path = ['GenomeElement','effect_size','randomly_generate','genes_num']
        render_text = "Number of Genomic Regions for each trait (list integer)"
        column, frow = None, None
        component =  EasyEntry(keys_path, self.config_path, render_text, "genes_num", self.control_frame, column, frow, "list")
        self.to_update_components.add(component)
        return component
        # controls = render_numerical_input(keys_path, self.config_path, render_text, self.control_frame, column, frow, "list")

    def render_randomly_generate(self):
        self.render_gff()
        effsize_min_component = self.render_effsize_min()
        effsize_max_component = self.render_effsize_max()
        normalize_component = self.render_normalize() 
    
    # def update_use_genetic_model(self):
    #     self.hide_elements_update_methods()
    #     new_use_network_model = self.use_genetic_model_var.get()
    #     if new_use_network_model in ["Yes", "No"]: 
    #         config = load_config_as_dict(self.config_path)
    #         config['GenomeElement']['use_genetic_model'] = string_to_bool_mapping[new_use_network_model]
    #         save_config(self.config_path, config)
            
    #         if new_use_network_model == "Yes":
    #             if not hasattr(self, "RP"):
    #                 def update_traits_num():
    #                     """
    #                     Updates the self.traits_num value in the params file
    #                     """
    #                     try:
    #                         traits_num_size_value = int(float(self.traits_num_entry.get()))
    #                         traits_num_size_value_2 = int(float(self.traits_num_entry_2.get()))
    #                         config = load_config_as_dict(self.config_path)
    #                         config['GenomeElement']['traits_num'] = [traits_num_size_value, traits_num_size_value_2]
    #                         save_config(self.config_path, config)   
    #                         message = "RP Parameters changed.\n\n" + "traits_num: " + str([traits_num_size_value, traits_num_size_value_2])
    #                         messagebox.showinfo("Update Successful", message)
    #                     except ValueError:
    #                         messagebox.showerror("Update Error", "Invalid Input.") 
    #                 self.traits_num_label = ttk.Label(self.control_frame, text="traits_num:")
    #                 self.traits_num_label.grid()
    #                 self.traits_num_entry = ttk.Entry(self.control_frame, foreground="black")
    #                 self.traits_num_entry.insert(0, self.traits_num[0])  
    #                 self.traits_num_entry_2 = ttk.Entry(self.control_frame, foreground="black")
    #                 self.traits_num_entry_2.insert(0, self.traits_num[1])
    #                 self.traits_num_entry.grid()
    #                 self.traits_num_entry_2.grid()

    #                 self.update_traits_num_button = tk.Button(self.control_frame, text="Update traits_num", command=update_traits_num)
    #                 self.update_traits_num_button.grid()
    #                     # traits num

    #                     # break
    #                 def update_effect_size_method():
    #                     """
    #                     Updates the self.traits_num value in the params file
    #                     """
    #                     new_effect_size_method = self.effect_size_method_var.get().strip().lower().replace(" ", "_")
    #                     config = load_config_as_dict(self.config_path)
    #                     config['GenomeElement']['effect_size']['method'] = new_effect_size_method
    #                     save_config(self.config_path, config)
    #                     try:
    #                         if new_effect_size_method == "user_input":
    #                             self.hide_elements_update_methods()
    #                             self.render_path_eff_size_table()
    #                         elif new_effect_size_method == "randomly_generate":
    #                             self.hide_elements_update_methods()
    #                             self.render_rg_options()
    #                     except ValueError:
    #                         messagebox.showerror("Update Error", "Invalid Input.") 

    #                 self.effect_size_method_label = ttk.Label(self.control_frame, text="effect_size_method:")
    #                 self.effect_size_method_label.grid()
    #                 self.effect_size_method_var = tk.StringVar()
    #                 self.effect_size_method_combobox = ttk.Combobox(self.control_frame, textvariable=self.effect_size_method_var, values=["user_input", "randomly_generate"], state="readonly")
    #                 self.effect_size_method_combobox.grid()
    #                 self.update_effect_size_method_button = tk.Button(self.control_frame, text="Update effect_size_method", command=update_effect_size_method)
    #                 self.update_effect_size_method_button.grid()
    #                     # break
    #             else:
    #                     # break
    #                 self.effect_size_method_label.grid()
    #                 self.effect_size_method_combobox.grid()
    #                 self.update_effect_size_method_button.grid()
    #                     # break
    #                 self.traits_num_label.grid()
    #                 self.traits_num_entry.grid()
    #                 self.update_traits_num_button.grid()
    #         elif new_use_network_model == "No":
    #             self.hide_elements_update_methods()
    #             if hasattr(self, 'method_label'): 
    #                 self.method_label.grid_forget()
    #                 self.method_combobox.grid_forget()
    #                 self.update_method_button.grid_forget()

    #         # break
    #         messagebox.showinfo("Update Successful", "use_network_model changed.")
    #     else:
    #         messagebox.showerror("Update Error", "Please enter 'Yes' or 'No' for use_network_model.")


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
        # return EasyEntry(keys_path, self.config_path, render_text, "effsize_min", self.control_frame, column, frow, "list")
        # render_effsize_min_controls = render_numerical_input(keys_path, self.config_path, render_text, self.control_frame, column, frow, "list")
        # self.effsize_min_label = ttk.Label(self.control_frame, text="effsize_min:")
        # self.effsize_min_label.grid()
        # self.effsize_min_entry = ttk.Entry(self.control_frame, foreground="black")
        # self.effsize_min_entry.insert(0, str(self.effsize_min))  
        # self.effsize_min_entry.grid()


        # components.add(self.effsize_min_label)
        # components.add(self.effsize_min_entry)
        
    def render_effsize_max(self):
        # self.effsize_max_label = ttk.Label(self.control_frame, text="effsize_max:")
        # self.effsize_max_entry = ttk.Entry(self.control_frame, foreground="black")
        # self.effsize_max_entry.insert(0, str(self.effsize_max))  
        # self.effsize_max_label.grid()
        # self.effsize_max_entry.grid()
        keys_path = ['GenomeElement','effect_size','randomly_generate','effsize_max']
        render_text = "Maximum Effect Size of each region for each trait (list numerical)"
        column, frow = None, None
        component = EasyEntry(keys_path, self.config_path, render_text, "effsize_min", self.control_frame, column, frow, "list")
        self.to_update_components.add(component)
        return component
        # components.add(self.effsize_max_label)
        # components.add(self.effsize_max_entry)

    def render_normalize(self):
        render_text = "Whether to Normalize randomly-selected effect sizes by the expected number of mutations?"
        keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', 'normalize']
        column, frow, = None, None
        # to_rerender, to_derender = None, None
        component =  EasyRadioButton(keys_path, self.config_path, render_text, "normalize", self.control_frame, column, frow)
        self.to_update_components.add(component)
        return component
        
        # self.normalize_label = ttk.Label(self.control_frame, text="normalize:")
        # self.normalize_label.grid()
        # self.normalize_var = tk.StringVar(value=bool_to_string_mapping[self.normalize])
        # self.normalize_combobox = ttk.Combobox(self.control_frame, textvariable=self.normalize_var, values=["Yes", "No"], state="readonly")
        # self.normalize_combobox.grid() 
        # components.add(self.normalize_label)
        # components.add(self.normalize_combobox)
        
    def hide_elements_update_methods(self):
        return
    def update_method(self):
        return

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
        keys_path = ['GenomeElement', 'effect_size', 'user_input', "path_effsize_table"]
        render_text = "Please provide the path to the effect size table:"
        column, frow = None, None
        component =  EasyPathSelector(keys_path, self.config_path, render_text, self.control_frame, column, frow)
        self.to_update_components.add(component)
        return component
        def choose_and_update_path():
            chosen_file = filedialog.askopenfilename(title="Select a path_effsize_table")
            if chosen_file:  
                # self.path_effsize_table = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['user_input']["path_effsize_table"]
                self.path_effsize_table = chosen_file
                self.chosen_path_network_label.config(text=f"path_effsize_table: {self.path_effsize_table}") 
                config = load_config_as_dict(self.config_path)
                config['GenomeElement']['effect_size']['user_input']["path_effsize_table"] = self.path_effsize_table
                save_config(self.config_path, config)


        self.path_network_label = ttk.Label(self.control_frame, text="Choose path_effsize_table")
        self.path_network_label.grid()
        self.choose_path_network_button = tk.Button(self.control_frame, text="path_effsize_table:", command = choose_and_update_path)
        self.choose_path_network_button.grid()
        self.chosen_path_network_label = ttk.Label(self.control_frame, text="Current path_effsize_table: " + self.path_effsize_table)
        self.chosen_path_network_label.grid()

        self.render_run_button()


    # def render_rg_options(self):
    #     if not hasattr(self, "gff_label"): 
    #         def clean_list_input(stripped_list_input, unstripped_list_input):
    #             if stripped_list_input == "":
    #                 parsed_new_seeded_host_id = []
    #             elif stripped_list_input.isdigit():
    #                 parsed_new_seeded_host_id = [int(float(stripped_list_input))]
    #             elif "," in unstripped_list_input:
    #                 parsed_new_seeded_host_id = [int(float(item.strip())) for item in stripped_list_input.split(',')]
    #             else:
    #                 raise ValueError("Invalid input format.")
                
    #             return parsed_new_seeded_host_id
            
    #         def update_all_rg_values():
    #             """
    #             Updates gff, genes_num, effsize min and max, and normalize in the params file
    #                 self.gff = ['GenomeElement']['effect_size']['randomly_generate']["gff"]
    #                 self.genes_num = ['GenomeElement']['effect_size']['randomly_generate']['genes_num']
    #                 self.effsize_min = ['GenomeElement']['effect_size']['randomly_generate']['effsize_min']
    #                 self.effsize_max = ['GenomeElement']['effect_size']['randomly_generate']['effsize_max']
    #                 self.normalize = ['GenomeElement']['effect_size']['randomly_generate']['normalize']
    #             """
    #             try:
    #                 new_normalize = str(self.normalize_var.get())
    #                 unstripped_list_genes_num_value = self.genes_num_entry.get().strip()
    #                 stripped_list_genes_num_value = unstripped_list_genes_num_value.strip("[]").strip()
    #                 unstripped_list_effsize_min_value = self.effsize_min_entry.get().strip()
    #                 stripped_list_effsize_min_value = unstripped_list_effsize_min_value.strip("[]").strip()
    #                 unstripped_list_effsize_max_value = self.effsize_max_entry.get().strip()
    #                 stripped_list_effsize_max_value = unstripped_list_effsize_max_value.strip("[]").strip()


    #                 genes_num_value = clean_list_input(stripped_list_genes_num_value, unstripped_list_genes_num_value)
    #                 effsize_min_value = clean_list_input(stripped_list_effsize_min_value, unstripped_list_effsize_min_value)
    #                 effsize_max_value = clean_list_input(stripped_list_effsize_max_value, unstripped_list_effsize_max_value)

    #                 config = load_config_as_dict(self.config_path)
    #                 config['GenomeElement']['effect_size']['randomly_generate']['genes_num'] = genes_num_value
    #                 config['GenomeElement']['effect_size']['randomly_generate']['effsize_min'] = effsize_min_value
    #                 config['GenomeElement']['effect_size']['randomly_generate']['effsize_max'] = effsize_max_value
    #                 config['GenomeElement']['effect_size']['randomly_generate']['normalize'] = string_to_bool_mapping[new_normalize]
    #                 save_config(self.config_path, config)   
    #                 messagebox.showinfo("Update Successful")
    #             except ValueError:
    #                 messagebox.showerror("Update Error", "Invalid Input.") 

    #         def choose_gff():
    #             """
    #             path selector
    #             self.gff = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['randomly_generate']["gff"]
    #             """
    #             chosen_file = filedialog.askopenfilename(title="Select a gff path")
    #             if chosen_file:  
    #                 self.gff = chosen_file
    #                 self.current_gff_label.config(text=f"Ref Path: {self.gff}") 
    #                 config = load_config_as_dict(self.config_path)
    #                 config['GenomeElement']['effect_size']['randomly_generate']["gff"] = self.gff
    #                 save_config(self.config_path, config)
            
    #         self.choose_gff_label = ttk.Label(self.control_frame, text="Choose gff path:")
    #         self.choose_gff_label.grid()
    #         self.choose_gff_button = tk.Button(self.control_frame, text="Choose path", command=choose_gff)
    #         self.choose_gff_button.grid()
    #         self.current_gff_label = ttk.Label(self.control_frame, text="Current gff path:" + self.gff)
    #         self.current_gff_label.grid()

    #         # self.update_ER_button = tk.Button(self.control_frame, text="Update rp_size", command=self.update_ER)
    #         self.update_all_rg_values_button = tk.Button(self.control_frame, text="Update All Parameters", command=update_all_rg_values)
    #         self.update_all_rg_values_button.grid()

    #         self.render_run_button()
    #     else:
    #         self.choose_gff_label.grid()
    #         self.choose_gff_button.grid()
    #         self.current_gff_label.grid()
    #         self.genes_num_label.grid()
    #         self.genes_num_entry.grid()
    #         self.effsize_min_label.grid()
    #         self.effsize_min_entry.grid()
    #         self.effsize_max_label.grid()
    #         self.effsize_max_entry.grid()
    #         self.normalize_label.grid()
    #         self.normalize_combobox.grid() 
    #         self.update_all_rg_values_button.grid()
        

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
            
            # run_effsize_generation(method, wk_dir, effsize_path=effsize_path, gff_in=gff_in, trait_n=trait_n, causal_sizes=causal_sizes, es_lows=es_lows, es_highs=es_highs, norm_or_not=norm_or_not, n_gen=n_gen, mut_rate=mut_rate)
            
            # err = run_effsize_generation(method, wk_dir, effsize_path=effsize_path, gff_in=gff_in, trait_n=trait_n, causal_sizes=causal_sizes, es_lows=es_lows, es_highs=es_highs, norm_or_not=norm_or_not, n_gen=n_gen, mut_rate=mut_rate)
            # if err:
            #     messagebox.showerror("Generation Error", "Generation Error: " + str(err))
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

        # if len(self.config_dict['GenomeElement']['traits_num']) == 0:
        #     self.traits_num = [0, 0]
        #     self.transmissibility = 0
        #     self.drug_resistance = 0
        # elif len(self.config_dict['GenomeElement']['traits_num']) == 2:
        #     self.traits_num = self.config_dict['GenomeElement']['traits_num']
        #     self.transmissibility = self.traits_num[0]
        #     self.drug_resistance = self.traits_num[1]
        # else:
        #     raise ValueError("Error: traits_num should have only 2 values.")

        self.generate_genetic_architecture_method = self.config_dict['GenomeElement']['effect_size']['method']
        self.path_effsize_table = self.config_dict['GenomeElement']['effect_size']['user_input']["path_effsize_table"]
        self.gff = self.config_dict['GenomeElement']['effect_size']['randomly_generate']["gff"]
        self.genes_num = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['genes_num']
        self.effsize_min = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['effsize_min']
        self.effsize_max = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['effsize_max']
        self.normalize = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['normalize']