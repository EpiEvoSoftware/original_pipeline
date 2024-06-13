import sys
import os
import time
import json
from utils import *
from tkinter import messagebox 
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import numpy as np
import json
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
from seed_host_matcher import *

def read_json_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


class HostMatch:
    """
    A class providing a visualization app.
    """

    def __init__(self, parent, tab_parent, config_path, tab_title, tab_index, hide = False):
        """
        Initializes the visualization app.

        Parameter k: The initial number of clusters
        Precondition: k is an int

        Parameter config_file: The configuration file, as a python dictionary
        Precondition: config_file is a valid dictionary
        """
        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_parent.add(parent, text=tab_title)
        self.tab_index = tab_index
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")
        
        self.config_path = config_path

        self.render_initial()
        self.render_next_button()

        
    def render_initial(self):
        self.graph_frame = ttk.Frame(self.parent)
        self.graph_frame.pack(side=tk.TOP, fill=tk.X, expand=False)
        fig, self.ax = plt.subplots(figsize=(4, 3), constrained_layout=True)
        self.ax.hist([], bins=[])
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()   

        load_button = ttk.Button(self.parent, text="Load input files", command=self.load_inputs, style="Large.TButton")
        load_button.pack()

        self.control_frame = ttk.Frame(self.parent)
        self.control_frame.pack(side=tk.BOTTOM, fill="both", padx=10, pady=10, expand=True)
        
    
    def load_inputs(self):
        config = load_config_as_dict(self.config_path)
        cwd = config["BasicRunConfiguration"]["cwdir"]
        self.network_file_path = os.path.join(cwd, "contact_network.adjlist")
        if not os.path.exists(self.network_file_path):
            messagebox.showerror("File not found", f"Input network file not found at expected location '{self.network_file_path}'")
            return
        
        num_seeds = config["SeedsConfiguration"]["seed_size"]
        if not isinstance(num_seeds, int) and num_seeds > 0:
            messagebox.showerror("Value error", f"Number of seeds needs to be a positive integer, it is currently" + num_seeds)
            return      
        
        display_genetic_effects = True
        csv_file_path = os.path.join(cwd, "seeds_trait_values.csv")
        if not os.path.exists(csv_file_path):
            display_genetic_effects = False
        
        self.display_graph(self.network_file_path)
        self.display_control(num_seeds, csv_file_path, display_genetic_effects)

    def display_graph(self, network_file_path):
        G = nx.read_adjlist(network_file_path)
        degrees = [G.degree(n) for n in G.nodes()]
        bin_size = max(1, int((max(degrees)-min(degrees))/30))

        self.ax.clear()
        self.ax.hist(
            degrees,
            bins=np.arange(min(degrees)-bin_size-0.5, max(degrees)+bin_size+0.5, bin_size),
            edgecolor="black",
        )
        self.ax.set_title("Degree Distribution")
        self.ax.set_xlabel("Degree")
        self.ax.set_ylabel("Number of Nodes")
 
        self.canvas.draw()    

    def display_control(self, num_seeds, csv_file_path, display_genetic_effects):
        for child in self.control_frame.winfo_children():
            child.destroy()

        # Setup table
        table = ttk.Treeview(self.control_frame, show='headings')
        self.table = table
        table.pack()
        table.bind("<Double-1>", self.on_double_click)
        
        match_hosts_button = ttk.Button(self.control_frame, text="Match Hosts", command=self.run_match_hosts, style='Large.TButton')
        match_hosts_button.pack()
        
        if display_genetic_effects:
            with open(csv_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                columns = reader.fieldnames + ["match_method", "method_parameter", "method_parameter_2", "host_id"]
                
                self.table["columns"] = columns
                for col in columns:
                    self.table.heading(col, text=col.replace('_', ' ').title())
                    self.table.column(col, width=150, anchor='center')
                    
                for row in reader:
                    values = [row[col] for col in reader.fieldnames]
                    extended_values = values + ["Random", "", "", ""] 
                    self.table.insert("", "end", values=extended_values)
        else:
            columns = ["seed_id", "match_method", "method_parameter", "method_parameter_2", "host_id"]
            self.table["columns"] = columns
            for col in columns:
                    self.table.heading(col, text=col.replace('_', ' ').title())
                    self.table.column(col, width=150, anchor='center')
            
            for i in range(num_seeds):
                values = [str(i), "Random", "", "", ""] 
                self.table.insert("", "end", values=values)
            
    def on_double_click(self, event):
        item = self.table.identify('item', event.x, event.y)
        column = self.table.identify_column(event.x)
        col_name = self.table["columns"][int(column.replace('#', '')) - 1]
        
        match_method = self.table.item(item, 'values')[self.table["columns"].index("match_method")]
                                                       
        if col_name == "match_method":
            self.choose_match_method(item, column)
        elif col_name == "method_parameter_2" and match_method == "Percentile":
            self.type_in_parameter(item, column)
        elif col_name == "method_parameter" and match_method != "Random":
            self.type_in_parameter(item, column)
                                                       
    
    def type_in_parameter(self, item, column):
        entry = tk.Entry(self.table)
        entry.insert(0, self.table.item(item, 'values')[int(column[1]) - 1]) 

        x, y, width, height = self.table.bbox(item, column)
        entry.place(x=x, y=y, width=width, height=height)

        def save_percentage(event):
            self.table.set(item, column=column, value=entry.get())
            entry.destroy()

        entry.bind("<Return>", save_percentage)
        entry.focus()

    def choose_match_method(self, item, column):
        combobox = ttk.Combobox(
            self.table, values=["Random", "Ranking", "Percentile"])
        combobox.set(self.table.item(item, 'values')[4])

        x, y, width, height = self.table.bbox(item, column)
        combobox.place(x=x, y=y, width=width, height=height)

        # Update method_parameter column when a match method is selected
        combobox.bind("<<ComboboxSelected>>", lambda event, item=item,
                      combobox=combobox: self.update_match_method_and_parameter(event, item, combobox))

    def update_match_method_and_parameter(self, event, item, combobox):
        new_method = combobox.get()
        self.table.set(item, column="match_method", value=new_method)
        self.table.set(item, column="method_parameter", value="")
        self.table.set(item, column="method_parameter_2", value="")
        combobox.destroy()

    def update_cell(self, item, col_name, combobox):
        self.table.set(item, column=col_name, value=combobox.get())
        combobox.destroy()

    def edit_method_parameter(self, item, column, ):
        match_method = self.table.item(item, 'values')[self.table["columns"].index("match_method")]
        options = self.get_method_parameter_options(match_method)

        combobox = ttk.Combobox(self.table, values=options)
        combobox.set(self.table.item(item, 'values')[5])

        x, y, width, height = self.table.bbox(item, column)
        combobox.place(x=x, y=y, width=width, height=height)

        combobox.bind("<<ComboboxSelected>>", lambda event, item=item,
                      combobox=combobox: self.update_cell(item, "method_parameter", combobox))

    def get_method_parameter_options(self, match_method):
        if match_method == "Percentile":
            return ["0-25%", "25-50%", "50-75%", "75-100%"]
        elif match_method == "Ranking":
            return ["1", "2", "3", "4", "5"]
        return [""]

    def run_match_hosts(self):
        ntwk = read_network(self.network_file_path)
        
        config = load_config_as_dict(self.config_path)
        cwdir = config["BasicRunConfiguration"]["cwdir"]
        num_seeds = len(self.table.get_children())
        rand_seed = config["BasicRunConfiguration"]["random_number_seed"]

        match_methods, match_params = self.collect_matching_criteria()
        match_dict = run_seed_host_match("randomly_generate", cwdir, num_seeds, match_scheme=match_methods, match_scheme_param=match_params, rand_seed=rand_seed)
        
        if match_dict[0] is not None:
            match_dict = match_dict[0]
        else:
            messagebox.showerror("Matching Error", "Matching Error: " + str(match_dict[1]))
            return

        for child in self.table.get_children():
            row = self.table.item(child)['values']
            seed_id = int(row[0])

            if seed_id in match_dict:
                host_id = match_dict[seed_id]

                updated_values = list(row)
                updated_values[-1] = host_id
                self.table.item(child, values=updated_values)

        self.display_matched_hosts(ntwk, match_dict)

    def collect_matching_criteria(self):
        match_methods = {}
        match_params = {}

        for child in self.table.get_children():
            row = self.table.item(child)['values']

            seed_id = int(row[0])

            match_method_col = self.table["columns"].index("match_method")
            method_parameter_col = self.table["columns"].index("method_parameter")
            method_parameter_col2 = self.table["columns"].index("method_parameter_2")
            
            
            match_method = row[match_method_col].lower()
            match_methods[seed_id] = match_method

            if match_method == "ranking":
                method_parameter = row[method_parameter_col]
                match_params[seed_id] = int(method_parameter)
            elif match_method == "percentile":
                method_parameter = row[method_parameter_col]
                method_parameter_2 = row[method_parameter_col2]
                percentages = [int(method_parameter), int(method_parameter_2)]
                match_params[seed_id] = percentages
            else:  # For "Random", no specific parameter is needed
                match_params[seed_id] = None

        match_methods = json.dumps(match_methods)
        match_params = json.dumps(match_params)
        return match_methods, match_params

    def display_matched_hosts(self, ntwk, match_dict):
        degrees = [ntwk.degree(n) for n in ntwk.nodes()]
        bin_size = max(1, int((max(degrees)-min(degrees))/30))

        self.ax.clear()
        degree_counts, _, _ = self.ax.hist(
            degrees,
            bins=np.arange(min(degrees)-bin_size-0.5, max(degrees)+bin_size+0.5, bin_size),
            edgecolor="black",
        )
        self.ax.set_title("Degree Distribution")
        self.ax.set_xlabel("Degree")
        self.ax.set_ylabel("Number of Nodes")

        max_count = np.max(degree_counts)
        annotation_height = max_count + max_count * 0.1  

        # Highlight the matched hosts and label them
        for seed_id, host_id in match_dict.items():
            host_degree = ntwk.degree(host_id)
            self.ax.axvline(x=host_degree, color='r', linestyle='--', lw=1)
            self.ax.text(host_degree, annotation_height, f'{seed_id}', rotation=45, color='blue', fontsize=8, ha='right', va='bottom')

        self.ax.set_ylim(top=annotation_height + max_count * 0.2)

        legend_elements = [Line2D([0], [0], color='r', linestyle='--', lw=1, label='Matched Hosts')]
        self.ax.legend(handles=legend_elements, loc='upper right')
 
        self.canvas.draw()  

    def render_next_button(self):
        next_button = ttk.Button(self.control_frame, text="Next", command=lambda: self.next_tab, style='Large.TButton')
        next_button.pack(side="bottom")

    def next_tab(self):
        current_tab_index = self.tab_index
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.tab(next_tab_index, state="normal")
        self.tab_parent.select(next_tab_index)