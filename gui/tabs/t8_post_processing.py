
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import shutil
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.join(os.path.dirname(current_dir), '../codes')
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

class PostProcessing:
    def __init__(self, parent, tab_parent, config_path):

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

        self.cwdir = self.load_config_as_dict()['BasicRunConfiguration']['cwdir']
        
# Postprocessing_options Configurations
        self.do_postprocess = self.load_config_as_dict()['Postprocessing_options']['do_postprocess']
        self.branch_color_trait = self.load_config_as_dict()['Postprocessing_options']['tree_plotting']['branch_color_trait']
        self.drug_resistance_heatmap = self.load_config_as_dict()['Postprocessing_options']['tree_plotting']['drug_resistance_heatmap']

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
        


    def load_config_as_dict(self):
        with open(self.config_path, 'r') as file:
            return json.load(file)

    def save_config(self, config):
        with open(self.config_path, 'w') as file:
            json.dump(config, file, indent=4)

    def render_all(self):
        self.render_do_postprocess()
        self.render_branch_color_trait()
        self.render_drug_resistance_heatmap()

    def update_generic(self):
        return
    
    def render_do_postprocess(self):
        self.do_postprocess_label = ttk.Label(self.control_frame, text="do_postprocess:")
        self.do_postprocess_label.pack()
        self.do_postprocess_var = tk.StringVar(value=self.do_postprocess)
        self.do_postprocess_combobox = ttk.Combobox(
            self.control_frame, textvariable=self.do_postprocess_var, 
            values=["Yes", "No"], state="readonly"
            )
        self.do_postprocess_combobox.pack()
        self.update_do_postprocess_button = tk.Button(self.control_frame, text="Update Method", command=self.update_generic)
        self.update_do_postprocess_button.pack()

    def render_branch_color_trait(self):
        self.branch_color_trait_label = ttk.Label(self.control_frame, text="branch_color_trait:")
        self.branch_color_trait_label.pack()
        self.branch_color_trait_entry = ttk.Entry(self.control_frame, foreground="black")
        self.branch_color_trait_entry.insert(0, self.branch_color_trait)  
        self.branch_color_trait_entry.pack()
        update_branch_color_trait_button = tk.Button(self.control_frame, text="Update branch_color_trait", command=self.update_generic)
        update_branch_color_trait_button.pack()

    def render_drug_resistance_heatmap(self):
        self.drug_resistance_heatmap_label = ttk.Label(self.control_frame, text="drug_resistance_heatmap:")
        self.drug_resistance_heatmap_label.pack()
        self.drug_resistance_heatmap_var = tk.StringVar(value=self.drug_resistance_heatmap)
        self.drug_resistance_heatmap_combobox = ttk.Combobox(
            self.control_frame, textvariable=self.drug_resistance_heatmap_var, 
            values=["Yes", "No"], state="readonly"
            )
        self.drug_resistance_heatmap_combobox.pack()
        self.update_drug_resistance_heatmap_button = tk.Button(self.control_frame, text="Update Method", command=self.update_generic)
        self.update_drug_resistance_heatmap_button.pack()
