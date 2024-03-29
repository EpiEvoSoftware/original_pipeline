
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import shutil
import sys
from tools import *
current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.join(os.path.dirname(current_dir), '../codes')
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

class PostProcessing:
    def __init__(self, parent, tab_parent, config_path):

        self.config_path = config_path

        self.cwdir = load_config_as_dict(self.config_path)['BasicRunConfiguration']['cwdir']
        
# Postprocessing_options Configurations
        self.do_postprocess = load_config_as_dict(self.config_path)['Postprocessing_options']['do_postprocess']
        self.branch_color_trait = load_config_as_dict(self.config_path)['Postprocessing_options']['tree_plotting']['branch_color_trait']
        self.drug_resistance_heatmap = load_config_as_dict(self.config_path)['Postprocessing_options']['tree_plotting']['drug_resistance_heatmap']

        self.parent = parent
        self.tab_parent = tab_parent
        self.dynamic_widgets = []
        
        self.control_frame = ttk.Frame(self.parent)
        self.control_frame.pack(fill='both', expand=True)

        self.render_all()

        # generate_config_file Button
        generate_config_file_button = tk.Button(self.parent, text="generate_config_file", command=self.generate_config_file)
        generate_config_file_button.pack()

    def generate_config_file(self):
        source = 'config_templates/base_params_test.json'
        target = os.path.join(self.cwdir, 'base_params.json')
        
        try:
            shutil.copy(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        

    def render_all(self):
        self.render_do_postprocess()
        self.render_branch_color_trait()
        self.render_drug_resistance_heatmap()
    
    def render_do_postprocess(self):
        """
        self.do_postprocess = load_config_as_dict(self.config_path)['Postprocessing_options']['do_postprocess']
        """
        def update():
            prev_val = self.do_postprocess
            self.do_postprocess = string_to_bool_mapping[self.do_postprocess_var.get()]
            config = load_config_as_dict(self.config_path)
            keys_path = ['Postprocessing_options', 'do_postprocess']
            update_nested_dict(config, keys_path, self.do_postprocess)
            save_config(self.config_path, config)
            if prev_val != self.do_postprocess:
                messagebox.showinfo("Success", "Updated successfully")

        self.do_postprocess_label = ttk.Label(self.control_frame, text="do_postprocess:")
        self.do_postprocess_label.pack()
        self.do_postprocess_var = tk.StringVar(value=bool_to_string_mapping[self.do_postprocess])
        self.do_postprocess_combobox = ttk.Combobox(
            self.control_frame, textvariable=self.do_postprocess_var, 
            values=["Yes", "No"], state="readonly"
            )
        self.do_postprocess_combobox.pack()
        self.update_do_postprocess_button = tk.Button(self.control_frame, text="Update Method", command=update)
        self.update_do_postprocess_button.pack()

    def render_branch_color_trait(self):
        """
        self.branch_color_trait = load_config_as_dict(self.config_path)['Postprocessing_options']['tree_plotting']['branch_color_trait']
        """
        def update():
            try:
                prev_val = self.branch_color_trait
                self.branch_color_trait = int(float(self.branch_color_trait_entry.get()))
                config = load_config_as_dict(self.config_path)
                keys_path = ['Postprocessing_options', 'tree_plotting', 'branch_color_trait']
                update_nested_dict(config, keys_path, self.branch_color_trait)
                save_config(self.config_path, config)
                if prev_val != self.branch_color_trait:
                    messagebox.showinfo("Success", "Updated successfully")
            except ValueError:
                messagebox.showerror("Update Error", "Please enter a valid number.")
            except Exception as e:
                messagebox.showerror("Update Error", str(e))
        self.branch_color_trait_label = ttk.Label(self.control_frame, text="branch_color_trait:")
        self.branch_color_trait_label.pack()
        self.branch_color_trait_entry = ttk.Entry(self.control_frame, foreground="black")
        self.branch_color_trait_entry.insert(0, self.branch_color_trait)  
        self.branch_color_trait_entry.pack()
        update_branch_color_trait_button = tk.Button(self.control_frame, text="Update branch_color_trait", command=update)
        update_branch_color_trait_button.pack()

    def render_drug_resistance_heatmap(self):
        """
        self.drug_resistance_heatmap = load_config_as_dict(self.config_path)['Postprocessing_options']['tree_plotting']['drug_resistance_heatmap']
        """
        def update():
            prev_val = self.drug_resistance_heatmap
            self.drug_resistance_heatmap = string_to_bool_mapping[self.drug_resistance_heatmap_var.get()]
            config = load_config_as_dict(self.config_path)
            keys_path = ['Postprocessing_options', 'tree_plotting', 'drug_resistance_heatmap']
            update_nested_dict(config, keys_path, self.drug_resistance_heatmap)
            save_config(self.config_path, config)
            if prev_val != self.drug_resistance_heatmap:
                messagebox.showinfo("Success", "Updated successfully")

        self.drug_resistance_heatmap_label = ttk.Label(self.control_frame, text="drug_resistance_heatmap:")
        self.drug_resistance_heatmap_label.pack()
        self.drug_resistance_heatmap_var = tk.StringVar(value=bool_to_string_mapping[self.drug_resistance_heatmap])
        self.drug_resistance_heatmap_combobox = ttk.Combobox(
            self.control_frame, textvariable=self.drug_resistance_heatmap_var, 
            values=["Yes", "No"], state="readonly"
            )
        self.drug_resistance_heatmap_combobox.pack()
        self.update_drug_resistance_heatmap_button = tk.Button(self.control_frame, text="Update Method", command=update)
        self.update_drug_resistance_heatmap_button.pack()
