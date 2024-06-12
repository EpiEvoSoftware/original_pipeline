import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from utils import load_config_as_dict
import json
import networkx as nx
import os
from network_generator import run_network_generation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class NetworkModel:
    def __init__(
        self,
        parent,
        tab_parent,
        network_graph_app,
        config_path,
        tab_title,
        tab_index,
        hide=False,
    ):
        self.top_frame = ttk.Frame(parent, width=200)
        self.bottom_frame = ttk.Frame(parent)

        self.top_frame.pack(side="right", fill="y", expand=False)
        self.bottom_frame.pack(side="left", fill="both", expand=True)

        
        self.graph = NetworkModelGraph(
            self.bottom_frame,
            tab_parent,
            network_graph_app,
            config_path,
        )
        self.sidebar = NetworkModelConfigurations(
            self.top_frame, tab_parent, config_path, self.graph, tab_index, tab_title
        )

        self.tab_title = tab_title
        self.config_path = config_path
        self.tab_parent = tab_parent
        self.tab_parent.add(parent, text=tab_title)
        self.parent = parent
        if hide:
            self.tab_parent.tab(tab_index, state="disabled")

    def update_graph(self, graph):
        self.graph.update_graph(graph)

class NetworkModelConfigurations:
    def __init__(
        self, parent, tab_parent, config_path, graph, tab_index, tab_title, hide=False
    ):
        self.config_path = config_path
        self.config = load_config_as_dict(self.config_path)
        self.control_frame = ttk.Frame(parent, width=300)
        self.control_frame.pack(padx=10, pady=(0, 10))
        self.tab_parent = tab_parent
        self.tab_index = tab_index
        self.graph = graph

        self.derender_group_use_network_model = set()
        self.derender_group_network_method = set()
        self.derender_group_network_model = set()
        self.update_config_entries = {}

        self.render_initial()
        self.render_next_button()

    def derender(self, widget_set):
        for widget in widget_set:
            widget.pack_forget()
        widget_set.clear()

    def render_initial(self):
        self.render_host_size()
        self.render_use_network_model()

    def render_host_size(self):
        host_size_label = tk.ttk.Label(self.control_frame, text="Host Size", style="Bold.TLabel")
        host_size_entry = tk.ttk.Entry(self.control_frame, foreground="black")
        host_size_entry.insert(0, str(self.config["NetworkModelParameters"]["host_size"]))
        self.update_config_entries["host_size"] = host_size_entry

        host_size_label.pack()
        host_size_entry.pack(pady=(0, 10))

    def render_use_network_model(self):
        def update():
            self.config["NetworkModelParameters"]["use_network_model"] = use_network_model_var.get()
            with open(self.config_path, "w") as file:
                json.dump(self.config, file, indent=4)

            if use_network_model_var.get():
                self.render_method()
            else:
                self.derender(self.derender_group_use_network_model)


        use_network_model_var = tk.BooleanVar(value=self.config["NetworkModelParameters"]["use_network_model"])
        use_network_model_label = tk.ttk.Label(self.control_frame, text="Use Network Model", style="Bold.TLabel")
        use_network_model_rb_true = tk.ttk.Radiobutton(
            self.control_frame,
            text="Yes",
            variable=use_network_model_var,
            value=True,
            command=update,
        )
        use_network_model_rb_false = tk.ttk.Radiobutton(
            self.control_frame,
            text="No",
            variable=use_network_model_var,
            value=False,
            command=update,
        )

        use_network_model_label.pack()
        use_network_model_rb_true.pack()
        use_network_model_rb_false.pack(pady=(0, 10))

        if use_network_model_var.get():
            self.render_method()
            

    def render_method(self):
        def update():
            self.config["NetworkModelParameters"]["method"] = network_method_var.get()
            with open(self.config_path, "w") as file:
                json.dump(self.config, file, indent=4)

            self.derender(self.derender_group_network_method)

            if network_method_var.get() == "user_input":
                self.render_select_file()
            elif network_method_var.get() == "randomly_generate":
                self.render_network_model()
            else:
                raise ValueError()

        network_method_var = tk.StringVar(value=self.config["NetworkModelParameters"]["method"])
        network_method_label = tk.ttk.Label(self.control_frame, text="Network Model Method", style="Bold.TLabel")
        network_method_rb_user = tk.ttk.Radiobutton(
            self.control_frame,
            text="User Input",
            variable=network_method_var,
            value="user_input",
            command=update,
        )
        network_method_rb_random = tk.ttk.Radiobutton(
            self.control_frame,
            text="Random Generation",
            variable=network_method_var,
            value="randomly_generate",
            command=update,
        )

        network_method_label.pack()
        network_method_rb_user.pack()
        network_method_rb_random.pack(pady=(0, 10))

        self.derender_group_use_network_model.update([network_method_label, network_method_rb_user, network_method_rb_random])

        if network_method_var.get() == "user_input":
            self.render_select_file()
        elif network_method_var.get() == "randomly_generate":
            self.render_network_model()

    def render_select_file(self):
        def choose_file():
            chosen_file = filedialog.askopenfilename(title="Select a File")

            if chosen_file:
                self.config["NetworkModelParameters"]["user_input"]["path_network"] = chosen_file
                with open(self.config_path, "w") as file:
                    json.dump(self.config, file, indent=4)
                
                file_value_label.config(text=chosen_file)
                
        file = self.config["NetworkModelParameters"]["user_input"]["path_network"]
        file_label = tk.ttk.Label(self.control_frame, text="Custom Network File", style="Bold.TLabel")

        if file == "":
            file_value_label = tk.ttk.Label(
                self.control_frame, text="No file selected", foreground="black"
            )
        else:
            file_value_label = tk.ttk.Label(
                self.control_frame, text=file, foreground="black"
            )

        file_button = tk.Button(self.control_frame, text="Choose File", command=choose_file)

        file_label.pack()
        file_value_label.pack()
        file_button.pack(pady=(0, 10))

        self.derender_group_use_network_model.update([file_label, file_value_label, file_button])
        self.derender_group_network_method.update([file_label, file_value_label, file_button])


    def render_network_model(self):
        def update(event):
            self.config["NetworkModelParameters"]["randomly_generate"]["network_model"] = network_model_var.get()
            with open(self.config_path, "w") as file:
                json.dump(self.config, file, indent=4)

            self.derender(self.derender_group_network_model)
            match network_model_var.get():
                case "ER":
                    self.render_ER()
                case "RP":
                    self.render_RP()
                case "BA":
                    self.render_BA()

        network_model_var = tk.StringVar(value=self.config["NetworkModelParameters"]["randomly_generate"]["network_model"])
        network_model_label = tk.ttk.Label(self.control_frame, text="Network Model", style="Bold.TLabel")
        network_model_combobox = ttk.Combobox(
            self.control_frame,
            textvariable=network_model_var,
            values=["ER", "RP", "BA"],
            state="readonly",
            width=20,
        )
        network_model_combobox.bind("<<ComboboxSelected>>", update)

        network_model_label.pack()
        network_model_combobox.pack(pady=(0, 10))

        self.derender_group_use_network_model.update([network_model_label, network_model_combobox])
        self.derender_group_network_method.update([network_model_label, network_model_combobox])

        match network_model_var.get():
            case "ER":
                self.render_ER()
            case "RP":
                self.render_RP()
            case "BA":
                self.render_BA()
    
    def render_ER(self):
        p_ER_label = tk.ttk.Label(self.control_frame, text="ER probability parameter", style="Bold.TLabel")
        p_ER_entry = tk.ttk.Entry(self.control_frame, foreground="black")
        p_ER_entry.insert(0, str(self.config["NetworkModelParameters"]["randomly_generate"]["ER"]["p_ER"]))
        self.update_config_entries["p_ER"] = p_ER_entry

        p_ER_label.pack()
        p_ER_entry.pack()

        self.derender_group_use_network_model.update([p_ER_label, p_ER_entry])
        self.derender_group_network_method.update([p_ER_label, p_ER_entry])
        self.derender_group_network_model.update([p_ER_label, p_ER_entry])

        self.render_run_network_generation()

    def render_RP(self):
        rp_size_label = tk.ttk.Label(self.control_frame, text="RP partition sizes", style="Bold.TLabel")
        rp_size_entry = tk.ttk.Entry(self.control_frame, foreground="black")
        rp_size_entry.insert(0, str(self.config["NetworkModelParameters"]["randomly_generate"]["RP"]["rp_size"]))
        self.update_config_entries["rp_size"] = rp_size_entry

        p_within_label = tk.ttk.Label(self.control_frame, text="RP within-probabilities", style="Bold.TLabel")
        p_within_entry = tk.ttk.Entry(self.control_frame, foreground="black")
        p_within_entry.insert(0, str(self.config["NetworkModelParameters"]["randomly_generate"]["RP"]["p_within"]))
        self.update_config_entries["p_within"] = p_within_entry

        p_between_label = tk.ttk.Label(self.control_frame, text="RP between-probability", style="Bold.TLabel")
        p_between_entry = tk.ttk.Entry(self.control_frame, foreground="black")
        p_between_entry.insert(0, str(self.config["NetworkModelParameters"]["randomly_generate"]["RP"]["p_between"]))
        self.update_config_entries["p_between"] = p_between_entry

        rp_size_label.pack()
        rp_size_entry.pack()
        p_within_label.pack()
        p_within_entry.pack()
        p_between_label.pack()
        p_between_entry.pack()

        self.derender_group_use_network_model.update([rp_size_label, rp_size_entry, p_within_label, p_within_entry, p_between_label, p_between_entry])
        self.derender_group_network_method.update([rp_size_label, rp_size_entry, p_within_label, p_within_entry, p_between_label, p_between_entry])
        self.derender_group_network_model.update([rp_size_label, rp_size_entry, p_within_label, p_within_entry, p_between_label, p_between_entry])

        self.render_run_network_generation()

    def render_BA(self):
        ba_m_label = tk.ttk.Label(self.control_frame, text="BA m parameter", style="Bold.TLabel")
        ba_m_entry = tk.ttk.Entry(self.control_frame, foreground="black")
        ba_m_entry.insert(0, str(self.config["NetworkModelParameters"]["randomly_generate"]["BA"]["ba_m"]))
        self.update_config_entries["ba_m"] = ba_m_entry

        ba_m_label.pack()
        ba_m_entry.pack()

        self.derender_group_use_network_model.update([ba_m_label, ba_m_entry])
        self.derender_group_network_method.update([ba_m_label, ba_m_entry])
        self.derender_group_network_model.update([ba_m_label, ba_m_entry])

        self.render_run_network_generation()

    def render_run_network_generation(self):
        def run_network_generate():
            if not self.update_config():
                return

            try:
                pop_size = self.config["NetworkModelParameters"]["host_size"]
                wk_dir = self.config["BasicRunConfiguration"]["cwdir"]
                network_model = self.config["NetworkModelParameters"]["randomly_generate"]["network_model"]
                rand_seed = self.config["BasicRunConfiguration"]["random_number_seed"]

                if network_model == "ER":
                    p_ER = self.config["NetworkModelParameters"]["randomly_generate"]["ER"]["p_ER"]
                    network, error = run_network_generation(
                        pop_size=pop_size,
                        wk_dir=wk_dir,
                        method="randomly_generate",
                        model="ER",
                        p_ER=p_ER,
                        rand_seed=rand_seed
                    )
                elif network_model == "BA":
                    m = self.config["NetworkModelParameters"]["randomly_generate"]["BA"]["ba_m"]
                    network, error = run_network_generation(
                        pop_size=pop_size,
                        wk_dir=wk_dir,
                        method="randomly_generate",
                        model="BA",
                        m=m,
                        rand_seed=rand_seed
                    )
                elif network_model == "RP":
                    rp_size = self.config["NetworkModelParameters"]["randomly_generate"]["RP"]["rp_size"]
                    p_within = self.config["NetworkModelParameters"]["randomly_generate"]["RP"]["p_within"]
                    p_between = self.config["NetworkModelParameters"]["randomly_generate"]["RP"]["p_between"]
                    network, error = run_network_generation(
                        pop_size=pop_size,
                        wk_dir=wk_dir,
                        method="randomly_generate",
                        model="RP",
                        rp_size=rp_size,
                        p_within=p_within,
                        p_between=p_between,
                        rand_seed=rand_seed
                    )
                else:
                    raise ValueError("Unsupported model.")

                if error is not None:
                    messagebox.showerror("Network Generation Error", str(error))
                else:
                    messagebox.showinfo("Success", "Network Generated successfully!")

                G = nx.read_adjlist(os.path.join(wk_dir, "contact_network.adjlist"))
                degrees = [G.degree(n) for n in G.nodes()]
                self.graph.plot_degree_distribution(degrees)

            except Exception as e:
                messagebox.showerror("Network Generation Error", str(e))

        run_network_generate_button = tk.Button(
            self.control_frame,
            text="Run Network Generation",
            command=run_network_generate,
        )
        run_network_generate_button.pack(pady=10)
        self.derender_group_use_network_model.add(run_network_generate_button)
        self.derender_group_network_method.add(run_network_generate_button)
        self.derender_group_network_model.add(run_network_generate_button)

    def render_next_button(self):
        def next_tab():
            if not self.update_config():
                return
            next_tab_index = (self.tab_index + 1) % self.tab_parent.index("end")
            self.tab_parent.tab(next_tab_index, state="normal")
            self.tab_parent.select(next_tab_index)
        next_button = tk.ttk.Button(self.control_frame, text="Next", command=next_tab)
        next_button.pack(side="bottom", pady=10)

    def update_config(self):
        try:
            host_size = int(self.update_config_entries["host_size"].get())
            self.config["NetworkModelParameters"]["host_size"] = host_size
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid int for Host Size.")
            return False
        if host_size == 0:
            messagebox.showerror("Warning", "Warning: Your host size is currently 0.")
        
        match self.config["NetworkModelParameters"]["randomly_generate"]["network_model"]:
            case "ER":
                try:
                    p_ER = float(self.update_config_entries["p_ER"].get())
                    assert(0 < p_ER <= 1)
                    self.config["NetworkModelParameters"]["randomly_generate"]["ER"]["p_ER"] = p_ER
                except (AssertionError, ValueError):
                    messagebox.showerror("Error", "Please enter a valid float for ER probability parameter. (0 < p_ER <= 1)")
                    return False
                
            case "RP":
                try:
                    rp_size = json.loads(self.update_config_entries["rp_size"].get())
                    rp_size[0] = int(rp_size[0])
                    rp_size[1] = int(rp_size[1])
                    assert(len(rp_size) == 2)
                    self.config["NetworkModelParameters"]["randomly_generate"]["RP"]["rp_size"] = rp_size
                except (AssertionError, ValueError):
                    messagebox.showerror("Error", "Please enter a valid list of two ints for partition sizes.")
                    return False
                
                try:
                    p_within = json.loads(self.update_config_entries["p_within"].get())
                    p_within[0] = float(p_within[0])
                    p_within[1] = float(p_within[1])
                    assert(len(rp_size) == 2)
                    self.config["NetworkModelParameters"]["randomly_generate"]["RP"]["p_within"] = p_within
                except (AssertionError, ValueError):
                    messagebox.showerror("Error", "Please enter a valid list of two floats for within-probabilities.")
                    return False
                
                try:
                    p_between = float(self.update_config_entries["p_between"].get())
                    self.config["NetworkModelParameters"]["randomly_generate"]["RP"]["p_between"] = p_between
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid float for between-probability.")
                    return False
                
            case "BA":
                try:
                    ba_m = int(self.update_config_entries["ba_m"].get())
                    self.config["NetworkModelParameters"]["randomly_generate"]["BA"]["ba_m"] = ba_m
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid integer for BA m parameter.")
                    return False

        with open(self.config_path, "w") as file:
            json.dump(self.config, file, indent=4)
        
        return True
    
