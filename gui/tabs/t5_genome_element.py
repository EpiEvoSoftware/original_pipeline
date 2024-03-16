import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class GenomeElement:
    def __init__(self, parent, tab_parent, config_path):
        

        self.network_model_to_string = {
            "Erdős–Rényi": "ER",
            "Barabási-Albert": "BA",
            "Random Partition": "RP"
        }

        self.string_to_network_mode = {
            "ER": "Erdős–Rényi",
            "BA": "Barabási-Albert",
            "RP": "Random Partition"
        }
        
        self.graph_values = ["Erdős–Rényi", "Barabási-Albert", "Random Partition"]

        self.string_to_bool_mapping = {
            "yes": True,
            "no": False,
            "Yes": True,
            "No": False
        }

        self.bool_to_string_mapping = {
            True: "Yes",
            False: "No"
        }

        self.config_path = config_path

    # User Configurations
        # bool
        self.use_genetic_model = self.load_config_as_dict()['GenomeElement']['use_genetic_model']
        # list
        self.traits_num = self.load_config_as_dict()['GenomeElement']['traits_num']

        # str
        self.path_effsize_table = self.load_config_as_dict()['GenomeElement']['effect_size']['user_input']["path_effsize_table"]

        # str
        self.gff = self.load_config_as_dict()['GenomeElement']['effect_size']['randomly_generate']["gff"]
        # list
        self.genes_num = self.load_config_as_dict()['GenomeElement']['effect_size']['randomly_generate']['genes_num']
        # list
        self.effsize_min = self.load_config_as_dict()['GenomeElement']['effect_size']['randomly_generate']['effsize_min']
        # list
        self.effsize_max = self.load_config_as_dict()['GenomeElement']['effect_size']['randomly_generate']['effsize_max']
        # bool
        self.normalize = self.load_config_as_dict()['GenomeElement']['effect_size']['randomly_generate']['normalize']
    # 

        self.parent = parent
        self.tab_parent = tab_parent
        self.dynamic_widgets = []

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 


        # Modified part for scrolling
            # 
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
            # 
        # 


        self.use_genetic_model_label = ttk.Label(self.scrollable_frame, text="use_genetic_model:")
        self.use_genetic_model_label.pack()
        self.use_genetic_model_var = tk.StringVar(value=self.bool_to_string_mapping[self.use_genetic_model])
        self.use_genetic_model_combobox = ttk.Combobox(self.scrollable_frame, textvariable=self.use_genetic_model_var, values=["Yes", "No"], state="readonly")
        self.use_genetic_model_combobox.pack()
        self.update_use_genetic_model_button = tk.Button(self.scrollable_frame, text="Update use_genetic_model", command=self.update_use_genetic_model)
        self.update_use_genetic_model_button.pack()

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

# Setup
    #   
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
    # 
