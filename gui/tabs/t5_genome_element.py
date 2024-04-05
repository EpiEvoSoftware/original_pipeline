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
    
from genetic_effect_generator import *


class GenomeElement:
    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):
        
        self.init_val(config_path)
        self.init_tab(parent, tab_parent, tab_title, tab_index, hide)
        self.initial_load()

        render_next_button(self.tab_index, self.tab_parent, self.parent)


    def initial_load(self):
        self.render_use_genetic_model()
        self.render_generate_genetic_architecture_method()
        self.render_user_input()
        
        self.randomly_generate_components = self.render_randomly_generate()
        # self.randomly_generate_grid_configs = derender_components(self.randomly_generate_components)

    def init_val(self, config_path):
        # testingrp
    # User Configurations
        # bool
        self.config_path = config_path
        self.config_dict = load_config_as_dict(self.config_path)
        self.use_genetic_model = self.config_dict['GenomeElement']['use_genetic_model']
        # list
        self.traits_num = self.config_dict['GenomeElement']['traits_num']

        if len(self.traits_num) > 0:
            self.transmissibility = self.traits_num[0]
            self.drug_resistance = self.traits_num[1]

        # str
        self.generate_genetic_architecture_method = self.config_dict['GenomeElement']['effect_size']['method']
        self.path_effsize_table = self.config_dict['GenomeElement']['effect_size']['user_input']["path_effsize_table"]

        # str
        self.gff = self.config_dict['GenomeElement']['effect_size']['randomly_generate']["gff"]
        # list
        self.genes_num = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['genes_num']
        # list
        self.effsize_min = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['effsize_min']
        # list
        self.effsize_max = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['effsize_max']
        # bool
        self.normalize = self.config_dict['GenomeElement']['effect_size']['randomly_generate']['normalize']
        # self.config_dict = load_config_as_dict(self.config_path)
        # self.use_genetic_model = load_config_as_dict(self.config_path)['GenomeElement']['use_genetic_model']
        # # list
        # self.traits_num = load_config_as_dict(self.config_path)['GenomeElement']['traits_num']

        # self.transmissibility = self.traits_num[0]
        # self.drug_resistance = self.traits_num[1]

        # # str
        # self.generate_genetic_architecture_method = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['method']
        # self.path_effsize_table = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['user_input']["path_effsize_table"]

        # # str
        # self.gff = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['randomly_generate']["gff"]
        # # list
        # self.genes_num = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['randomly_generate']['genes_num']
        # # list
        # self.effsize_min = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['randomly_generate']['effsize_min']
        # # list
        # self.effsize_max = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['randomly_generate']['effsize_max']
        # # bool
        # self.normalize = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['randomly_generate']['normalize']
    # 
