import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(os.path.dirname(current_dir), '../codes')
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# from seed_host_match_func import *
# from network_func import *
from seed_host_match_func_v0 import *
from network_generator import *


import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import numpy as np
from tools import *
import json
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def read_json_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


class NetworkGraphApp:
    """
    A class providing a visualization app.
    """

    def __init__(self, parent, tab_parent, config_path):
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

        self.parent = parent
        self.tab_parent = tab_parent

        self.config_path = config_path

        self.pop_size = int(self.load_config_as_dict()['NetworkModelParameters']['host_size'])

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

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.graph_frame = ttk.Frame(self.parent)
        self.graph_frame.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.graph_type = tk.StringVar()
        ttk.Label(self.control_frame, text="Select Graph Type:",
                  style='Large.TLabel').pack()
        graph_type_dropdown = ttk.Combobox(
            self.control_frame,
            textvariable=self.graph_type,
            values=["Erdős–Rényi", "Barabási-Albert",
                    "Random Partition"],
            style='Large.TButton'
        )
        # TODO: Look for more responsive tk classes to replace Combobox
        graph_type_dropdown.pack()
        graph_type_dropdown.bind(
            "<<ComboboxSelected>>", self.update_parameters)

        self.parameter_entries = {}
        self.parameter_labels = []

        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.degree_button = ttk.Button(
            self.control_frame, text="Plot Degree Distribution", command=self.plot_degree_distribution, style='Large.TButton')
        self.degree_button.pack()
        # TODO: ask user for partition numbers, max 10

        # # -----------------------------------------
        # # Creating the table
        # # -----------------------------------------
        # self.table = ttk.Treeview(self.control_frame, columns=(
        #     'id', 't1', 't2', 'host_id'), show='headings')

        # # Defining and setting the width of the columns
        # self.table.column('id', width=50)
        # self.table.column('t1', width=50)
        # self.table.column('t2', width=50)
        # self.table.column('host_id', width=100)
        # # TODO: after choosing the Percentile, match it to the specific node

        # # Defining the columns
        # self.table.heading('id', text='ID')
        # self.table.heading('t1', text='t1')
        # self.table.heading('t2', text='t2')
        # self.table.heading('host_id', text='host_id')

        # # # Defining the headings
        # # self.table.heading('id', text='ID')
        # # self.table.heading('t1', text='t1')
        # # self.table.heading('t2', text='t2')
        # # self.table.heading('host_id', text='host_id')
        # # TODO: generate from text file, will have t3, t4
        # # TODO: limit x axis when to the right, its too to the left

        # # Adding rows to the table
        # data = [
        #     ("1", "?", "?", "1111"),
        #     ("2", "?", "?", "1111"),
        #     ("3", "?", "?", "1111"),
        #     ("4", "?", "?", "1111"),
        # ]

        # for row in data:
        #     self.table.insert('', tk.END, values=row)

        # # Positioning the table in the GUI
        # self.table.pack(side='right', fill='both', expand=True)

        self.create_table()

    def create_table(self):
        self.table_frame = ttk.Frame(self.parent)
        self.table_frame.pack(side=tk.BOTTOM, fill=tk.X,
                              padx=10, pady=10, expand=False)

        columns = ("seed_id", "transmissibility", "drugresist_1", "drugresist_2", "match_method", "method_parameter", "method_parameter_2", "host_id")
        self.table = ttk.Treeview(
            self.table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.table.heading(col, text=col.replace('_', ' ').title())
            if col in ["seed_id", "transmissibility", "drugresist_1", "drugresist_2"]:
                self.table.column(col, width=100, anchor=tk.CENTER)  
            else:
                self.table.column(col, width=150, anchor=tk.CENTER)  
        self.table.pack(side=tk.LEFT, fill=tk.X)

        self.populate_table_from_csv('test/test_drugresist/seeds_trait_values.csv') 

        self.table.bind("<Double-1>", self.on_double_click)
        

        self.degree_button = ttk.Button(
            self.table_frame, text="Match All Hosts", command=self.match_hosts, style='Large.TButton')
        self.degree_button.pack()
    
    def populate_table_from_csv(self, csv_path):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.table.insert("", "end", values=(
                    row['seed_id'], row['transmissibility'], row['drugresist_1'], row['drugresist_2'], "", ""))

    def plot_degree_distribution(self):
        graph_type = self.graph_type.get()
        wk_dir = "/Users/vivianzhao/Desktop/TB_software_new/original_pipeline/test/" 
        wk_dir = "/Users/andrewhahn/T7/original_pipeline/test/"
        if graph_type == "Erdős–Rényi":
            p = float(self.parameter_entries["p"].get())
            run_network_generation(pop_size=1000, wk_dir=wk_dir, method="randomly_generate", model="ER", p_ER=p)
        elif graph_type == "Random Partition":
            p_in = float(self.parameter_entries["p_in"].get())
            p_out = float(self.parameter_entries["p_out"].get())
            rp_size = [500, 500]  # Example partition sizes
            p_within = [p_in, p_in]
            run_network_generation(pop_size=1000, wk_dir=wk_dir, method="randomly_generate", model="RP", rp_size=rp_size, p_within=p_within, p_between=p_out)
        elif graph_type == "Barabási-Albert":
            m = int(self.parameter_entries["m"].get())
            run_network_generation(pop_size=1000, wk_dir=wk_dir, method="randomly_generate", model="BA", m=m)

        G = nx.read_adjlist(os.path.join(wk_dir, "contact_network.adjlist"))
        degrees = [G.degree(n) for n in G.nodes()]

        self.ax.clear()
        self.ax.hist(degrees, bins=range(
            min(degrees), max(degrees) + 1, 1), edgecolor='black')
        self.ax.set_title("Degree Distribution")
        self.ax.set_xlabel("Degree")
        self.ax.set_ylabel("Number of Nodes")

        x_min = self.ax.get_xlim()[0]
        current_range = self.ax.get_xlim()[1] - x_min

        quartile = 3
        # # partitions = [current_range//4, current_range//2, current_range*3//4]
        # partitions = []
        # n = len(degrees)
        # for partition in range(quartile):
        #     partitions.append(degrees[n//partition])

        partitions = [current_range/4 + x_min, current_range /
                      2 + x_min, current_range*3/4 + x_min]
        for partition in partitions:
            self.ax.axvline(x=partition, color='k', linestyle='--')

        self.canvas.draw()
        # TODO: change names from t1, t2 to more descriptive name

        return

    # def plot_degree_distribution(self):
    #     graph_type = self.graph_type.get()
    #     selected_graph_type = self.network_dict[graph_type]

    #     if selected_graph_type == "ER":
    #         p = float(self.parameter_entries["p"].get())
    #         G = network_generate.ER_generate(self.pop_size, p)
    #     elif selected_graph_type == "RP":
    #         p_in = float(self.parameter_entries["p_in"].get())
    #         p_out = float(self.parameter_entries["p_out"].get())

    #         G = network_generate.rp_generate([500, 500], [p_in, p_in], p_out)
    #         # TODO: replace with correct parameters in the config file
    #     elif selected_graph_type == "BA":
    #         m = int(self.parameter_entries["m"].get())
    #         # TODO error handling: ValueError: invalid literal for int() with base 10: ''
    #         G = network_generate.ba_generate(self.pop_size, m)
    #     else:
    #         messagebox.showwarning('Error', 'Unsupported Graph Type')

    #     degrees = [G.degree(n) for n in G.nodes()]

    #     # --------- by x axis

    #     partitions = [25, 50, 75]

    #     self.ax.clear()
    #     self.ax.hist(degrees, bins=range(
    #         min(degrees), max(degrees) + 1, 1), edgecolor='black')

    #     # Draw vertical lines for partitions
    #     for partition in partitions:
    #         self.ax.axvline(x=partition, color='k', linestyle='--')

    #     # Setting titles and labels
    #     self.ax.set_title("Degree Distribution")
    #     self.ax.set_xlabel("Degree")
    #     self.ax.set_ylabel("Number of Nodes")
    #     self.canvas.draw()

    #     # Creating a dictionary to hold nodes for each partition
    #     partitioned_nodes = {partition: [] for partition in partitions + [100]}

    #     # Assign nodes to partitions
    #     for node, degree in enumerate(degrees):
    #         for partition in partitions:
    #             if degree <= partition:
    #                 partitioned_nodes[partition].append(node)
    #                 break
    #         else:
    #             # For nodes with degree greater than the last partition value
    #             partitioned_nodes[100].append(node)

    #     return partitioned_nodes

    #     # --------- by node values

    #     # Calculate quartiles
    #     Q1, median, Q3 = np.percentile(degrees, [25, 50, 75])

    #     self.ax.clear()
    #     self.ax.hist(degrees, bins=range(
    #         min(degrees), max(degrees) + 1, 1), edgecolor='black')

    #     # Draw vertical lines for quartiles
    #     for quartile in [Q1, median, Q3]:
    #         self.ax.axvline(x=quartile, color='k', linestyle='--')

    #     # Setting titles and labels
    #     self.ax.set_title("Degree Distribution")
    #     self.ax.set_xlabel("Degree")
    #     self.ax.set_ylabel("Number of Nodes")
    #     self.canvas.draw()

    #     # Returning the quartile values
    #     return Q1, median, Q3

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
        ntwk_path = "/Users/vivianzhao/Desktop/TB_software_new/original_pipeline/test/contact_network.adjlist"
        ntwk = read_network(ntwk_path)

        match_methods, match_params = self.collect_matching_criteria()

        match_dict = match_all_hosts(ntwk, match_methods, match_params, 5)


        for child in self.table.get_children():
            row = self.table.item(child)['values']
            seed_id = int(row[0])

            if seed_id in match_dict:
                host_id = match_dict[seed_id]

                updated_values = list(row)
                updated_values[-1] = host_id
                self.table.item(child, values=updated_values)

        self.highlight_matched_hosts(ntwk, match_dict)

    def highlight_matched_hosts(self, ntwk, match_dict):
        
        self.ax.clear()
        
        degrees = [ntwk.degree(n) for n in ntwk.nodes()]
        degree_counts, bins, _ = self.ax.hist(degrees, bins=range(min(degrees), max(degrees) + 1, 1), edgecolor='black')
        self.ax.set_title("Degree Distribution")
        self.ax.set_xlabel("Degree")
        self.ax.set_ylabel("Number of Nodes")

        # Determine the y-position for annotations based on the histogram
        max_count = np.max(degree_counts)
        annotation_height = max_count + max_count * 0.1  # Slightly above the highest bar

        # Highlight the matched hosts and label them
        for seed_id, host_id in match_dict.items():
            host_degree = ntwk.degree(host_id)
            # Draw a vertical line for the matched host
            self.ax.axvline(x=host_degree, color='r', linestyle='--', lw=1)
            # Annotate the line with seed_id
            self.ax.text(host_degree, annotation_height, f'{seed_id}', rotation=45, color='blue', fontsize=8, ha='right', va='bottom')

        # Since the annotation might go beyond the current y-limit, adjust the limit
        self.ax.set_ylim(top=annotation_height + max_count * 0.2)

        # Add a legend entry for matched hosts
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], color='r', linestyle='--', lw=1, label='Matched Hosts')]
        self.ax.legend(handles=legend_elements, loc='upper right')

        # Redraw the canvas
        self.canvas.draw()

    def collect_matching_criteria(self):
        match_methods = {}
        match_params = {}

        for child in self.table.get_children():
            row = self.table.item(child)['values']

            seed_id = int(row[0])

            match_method = row[4]

            method_parameter = row[5]
            
            

            match_methods[seed_id] = match_method

            if match_method == "Ranking":
                match_params[seed_id] = int(method_parameter)
            elif match_method == "Percentile":
                method_parameter_2 = row[6]
                percentages = [int(method_parameter), int(method_parameter_2)]
                match_params[seed_id] = percentages
            else:  # For "Random", no specific parameter is needed
                match_params[seed_id] = None

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


