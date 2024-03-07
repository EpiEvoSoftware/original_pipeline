import tkinter as tk
from tkinter import ttk, messagebox, filedialog
# from __main__ import load_config_as_dict

class Configuration:
    def __init__(self, parent, tab_parent, config_path):
        self.parent = parent
        self.tab_parent = tab_parent

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True)  # pack the frame

        self.name_label = ttk.Label(self.control_frame, text="Number of Generations")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.name_label = ttk.Label(self.control_frame, text="Mutation")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Model For Transmissibility")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["Additive", "Bi-Allereic"], foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Model For Drug Resistance")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["Additive", "Bi-Allereic"], foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Within-Host-Evolution")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["On", "Off"], foreground="White")
        self.surname_combobox.pack()


        self.name_label = ttk.Label(self.control_frame, text="Caps for Within-Host Population")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

    def go_to_next_tab(self):
        current_tab_index = self.tab_parent.index(self.tab_parent.select())
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.select(next_tab_index)


        import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox

class Seeds:
    def __init__(self, parent, tab_parent, config_path):
        self.parent = parent
        self.tab_parent = tab_parent
        self.dynamic_widgets = []

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True)

        diagnostic_label = ttk.Label(self.control_frame, text="Working Directory")
        diagnostic_label.pack()
        choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        choose_file_button.pack()

        self.name_label = ttk.Label(self.control_frame, text="Seeds Size")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Seeds VCF File")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["Customize", "SLiM Burn-In"], foreground="White")
        self.surname_combobox.pack()

        self.surname_combobox.bind("<<ComboboxSelected>>", self.on_combobox_change)

        self.dynamic_widgets = []

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

    def choose_file(self):  
        filename = filedialog.askopenfilename(title="Select a file")
        print("Selected file:", filename) 

    def go_to_next_tab(self):
        current_tab_index = self.tab_parent.index(self.tab_parent.select())
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.select(next_tab_index)

    def on_combobox_change(self, event):
        """
        Clear previously displayed widgets
        Check the combobox value and render appropriate UI elements
        """
        for widget in self.dynamic_widgets:
            widget.destroy()
        self.dynamic_widgets.clear()

        choice = self.surname_combobox.get()
        if choice == "Customize":
            self.render_customize_options()
        elif choice == "SLiM Burn-In":
            self.render_slim_burn_in_options()

    def render_customize_options(self):
        labels = ["Path to Seed", "Path to Seed Phylogeny"]
        for label_text in labels:
            label = ttk.Label(self.control_frame, text=label_text)
            label.pack()
            button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
            button.pack()
            
            self.dynamic_widgets.extend([label, button])

    def render_slim_burn_in_options(self):
        entries = ["Burn-In Ne", "Burn-In Input Rate", "Generations, Run", "Scaling Factor"]
        for entry_text in entries:
            label = ttk.Label(self.control_frame, text=entry_text)
            label.pack()
            entry = ttk.Entry(self.control_frame, foreground="White")
            entry.pack()
            
            self.dynamic_widgets.extend([label, entry])


