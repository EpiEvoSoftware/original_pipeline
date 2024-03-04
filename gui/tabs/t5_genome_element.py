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
        self.path_effsize_table = self.load_config_as_dict()['GenomeElement']['user_input']["path_effsize_table"]

        # str
        self.gff = self.load_config_as_dict()['GenomeElement']['randomly_generate']["gff"]
        # list
        self.genes_num = self.load_config_as_dict()['GenomeElement']['randomly_generate']['ER']['genes_num']
        # list
        self.effsize_min = self.load_config_as_dict()['GenomeElement']['randomly_generate']['RP']['effsize_min']
        # list
        self.effsize_max = self.load_config_as_dict()['GenomeElement']['randomly_generate']['RP']['effsize_max']
        # bool
        self.normalize = self.load_config_as_dict()['GenomeElement']['randomly_generate']['RP']['normalize']
    # 

    # User Configurations for network model
        self.use_genetic_model = self.load_config_as_dict()['NetworkModelParameters']['use_genetic_model']
        self.host_size = self.load_config_as_dict()['NetworkModelParameters']['host_size']

        self.path_network = self.load_config_as_dict()['NetworkModelParameters']['user_input']["path_network"]

        self.network_model = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']["network_model"]

        self.p_ER = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['ER']['p_ER']

        self.genes_num = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['RP']['genes_num']
        self.p_within = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['RP']['p_within']
        self.p_between = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['RP']['p_between']

        self.ba_m = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['BA']['ba_m']
    # 

        self.parent = parent
        self.tab_parent = tab_parent
        self.dynamic_widgets = []

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 


        # Modified part for scrolling
            # Testings
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


        # host_size_label = self.load_config_as_dict()['NetworkModelParameters']['host_size']
        self.host_size_label = ttk.Label(self.scrollable_frame, text="host_size:")
        self.host_size_label.pack()
        self.host_size_entry = ttk.Entry(self.scrollable_frame, foreground="black")
        self.host_size_entry.insert(0, self.host_size)  
        self.host_size_entry.pack()
        update_host_size_button = tk.Button(self.scrollable_frame, text="Update host_size", command=self.update_host_size)
        update_host_size_button.pack()
        # 

    
        # self.use_genetic_model = self.load_config_as_dict()['NetworkModelParameters']['use_genetic_model']
        self.use_genetic_model_label = ttk.Label(self.scrollable_frame, text="use_genetic_model:")
        self.use_genetic_model_label.pack()
        self.use_genetic_model_var = tk.StringVar(value=self.bool_to_string_mapping[self.use_genetic_model])
        self.use_genetic_model_combobox = ttk.Combobox(self.scrollable_frame, textvariable=self.use_genetic_model_var, values=["Yes", "No"], state="readonly")
        self.use_genetic_model_combobox.pack()
        self.update_use_genetic_model_button = tk.Button(self.scrollable_frame, text="Update use_genetic_model", command=self.update_use_genetic_model)
        self.update_use_genetic_model_button.pack()

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

    def update_host_size(self):
        try:
            new_host_size = int(self.host_size_entry.get())  
            config = self.load_config_as_dict() 
            config['NetworkModelParameters']['host_size'] = new_host_size 
            self.save_config(config)  
            messagebox.showinfo("Update Successful", "host_size changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for host_size.") 

    def update_mut_rate(self):
        try:
            new_mut_rate = int(self.mut_rate_entry.get())  
            config = self.load_config_as_dict() 
            config['EvolutionModel']['mut_rate'] = new_mut_rate 
            self.save_config(config)  
            messagebox.showinfo("Update Successful", "mut_rate changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for mut_rate.") 

    def update_cap_withinhost(self):
        try:
            new_cap_withinhost = int(self.cap_withinhost_entry.get())  
            config = self.load_config_as_dict() 
            config['EvolutionModel']['cap_withinhost'] = new_cap_withinhost 
            self.save_config(config)  
            messagebox.showinfo("Update Successful", "cap_withinhost changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for cap_withinhost.") 

    def update_within_host_reproduction_rate(self):
        try:
            new_within_host_reproduction_rate = int(self.within_host_reproduction_rate_entry.get())  
            config = self.load_config_as_dict() 
            config['EvolutionModel']['within_host_reproduction_rate'] = new_within_host_reproduction_rate 
            self.save_config(config)  
            messagebox.showinfo("Update Successful", "within_host_reproduction_rate changed.")  
        except ValueError:
            messagebox.showerror("Update Error", "Please enter a valid integer for within_host_reproduction_rate.") 

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

    def choose_network_path(self):  
        chosen_path = filedialog.askdirectory(title="Select a Directory")
        if chosen_path:  
            self.network_path = chosen_path
            self.network_path_label = ttk.Label(self.scrollable_frame, text="Current Network Path: " + self.network_path)
            self.network_path_label.pack()
            self.network_path_label.config(text=f"Path Network: {self.network_path}") 
            config = self.load_config_as_dict()
            config['NetworkModelParameters']['user_input']["path_network"] = self.network_path
            self.save_config(config)

    def update_use_genetic_model(self):
        self.hide_elements_update_methods()
        new_use_genetic_model = self.use_genetic_model_var.get()
        if new_use_genetic_model in ["Yes", "No"]: 
            config = self.load_config_as_dict()
            config['NetworkModelParameters']['use_genetic_model'] = self.string_to_bool_mapping[new_use_genetic_model]
            self.save_config(config)

            # break
            if new_use_genetic_model == "Yes":
                if not hasattr(self, 'method_label'):  # create the label if it doesn't exist
                    # break
                    self.method_label = ttk.Label(self.scrollable_frame, text="method:")
                    self.method_label.pack()
                    self.method_var = tk.StringVar()
                    self.method_combobox = ttk.Combobox(self.scrollable_frame, textvariable=self.method_var, values=["user_input", "randomly generate"], state="readonly")
                    self.method_combobox.pack()
                    self.update_method_button = tk.Button(self.scrollable_frame, text="Update method", command=self.update_method)
                    self.update_method_button.pack()
                    # break
                else:
                    # break, show the label if it was previously created
                    self.method_label.pack()
                    self.method_combobox.pack()
                    self.update_method_button.pack()
                    # break
            elif new_use_genetic_model == "No":
                self.hide_elements_update_methods()
                if hasattr(self, 'method_label'): 
                    self.method_label.pack_forget()
                    self.method_combobox.pack_forget()
                    self.update_method_button.pack_forget()

            # break
            messagebox.showinfo("Update Successful", "use_genetic_model changed.")
        else:
            messagebox.showerror("Update Error", "Please enter 'Yes' or 'No' for use_genetic_model.")


    def update_method(self):
        new_method = self.method_var.get().strip().lower()  # Normalize input
        if new_method in ["user_input", "randomly generate"]: #TODO: change to dropdown
            messagebox.showinfo("Update Successful", "method changed to " + new_method)
            # add conditional logic for path network and network_model
            if new_method == "user_input":
                self.hide_elements_update_methods()
                if not hasattr(self, 'path_network_label'):  
                    # create the label if it doesn't exist
                    self.path_network_label = ttk.Label(self.scrollable_frame, text="Choose path_network")
                    self.path_network_label.pack()
                    self.choose_path_network_button = tk.Button(self.scrollable_frame, text="path_network:", command=self.choose_network_path)
                    self.choose_path_network_button.pack()
                    self.chosen_path_network_label = ttk.Label(self.scrollable_frame, text="Current path_network: " + self.path_network)
                    self.chosen_path_network_label.pack()

                else:
                    # break, show the label if it was previously created
                    self.path_network_label.pack()
                    self.choose_path_network_button.pack()
                    self.chosen_path_network_label.pack()

            elif new_method == "randomly generate":
                self.hide_elements_update_methods()
                
                if not hasattr(self, 'network_model_label'): 
                # self.network_model = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']["network_model"]
                    self.network_model_label = ttk.Label(self.scrollable_frame, text="network_model:")
                    self.network_model_label.pack()
                    self.network_model_var = tk.StringVar(value = self.string_to_network_mode[self.network_model])
                    self.network_model_combobox = ttk.Combobox(
                        self.scrollable_frame,
                        textvariable=self.network_model_var,
                        values=self.graph_values,
                        state="readonly"
                    )
                    self.network_model_combobox.pack()
                    self.update_method_button = tk.Button(self.scrollable_frame, text="Update network_model", command=self.update_network_model)
                    self.update_method_button.pack()
                else:
                    self.network_model_label.pack()
                    self.network_model_combobox.pack()
                    self.update_method_button.pack()

        else:
            messagebox.showerror("Update Error", "Please enter 'user_input' or 'randomly generate' for method.")

    def update_network_model(self):
        # self.network_model = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']["network_model"]
        new_network_model_unconverted = self.network_model_var.get()
        new_network_model = self.network_model_to_string[self.network_model_var.get()]
        if new_network_model in ["ER", "RP", "BA"]: 
            config = self.load_config_as_dict()
            config['NetworkModelParameters']['randomly_generate']["network_model"] = new_network_model
            self.save_config(config)

            self.hide_elements_network_values()
            if new_network_model == "ER":
                # self.p_ER = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['ER']['p_ER']
                if not hasattr(self, 'p_ER_label'):     
                    def update_ER():
                        """
                        Updates the self.p_ER value in the params file
                        """
                        try:
                            p_ER_value = float(self.p_ER_entry.get())
                            config = self.load_config_as_dict()
                            config['NetworkModelParameters']['randomly_generate']['ER']['p_ER'] = p_ER_value
                            self.save_config(config)   
                            messagebox.showinfo("Update Successful", "p_ER changed")
                        except ValueError:
                            messagebox.showerror("Update Error", "Please enter a valid float for host_size.") 
                    self.p_ER_label = ttk.Label(self.scrollable_frame, text="p_ER:")
                    self.p_ER_label.pack()
                    self.p_ER_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.p_ER_entry.insert(0, self.p_ER)  
                    self.p_ER_entry.pack()
                    # self.update_ER_button = tk.Button(self.scrollable_frame, text="Update p_ER", command=self.update_ER)
                    self.update_ER_button = tk.Button(self.scrollable_frame, text="Update p_ER", command=update_ER)
                    self.update_ER_button.pack()
                else:
                    self.p_ER_label.pack()
                    self.p_ER_entry.pack()
                    self.update_ER_button.pack()

            elif new_network_model == "RP":
                # self.genes_num = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['RP']['genes_num']
                    # int int
                # self.p_within = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['RP']['p_within']
                    # float float
                # self.p_between = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['RP']['p_between']
                    # int
                
                if not hasattr(self, "RP"):
                    def update_all_RP():
                        """
                        Updates the self.genes_num value in the params file
                        """
                        try:
                            genes_num_value = int(self.genes_num_entry.get())
                            genes_num_value_2 = int(self.genes_num_entry_2.get())
                            p_within_value = int(self.p_within_entry.get())
                            p_within_value_2 = int(self.p_within_entry_2.get())
                            p_between_value = int(self.p_between_entry.get())

                            config = self.load_config_as_dict()
                            config['NetworkModelParameters']['randomly_generate']['RP']['genes_num'] = [genes_num_value, genes_num_value_2]
                            config['NetworkModelParameters']['randomly_generate']['RP']['p_within'] = [p_within_value, p_within_value_2]
                            config['NetworkModelParameters']['randomly_generate']['RP']['p_between'] = p_between_value
                            self.save_config(config)   
                            message = "RP Parameters changed.\n\n" + "genes_num: " + str([genes_num_value, genes_num_value_2]) + "\n"
                            message2 = "p_within: " + str([p_within_value, p_within_value_2]) + "\n"
                            message3 = "p_between_value: " + str(p_between_value)
                            messagebox.showinfo("Update Successful", message + message2 + message3)
                        except ValueError:
                            messagebox.showerror("Update Error", "Invalid Input.") 
                      
                    
                    self.genes_num_label = ttk.Label(self.scrollable_frame, text="genes_num:")
                    self.genes_num_label.pack()
                    self.genes_num_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.genes_num_entry.insert(0, self.genes_num[0])  
                    self.genes_num_entry_2 = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.genes_num_entry_2.insert(0, self.genes_num[1])
                    self.genes_num_entry.pack()
                    self.genes_num_entry_2.pack()

                    self.p_within_label = ttk.Label(self.scrollable_frame, text="p_within:")
                    self.p_within_label.pack()
                    self.p_within_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.p_within_entry.insert(0, self.p_within[0])
                    self.p_within_entry_2 = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.p_within_entry_2.insert(0, self.p_within[1])
                    self.p_within_entry.pack()
                    self.p_within_entry_2.pack()

                    self.p_between_label = ttk.Label(self.scrollable_frame, text="p_between:")
                    self.p_between_label.pack()
                    self.p_between_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.p_between_entry.insert(0, self.p_between)  
                    self.p_between_entry.pack()

                    # self.update_ER_button = tk.Button(self.scrollable_frame, text="Update genes_num", command=self.update_ER)
                    self.update_ER_button = tk.Button(self.scrollable_frame, text="Update All RP parameters", command=update_all_RP)
                    self.update_ER_button.pack()

                else:
                    self.genes_num_label.pack()
                    self.genes_num_entry.pack()
                    self.p_within_label
                    self.p_within_entry.pack()
                    self.p_within_entry_2.pack()
                    self.p_between_label
                    self.p_between_entry.pack()
                    self.update_ER_button.pack()

            elif new_network_model == "BA":
                if not hasattr(self, "ba_m_label"):
                    # self.ba_m = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['BA']['ba_m']
                    def update_ba_m():
                        """
                        Updates the self.ba_m value in the params file
                        """
                        try:
                            ba_m_value = int(self.ba_m_entry.get())
                            config = self.load_config_as_dict()
                            config['NetworkModelParameters']['randomly_generate']['BA']['ba_m'] = ba_m_value
                            self.save_config(config)   
                            messagebox.showinfo("Update Successful", "ba_m changed")
                        except ValueError:
                            messagebox.showerror("Update Error", "Please enter a valid int for host_size.") 
                    self.ba_m_label = ttk.Label(self.scrollable_frame, text="ba_m:")
                    self.ba_m_label.pack()
                    self.ba_m_entry = ttk.Entry(self.scrollable_frame, foreground="black")
                    self.ba_m_entry.insert(0, self.ba_m)  
                    self.ba_m_entry.pack()
                    # self.update_ER_button = tk.Button(self.scrollable_frame, text="Update ba_m", command=self.update_ER)
                    self.update_ER_button = tk.Button(self.scrollable_frame, text="Update ba_m", command=update_ba_m)
                    self.update_ER_button.pack()
                else:
                    self.ba_m_label.pack()
                    self.ba_m_entry.pack()
                    self.update_ER_button.pack()

            # else:
            #     self.hide_elements_network_values()

            self.render_run_eff_size_generation()
            messagebox.showinfo("Update Successful", "network_model changed to " + new_network_model_unconverted + ".")

        else:
            messagebox.showerror("Update Error", "Invalid Entry for network_model.")

    
    def render_run_eff_size_generation(self):
        def run_eff_size_generate():
            messagebox.showerror("Update Error", "helloo world")
        if not hasattr(self, 'run_eff_size_generate_button'):
            self.run_eff_size_generate_button = tk.Button(self.scrollable_frame, text="run_eff_size_generation", command=run_eff_size_generate)
            self.run_eff_size_generate_button.pack()
        else:
            self.run_eff_size_generate_button.pack()

    def hide_elements_update_methods(self):
        self.hide_elements_network_values()
        if hasattr(self, 'run_eff_size_generate_button'):
            self.run_eff_size_generate_button.pack_forget()
        if hasattr(self, 'path_network_label'):
        # if new_method == "user_input":
            self.path_network_label.pack_forget()
            self.choose_path_network_button.pack_forget()
            self.path_network_label.pack_forget()
            self.chosen_path_network_label.pack_forget()
        if hasattr(self, 'network_model_combobox'):
        # if new_method == "randomly generate":
            self.network_model_combobox.pack_forget()
            self.update_method_button.pack_forget()
            self.network_model_label.pack_forget()

    def hide_elements_network_values(self):
        if hasattr(self, 'run_eff_size_generate_button'):
            self.run_eff_size_generate_button.pack_forget()
        if hasattr(self, 'p_ER_label'):
        # if new_network_model == "ER":
            self.p_ER_label.pack_forget()
            self.p_ER_entry.pack_forget()
            self.update_ER_button.pack_forget()
        if hasattr(self, 'genes_num_label'):
        # if new_network_model == "RP":
            self.genes_num_label.pack_forget()
            self.genes_num_entry.pack_forget()
            self.genes_num_entry_2.pack_forget()
            self.p_within_label.pack_forget()
            self.p_within_entry.pack_forget()
            self.p_within_entry_2.pack_forget()
            self.p_between_label.pack_forget()
            self.p_between_entry.pack_forget()
            self.update_ER_button.pack_forget()
        if hasattr(self, 'ba_m_label'):
        # if new_network_model == "BA":
            self.ba_m_label.pack_forget()
            self.ba_m_entry.pack_forget()
            self.update_ER_button.pack_forget()