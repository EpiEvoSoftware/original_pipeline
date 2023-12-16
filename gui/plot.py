import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import numpy as np
from network import *
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class NetworkGraphApp:
    """
    A class providing a visualization app.
    """

    def __init__(self, parent, config_file):
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
        self.pop_size = int(config_file["host_size"])

        # window_width = 800
        # window_height = 600
        # self.root.geometry(f"{window_width}x{window_height}")
        # For controlling GUI height and width

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

        self.create_table()

    def plot_degree_distribution(self):
        graph_type = self.graph_type.get()
        if graph_type == "Erdős–Rényi":
            p = float(self.parameter_entries["p"].get())
            G = ER_generate(1000, p)
        elif graph_type == "Random Partition":
            p_in = float(self.parameter_entries["p_in"].get())
            p_out = float(self.parameter_entries["p_out"].get())

            G = rp_generate([500, 500], [p_in, p_in], p_out)
        elif graph_type == "Barabási-Albert":
            m = int(self.parameter_entries["m"].get())
            G = ba_generate(1000, m)

        degrees = [G.degree(n) for n in G.nodes()]

        self.ax.clear()
        self.ax.hist(degrees, bins=range(
            min(degrees), max(degrees) + 1, 1), edgecolor='black')
        self.ax.set_title("Degree Distribution")
        self.ax.set_xlabel("Degree")
        self.ax.set_ylabel("Number of Nodes")
        self.canvas.draw()

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

    def create_table(self):
        self.table_frame = ttk.Frame(self.parent)
        self.table_frame.pack(side=tk.BOTTOM, fill=tk.X,
                              padx=10, pady=10, expand=False)

        columns = ("id", "t1", "t2", "host_range", "host_id")
        self.table = ttk.Treeview(
            self.table_frame, columns=columns, show='headings')
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor=tk.CENTER)
        self.table.pack(side=tk.LEFT, fill=tk.X)

        for i in range(1, 5):
            t1 = round(random.uniform(0, 1), 2)
            t2 = round(random.uniform(0, 1), 2)
            self.table.insert("", "end", values=(i, t1, t2, "", ""))

        self.table.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        item = self.table.identify('item', event.x, event.y)
        column = self.table.identify_column(event.x)
        # Assuming host_range is the fourth column
        if self.table.identify_column(event.x) == "#4":
            self.edit_host_range(item, column)

    def edit_host_range(self, item, column):
        # Create a combobox
        combobox = ttk.Combobox(
            self.table, values=["0-25%", "25-50%", "50-75%", "75-100%"])
        combobox.set(self.table.item(item, 'values')[3])  # Set current value

        # Place combobox in the cell
        x, y, width, height = self.table.bbox(item, column)
        combobox.place(x=x, y=y, width=width, height=height)

        # Bind selection event
        combobox.bind("<<ComboboxSelected>>", lambda event, item=item,
                      combobox=combobox: self.update_host_range(item, combobox))

    def update_host_range(self, item, combobox):
        self.table.set(item, column="host_range", value=combobox.get())
        combobox.destroy()


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = NetworkGraphApp(root)
#     root.mainloop()
