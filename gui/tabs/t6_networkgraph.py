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


class NetworkGraphApp:
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
        if isinstance(parent, tk.Tk):
            self.parent.title("Network Graph Visualization")

        self.tab_parent = tab_parent
        self.tab_parent.add(parent, text=tab_title)
        self.tab_index = tab_index
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")
        

        self.config_path = config_path
        
        self.config = load_config_as_dict(self.config_path)
        # fix loadings
        self.wk_dir = self.config["BasicRunConfiguration"]["cwdir"]
        self.network_file_path = os.path.join(self.wk_dir, "contact_network.adjlist")
        

        self.pop_size = int(self.config['NetworkModelParameters']['host_size'])

        self.network_dict = {
            "Erdős–Rényi": "ER",
            "Barabási-Albert": "BA",
            "Random Partition": "RP"
        }


        style = ttk.Style()
        style.configure('Large.TButton', font=(
            'Helvetica', 12))
        style.configure('Large.TLabel', font=(
            'Helvetica', 12))

        self.graph_frame = ttk.Frame(self.parent)
        self.graph_frame.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.parameter_entries = {}
        self.parameter_labels = []

        self.fig, self.ax = plt.subplots(figsize=(5, 3), constrained_layout=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.plot_degree_distribution()

        
        self.last_checked_time = 0  
        self.seed_csv = os.path.join(self.wk_dir, 'seeds_trait_values.csv')
        self.poll_for_csv_updates() 
        
        seed_csv = os.path.join(self.wk_dir, 'seeds_trait_values.csv')
        self.populate_table_from_csv(seed_csv)
        
        
    def populate_table_from_csv(self, csv_path):
        if not os.path.exists(csv_path):
            if hasattr(self, 'table_frame'):
                self.table_frame.destroy()
                delattr(self, 'table_frame')
            return
        
        if not hasattr(self, 'table_frame'):
            self.setup_table_ui()


        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            columns = reader.fieldnames + ["match_method", "method_parameter", "method_parameter_2", "host_id"]
            
            if not self.table["columns"]: 
                self.table["columns"] = columns
                self.table.delete(*self.table.get_children())
                for col in columns:
                    self.table.heading(col, text=col.replace('_', ' ').title())
                    self.table.column(col, width=150, anchor='center')
                    
            self.table.delete(*self.table.get_children())
            for row in reader:
                # values = tuple(row[col] for col in reader.fieldnames)
                values = [row[col] for col in reader.fieldnames]
                extended_values = values + ["Random", "", "", ""] 
                self.table.insert("", "end", values=extended_values)

    def setup_table_ui(self):
        self.table_frame = ttk.Frame(self.parent)
        self.table_frame.pack(side=tk.BOTTOM, fill="both", padx=10, pady=10, expand=True)
        
        self.table = ttk.Treeview(self.table_frame, show='headings')
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(self.table_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.degree_button = ttk.Button(button_frame, text="Match All Hosts", command=self.match_hosts, style='Large.TButton')
        self.degree_button.pack(side=tk.TOP, pady=35, padx=5, fill=tk.X)
        
        next_button = ttk.Button(button_frame, text="Next", command=lambda: self.next_tab(), style='Large.TButton')
        next_button.pack(side=tk.BOTTOM, padx=5, fill=tk.X)
        
        self.table.bind("<Double-1>", self.on_double_click)

    def next_tab(self):
        current_tab_index = self.tab_index
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.tab(next_tab_index, state="normal")
        self.tab_parent.select(next_tab_index)

    def poll_for_csv_updates(self):
        try:
            self.populate_table_from_csv(self.seed_csv)
        except Exception as e:
            print(f"Error while updating from CSV: {e}")
        finally:
            self.parent.after(1000, self.poll_for_csv_updates)
            
    def update_parameters(self, event=None):
        # clear existing parameters
        for label in self.parameter_labels:
            label.destroy()
        for entry in self.parameter_entries.values():
            entry.destroy()

        self.parameter_labels.clear()
        self.parameter_entries.clear()

        graph_type = self.graph_type.get()
        selected_graph_type = self.network_dict[graph_type]
        params = []

        if selected_graph_type == "ER":
            params = [("p", "float")]
        elif selected_graph_type == "RP":
            params = [("p_in", "float"), ("p_out", "float")]
        elif selected_graph_type == "BA":
            params = [("m", "int")]
        else:
            messagebox.showwarning('Error', 'Unsupported Graph Type')

        # create new parameters
        for param, dtype in params:
            label = ttk.Label(self.control_frame,
                              text=f"{param} ({dtype}):", style='Large.TLabel')
            label.pack()
            self.parameter_labels.append(label)
            entry = tk.Entry(self.control_frame)
            entry.pack()
            self.parameter_entries[param] = entry

        self.degree_button.pack_forget()
        self.degree_button.pack()

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
                                                       
                                                    
        # if column == "#6" and match_method != "Random":  # Columns for "method_parameter" and "method_parameter_2"
        #     self.type_in_parameter(item, column)
        # elif column == "#7" and match_method == "Percentile":  # column number for "method_parameter 2"
        #     self.type_in_parameter(item, column)
        # elif column == "#5":  # Column for "match_method"
        #     self.choose_match_method(item, column)
    
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

    def match_hosts(self):
        ntwk = read_network(self.network_file_path)
        
        num_seed = len(self.table.get_children())

        match_methods, match_params = self.collect_matching_criteria()
        match_dict = run_seed_host_match("randomly_generate", self.wk_dir, num_seed, match_scheme=match_methods, match_scheme_param=match_params)
        
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

        self.highlight_matched_hosts(ntwk, match_dict)
    
    def plot_degree_distribution(self):
        self.config = self.load_config_as_dict()
        self.wk_dir = self.config["BasicRunConfiguration"]["cwdir"]
        self.network_file_path = os.path.join(self.wk_dir, "contact_network.adjlist")
        if os.path.exists(self.network_file_path) and self.wk_dir!="":
            try:
                G = nx.read_adjlist(self.network_file_path)
                degrees = [G.degree(n) for n in G.nodes()]
                self.ax.clear()
            
                degrees = [G.degree(n) for n in G.nodes()]
                self.ax.hist(degrees, bins=range(min(degrees), max(degrees) + 1, 1), edgecolor='black')
                self.ax.set_title("Degree Distribution")
                self.ax.set_xlabel("Degree")
                self.ax.set_ylabel("Number of Nodes")
                
                self.canvas.draw()
            except FileNotFoundError:
                messagebox.showerror("Error", f"Network file not found at {self.network_file_path}")
                return

    def highlight_matched_hosts(self, ntwk, match_dict):
        
        self.ax.clear()
        
        degrees = [ntwk.degree(n) for n in ntwk.nodes()]
        degree_counts, bins, _ = self.ax.hist(degrees, bins=range(min(degrees), max(degrees) + 1, 1), edgecolor='black')
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

    def collect_matching_criteria(self):
        match_methods = {}
        match_params = {}

        for child in self.table.get_children():
            row = self.table.item(child)['values']

            seed_id = int(row[0])

            match_method_col = self.table["columns"].index("match_method")
            method_parameter_col = self.table["columns"].index("method_parameter")
            method_parameter_col2 = self.table["columns"].index("method_parameter_2")
            
            
            match_method = (row[match_method_col]).lower()

            method_parameter = row[method_parameter_col]
            
            

            match_methods[seed_id] = match_method

            if match_method == "ranking":
                match_params[seed_id] = int(method_parameter)
            elif match_method == "percentile":
                method_parameter_2 = row[method_parameter_col2]
                percentages = [int(method_parameter), int(method_parameter_2)]
                match_params[seed_id] = percentages
            else:  # For "Random", no specific parameter is needed
                match_params[seed_id] = None

        match_methods = json.dumps(match_methods)
        match_params = json.dumps(match_params)
        return match_methods, match_params
    
    def load_config_as_dict(self):
        with open(self.config_path, 'r') as file:
            return json.load(file)