# 
    def update_use_genetic_model(self):
        # self.use_genetic_model = self.load_config_as_dict()['GenomeElement']['use_genetic_model']
        self.hide_elements_update_methods()
        new_use_network_model = self.use_genetic_model_var.get()
        if new_use_network_model in ["Yes", "No"]: 
            config = self.load_config_as_dict()
            config['GenomeElement']['use_genetic_model'] = self.string_to_bool_mapping[new_use_network_model]
            self.save_config(config)

            # break
            if new_use_network_model == "Yes":
                if not hasattr(self, "RP"):
                    def update_traits_num():
                        """
                        Updates the self.traits_num value in the params file
                        """
                        try:
                            traits_num_size_value = int(self.traits_num_entry.get())
                            traits_num_size_value_2 = int(self.traits_num_entry_2.get())
                            config = self.load_config_as_dict()
                            config['GenomeElement']['traits_num'] = [traits_num_size_value, traits_num_size_value_2]
                            self.save_config(config)   
                            message = "RP Parameters changed.\n\n" + "traits_num: " + str([traits_num_size_value, traits_num_size_value_2])
                            messagebox.showinfo("Update Successful", message)
                        except ValueError:
                            messagebox.showerror("Update Error", "Invalid Input.") 
                    self.traits_num_label = ttk.Label(self.scrollable_frame, text="traits_num:")
                    self.traits_num_label.pack()
                    self.traits_num_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.traits_num_entry.insert(0, self.traits_num[0])  
                    self.traits_num_entry_2 = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.traits_num_entry_2.insert(0, self.traits_num[1])
                    self.traits_num_entry.pack()
                    self.traits_num_entry_2.pack()

                    self.update_traits_num_button = tk.Button(self.scrollable_frame, text="Update traits_num", command=update_traits_num)
                    self.update_traits_num_button.pack()
                        # traits num

                        # break
                    def update_effect_size_method():
                        """
                        Updates the self.traits_num value in the params file
                        """
                        new_effect_size_method = self.effect_size_method_var.get().strip().lower()
                        try:
                            if new_effect_size_method == "user_input":
                                self.hide_elements_update_methods()
                                self.render_path_eff_size_table()
                                # if not hasattr(self, 'path_network_label'):  
                                #     self.render_path_eff_size_table()
                                # else:
                                #     # break, show the label if it was previously created
                                #     self.path_network_label.pack()
                                #     self.choose_path_network_button.pack()
                                #     self.chosen_path_network_label.pack()

                            elif new_effect_size_method == "randomly generate":
                                self.hide_elements_update_methods()
                                self.render_rg_options()
                        except ValueError:
                            messagebox.showerror("Update Error", "Invalid Input.") 

                    self.effect_size_method_label = ttk.Label(self.scrollable_frame, text="effect_size_method:")
                    self.effect_size_method_label.pack()
                    self.effect_size_method_var = tk.StringVar()
                    self.effect_size_method_combobox = ttk.Combobox(self.scrollable_frame, textvariable=self.effect_size_method_var, values=["user_input", "randomly generate"], state="readonly")
                    self.effect_size_method_combobox.pack()
                    self.update_effect_size_method_button = tk.Button(self.scrollable_frame, text="Update effect_size_method", command=update_effect_size_method)
                    self.update_effect_size_method_button.pack()
                        # break
                else:
                        # break
                    self.effect_size_method_label.pack()
                    self.effect_size_method_combobox.pack()
                    self.update_effect_size_method_button.pack()
                        # break
                    self.traits_num_label.pack()
                    self.traits_num_entry.pack()
                    self.update_traits_num_button.pack()
            elif new_use_network_model == "No":
                self.hide_elements_update_methods()
                if hasattr(self, 'method_label'): 
                    self.method_label.pack_forget()
                    self.method_combobox.pack_forget()
                    self.update_method_button.pack_forget()

            # break
            messagebox.showinfo("Update Successful", "use_network_model changed.")
        else:
            messagebox.showerror("Update Error", "Please enter 'Yes' or 'No' for use_network_model.")

