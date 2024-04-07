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
    
    def render_genetic_architecture_group(self):
        """
        first render group for yes/no forms
        """
        return

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
        return EasyPathSelector(keys_path, config_path, render_text, control_frame, column, frow)
        # path_select_controls = render_path_select(keys_path, config_path, render_text, control_frame, column, frow)
        # return path_select_controls

    def render_number_of_traits(self):
        return

    def render_number_of_traits_title(self):
        self.render_number_of_traits_text = "Number of traits (Integer):"
        self.number_of_traits_label = ttk.Label(self.control_frame, text=self.render_number_of_traits_text, style = "Bold.TLabel")
        self.number_of_traits_label.grid()
        # components.add(self.number_of_traits_label)
# 
    def render_transmissibility(self):
        keys_path = ['GenomeElement', 'traits_num', 'transmissibility']
        self.render_transmissibility_text = "Transmissibility"
        return EasyEntry(keys_path, self.config_path, self.render_transmissibility_text, 'transmissibility', self.control_frame, None, None, 'integer')
        self.transmissibility_label = ttk.Label(self.control_frame, text=self.render_transmissibility_text, style = "Bold.TLabel")
        self.transmissibility_entry = ttk.Entry(self.control_frame, foreground="black")
        self.transmissibility_entry.insert(0, self.transmissibility)

        self.transmissibility_entry.grid()
        self.transmissibility_label.grid()
        # components.add(self.transmissibility, self.transmissibility_entry)

    def render_drug_resistance(self):
        keys_path = ['GenomeElement', 'traits_num', 'drug_resistance']
        self.render_drug_resistance_text = "Drug-Resistance"
        self.drug_resistance_label = ttk.Label(self.control_frame, text=self.render_drug_resistance_text, style = "Bold.TLabel")
        self.drug_resistance_entry = ttk.Entry(self.control_frame, foreground="black")
        self.drug_resistance_entry.insert(0, self.drug_resistance)

        self.drug_resistance_entry.grid()
        self.drug_resistance_label.grid()


    def render_generate_genetic_architecture_method(self):
        """
        generate_genetic_architecture_method
        self.generate_genetic_architecture_method = ['GenomeElement']['effect_size']['method']
        """
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
        # controls = render_numerical_input(keys_path, self.config_path, render_text, self.control_frame, column, frow, "list")
        return None

    def render_randomly_generate(self):
        gff_component = self.render_gff()
        effsize_min_component = self.render_effsize_min()
        effsize_max_component = self.render_effsize_max()
        normalize_component = self.render_normalize() 
    
    def update_use_genetic_model(self):
        self.hide_elements_update_methods()
        new_use_network_model = self.use_genetic_model_var.get()
        if new_use_network_model in ["Yes", "No"]: 
            config = load_config_as_dict(self.config_path)
            config['GenomeElement']['use_genetic_model'] = string_to_bool_mapping[new_use_network_model]
            save_config(self.config_path, config)
            
            if new_use_network_model == "Yes":
                if not hasattr(self, "RP"):
                    def update_traits_num():
                        """
                        Updates the self.traits_num value in the params file
                        """
                        try:
                            traits_num_size_value = int(float(self.traits_num_entry.get()))
                            traits_num_size_value_2 = int(float(self.traits_num_entry_2.get()))
                            config = load_config_as_dict(self.config_path)
                            config['GenomeElement']['traits_num'] = [traits_num_size_value, traits_num_size_value_2]
                            save_config(self.config_path, config)   
                            message = "RP Parameters changed.\n\n" + "traits_num: " + str([traits_num_size_value, traits_num_size_value_2])
                            messagebox.showinfo("Update Successful", message)
                        except ValueError:
                            messagebox.showerror("Update Error", "Invalid Input.") 
                    self.traits_num_label = ttk.Label(self.control_frame, text="traits_num:")
                    self.traits_num_label.grid()
                    self.traits_num_entry = ttk.Entry(self.control_frame, foreground="black")
                    self.traits_num_entry.insert(0, self.traits_num[0])  
                    self.traits_num_entry_2 = ttk.Entry(self.control_frame, foreground="black")
                    self.traits_num_entry_2.insert(0, self.traits_num[1])
                    self.traits_num_entry.grid()
                    self.traits_num_entry_2.grid()

                    self.update_traits_num_button = tk.Button(self.control_frame, text="Update traits_num", command=update_traits_num)
                    self.update_traits_num_button.grid()
                        # traits num

                        # break
                    def update_effect_size_method():
                        """
                        Updates the self.traits_num value in the params file
                        """
                        new_effect_size_method = self.effect_size_method_var.get().strip().lower().replace(" ", "_")
                        config = load_config_as_dict(self.config_path)
                        config['GenomeElement']['effect_size']['method'] = new_effect_size_method
                        save_config(self.config_path, config)
                        try:
                            if new_effect_size_method == "user_input":
                                self.hide_elements_update_methods()
                                self.render_path_eff_size_table()
                            elif new_effect_size_method == "randomly_generate":
                                self.hide_elements_update_methods()
                                self.render_rg_options()
                        except ValueError:
                            messagebox.showerror("Update Error", "Invalid Input.") 

                    self.effect_size_method_label = ttk.Label(self.control_frame, text="effect_size_method:")
                    self.effect_size_method_label.grid()
                    self.effect_size_method_var = tk.StringVar()
                    self.effect_size_method_combobox = ttk.Combobox(self.control_frame, textvariable=self.effect_size_method_var, values=["user_input", "randomly_generate"], state="readonly")
                    self.effect_size_method_combobox.grid()
                    self.update_effect_size_method_button = tk.Button(self.control_frame, text="Update effect_size_method", command=update_effect_size_method)
                    self.update_effect_size_method_button.grid()
                        # break
                else:
                        # break
                    self.effect_size_method_label.grid()
                    self.effect_size_method_combobox.grid()
                    self.update_effect_size_method_button.grid()
                        # break
                    self.traits_num_label.grid()
                    self.traits_num_entry.grid()
                    self.update_traits_num_button.grid()
            elif new_use_network_model == "No":
                self.hide_elements_update_methods()
                if hasattr(self, 'method_label'): 
                    self.method_label.grid_forget()
                    self.method_combobox.grid_forget()
                    self.update_method_button.grid_forget()

            # break
            messagebox.showinfo("Update Successful", "use_network_model changed.")
        else:
            messagebox.showerror("Update Error", "Please enter 'Yes' or 'No' for use_network_model.")


    def render_use_genetic_model(self, to_rerender, to_derender):
        keys_path = ['GenomeElement', 'use_genetic_model']
        render_use_genetic_model_text = "Do you want to use genetic architecture for traits (transmissibility and/or Drug-resistance)?"
        column, frow = None, None
        # EasyWidget
        use_genetic_model_rb = EasyRadioButton(keys_path, self.config_path, render_use_genetic_model_text, "use_genetic_model", self.control_frame, column, frow, to_rerender, to_derender)
        use_genetic_model_rb.derender_itself()
        use_genetic_model_rb.rerender_itself()
    
    def render_effsize_min(self):
        keys_path = ['GenomeElement','effect_size','randomly_generate','effsize_min']
        render_text = "Minimum Effect Size of each region for each trait (list numerical)"
        frow, column = None, None
        return EasyEntry(keys_path, self.config_path, render_text, "effsize_min", self.control_frame, column, frow, "list")
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
        effsize_max = EasyEntry(keys_path, self.config_path, render_text, "effsize_min", self.control_frame, column, frow, "list")
        # components.add(self.effsize_max_label)
        # components.add(self.effsize_max_entry)

    def render_normalize(self):
        render_text = "Maximum Effect Size of each region for each trait (list numerical)"
        keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', 'normalize']
        column, frow, to_rerender, to_derender = None, None, None, None
        normalize = EasyRadioButton(keys_path, self.config_path, render_text, "normalize", self.control_frame, column, frow, to_rerender, to_derender)

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


    def render_rg_options(self):
        if not hasattr(self, "gff_label"): 
            def clean_list_input(stripped_list_input, unstripped_list_input):
                if stripped_list_input == "":
                    parsed_new_seeded_host_id = []
                elif stripped_list_input.isdigit():
                    parsed_new_seeded_host_id = [int(float(stripped_list_input))]
                elif "," in unstripped_list_input:
                    parsed_new_seeded_host_id = [int(float(item.strip())) for item in stripped_list_input.split(',')]
                else:
                    raise ValueError("Invalid input format.")
                
                return parsed_new_seeded_host_id
            
            def update_all_rg_values():
                """
                Updates gff, genes_num, effsize min and max, and normalize in the params file
                    self.gff = ['GenomeElement']['effect_size']['randomly_generate']["gff"]
                    self.genes_num = ['GenomeElement']['effect_size']['randomly_generate']['genes_num']
                    self.effsize_min = ['GenomeElement']['effect_size']['randomly_generate']['effsize_min']
                    self.effsize_max = ['GenomeElement']['effect_size']['randomly_generate']['effsize_max']
                    self.normalize = ['GenomeElement']['effect_size']['randomly_generate']['normalize']
                """
                try:
                    new_normalize = str(self.normalize_var.get())
                    unstripped_list_genes_num_value = self.genes_num_entry.get().strip()
                    stripped_list_genes_num_value = unstripped_list_genes_num_value.strip("[]").strip()
                    unstripped_list_effsize_min_value = self.effsize_min_entry.get().strip()
                    stripped_list_effsize_min_value = unstripped_list_effsize_min_value.strip("[]").strip()
                    unstripped_list_effsize_max_value = self.effsize_max_entry.get().strip()
                    stripped_list_effsize_max_value = unstripped_list_effsize_max_value.strip("[]").strip()


                    genes_num_value = clean_list_input(stripped_list_genes_num_value, unstripped_list_genes_num_value)
                    effsize_min_value = clean_list_input(stripped_list_effsize_min_value, unstripped_list_effsize_min_value)
                    effsize_max_value = clean_list_input(stripped_list_effsize_max_value, unstripped_list_effsize_max_value)

                    config = load_config_as_dict(self.config_path)
                    config['GenomeElement']['effect_size']['randomly_generate']['genes_num'] = genes_num_value
                    config['GenomeElement']['effect_size']['randomly_generate']['effsize_min'] = effsize_min_value
                    config['GenomeElement']['effect_size']['randomly_generate']['effsize_max'] = effsize_max_value
                    config['GenomeElement']['effect_size']['randomly_generate']['normalize'] = string_to_bool_mapping[new_normalize]
                    save_config(self.config_path, config)   
                    messagebox.showinfo("Update Successful")
                except ValueError:
                    messagebox.showerror("Update Error", "Invalid Input.") 

            def choose_gff():
                """
                path selector
                self.gff = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['randomly_generate']["gff"]
                """
                chosen_file = filedialog.askopenfilename(title="Select a gff path")
                if chosen_file:  
                    self.gff = chosen_file
                    self.current_gff_label.config(text=f"Ref Path: {self.gff}") 
                    config = load_config_as_dict(self.config_path)
                    config['GenomeElement']['effect_size']['randomly_generate']["gff"] = self.gff
                    save_config(self.config_path, config)
            
            self.choose_gff_label = ttk.Label(self.control_frame, text="Choose gff path:")
            self.choose_gff_label.grid()
            self.choose_gff_button = tk.Button(self.control_frame, text="Choose path", command=choose_gff)
            self.choose_gff_button.grid()
            self.current_gff_label = ttk.Label(self.control_frame, text="Current gff path:" + self.gff)
            self.current_gff_label.grid()

            # self.update_ER_button = tk.Button(self.control_frame, text="Update rp_size", command=self.update_ER)
            self.update_all_rg_values_button = tk.Button(self.control_frame, text="Update All Parameters", command=update_all_rg_values)
            self.update_all_rg_values_button.grid()

            self.render_run_button()
        else:
            self.choose_gff_label.grid()
            self.choose_gff_button.grid()
            self.current_gff_label.grid()
            self.genes_num_label.grid()
            self.genes_num_entry.grid()
            self.effsize_min_label.grid()
            self.effsize_min_entry.grid()
            self.effsize_max_label.grid()
            self.effsize_max_entry.grid()
            self.normalize_label.grid()
            self.normalize_combobox.grid() 
            self.update_all_rg_values_button.grid()
        

    def render_run_button(self):
        def effect_size_generation():
            config = load_config_as_dict(self.config_path) 

            method = config['GenomeElement']['effect_size']['method']
            wk_dir = config["BasicRunConfiguration"]["cwdir"]
            n_gen = config["EvolutionModel"]["n_generation"]
            mut_rate = config["EvolutionModel"]["mut_rate"]
            trait_n = config['GenomeElement']['traits_num']

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
                print("Invalid method specified")
                return
            
            run_effsize_generation(method, wk_dir, effsize_path=effsize_path, gff_in=gff_in, trait_n=trait_n, causal_sizes=causal_sizes, es_lows=es_lows, es_highs=es_highs, norm_or_not=norm_or_not, n_gen=n_gen, mut_rate=mut_rate)

            
        self.run_effect_size_generation_button = tk.Button(self.control_frame, text="run_effect_size_generation_button", command=effect_size_generation)
        self.run_effect_size_generation_button.grid()


    def init_tab(self, parent, tab_parent, tab_title, tab_index, hide):
        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_index = tab_index
        self.tab_parent.add(parent, text=tab_title)
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")
        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True)

    def initial_load(self):
        self.render_randomly_generate()
        return
        # render_user_input_controls = self.render_user_input()
        # feed render_user_input controls into render_genetic_architecture_group
        # render + derender everything, feed renderers/derenderers
        self.render_genetic_architecture_group()
        self.render_use_genetic_model(None, None)
        return
        
        self.render_generate_genetic_architecture_method()
        
        # self.render_randomly_generate()

    def global_update(self):
        users_validation_messages = []

        for id, updater in zip(self.component_id, self.updaters.values()):
            updater(users_validation_messages, id)

        match len(users_validation_messages):
            case 0:
                messagebox.showinfo("Update Successful", "Parameters Updated.")
                return 0
            case _:
                error_message_str = "\n\n".join(users_validation_messages)
                messagebox.showerror("Update Error", error_message_str)
                return 1
            

    def init_val(self, config_path):
        self.updaters = {}
        self.rerenderers = {}
        self.derenderers = {}
        self.component_id = [
            "genetic_model",
            "gff",
            "number_of_traits",
            "transmissibility",
            "drug_resistance",
            "generate_genetic_architecture_method",
            "genes_num",
            "randomly_generate",
            "genetic_model",
            "effsize_min",
            "effsize_max",
            "path_effsize_table",
            "rg_options"
        ]
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