class NetworkModelGraph:
    def __init__(
        self, parent, tab_parent, network_graph_app, config_path
    ):
        self.parent = parent
        self.tab_parent = tab_parent
        self.network_graph_app = network_graph_app

        self.config = load_config_as_dict(config_path)
        self.wk_dir = self.config["BasicRunConfiguration"]["cwdir"]
        self.network_file_path = os.path.join(self.wk_dir, "contact_network.adjlist")

        self.create_graph_frame()

    def create_graph_frame(self):
        self.graph_frame = ttk.Frame(self.parent)
        self.graph_frame.pack(fill="both", expand=True)
        self.plot_degree_distribution([])

    def update_graph(self, graph):
        self.network_graph_app = graph
        self.network_graph_app.plot_degree_distribution()

    def plot_degree_distribution(self, degrees):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
        if degrees:
            bin_size = max(1, int((max(degrees)-min(degrees))/30))
            ax.hist(
                degrees,
                bins=np.arange(min(degrees)-bin_size-0.5, max(degrees)+bin_size+0.5, bin_size),
                edgecolor="black",
            )
        elif os.path.exists(self.network_file_path) and self.wk_dir != "":
            G = nx.read_adjlist(self.network_file_path)
            degrees = [G.degree(n) for n in G.nodes()]
            bin_size = max(1, int((max(degrees)-min(degrees))/30))
            ax.hist(
                degrees,
                bins=np.arange(min(degrees)-bin_size-0.5, max(degrees)+bin_size+0.5, bin_size),
                edgecolor="black",
            )

        else:
            ax.hist([], bins=[])
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 1)
        ax.set_title("Degree Distribution")
        ax.set_xlabel("Degree")
        ax.set_ylabel("Number of Nodes")

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        if self.network_graph_app is not None:
            self.network_graph_app.plot_degree_distribution()