# 
    def render_user_input(self):
        user_input_components = set()
        # self.render_gff(user_input_components)
        # self.render_effsize_min(user_input_components)
        # self.render_effsize_max(user_input_components)
        # self.render_normalize(user_input_components)
        return user_input_components
    
    # def render_path_select(components, keys_path, update_var, config_path, render_text, label, var)
    def render_gff(self, components):
        keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', "gff"]
        config_path = self.config_path
        render_text = "Please provide the genome annotation in a gff-like format:"
        control_frame = self.control_frame
        column, frow = None, None
        render_path_select(components, keys_path, config_path, render_text, control_frame, column, frow)
        # """
        # self.gff = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['randomly_generate']["gff"]
        # keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', "gff"]
        # """
        # def update():
        #     # chosen_file = filedialog.askopenfilename(title="Select a File", filetypes=[("gff files", "*.csv")])
        #     chosen_file = filedialog.askopenfilename(title="Select a File")
        #     if chosen_file:
        #         keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', "gff"]
        #         no_validate_update(self.gff_var, self.config_path, keys_path)
        #         self.gff = chosen_file
        #         self.gff_value_label.config(text=self.gff) 

        # self.render_gff_text = "Please provide the genome annotation in a gff-like format:"
        # self.gff_var = tk.StringVar(value=self.gff)
        # self.gff_label = ttk.Label(self.control_frame, text=self.render_gff_text, style = "Bold.TLabel")

        # if self.gff == "":
        #     self.gff_value_label = ttk.Label(self.control_frame, text = "None selected", foreground="black")
        # else:
        #     self.gff_value_label = ttk.Label(self.control_frame, text = self.gff, foreground="black")

        # self.gff_button = tk.Button(self.control_frame, text="Choose File", command=update)

        # # self.gff_label.grid(row = 12, column = 1, sticky = 'w', pady = 5)
        # # self.gff_value_label.grid(row=13, column=1, sticky='w', pady=5)
        # # self.gff_button.grid(row=14, column=1, sticky='e', pady=5)
        # self.gff_label.grid()
        # self.gff_value_label.grid()
        # self.gff_button.grid()


        # components.add(self.gff_label)
        # components.add(self.gff_value_label)
        # components.add(self.gff_button)

    def render_number_of_traits(self, components):
        return

    def render_number_of_traits_title(self, components):
        self.render_number_of_traits_text = "Number of traits (integer):"
        self.number_of_traits_label = ttk.Label(self.control_frame, text=self.render_number_of_traits_text, style = "Bold.TLabel")
        self.number_of_traits_label.grid()
        components.add(self.number_of_traits_label)

    def render_transmissibility(self, components):
        self.render_transmissibility_text = "Transmissibility"
        self.transmissibility_label = ttk.Label(self.control_frame, text=self.render_transmissibility_text, style = "Bold.TLabel")
        self.transmissibility_entry = ttk.Entry(self.control_frame, foreground="black")
        self.transmissibility_entry.insert(0, self.transmissibility)

        self.transmissibility_entry.grid()
        self.transmissibility_label.grid()
        components.add(self.transmissibility, self.transmissibility_entry)

    def render_drug_resistance(self, components):
        self.render_drug_resistance_text = "Drug-Resistance"
        self.drug_resistance_label = ttk.Label(self.control_frame, text=self.render_drug_resistance_text, style = "Bold.TLabel")
        self.drug_resistance_entry = ttk.Entry(self.control_frame, foreground="black")
        self.drug_resistance_entry.insert(0, self.drug_resistance)

        self.drug_resistance_entry.grid()
        self.drug_resistance_label.grid()
        components.add(self.drug_resistance, self.drug_resistance_entry)


    # def render_gff(self, components):
    #     """
    #     self.gff = load_config_as_dict(self.config_path)['GenomeElement']['effect_size']['randomly_generate']["gff"]
    #     keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', "gff"]
    #     """
    #     def update():
    #         # chosen_file = filedialog.askopenfilename(title="Select a File", filetypes=[("gff files", "*.csv")])
    #         chosen_file = filedialog.askopenfilename(title="Select a File")
    #         if chosen_file:
    #             keys_path = ['GenomeElement', 'effect_size', 'randomly_generate', "gff"]
    #             no_validate_update(self.gff_var, self.config_path, keys_path)
    #             self.gff = chosen_file
    #             self.gff_value_label.config(text=self.gff) 

    #     self.render_gff_text = "Please provide the genome annotation in a gff-like format:"
    #     self.gff_var = tk.StringVar(value=self.gff)
    #     self.gff_label = ttk.Label(self.control_frame, text=self.render_gff_text, style = "Bold.TLabel")

    #     if self.gff == "":
    #         self.gff_value_label = ttk.Label(self.control_frame, text = "None selected", foreground="black")
    #     else:
    #         self.gff_value_label = ttk.Label(self.control_frame, text = self.gff, foreground="black")

    #     self.gff_button = tk.Button(self.control_frame, text="Choose File", command=update)

    #     # self.gff_label.grid(row = 12, column = 1, sticky = 'w', pady = 5)
    #     # self.gff_value_label.grid(row=13, column=1, sticky='w', pady=5)
    #     # self.gff_button.grid(row=14, column=1, sticky='e', pady=5)
    #     self.gff_label.grid()
    #     self.gff_value_label.grid()
    #     self.gff_button.grid()


    #     components.add(self.gff_label)
    #     components.add(self.gff_value_label)
    #     components.add(self.gff_button)


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


    def render_genes_num(self, components):
        """
        # self.genes_num = ['GenomeElement']['effect_size']['randomly_generate']['genes_num']
        """
        self.render_genes_num_text = "Number of Genomic Regions for each trait (list integer)"
        self.genes_num_label = ttk.Label(self.control_frame, text=self.render_genes_num_text, style = "Bold.TLabel")
        self.genes_num_entry = ttk.Entry(self.control_frame, foreground="black")
        self.genes_num_entry.insert(0, str(self.genes_num))  

        self.genes_num_label.grid()
        self.genes_num_entry.grid()

        components.add(self.genes_num_label)
        components.add(self.genes_num_entry)
    def render_randomly_generate(self):
        randomly_generate_components = set()
        self.render_gff(randomly_generate_components)
        self.render_effsize_min(randomly_generate_components)
        self.render_effsize_max(randomly_generate_components)
        self.render_normalize(randomly_generate_components)
        return randomly_generate_components
    
    def update_use_genetic_model(self):
        # self.use_genetic_model = load_config_as_dict(self.config_path)['GenomeElement']['use_genetic_model']
        self.hide_elements_update_methods()
        new_use_network_model = self.use_genetic_model_var.get()
        if new_use_network_model in ["Yes", "No"]: 
            config = load_config_as_dict(self.config_path)
            config['GenomeElement']['use_genetic_model'] = string_to_bool_mapping[new_use_network_model]
            save_config(self.config_path, config)
            

            # break
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
                                # if not hasattr(self, 'path_network_label'):  
                                #     self.render_path_eff_size_table()
                                # else:
                                #     # break, show the label if it was previously created
                                #     self.path_network_label.grid()
                                #     self.choose_path_network_button.grid()
                                #     self.chosen_path_network_label.grid()

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

    def render_use_genetic_model(self):
        """
        self.use_genetic_model = load_config_as_dict(self.config_path)['GenomeElement']['use_genetic_model']
        """
        def update():
            keys_path = ['GenomeElement', 'use_genetic_model']
            no_validate_update(self.use_genetic_model_var, self.config_path, keys_path)
            use_genetic_model_local = get_dict_val(load_config_as_dict(self.config_path), keys_path)
            if use_genetic_model_local:
                print("use_genetic_model_local: ", use_genetic_model_local)
                # self.use_method_grid_configs = derender_components(self.use_method_components)
                # self.user_input_grid_configs = derender_components(self.user_input_components)
                # self.wf_grid_configs = derender_components(self.wf_components)
                # self.epi_grid_configs = derender_components(self.epi_components)
            else:
                print("use_genetic_model_local: ", use_genetic_model_local)
                # rerender_components(self.use_method_components, self.use_method_grid_configs)
                # rerender_components(self.user_input_components, self.user_input_grid_configs)  
                # keys_path = ['SeedsConfiguration', 'method']
                # use_method_local = get_dict_val(load_config_as_dict(self.config_path), keys_path)
                # match use_method_local:
                #     case "user_input":
                #         rerender_components(self.user_input_components, self.user_input_grid_configs)  
                #     case "SLiM_burnin_WF":
                #         rerender_components(self.wf_components, self.wf_grid_configs)    
                #     case "SLiM_burnin_epi":
                #         rerender_components(self.epi_components, self.epi_grid_configs)
            

        self.render_use_genetic_model_text = "Do you want to use genetic architecture for traits (transmissibility and/or Drug-resistance)?"
        self.use_genetic_model_var = tk.BooleanVar(value=self.use_genetic_model)
        self.use_genetic_model_label = ttk.Label(self.control_frame, text=self.render_use_genetic_model_text, style = "Bold.TLabel")
        self.use_genetic_true = ttk.Radiobutton(self.control_frame, text="Yes", variable=self.use_genetic_model_var, value=True, command = update)
        self.use_genetic_false = ttk.Radiobutton(self.control_frame, text="No", variable=self.use_genetic_model_var, value=False, command = update)

        self.use_genetic_model_label.grid()
        self.use_genetic_true.grid()
        self.use_genetic_false.grid()
        # self.use_genetic_model_label.grid(row = 3, column = 1, sticky = 'w', pady = 5)
        # self.use_genetic_true.grid(row = 4, column = 1, columnspan= 3, sticky='w', pady=5)
        # self.use_genetic_false.grid(row = 5, column = 1, columnspan= 3, sticky='w', pady=5)
    def render_effsize_min(self, components):
        self.effsize_min_label = ttk.Label(self.control_frame, text="effsize_min:")
        self.effsize_min_label.grid()
        self.effsize_min_entry = ttk.Entry(self.control_frame, foreground="black")
        self.effsize_min_entry.insert(0, str(self.effsize_min))  
        self.effsize_min_entry.grid()
        components.add(self.effsize_min_label)
        components.add(self.effsize_min_entry)
        
    def render_effsize_max(self, components):
        self.effsize_max_label = ttk.Label(self.control_frame, text="effsize_max:")
        self.effsize_max_entry = ttk.Entry(self.control_frame, foreground="black")
        self.effsize_max_entry.insert(0, str(self.effsize_max))  
        self.effsize_max_label.grid()
        self.effsize_max_entry.grid()
        components.add(self.effsize_max_label)
        components.add(self.effsize_max_entry)

    def render_normalize(self, components):
        self.normalize_label = ttk.Label(self.control_frame, text="normalize:")
        self.normalize_label.grid()
        self.normalize_var = tk.StringVar(value=bool_to_string_mapping[self.normalize])
        self.normalize_combobox = ttk.Combobox(self.control_frame, textvariable=self.normalize_var, values=["Yes", "No"], state="readonly")
        self.normalize_combobox.grid() 
        components.add(self.normalize_label)
        components.add(self.normalize_combobox)
        
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
            
    def parse_list_input(input_str):
        if input_str.startswith('[') and input_str.endswith(']'):
            input_str = input_str[1:-1]  
        return [int(float(item.strip())) for item in input_str.split(',') if item.strip().isdigit()]

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