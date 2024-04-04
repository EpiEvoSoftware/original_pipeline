import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox
import json
from tools import *
class EvolutionaryModel:
    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):
        self.config_path = config_path

        self.n_generation = load_config_as_dict(self.config_path)['EvolutionModel']['n_generation']
        self.mut_rate = load_config_as_dict(self.config_path)['EvolutionModel']['mut_rate']
        self.trans_type = load_config_as_dict(self.config_path)['EvolutionModel']['trans_type']
        self.dr_type = load_config_as_dict(self.config_path)['EvolutionModel']['dr_type']
        self.within_host_reproduction = load_config_as_dict(self.config_path)['EvolutionModel']['within_host_reproduction']
        self.within_host_reproduction_rate = load_config_as_dict(self.config_path)['EvolutionModel']['within_host_reproduction_rate']
        self.cap_withinhost = load_config_as_dict(self.config_path)['EvolutionModel']['cap_withinhost']

        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_index = tab_index
        self.tab_parent.add(parent, text=tab_title)
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(padx=10, pady=10) 
        self.render_n_generations()

        

        self.render_mut_rate()
        
        self.render_trans_type() 
        self.render_dr_type() 

        self.render_within_host_reproduction()        
        self.render_within_host_reproduction_rate()
       
        self.render_cap_withinhost() 
        render_next_button(self.tab_index, self.tab_parent, self.parent, self.update)

    def update(self):
        error_messages = []
        self.update_n_generation(error_messages)
        self.update_cap_withinhost(error_messages)
        self.update_dr_type(error_messages)
        self.update_mut_rate(error_messages)
        self.update_trans_type(error_messages)
        self.update_within_host_reproduction_rate(error_messages)
        self.update_within_host_reproduction(error_messages)
        if len(error_messages) == 0:
            messagebox.showinfo("Update Successful", "Parameters Updated.")
            return 0
        else:
            error_message_str = "\n\n".join(error_messages)
            messagebox.showerror("Update Error", error_message_str) 
            return 1
    
    # def render_t2_title(self):
    #     self.t2_title = ttk.Label(self.control_frame, text="Simulation Settings", style="Title.TLabel", width = 100)
    #     self.t2_title.grid(row=0, column=0, columnspan = 2, pady=5, sticky='e')

    def render_n_generations(self):
        self.padx_width = 10
        self.n_generation_label = ttk.Label(self.control_frame, text="Number of Generations (Integer)", style="Bold.TLabel", width = minwidth//2)
        self.n_generation_label.grid(row = 1, column = 0, sticky = 'w', pady = 5, padx = self.padx_width)
        self.n_generation_entry = ttk.Entry(self.control_frame, foreground="black")
        self.n_generation_entry.insert(0, self.n_generation)  
        self.n_generation_entry.grid(row = 2, column = 0, sticky = 'w', pady = 2, padx = self.padx_width)

    def render_mut_rate(self):
        self.mut_rate_label = ttk.Label(self.control_frame, text="Mutation Rate Per Site Per Generation (Numerical)", width = minwidth//2, style = "Bold.TLabel")
        self.mut_rate_label.grid(row = 1, column = 1, sticky = 'w', pady = 5)
        self.mut_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.mut_rate_entry.insert(0, self.mut_rate)

        self.mut_rate_entry.grid(row = 2, column = 1, sticky = 'w', pady = 5, padx=0)
        update_mut_rate_button = tk.Button(self.control_frame, text="Update mut_rate", command=self.update_mut_rate)
    def render_trans_type(self):
        self.trans_type_label = ttk.Label(self.control_frame, text="Transmissibility Trait Type", style = "Bold.TLabel")
        self.trans_type_label.grid(row = 3, column = 0, columnspan = 2, sticky = 'w', pady = 5, padx=10)
        
        self.trans_type_var = tk.StringVar(value=self.trans_type)
        self.trans_type_combobox = ttk.Combobox(self.control_frame, textvariable=self.trans_type_var, values=["Bi-Allelic", "Additive"], state="readonly")
        self.trans_type_combobox.grid(row = 4, column = 0, columnspan = 2, sticky = 'w', pady = 5, padx=10)
    def render_dr_type(self):
        def update(event):
            value = self.dr_type_combobox.get()
        self.dr_type_label = ttk.Label(self.control_frame, text="Drug-Resistance Trait Type", style = "Bold.TLabel")
        self.dr_type_label.grid(row = 5, column = 0, columnspan = 2, sticky = 'w', pady = 5, padx=10)
        self.dr_type_var = tk.StringVar(value=self.dr_type)
        self.dr_type_combobox = ttk.Combobox(self.control_frame, textvariable=self.dr_type_var, values=["Bi-Allelic", "Additive"], state="readonly")
        self.dr_type_combobox.grid(row = 6, column = 0, columnspan = 2, sticky = 'w', pady = 5, padx=10)
        self.dr_type_combobox.bind("<<ComboboxSelected>>", update)        

    def render_within_host_reproduction(self):
        def update():
            value = self.dr_type_combobox.get()

        self.within_host_reproduction_var = tk.BooleanVar(value=self.within_host_reproduction)  #
        self.within_host_reproduction_label = ttk.Label(self.control_frame, text="Within-host Reproduction", style = "Bold.TLabel")
        self.within_host_reproduction_label.grid(row = 7, column = 0, sticky = 'w', pady = 5, padx=10)

        self.rb_true = ttk.Radiobutton(self.control_frame, text="Yes", variable=self.within_host_reproduction_var, value=True, command = update)
        self.rb_true.grid(row = 8, column = 0, sticky = 'w', pady = 5, padx=10)

        self.rb_false = ttk.Radiobutton(self.control_frame, text="No", variable=self.within_host_reproduction_var, value=False, command = update)
        self.rb_false.grid(row = 9, column = 0, sticky = 'w', pady = 5, padx=10)

    def render_within_host_reproduction_rate(self):
        self.render_within_host_reproduction_rate_title = "Within-host Reproduction Rate Per Generation (Numerical)"
        self.within_host_reproduction_rate_label = ttk.Label(self.control_frame, text=self.render_within_host_reproduction_rate_title, style = "Bold.TLabel")
        self.within_host_reproduction_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.within_host_reproduction_rate_entry.insert(0, self.within_host_reproduction_rate) 
        
        self.within_host_reproduction_rate_label.grid(row = 7, column = 1, sticky = 'w', pady = 5, padx=0)
        self.within_host_reproduction_rate_entry.grid(row = 8, column = 1, sticky = 'w', pady = 5, padx=0)
 
    def render_cap_withinhost(self):
        self.cap_withinhost_label = ttk.Label(self.control_frame, text="Maximum Number of Pathogens within Host (Integer)", style = "Bold.TLabel")
        self.cap_withinhost_label.grid(row = 10, column = 0, sticky = 'w', pady = 5, padx = self.padx_width)
        self.cap_withinhost_entry = ttk.Entry(self.control_frame, foreground="black")
        self.cap_withinhost_entry.insert(0, self.cap_withinhost)  
        self.cap_withinhost_entry.grid(row = 11, column = 0, sticky = 'w', pady = 5, padx = self.padx_width)

    def update_n_generation(self, error_messages):
        try:
            new_n_generation = int(float(self.n_generation_entry.get()))  
            config = load_config_as_dict(self.config_path) 
            config['EvolutionModel']['n_generation'] = new_n_generation 
            save_config(self.config_path, config)  
        except ValueError:
            error_messages.append("Please enter a valid integer for n_generation.")

    def update_mut_rate(self, error_messages):
        try:
            new_mut_rate = int(float(self.mut_rate_entry.get()))  
            config = load_config_as_dict(self.config_path) 
            config['EvolutionModel']['mut_rate'] = new_mut_rate 
            save_config(self.config_path, config)  
        except ValueError:
            error_messages.append("Please enter a valid number for mut_rate.")

    def update_cap_withinhost(self, error_messages):
        try:
            new_cap_withinhost = int(float(self.cap_withinhost_entry.get()))  
            config = load_config_as_dict(self.config_path) 
            config['EvolutionModel']['cap_withinhost'] = new_cap_withinhost 
            save_config(self.config_path, config)  
        except ValueError:
            error_messages.append("Please enter a valid integer for cap_withinhost.")

    def update_within_host_reproduction_rate(self, error_messages):
        try:
            new_within_host_reproduction_rate = int(float(self.within_host_reproduction_rate_entry.get()))  
            config = load_config_as_dict(self.config_path) 
            config['EvolutionModel']['within_host_reproduction_rate'] = new_within_host_reproduction_rate 
            save_config(self.config_path, config)  
        except ValueError:
            error_messages.append("Please enter a valid number for " + self.render_within_host_reproduction_rate_title + ".")

    def update_trans_type(self, error_messages):
        new_trans_type = self.trans_type_var.get()
        if new_trans_type in ["Additive", "Bi-Allelic"]: #TODO: change to dropdown
            config = load_config_as_dict(self.config_path)
            config['EvolutionModel']['trans_type'] = new_trans_type
            save_config(self.config_path, config)
        else:
            error_messages.append("Please enter 'additive' or 'bi-allele' for trans_type.")

    def update_dr_type(self, error_messages):
        new_dr_type = self.dr_type_var.get()
        if new_dr_type in ["Additive", "Bi-Allelic"]:
            config = load_config_as_dict(self.config_path)
            config['EvolutionModel']['dr_type'] = new_dr_type
            save_config(self.config_path, config)
        else:
            error_messages.append("Please enter 'additive' or 'bi-allele' for dr_type.")

    def update_within_host_reproduction(self, error_messages):
        input_value = self.within_host_reproduction_var.get()
        config = load_config_as_dict(self.config_path)
        config['EvolutionModel']['within_host_reproduction'] = input_value
        save_config(self.config_path, config)
        # if input_value in ["true", "false"]:
        #     new_within_host_reproduction = input_value == "true" 
        #     if new_within_host_reproduction == True:
        #         self.within_host_reproduction_rate_label.grid()
        #         self.within_host_reproduction_rate_entry.grid()
        #         # self.update_within_host_reproduction_rate_button.grid()
        #     else:
        #         self.within_host_reproduction_rate_label.grid_forget()
        #         self.within_host_reproduction_rate_entry.grid_forget()
        #         # self.update_within_host_reproduction_rate_button.grid_forget()
        #     config = load_config_as_dict(self.config_path)
        #     config['EvolutionModel']['within_host_reproduction'] = new_within_host_reproduction
        #     save_config(self.config_path, config)
        # else:
        #     error_messages.append("Please enter 'true' or 'false' for within_host_reproduction.")



