import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class GenomeEffSize:
    def __init__(self, parent, tab_parent, config_path):

        self.network_dict = {
            "Erdős–Rényi": "ER",
            "Barabási-Albert": "BA",
            "Random Partition": "RP"
        }

        self.config_path = config_path

        self.path_network = self.load_config_as_dict()['NetworkModelParameters']['user_input']["path_network"]
        self.use_network_model = self.load_config_as_dict()['NetworkModelParameters']['use_network_model']
        self.host_size = self.load_config_as_dict()['NetworkModelParameters']['host_size']
        self.network_model = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']["network_model"]
        self.p_er = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['ER']['p_ER']
        self.rp_size = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['RP']['rp_size']
        self.p_within = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['RP']['p_within']
        self.p_between = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['RP']['p_between']
        self.ba_m = self.load_config_as_dict()['NetworkModelParameters']['randomly_generate']['BA']['ba_m']

        self.parent = parent
        self.tab_parent = tab_parent
        self.dynamic_widgets = []

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 

        # break
        # self.surname_label = ttk.Label(self.control_frame, text="Model")
        # self.surname_label.pack()
        # self.model_combobox = ttk.Combobox(self.control_frame, values=["Yes", "No"], foreground="White")
        # self.model_combobox.pack()

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
        

        # self.use_network_model_response = tk.StringVar(value = self.bool_to_string_mapping[self.use_network_model])
        # ttk.Label(self.control_frame, text="use_network_model",
        #           style='Large.TLabel').pack()
        # self.use_network_model_response_dropdown = ttk.Combobox(
        #     self.control_frame,
        #     textvariable=self.use_network_model_response,
        #     values=["Yes", "No"],
        #     style='Large.TButton'
        # )
        # self.use_network_model_response_dropdown.pack()
        # self.use_network_model_response_dropdown.bind(
        #     "<<ComboboxSelected>>", self.on_use_network_model_response_combobox_change)

        # self.use_network_model_response_dropdown_parameter_entries = {}
        # self.use_network_model_response_dropdown_parameter_labels = []

        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
    
        self.use_network_model_label = ttk.Label(self.control_frame, text="use_network_model:")
        self.use_network_model_label.pack()
        self.use_network_model_var = tk.StringVar(value=self.bool_to_string_mapping[self.use_network_model])
        self.use_network_model_combobox = ttk.Combobox(self.control_frame, textvariable=self.use_network_model_var, values=["Yes", "No"], state="readonly")
        self.use_network_model_combobox.pack()
        update_use_network_model_button = tk.Button(self.control_frame, text="Update use_network_model", command=self.update_use_network_model)
        update_use_network_model_button.pack()

        if self.use_network_model == True:
            self.method_label = ttk.Label(self.control_frame, text="method:")
            self.method_label.pack()
            self.method_var = tk.StringVar()
            self.method_combobox = ttk.Combobox(self.control_frame, textvariable=self.method_var, values=["randomly generate", "user_input"], state="readonly")
            self.method_combobox.pack()
            self.update_method_button = tk.Button(self.control_frame, text="Update method", command=self.update_method)
            self.update_method_button.pack()

        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak

        if self.use_network_model == "Yes":
            self.asdf = ttk.Label(self.control_frame, text="use_network_model:")


        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak
        # break v break breakvbreakbreakbreakbreak



        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

    def update_host_size(self):
        try:
            new_host_size = int(self.host_size_entry.get())  
            config = self.load_config_as_dict() 
            config['EvolutionModel']['host_size'] = new_host_size 
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




    # def update_within_host_reproduction(self):
    #     input_value = self.within_host_reproduction_entry.get().strip().lower()  
    #     print(input_value)
    #     if input_value in ["true", "false"]:
    #         new_within_host_reproduction = input_value == "true" 
    #         if new_within_host_reproduction == True:
    #             self.within_host_reproduction_rate_label.pack()
    #             self.within_host_reproduction_rate_entry.pack()
    #             self.update_within_host_reproduction_rate_button.pack()
    #         else:
    #             self.within_host_reproduction_rate_label.pack_forget()
    #             self.within_host_reproduction_rate_entry.pack_forget()
    #             self.update_within_host_reproduction_rate_button.pack_forget()
    #         config = self.load_config_as_dict()
    #         config['EvolutionModel']['within_host_reproduction'] = new_within_host_reproduction
    #         self.save_config(config)
    #         messagebox.showinfo("Update Successful", "within_host_reproduction changed.")
    #     else:
    #         messagebox.showerror("Update Error", "Please enter 'true' or 'false' for within_host_reproduction.")


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