import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class GenomeEffSize:
    def __init__(self, parent, tab_parent, config_path):
        self.parent = parent
        self.tab_parent = tab_parent

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 

        diagnostic_label = ttk.Label(self.control_frame, text="Reference Genome")
        diagnostic_label.pack()

        choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        choose_file_button.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Effect Size Table")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["Customize", "Randomly Generate From GFF"], foreground="White")
        self.surname_combobox.pack()

        self.surname_combobox.bind("<<ComboboxSelected>>", self.on_combobox_change)

        self.dynamic_widgets = []

        # #if 1

        # diagnostic_label = ttk.Label(self.control_frame, text="Path To File")
        # diagnostic_label.pack()
        # choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        # choose_file_button.pack()


        # #if 2

        # diagnostic_label = ttk.Label(self.control_frame, text="Path To GFF")
        # diagnostic_label.pack()
        # choose_file_button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        # choose_file_button.pack()

        # self.name_label = ttk.Label(self.control_frame, text="Number of Effect Size Groups")
        # self.name_label.pack()
        # self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        # self.name_entry.pack()

        # next_button = tk.Button(self.parent, text="Show")
        # next_button.pack()
        # # Show table 1

        # # Show Table 2

        next_button = tk.Button(self.parent, text="Normalize")
        next_button.pack()

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

    def choose_file(self):  # 
        filename = filedialog.askopenfilename(title="Select a file")
        print("Selected file:", filename)  # replace

    def go_to_next_tab(self):
        current_tab_index = self.tab_parent.index(self.tab_parent.select())
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.select(next_tab_index)

    def on_combobox_change(self, event):
        """
        Clear previously displayed widgets
        Check the combobox value and render appropriate UI elements
        """
        for widget in self.dynamic_widgets:
            widget.destroy()
        self.dynamic_widgets.clear()

        choice = self.surname_combobox.get()
        if choice == "Customize":
            self.render_customize_options()
        elif choice == "Randomly Generate From GFF":
            self.render_generate_from_gff()

    def render_customize_options(self):
        label = ttk.Label(self.control_frame, text="Path to File")
        label.pack()
        button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        button.pack()
        
        self.dynamic_widgets.extend([label, button])

    def render_generate_from_gff(self):

        label = ttk.Label(self.control_frame, text="Path to gff")
        label.pack()
        button = tk.Button(self.control_frame, text="Choose File", command=self.choose_file)
        button.pack()

        name_label = ttk.Label(self.control_frame, text="Number of Effect Size Groups")
        name_label.pack()
        name_entry = ttk.Entry(self.control_frame, foreground="White")
        name_entry.pack()

        self.dynamic_widgets.extend([label, button, name_label, name_entry])



import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import numpy as np
from network import *
from tools import *
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