# 
    def hide_elements_update_methods(self):
        return
    def update_method(self):
        return
    
    def render_path_eff_size_table(self):
        def choose_and_update_path():
            chosen_file = filedialog.askopenfilename(title="Select a path_effsize_table")
            if chosen_file:  
                # self.path_effsize_table = self.load_config_as_dict()['GenomeElement']['effect_size']['user_input']["path_effsize_table"]
                self.path_effsize_table = chosen_file
                self.chosen_path_network_label.config(text=f"path_effsize_table: {self.path_effsize_table}") 
                config = self.load_config_as_dict()
                config['GenomeElement']['effect_size']['user_input']["path_effsize_table"] = self.path_effsize_table
                self.save_config(config)


        self.path_network_label = ttk.Label(self.scrollable_frame, text="Choose path_effsize_table")
        self.path_network_label.pack()
        self.choose_path_network_button = tk.Button(self.scrollable_frame, text="path_effsize_table:", command = choose_and_update_path)
        self.choose_path_network_button.pack()
        self.chosen_path_network_label = ttk.Label(self.scrollable_frame, text="Current path_effsize_table: " + self.path_effsize_table)
        self.chosen_path_network_label.pack()

        self.render_run_button()


    def render_rg_options(self):
        if not hasattr(self, "gff_label"): 
            def clean_list_input(stripped_list_input, unstripped_list_input):
                if stripped_list_input == "":
                    parsed_new_seeded_host_id = []
                elif stripped_list_input.isdigit():
                    parsed_new_seeded_host_id = [int(stripped_list_input)]
                elif "," in unstripped_list_input:
                    parsed_new_seeded_host_id = [int(item.strip()) for item in stripped_list_input.split(',')]
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
                    gff_value = str(self.gff_entry.get())
                    unstripped_list_genes_num_value = self.genes_num_entry.get().strip()
                    stripped_list_genes_num_value = unstripped_list_genes_num_value.strip("[]").strip()
                    unstripped_list_effsize_min_value = self.effsize_min_entry.get().strip()
                    stripped_list_effsize_min_value = unstripped_list_effsize_min_value.strip("[]").strip()
                    unstripped_list_effsize_max_value = self.effsize_max_entry.get().strip()
                    stripped_list_effsize_max_value = unstripped_list_effsize_max_value.strip("[]").strip()


                    genes_num_value = clean_list_input(stripped_list_genes_num_value, unstripped_list_genes_num_value)
                    effsize_min_value = clean_list_input(stripped_list_effsize_min_value, unstripped_list_effsize_min_value)
                    effsize_max_value = clean_list_input(stripped_list_effsize_max_value, unstripped_list_effsize_max_value)

                    config = self.load_config_as_dict()
                    config['GenomeElement']['effect_size']['randomly_generate']["gff"] = gff_value
                    config['GenomeElement']['effect_size']['randomly_generate']['genes_num'] = genes_num_value
                    config['GenomeElement']['effect_size']['randomly_generate']['effsize_min'] = effsize_min_value
                    config['GenomeElement']['effect_size']['randomly_generate']['effsize_max'] = effsize_max_value
                    config['GenomeElement']['effect_size']['randomly_generate']['normalize'] = self.string_to_bool_mapping[new_normalize]
                    self.save_config(config)   
                    messagebox.showinfo("Update Successful")
                except ValueError:
                    messagebox.showerror("Update Error", "Invalid Input.") 
                
            
            self.gff_label = ttk.Label(self.scrollable_frame, text="gff:")
            self.gff_label.pack()
            self.gff_entry = ttk.Entry(self.scrollable_frame, foreground="black")
            self.gff_entry.insert(0, self.gff)  
            self.gff_entry.pack()

            self.genes_num_label = ttk.Label(self.scrollable_frame, text="genes_num:")
            self.genes_num_label.pack()
            self.genes_num_entry = ttk.Entry(self.scrollable_frame, foreground="black")
            self.genes_num_entry.insert(0, str(self.genes_num))  
            self.genes_num_entry.pack()

            self.effsize_min_label = ttk.Label(self.scrollable_frame, text="effsize_min:")
            self.effsize_min_label.pack()
            self.effsize_min_entry = ttk.Entry(self.scrollable_frame, foreground="black")
            self.effsize_min_entry.insert(0, str(self.effsize_min))  
            self.effsize_min_entry.pack()

            self.effsize_max_label = ttk.Label(self.scrollable_frame, text="effsize_max:")
            self.effsize_max_label.pack()
            self.effsize_max_entry = ttk.Entry(self.scrollable_frame, foreground="black")
            self.effsize_max_entry.insert(0, str(self.effsize_max))  
            self.effsize_max_entry.pack()

            self.normalize_label = ttk.Label(self.scrollable_frame, text="normalize:")
            self.normalize_label.pack()
            self.normalize_var = tk.StringVar(value=self.bool_to_string_mapping[self.normalize])
            self.normalize_combobox = ttk.Combobox(self.scrollable_frame, textvariable=self.normalize_var, values=["Yes", "No"], state="readonly")
            self.normalize_combobox.pack() 

            # self.update_ER_button = tk.Button(self.scrollable_frame, text="Update rp_size", command=self.update_ER)
            self.update_all_rg_values_button = tk.Button(self.scrollable_frame, text="Update All Parameters", command=update_all_rg_values)
            self.update_all_rg_values_button.pack()

            self.render_run_button()
        else:
            self.gff_label.pack()
            self.gff_entry.pack()
            self.genes_num_label.pack()
            self.genes_num_entry.pack()
            self.effsize_min_label.pack()
            self.effsize_min_entry.pack()
            self.effsize_max_label.pack()
            self.effsize_max_entry.pack()
            self.normalize_label.pack()
            self.normalize_combobox.pack() 
            self.update_all_rg_values_button.pack()

    def render_run_button(self):
        def effect_size_generation():
            return
        self.run_effect_size_generation_button = tk.Button(self.scrollable_frame, text="run_effect_size_generation_button", command=effect_size_generation)
        self.run_effect_size_generation_button.pack()