# break

    def on_use_network_model_response_combobox_change(self, event=None):
        """
        Clear previously displayed widgets
        Check the combobox value and render appropriate UI elements
        """
        # for widget in self.dynamic_widgets:
        #     widget.destroy()
        # self.dynamic_widgets.clear()
        # self.method_combobox.pack_forget()
        # self.method_combobox_label.pack_forget()

        choice = self.use_network_model_response_dropdown.get()
        if choice == "Yes":
            self.method_string = tk.StringVar(value = "")
            self.method_combobox_label = ttk.Label(self.control_frame, text=f"method:", style='Large.TLabel').pack()
            self.method_combobox = ttk.Combobox(
                self.control_frame,
                textvariable=self.method_string,
                values=["user_input", "randomly generate"],
                style='Large.TButton'
            )
            self.method_combobox.pack()
            self.method_combobox.bind("<<ComboboxSelected>>", self.on_method_combobox_change)
        elif choice == "No":
            self.method_combobox.pack_forget() #TODO: fix nontype object has no attribute pack forget
            self.method_combobox_label.pack_forget()

    def choose_network_path(self):  
        chosen_path = filedialog.askdirectory(title="Select a Directory")
        if chosen_path:  
            self.network_path = chosen_path
            self.network_path_label = ttk.Label(self.control_frame, text="Current Network Path: " + self.network_path)
            self.network_path_label.pack()
            self.network_path_label.config(text=f"Path Network: {self.network_path}") 
            config = self.load_config_as_dict()
            config['NetworkModelParameters']['user_input']["path_network"] = self.network_path
            self.save_config(config)
    
    
    def on_method_combobox_change(self, event=None):
        for widget in self.dynamic_widgets:
            widget.destroy()
        self.dynamic_widgets.clear()

        choice = self.use_network_model_response_dropdown.get()
        if choice == "user_input":
            network_path_label = ttk.Label(self.control_frame, text="Choose Network Path")
            network_path_label.pack()
            choose_network_path_button = tk.Button(self.control_frame, text="Choose Path", command=self.choose_network_path)
            choose_network_path_button.pack()
            self.network_path_label = ttk.Label(self.control_frame, text="Current Network Path: " + self.network_path)
            self.network_path_label.pack()
            # render run network generate
            
        elif choice == "randomly generate":
            self.network_model_string = tk.StringVar()
            ttk.Label(self.control_frame, text="Select Network Model Type:", style='Large.TLabel').pack()
            network_model_combobox = ttk.Combobox(
                self.control_frame,
                textvariable=self.network_model_string,
                values=["Erdős–Rényi", "Barabási-Albert",
                        "Random Partition"],
                style='Large.TButton'
            )

            network_model_combobox.pack()
            network_model_combobox.bind("<<ComboboxSelected>>", self.update_parameters)

            self.network_model_combobox_parameter_entries = {}
            self.network_model_combobox_parameter_labels = []

            self.degree_button = ttk.Button(
            self.control_frame, text="Run Network Generation", command=self.run_network_generation, style='Large.TButton')
            self.degree_button.pack()


    def run_network_generation(self):
        return


    def update_parameters(self, event=None):
        # clear existing parameters
        for label in self.network_model_combobox_parameter_labels:
            label.destroy()
        for entry in self.network_model_combobox_parameter_entries.values():
            entry.destroy()

        self.network_model_combobox_parameter_labels.clear()
        self.network_model_combobox_parameter_entries.clear()

        network_model = self.network_model_string.get()
        selected_graph_type = self.network_dict[network_model]
        params = []

        if selected_graph_type == "ER":
            params = [("p_er", "float")]
        elif selected_graph_type == "RP":
            params = [("rp_size", "int, int"), ("p_within", "float, float"), ("p_between", "float")]
        elif selected_graph_type == "BA":
            params = [("m", "int")]
        else:
            messagebox.showwarning('Error', 'Unsupported Network Type')

        # create new parameters
        for param, dtype in params:
            label = ttk.Label(self.control_frame,
                              text=f"{param} ({dtype}):", style='Large.TLabel')
            label.pack()
            self.network_model_combobox_parameter_labels.append(label)
            entry = tk.Entry(self.control_frame)
            entry.pack()
            self.network_model_combobox_parameter_entries[param] = entry

        self.degree_button.pack_forget()
        self.degree_button.pack()


    def update_use_network_model(self):
        new_use_network_model = self.use_network_model_var.get()
        if new_use_network_model in ["Yes", "No"]: 
            config = self.load_config_as_dict()
            config['NetworkModelParameters']['use_network_model'] = self.string_to_bool_mapping[new_use_network_model]
            self.save_config(config)

            # break
            if new_use_network_model == "Yes":
                if not hasattr(self, 'method_label'):  # create the label if it doesn't exist
                    # break
                    self.method_label = ttk.Label(self.control_frame, text="method:")
                    self.method_label.pack()
                    self.method_var = tk.StringVar()
                    self.method_combobox = ttk.Combobox(self.control_frame, textvariable=self.method_var, values=["randomly generate", "user_input"], state="readonly")
                    self.method_combobox.pack()
                    self.update_method_button = tk.Button(self.control_frame, text="Update method", command=self.update_method)
                    self.update_method_button.pack()
                    # break
                else:
                    # break, show the label if it was previously created
                    self.method_label.pack()
                    self.method_combobox.pack()
                    self.update_method_button.pack()
                    # break
            else:
                if hasattr(self, 'method_label'):
                    self.method_label.pack_forget()
                    self.method_combobox.pack_forget()
                    self.update_method_button.pack_forget()
            # break
            messagebox.showinfo("Update Successful", "use_network_model changed.")
        else:
            messagebox.showerror("Update Error", "Please enter 'Yes' or 'No' for use_network_model.")


    def update_method(self):
        new_method = self.method_var.get().strip().lower()  # Normalize input
        if new_method in ["user_input", "randomly generate"]: #TODO: change to dropdown
            messagebox.showinfo("Update Successful", "method changed to " + new_method)
            # add conditional logic for path network and network_model
            if new_method == "user_input":
                if not hasattr(self, 'path_network_label'):  # create the label if it doesn't exist
                    # break
                    # self.path_network_label = ttk.Label(self.control_frame, text="path_network:")
                    # self.path_network_label.pack()
                    # self.path_network_var = tk.StringVar(value = self.path_network)
                    # self.path_network_combobox = ttk.Combobox(self.control_frame, textvariable=self.path_network_var, values=["randomly generate", "user_input"], state="readonly")
                    # self.path_network_combobox.pack()
                    # self.update_path_network_button = tk.Button(self.control_frame, text="Update path_network", command=self.update_path_network)
                    # self.update_path_network_button.pack()
                    path_network_label = ttk.Label(self.control_frame, text="Choose path_network")
                    path_network_label.pack()
                    self.choose_path_network_button = tk.Button(self.control_frame, text="path_network:", command=self.choose_network_path)
                    self.choose_path_network_button.pack()
                    self.path_network_label = ttk.Label(self.control_frame, text="Current path_network: " + self.path_network)
                    self.path_network_label.pack()
                    # break
                else:
                    # break, show the label if it was previously created
                    self.path_network_label.pack()
                    self.choose_path_network_button.pack()
                    self.path_network_label.pack()
                    # break
            elif new_method == "randomly generate":
                if hasattr(self, 'path_network_label'):
                    self.path_network_label.pack_forget()
                    self.choose_path_network_button.pack_forget()
                    self.path_network_label.pack_forget()
        else:
            messagebox.showerror("Update Error", "Please enter 'user_input' or 'randomly generate' for method.")

    
    def update_path_network(self):
        new_path_network = self.path_network_var.get().strip().lower()  # Normalize input
        if isinstance(new_path_network, str):
        # if os.path.exists(new_path_network):
            # Assuming you want to save the path as is, without converting to lowercase
            config = self.load_config_as_dict()
            config['NetworkModelParameter']['user_input']['path_network'] = new_path_network
            self.save_config(config)
            

            next_button = tk.Button(self.parent, text="Run Network Generate")
            next_button.pack()
            messagebox.showinfo("Update Successful", "path_network changed to \"" + new_path_network + "\"")
        else:
            messagebox.showerror("Update Error", "The provided path does not exist. Please enter a valid path for path_network.")