class NetworkGraphApp:
    """
    A class providing a visualization app.
    """

    def __init__(self, parent, tab_parent, config_path):
        """
        Initializes the visualization app.

        Parameter k: The initial number of clusters
        Precondition: k is an int

        Parameter config_path: The configuration file, as a python dictionary
        Precondition: config_path is a valid dictionary
        """
        self.parent = parent
        self.tab_parent = tab_parent

        if isinstance(parent, tk.Tk):
            self.parent.title("Network Graph Visualization")
        # self.pop_size = int(config_path["host_size"])

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


        # -----------------------------------------
        # Creating the table
        # -----------------------------------------
        self.table = ttk.Treeview(self.control_frame, columns=('id', 't1', 't2', 'host_id'), show='headings')

        # Defining and setting the width of the columns
        self.table.column('id', width=50)
        self.table.column('t1', width=50)
        self.table.column('t2', width=50)
        self.table.column('host_id', width=100)
        # TODO: after choosing the quantile, match it to the specific node
        
        # Defining the columns
        self.table.heading('id', text='ID')
        self.table.heading('t1', text='t1')
        self.table.heading('t2', text='t2')
        self.table.heading('host_id', text='host_id')

        # # Defining the headings
        # self.table.heading('id', text='ID')
        # self.table.heading('t1', text='t1')
        # self.table.heading('t2', text='t2')
        # self.table.heading('host_id', text='host_id')
        # TODO: generate from text file, will have t3, t4
        # TODO: limit x axis when to the right, its too to the left

        # Adding rows to the table
        data = [
            ("1", "?", "?", "1111"),
            ("2", "?", "?", "1111"),
            ("3", "?", "?", "1111"),
            ("4", "?", "?", "1111"),
        ]

        for row in data:
            self.table.insert('', tk.END, values=row)

        # Positioning the table in the GUI
        self.table.pack(side='right', fill='both', expand=True)

        next_button = tk.Button(self.parent, text="Next", command=self.go_to_next_tab)
        next_button.pack()

        self.create_table()

        # self.table = ttk.Treeview(self.control_frame, columns=('id', 't1', 't2', 'host_id'), show='headings')
        # You may need to pack or grid the table as well depending on your layout requirements

    def go_to_next_tab(self):
        current_tab_index = self.tab_parent.index(self.tab_parent.select())
        next_tab_index = (current_tab_index + 1) % self.tab_parent.index("end")
        self.tab_parent.select(next_tab_index)

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
        
        x_min = self.ax.get_xlim()[0]
        current_range = self.ax.get_xlim()[1] - x_min

        quartile = 3
        # partitions = [current_range//4, current_range//2, current_range*3//4]
        partitions = []
        n = len(degrees)
        for partition in range(quartile):
            partitions.append(degrees[n//partition])

        # partitions = [current_range/4 + x_min, current_range/2 + x_min, current_range*3/4 + x_min]
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


import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class EpiModel:
    def __init__(self, parent, tab_parent, config_path):
        self.parent = parent
        self.tab_parent = tab_parent

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True) 

        self.surname_label = ttk.Label(self.control_frame, text="Model")
        self.surname_label.pack()
        self.model_combobox = ttk.Combobox(self.control_frame, values=["SIR", "SEIR"], foreground="White")
        self.model_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Transmission Rate (S->I/E)")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="I->R")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="R->I")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Sample Rate")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Recovery Probability After Sampling")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Massive Sampling")
        self.surname_label.pack()
        self.sampling_combobox = ttk.Combobox(self.control_frame, values=["On", "Off"], foreground="White")
        self.sampling_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Number of Massive Sampling Event")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Treatment")
        self.surname_label.pack()
        self.treatment_combobox = ttk.Combobox(self.control_frame, values=["On", "Off"], foreground="White")
        self.treatment_combobox.pack()

        self.surname_combobox.bind("<<ComboboxSelected>>", self.on_combobox_change)
        self.dynamic_widgets = []

        self.treatment_combobox.bind("<<ComboboxSelected>>", self.on_combobox_change)
        self.dynamic_widgets = []

        self.model_combobox.bind("<<ComboboxSelected>>", self.on_combobox_change)
        self.dynamic_widgets = []


    def clear_dynamic_widgets(self, widget_group):
        """Clear widgets from a specific group."""
        for widget in widget_group:
            widget.destroy()  # or widget.pack_forget() if reusing
        widget_group.clear()

    def on_model_change(self, event):
        """
        """


    def on_combobox_change(self, event):
        """
        Clear previously displayed widgets
        Check the combobox value and render appropriate UI elements
        """
        for widget in self.dynamic_widgets:
            widget.destroy()
        self.dynamic_widgets.clear()

        if self.surname_combobox.get() == "On":
            self.render_massive_sampling_on()
       
        if self.treatment_combobox.get() == "On":
            self.render_treatment_on()

        if self.model_combobox.get() == "SEIR":
            self.render_seir()
        


    def render_seir(self):
        entries = ["Latency Probability", "E->I", "I->E", "E->R"]
        for entry_text in entries:
            label = ttk.Label(self.control_frame, text=entry_text)
            label.pack()
            entry = ttk.Entry(self.control_frame, foreground="White")
            entry.pack()
            
            self.dynamic_widgets.extend([label, entry])

    def render_massive_sampling_on(self):
        entries = ["Generation", "Sample Probability", "Recovery Probability Afterwards"]
        for entry_text in entries:
            label = ttk.Label(self.control_frame, text=entry_text)
            label.pack()
            entry = ttk.Entry(self.control_frame, foreground="White")
            entry.pack()
            
            self.dynamic_widgets.extend([label, entry])

    def render_treatment_on(self):
        entries = ["Number of Epochs", "Start", "End"]
        for entry_text in entries:
            label = ttk.Label(self.control_frame, text=entry_text)
            label.pack()
            entry = ttk.Entry(self.control_frame, foreground="White")
            entry.pack()
            
            self.dynamic_widgets.extend([label, entry])