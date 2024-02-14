import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class GenomeEffSize:
    def __init__(self, parent, tab_parent, config_path):
        self.config_path = config_path

        self.host_size = self.load_config_as_dict()['NetworkModelParameters']['host_size']
        self.mut_rate = self.load_config_as_dict()['EvolutionModel']['mut_rate']
        self.trans_type = self.load_config_as_dict()['EvolutionModel']['trans_type']
        self.dr_type = self.load_config_as_dict()['EvolutionModel']['dr_type']
        self.within_host_reproduction = self.load_config_as_dict()['EvolutionModel']['within_host_reproduction']
        self.within_host_reproduction_rate = self.load_config_as_dict()['EvolutionModel']['within_host_reproduction_rate']
        self.cap_withinhost = self.load_config_as_dict()['EvolutionModel']['cap_withinhost']

        self.parent = parent
        self.tab_parent = tab_parent
        self.dynamic_widgets = []

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 

        self.host_size_label = ttk.Label(self.control_frame, text="host_size:")
        self.host_size_label.pack()
        self.host_size_entry = ttk.Entry(self.control_frame, foreground="black")
        self.host_size_entry.insert(0, self.host_size)  
        self.host_size_entry.pack()
        update_host_size_button = tk.Button(self.control_frame, text="Update host_size", command=self.update_host_size)
        update_host_size_button.pack()

        self.mut_rate_label = ttk.Label(self.control_frame, text="mut_rate:")
        self.mut_rate_label.pack()
        self.mut_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.mut_rate_entry.insert(0, self.mut_rate)  
        self.mut_rate_entry.pack()
        update_mut_rate_button = tk.Button(self.control_frame, text="Update mut_rate", command=self.update_mut_rate)
        update_mut_rate_button.pack()

        self.trans_type_label = ttk.Label(self.control_frame, text="trans_type:")
        self.trans_type_label.pack()
        self.trans_type_entry = ttk.Entry(self.control_frame, foreground="black")
        self.trans_type_entry.insert(0, self.trans_type)  
        self.trans_type_entry.pack()
        update_trans_type_button = tk.Button(self.control_frame, text="Update trans_type", command=self.update_trans_type)
        update_trans_type_button.pack()

        self.dr_type_label = ttk.Label(self.control_frame, text="dr_type:")
        self.dr_type_label.pack()
        self.dr_type_entry = ttk.Entry(self.control_frame, foreground="black")
        self.dr_type_entry.insert(0, self.dr_type)  
        self.dr_type_entry.pack()
        update_dr_type_button = tk.Button(self.control_frame, text="Update dr_type", command=self.update_dr_type)
        update_dr_type_button.pack()

        self.within_host_reproduction_var = tk.StringVar(value=str(self.within_host_reproduction))  #
        self.within_host_reproduction_label = ttk.Label(self.control_frame, text="within_host_reproduction:")
        self.within_host_reproduction_label.pack()
        self.within_host_reproduction_entry = ttk.Entry(self.control_frame, textvariable=self.within_host_reproduction_var, foreground="black")
        self.within_host_reproduction_entry.pack()
        update_within_host_reproduction_button = tk.Button(self.control_frame, text="Update within_host_reproduction", command=self.update_within_host_reproduction)
        update_within_host_reproduction_button.pack()
        
        self.within_host_reproduction_rate_label = ttk.Label(self.control_frame, text="within_host_reproduction_rate:")
        self.within_host_reproduction_rate_entry = ttk.Entry(self.control_frame, foreground="black")
        self.within_host_reproduction_rate_entry.insert(0, self.within_host_reproduction_rate) 
        self.update_within_host_reproduction_rate_button = tk.Button(self.control_frame, text="Update within_host_reproduction_rate", command=self.update_within_host_reproduction_rate)
        
        if self.within_host_reproduction == True:
            self.within_host_reproduction_rate_label.pack()
            self.within_host_reproduction_rate_entry.pack()
            self.update_within_host_reproduction_rate_button.pack()

        self.cap_withinhost_label = ttk.Label(self.control_frame, text="cap_withinhost:")
        self.cap_withinhost_label.pack()
        self.cap_withinhost_entry = ttk.Entry(self.control_frame, foreground="black")
        self.cap_withinhost_entry.insert(0, self.cap_withinhost)  
        self.cap_withinhost_entry.pack()
        update_cap_withinhost_button = tk.Button(self.control_frame, text="Update cap_withinhost", command=self.update_cap_withinhost)
        update_cap_withinhost_button.pack()

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

    def update_trans_type(self):
        new_trans_type = self.trans_type_entry.get().strip().lower()  # Normalize input
        if new_trans_type in ["additive", "bi-allele"]:
            config = self.load_config_as_dict()
            config['EvolutionModel']['trans_type'] = new_trans_type
            self.save_config(config)
            messagebox.showinfo("Update Successful", "trans_type changed.")
        else:
            messagebox.showerror("Update Error", "Please enter 'additive' or 'bi-allele' for trans_type.")

    def update_dr_type(self):
        new_dr_type = self.dr_type_entry.get().strip().lower()  
        if new_dr_type in ["additive", "bi-allele"]:
            config = self.load_config_as_dict()
            config['EvolutionModel']['dr_type'] = new_dr_type
            self.save_config(config)
            messagebox.showinfo("Update Successful", "dr_type changed.")
        else:
            messagebox.showerror("Update Error", "Please enter 'additive' or 'bi-allele' for dr_type.")

    def update_within_host_reproduction(self):
        input_value = self.within_host_reproduction_entry.get().strip().lower()  
        print(input_value)
        if input_value in ["true", "false"]:
            new_within_host_reproduction = input_value == "true" 
            if new_within_host_reproduction == True:
                self.within_host_reproduction_rate_label.pack()
                self.within_host_reproduction_rate_entry.pack()
                self.update_within_host_reproduction_rate_button.pack()
            else:
                self.within_host_reproduction_rate_label.pack_forget()
                self.within_host_reproduction_rate_entry.pack_forget()
                self.update_within_host_reproduction_rate_button.pack_forget()
            config = self.load_config_as_dict()
            config['EvolutionModel']['within_host_reproduction'] = new_within_host_reproduction
            self.save_config(config)
            messagebox.showinfo("Update Successful", "within_host_reproduction changed.")
        else:
            messagebox.showerror("Update Error", "Please enter 'true' or 'false' for within_host_reproduction.")


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

