import sys
import os
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

        # window_width = 800
        # window_height = 600
        # self.root.geometry(f"{window_width}x{window_height}")
        # For controlling GUI height and width

        self.network_dict = {
            "Erdős–Rényi": "ER",
            "Barabási-Albert": "BA",
            "Random Partition": "RP"
        }

        # TODO: fix read_txt and list_files so that it reads from the txt file for the table
        # read_txt("./files/trait_vals_seeds.txt")
        # list_files("./files")

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

        self.create_table()

    def create_table(self):
        self.table_frame = ttk.Frame(self.parent)
        self.table_frame.pack(side=tk.BOTTOM, fill=tk.X,
                              padx=10, pady=10, expand=False)

        columns = ("seed_id", "transmissibility_1", "drugresist_1", "drugresist_2", "match_method", "method_parameter", "method_parameter_2", "host_id")
        self.table = ttk.Treeview(
            self.table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.table.heading(col, text=col.replace('_', ' ').title())
            if col in ["seed_id", "transmissibility", "drugresist_1", "drugresist_2"]:
                self.table.column(col, width=100, anchor=tk.CENTER)  
            else:
                self.table.column(col, width=150, anchor=tk.CENTER)  
        self.table.pack(side=tk.LEFT, fill=tk.X)

        seed_csv = os.path.join(self.wk_dir, 'seeds_trait_values.csv')
        self.populate_table_from_csv(seed_csv) 

        self.table.bind("<Double-1>", self.on_double_click)

        self.degree_button = ttk.Button(
            self.table_frame, text="Match All Hosts", command=self.match_hosts, style='Large.TButton')
        self.degree_button.pack()
    
    def populate_table_from_csv(self, csv_path):
        if os.path.exists(csv_path):
            with open(csv_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    values = tuple(row[col] for col in reader.fieldnames)
                    extended_values = values + ("Random", "")
                    self.table.insert("", "end", values=extended_values)



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
        match_method = self.table.item(item, 'values')[4]
        if column in ("#6", "#7") and match_method == "Percentile":  # Columns for "method_parameter" and "method_parameter_2"
            self.edit_percentage_parameter(item, column)
        elif column == "#6" and match_method != "" and match_method != "Random":  # column number for "method_parameter"
            self.edit_method_parameter(item, column)
        elif column == "#5":  # Column for "match_method"
            self.choose_match_method(item, column)
    
    def edit_percentage_parameter(self, item, column):
        entry = tk.Entry(self.table)
        entry.insert(0, self.table.item(item, 'values')[int(column[1]) - 1])  # Pre-fill with current value

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
        match_method = self.table.item(item, 'values')[4]
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
                # if degrees == []:
                #     messagebox.showerror("Error", f"Network file path is empty")
                #     return
                self.ax.clear()
            
                degrees = [G.degree(n) for n in G.nodes()]
                self.ax.hist(degrees, bins=range(min(degrees), max(degrees) + 1, 1), edgecolor='black')
                self.ax.set_title("Degree Distribution")
                self.ax.set_xlabel("Degree")
                self.ax.set_ylabel("Number of Nodes")
                
                # self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
                self.canvas.draw()
                # self.canvas_widget = self.canvas.get_tk_widget()
                # self.canvas_widget.pack(fill=tk.BOTH, expand=True)
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

            match_method = (row[4]).lower()

            method_parameter = row[5]
            print(method_parameter)
            
            

            match_methods[seed_id] = match_method

            if match_method == "ranking":
                match_params[seed_id] = int(method_parameter)
            elif match_method == "percentile":
                method_parameter_2 = row[6]
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

# if __name__ == "__main__":
#     root = tk.Tk()
#     config_path = '../test/params_test.json'  # Replace with the actual path
#     config_data = read_json_config(config_path)
#     app = NetworkGraphApp(root, config_data)
#     root.mainloop()


