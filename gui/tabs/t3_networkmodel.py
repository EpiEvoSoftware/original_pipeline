import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import sys
import os
from utils import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from network_generator import *


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

        self.tab_title = tab_title
        self.config_path = config_path
        self.graph = NetworkModelGraph(
            self.bottom_frame,
            tab_parent,
            network_graph_app,
            config_path,
            tab_index,
            tab_title,
        )
        self.sidebar = NetworkModelConfigurations(
            self.top_frame, tab_parent, config_path, self.graph, tab_index, tab_title
        )
        self.tab_parent = tab_parent
        self.tab_parent.add(parent, text=tab_title)
        self.parent = parent
        if hide:
            self.tab_parent.tab(tab_index, state="disabled")
        # self.tab_index = tab_index

    def update_graph(self, graph):
        self.graph.update_graph(graph)


class NetworkModelConfigurations(TabBase):
    def __init__(
        self, parent, tab_parent, config_path, graph, tab_index, tab_title, hide=False
    ):
        self.graph = graph
        super().__init__(parent, tab_parent, config_path, tab_title, tab_index, hide)

    def render_host_size(self, hide, column, columnspan, frow):
        text = "Host Size:"
        keys_path = ["NetworkModelParameters", "host_size"]
        column, frow, hide, columnspan = 0, 0, False, 1
        component = EasyEntry(
            keys_path,
            self.config_path,
            text,
            "host_size",
            self.control_frame,
            column,
            frow,
            "integer",
            hide,
            columnspan,
        )
        if not hide:
            self.visible_components.add(component)

    def render_use_network_model(
        self, to_rerender, to_derender, hide=True, column=None, frow=None, columnspan=1
    ):
        text = "Use Network Model"
        keys_path = ["NetworkModelParameters", "use_network_model"]

        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)
            if var.get():
                self.global_group_control.rerender_itself()
            else:
                self.global_group_control.derender_itself()

        component = EasyRadioButton(
            keys_path,
            self.config_path,
            text,
            "use_network_model",
            self.control_frame,
            column,
            frow,
            hide,
            to_rerender,
            to_derender,
            columnspan,
            radiobuttonselected,
        )

        if not hide:
            self.visible_components.add(component)
        return component

    def render_path_network(self, hide=True, column=None, frow=None, columnspan=1):
        text = "Path Network:"
        keys_path = ["NetworkModelParameters", "user_input", "path_network"]
        component = EasyPathSelector(
            keys_path,
            self.config_path,
            text,
            self.control_frame,
            column,
            hide,
            frow,
            columnspan,
        )

        self.visible_components.add(component)
        return component

    def init_landing_group(self, hide):
        to_rerender, to_derender = None, None
        self.render_host_size(hide, 0, 1, self.increment_frow(increment=True))
        self.network_model_component = self.render_use_network_model(
            to_rerender,
            to_derender,
            hide,
            0,
            self.increment_frow(increment=True, by=4),
            1,
        )

    def init_method_group(self, hide):
        to_rerender, to_derender = None, None
        method = self.render_method(1, 0, 10, to_rerender, to_derender, hide, 20)
        print(method)
        self.frow = 10
        method_group_control = [method]

        self.method_group_control = GroupControls()
        for control in method_group_control:
            self.method_group_control.add(control)
        self.global_group_control.add(self.method_group_control)

    def init_path_network_group(self, hide):
        to_rerender, to_derender = None, None
        method = self.render_path_network(hide, 0, self.increment_frow(), 1)
        group_control = [method]

        self.method_path_network_group_control = GroupControls()
        for control in group_control:
            self.method_path_network_group_control.add(control)
        self.global_group_control.add(self.method_path_network_group_control)

    def render_method(
        self,
        columnspan,
        column,
        frow,
        to_rerender=None,
        to_derender=None,
        hide=True,
        width=20,
    ):
        """
        generate_genetic_architecture_method
        self.generate_genetic_architecture_method = ['GenomeElement']['effect_size']['method']
        """

        def comboboxselected(var, to_rerender, to_derender):
            match var.get():
                case "user_input":
                    pass
                    # self.generate_genetic_architecture_method.set_to_rerender(
                    #     self.user_input_group_control.rerender_itself
                    # )
                    # self.generate_genetic_architecture_method.set_to_derender(
                    #     self.random_generate_group_control.derender_itself
                    # )
                case "randomly_generate":
                    pass
                    # self.generate_genetic_architecture_method.set_to_rerender(
                    #     self.random_generate_group_control.rerender_itself
                    # )
                    # self.generate_genetic_architecture_method.set_to_derender(
                    #     self.user_input_group_control.derender_itself
                    # )
                case _:
                    raise ValueError("Invalid method specified")
            to_rerender()
            to_derender()

        text = "Method"
        keys_path = ["user_input", "randomly generate"]
        component = EasyCombobox(
            keys_path,
            self.config_path,
            text,
            self.control_frame,
            column,
            frow,
            keys_path,
            to_rerender,
            to_derender,
            comboboxselected,
            hide,
            width,
            columnspan,
            None,
            True,
        )
        if not hide:
            self.visible_components.add(component)

        return component

    def load_page(self):
        self.global_group_control = GroupControls()
        self.init_landing_group(hide=False)
        self.init_method_group(hide=False)
        self.init_path_network_group(hide=False)
        pass
        # self.init_val(config_path)
        # self.parent = parent
        # self.tab_parent = tab_parent
        #
        # self.control_frame = ttk.Frame(self.parent, width=300)
        # self.control_frame.pack(fill="both", expand=True)

        # host_size_label = load_config_as_dict(self.config_path)['NetworkModelParameters']['host_size']
        # self.host_size_label = ttk.Label(self.control_frame, text="host_size:")
        # self.host_size_label.grid()
        # self.host_size_entry = ttk.Entry(self.control_frame, foreground="black")
        # self.host_size_entry.insert(0, self.host_size)
        # self.host_size_entry.grid()

        # self.visible_components.add(component)
        # return component
        # update_host_size_button = tk.Button(
        #     self.control_frame,
        #     text="Update host_size",
        #     command=self.update_host_size,
        # )
        # update_host_size_button.grid()

        # self.use_network_model = load_config_as_dict(self.config_path)['NetworkModelParameters']['use_network_model']

        # render_next_button(self.tab_index, self.tab_parent, self.parent, lambda: 0)

    def update(self):
        error_messages = []
        self.update_n_replicates(error_messages)
        if len(error_messages) == 0:
            messagebox.showinfo("Update Successful", "Parameters Updated.")
            return 0
        else:
            error_message_str = "\n".join(error_messages)
            messagebox.showerror("Update Error", error_message_str)

    def update_host_size(self):
        try:
            new_host_size = int(float(self.host_size_entry.get()))
            config = load_config_as_dict(self.config_path)
            config["NetworkModelParameters"]["host_size"] = new_host_size
            save_config(self.config_path, config)
            messagebox.showinfo("Update Successful", "host_size changed.")
        except ValueError:
            messagebox.showerror(
                "Update Error", "Please enter a valid integer for host_size."
            )

    def update_mut_rate(self):
        try:
            new_mut_rate = int(float(self.mut_rate_entry.get()))
            config = load_config_as_dict(self.config_path)
            config["EvolutionModel"]["mut_rate"] = new_mut_rate
            save_config(self.config_path, config)
            messagebox.showinfo("Update Successful", "mut_rate changed.")
        except ValueError:
            messagebox.showerror(
                "Update Error", "Please enter a valid integer for mut_rate."
            )

    def update_cap_withinhost(self):
        try:
            new_cap_withinhost = int(float(self.cap_withinhost_entry.get()))
            config = load_config_as_dict(self.config_path)
            config["EvolutionModel"]["cap_withinhost"] = new_cap_withinhost
            save_config(self.config_path, config)
            messagebox.showinfo("Update Successful", "cap_withinhost changed.")
        except ValueError:
            messagebox.showerror(
                "Update Error", "Please enter a valid integer for cap_withinhost."
            )

    def update_within_host_reproduction_rate(self):
        try:
            new_within_host_reproduction_rate = int(
                float(self.within_host_reproduction_rate_entry.get())
            )
            config = load_config_as_dict(self.config_path)
            config["EvolutionModel"]["within_host_reproduction_rate"] = (
                new_within_host_reproduction_rate
            )
            save_config(self.config_path, config)
            messagebox.showinfo(
                "Update Successful", "within_host_reproduction_rate changed."
            )
        except ValueError:
            messagebox.showerror(
                "Update Error",
                "Please enter a valid integer for within_host_reproduction_rate.",
            )

    def choose_network_path(self):
        chosen_path = filedialog.askdirectory(title="Select a Directory")
        if chosen_path:
            self.network_path = chosen_path
            self.network_path_label = ttk.Label(
                self.control_frame, text="Current Network Path: " + self.network_path
            )
            self.network_path_label.grid()
            self.network_path_label.config(text=f"Path Network: {self.network_path}")
            config = load_config_as_dict(self.config_path)
            config["NetworkModelParameters"]["user_input"]["path_network"] = (
                self.network_path
            )
            save_config(self.config_path, config)

    def update_use_network_model(self):
        self.hide_elements_update_methods()
        new_use_network_model = self.use_network_model_var.get()
        if new_use_network_model in ["Yes", "No"]:
            config = load_config_as_dict(self.config_path)
            config["NetworkModelParameters"]["use_network_model"] = (
                string_to_bool_mapping[new_use_network_model]
            )
            save_config(self.config_path, config)

            # break
            if new_use_network_model == "Yes":
                if not hasattr(
                    self, "method_label"
                ):  # create the label if it doesn't exist
                    # break
                    self.method_label = ttk.Label(self.control_frame, text="method:")
                    self.method_label.grid()
                    self.method_var = tk.StringVar()
                    self.method_combobox = ttk.Combobox(
                        self.control_frame,
                        textvariable=self.method_var,
                        values=["user_input", "randomly generate"],
                        state="readonly",
                    )
                    self.method_combobox.grid()
                    self.update_method_button = tk.Button(
                        self.control_frame,
                        text="Update method",
                        command=self.update_method,
                    )
                    self.update_method_button.grid()
                    # break
                else:
                    # break, show the label if it was previously created
                    self.method_label.grid()
                    self.method_combobox.grid()
                    self.update_method_button.grid()
                    # break
            elif new_use_network_model == "No":
                self.hide_elements_update_methods()
                if hasattr(self, "method_label"):
                    self.method_label.pack_forget()
                    self.method_combobox.pack_forget()
                    self.update_method_button.pack_forget()

            # break
            messagebox.showinfo("Update Successful", "use_network_model changed.")
        else:
            messagebox.showerror(
                "Update Error", "Please enter 'Yes' or 'No' for use_network_model."
            )

    def update_method(self):
        new_method = self.method_var.get().strip().lower()  # Normalize input
        if new_method in [
            "user_input",
            "randomly generate",
        ]:  # TODO: change to dropdown
            messagebox.showinfo("Update Successful", "method changed to " + new_method)
            # add conditional logic for path network and network_model
            if new_method == "user_input":
                self.hide_elements_update_methods()
                if not hasattr(self, "path_network_label"):
                    # create the label if it doesn't exist
                    self.path_network_label = ttk.Label(
                        self.control_frame, text="Choose path_network"
                    )
                    self.path_network_label.grid()
                    self.choose_path_network_button = tk.Button(
                        self.control_frame,
                        text="path_network:",
                        command=self.choose_network_path,
                    )
                    self.choose_path_network_button.grid()
                    self.chosen_path_network_label = ttk.Label(
                        self.control_frame,
                        text="Current path_network: " + self.path_network,
                    )
                    self.chosen_path_network_label.grid()

                else:
                    # break, show the label if it was previously created
                    self.path_network_label.grid()
                    self.choose_path_network_button.grid()
                    self.chosen_path_network_label.grid()

            elif new_method == "randomly generate":
                self.hide_elements_update_methods()

                if not hasattr(self, "network_model_label"):
                    # self.network_model = load_config_as_dict(self.config_path)['NetworkModelParameters']['randomly_generate']["network_model"]
                    self.network_model_label = ttk.Label(
                        self.control_frame, text="network_model:"
                    )
                    self.network_model_label.grid()
                    self.network_model_var = tk.StringVar(
                        value=self.string_to_network_mode.get(self.network_model, "")
                    )
                    self.network_model_combobox = ttk.Combobox(
                        self.control_frame,
                        textvariable=self.network_model_var,
                        values=self.graph_values,
                        state="readonly",
                    )
                    self.network_model_combobox.grid()
                    self.update_method_button = tk.Button(
                        self.control_frame,
                        text="Update network_model",
                        command=self.update_network_model,
                    )
                    self.update_method_button.grid()
                else:
                    self.network_model_label.grid()
                    self.network_model_combobox.grid()
                    self.update_method_button.grid()

        else:
            messagebox.showerror(
                "Update Error",
                "Please enter 'user_input' or 'randomly generate' for method.",
            )

    def update_network_model(self):
        # self.network_model = load_config_as_dict(self.config_path)['NetworkModelParameters']['randomly_generate']["network_model"]
        new_network_model_unconverted = self.network_model_var.get()
        new_network_model = self.network_model_to_string[self.network_model_var.get()]
        if new_network_model in ["ER", "RP", "BA"]:
            config = load_config_as_dict(self.config_path)
            config["NetworkModelParameters"]["randomly_generate"]["network_model"] = (
                new_network_model
            )
            save_config(self.config_path, config)

            self.hide_elements_network_values()
            if new_network_model == "ER":
                # self.p_ER = load_config_as_dict(self.config_path)['NetworkModelParameters']['randomly_generate']['ER']['p_ER']
                if not hasattr(self, "p_ER_label"):

                    def update_ER():
                        """
                        Updates the self.p_ER value in the params file
                        """
                        try:
                            p_ER_value = float(self.p_ER_entry.get())
                            config = load_config_as_dict(self.config_path)
                            config["NetworkModelParameters"]["randomly_generate"]["ER"][
                                "p_ER"
                            ] = p_ER_value
                            save_config(self.config_path, config)
                            messagebox.showinfo("Update Successful", "p_ER changed")
                        except ValueError:
                            messagebox.showerror(
                                "Update Error",
                                "Please enter a valid float for host_size.",
                            )

                    self.p_ER_label = ttk.Label(self.control_frame, text="p_ER:")
                    self.p_ER_label.grid()
                    self.p_ER_entry = ttk.Entry(self.control_frame, foreground="black")
                    self.p_ER_entry.insert(0, self.p_ER)
                    self.p_ER_entry.grid()
                    # self.update_ER_button = tk.Button(self.control_frame, text="Update p_ER", command=self.update_ER)
                    self.update_ER_button = tk.Button(
                        self.control_frame, text="Update p_ER", command=update_ER
                    )
                    self.update_ER_button.grid()
                else:
                    self.p_ER_label.grid()
                    self.p_ER_entry.grid()
                    self.update_ER_button.grid()

            elif new_network_model == "RP":
                # self.rp_size = load_config_as_dict(self.config_path)['NetworkModelParameters']['randomly_generate']['RP']['rp_size']
                # int int
                # self.p_within = load_config_as_dict(self.config_path)['NetworkModelParameters']['randomly_generate']['RP']['p_within']
                # float float
                # self.p_between = load_config_as_dict(self.config_path)['NetworkModelParameters']['randomly_generate']['RP']['p_between']
                # int

                if not hasattr(self, "RP"):

                    def update_all_RP():
                        """
                        Updates the self.rp_size value in the params file
                        """
                        try:
                            rp_size_value = int(float(self.rp_size_entry.get()))
                            rp_size_value_2 = int(float(self.rp_size_entry_2.get()))
                            p_within_value = float(self.p_within_entry.get())
                            p_within_value_2 = float(self.p_within_entry_2.get())
                            p_between_value = float(self.p_between_entry.get())

                            config = load_config_as_dict(self.config_path)
                            config["NetworkModelParameters"]["randomly_generate"]["RP"][
                                "rp_size"
                            ] = [rp_size_value, rp_size_value_2]
                            config["NetworkModelParameters"]["randomly_generate"]["RP"][
                                "p_within"
                            ] = [p_within_value, p_within_value_2]
                            config["NetworkModelParameters"]["randomly_generate"]["RP"][
                                "p_between"
                            ] = p_between_value
                            save_config(self.config_path, config)
                            message = (
                                "RP Parameters changed.\n\n"
                                + "rp_size: "
                                + str([rp_size_value, rp_size_value_2])
                                + "\n"
                            )
                            message2 = (
                                "p_within: "
                                + str([p_within_value, p_within_value_2])
                                + "\n"
                            )
                            message3 = "p_between_value: " + str(p_between_value)
                            messagebox.showinfo(
                                "Update Successful", message + message2 + message3
                            )
                        except ValueError:
                            messagebox.showerror("Update Error", "Invalid Input.")

                    self.rp_size_label = ttk.Label(self.control_frame, text="rp_size:")
                    self.rp_size_label.grid()
                    self.rp_size_entry = ttk.Entry(
                        self.control_frame, foreground="black"
                    )
                    self.rp_size_entry.insert(0, self.rp_size[0])
                    self.rp_size_entry_2 = ttk.Entry(
                        self.control_frame, foreground="black"
                    )
                    self.rp_size_entry_2.insert(0, self.rp_size[1])
                    self.rp_size_entry.grid()
                    self.rp_size_entry_2.grid()

                    self.p_within_label = ttk.Label(
                        self.control_frame, text="p_within:"
                    )
                    self.p_within_label.grid()
                    self.p_within_entry = ttk.Entry(
                        self.control_frame, foreground="black"
                    )
                    self.p_within_entry.insert(0, self.p_within[0])
                    self.p_within_entry_2 = ttk.Entry(
                        self.control_frame, foreground="black"
                    )
                    self.p_within_entry_2.insert(0, self.p_within[1])
                    self.p_within_entry.grid()
                    self.p_within_entry_2.grid()

                    self.p_between_label = ttk.Label(
                        self.control_frame, text="p_between:"
                    )
                    self.p_between_label.grid()
                    self.p_between_entry = ttk.Entry(
                        self.control_frame, foreground="black"
                    )
                    self.p_between_entry.insert(0, self.p_between)
                    self.p_between_entry.grid()

                    # self.update_ER_button = tk.Button(self.control_frame, text="Update rp_size", command=self.update_ER)
                    self.update_ER_button = tk.Button(
                        self.control_frame,
                        text="Update All RP parameters",
                        command=update_all_RP,
                    )
                    self.update_ER_button.grid()

                else:
                    self.rp_size_label.grid()
                    self.rp_size_entry.grid()
                    self.p_within_label
                    self.p_within_entry.grid()
                    self.p_within_entry_2.grid()
                    self.p_between_label
                    self.p_between_entry.grid()
                    self.update_ER_button.grid()

            elif new_network_model == "BA":
                if not hasattr(self, "ba_m_label"):
                    # self.ba_m = load_config_as_dict(self.config_path)['NetworkModelParameters']['randomly_generate']['BA']['ba_m']
                    def update_ba_m():
                        """
                        Updates the self.ba_m value in the params file
                        """
                        try:
                            ba_m_value = int(float(self.ba_m_entry.get()))
                            config = load_config_as_dict(self.config_path)
                            config["NetworkModelParameters"]["randomly_generate"]["BA"][
                                "ba_m"
                            ] = ba_m_value
                            save_config(self.config_path, config)
                            messagebox.showinfo("Update Successful", "ba_m changed")
                        except ValueError:
                            messagebox.showerror(
                                "Update Error",
                                "Please enter a valid int for host_size.",
                            )

                    self.ba_m_label = ttk.Label(self.control_frame, text="ba_m:")
                    self.ba_m_label.grid()
                    self.ba_m_entry = ttk.Entry(self.control_frame, foreground="black")
                    self.ba_m_entry.insert(0, self.ba_m)
                    self.ba_m_entry.grid()
                    # self.update_ER_button = tk.Button(self.control_frame, text="Update ba_m", command=self.update_ER)
                    self.update_ER_button = tk.Button(
                        self.control_frame, text="Update ba_m", command=update_ba_m
                    )
                    self.update_ER_button.grid()
                else:
                    self.ba_m_label.grid()
                    self.ba_m_entry.grid()
                    self.update_ER_button.grid()

            self.render_run_network_generation()
            messagebox.showinfo(
                "Update Successful",
                "network_model changed to " + new_network_model_unconverted + ".",
            )

        else:
            messagebox.showerror("Update Error", "Invalid Entry for network_model.")

    def render_run_network_generation(self):
        def run_network_generate():
            self.config_dict = load_config_as_dict(self.config_path)
            wk_dir = self.config_dict["BasicRunConfiguration"]["cwdir"]
            try:
                pop_size = self.config_dict["NetworkModelParameters"]["host_size"]
                graph_type = self.network_model_var.get()

                self.network_model = self.config_dict["NetworkModelParameters"][
                    "randomly_generate"
                ]["network_model"]

                if graph_type == "Erdős–Rényi":
                    p_ER = self.config_dict["NetworkModelParameters"][
                        "randomly_generate"
                    ]["ER"]["p_ER"]
                    network, error = run_network_generation(
                        pop_size=pop_size,
                        wk_dir=wk_dir,
                        method="randomly_generate",
                        model="ER",
                        p_ER=p_ER,
                    )
                elif graph_type == "Barabási-Albert":
                    m = self.config_dict["NetworkModelParameters"]["randomly_generate"][
                        "BA"
                    ]["ba_m"]
                    network, error = run_network_generation(
                        pop_size=pop_size,
                        wk_dir=wk_dir,
                        method="randomly_generate",
                        model="BA",
                        m=m,
                    )
                elif graph_type == "Random Partition":
                    rp_size = self.config_dict["NetworkModelParameters"][
                        "randomly_generate"
                    ]["RP"]["rp_size"]
                    p_within = self.config_dict["NetworkModelParameters"][
                        "randomly_generate"
                    ]["RP"]["p_within"]
                    p_between = self.config_dict["NetworkModelParameters"][
                        "randomly_generate"
                    ]["RP"]["p_between"]
                    network, error = run_network_generation(
                        pop_size=pop_size,
                        wk_dir=wk_dir,
                        method="randomly_generate",
                        model="RP",
                        rp_size=rp_size,
                        p_within=p_within,
                        p_between=p_between,
                    )
                else:
                    raise ValueError("Unsupported model.")

                if error is not None:
                    raise Exception(error)

                G = nx.read_adjlist(os.path.join(wk_dir, "contact_network.adjlist"))
                degrees = [G.degree(n) for n in G.nodes()]
                self.graph.plot_degree_distribution(degrees)

            except Exception as e:
                messagebox.showerror("Network Generation Error", str(e))

        if not hasattr(self, "run_network_generate_button"):
            self.run_network_generate_button = tk.Button(
                self.control_frame,
                text="run_network_generation",
                command=run_network_generate,
            )
            self.run_network_generate_button.grid()
        else:
            self.run_network_generate_button.grid()

        # if not hasattr(self, 'graph_frame'):
        #     self.graph_frame = ttk.Frame(self.control_frame)
        #     self.graph_frame.pack(fill='both', expand=True, after=self.control_frame)

        # def plot_degree_distribution(degrees):

        #     fig, ax = plt.subplots(figsize=(6, 4))
        #     ax.hist(degrees, bins=range(min(degrees), max(degrees) + 1, 1), edgecolor='black')
        #     ax.set_title("Degree Distribution")
        #     ax.set_xlabel("Degree")
        #     ax.set_ylabel("Number of Nodes")

        #     canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        #     canvas.draw()
        #     canvas_widget = canvas.get_tk_widget()
        #     canvas_widget.pack(fill=tk.BOTH, expand=True)

    def hide_elements_update_methods(self):
        self.hide_elements_network_values()
        if hasattr(self, "run_network_generate_button"):
            self.run_network_generate_button.pack_forget()
        if hasattr(self, "path_network_label"):
            # if new_method == "user_input":
            self.path_network_label.pack_forget()
            self.choose_path_network_button.pack_forget()
            self.path_network_label.pack_forget()
            self.chosen_path_network_label.pack_forget()
        if hasattr(self, "network_model_combobox"):
            # if new_method == "randomly generate":
            self.network_model_combobox.pack_forget()
            self.update_method_button.pack_forget()
            self.network_model_label.pack_forget()

    def hide_elements_network_values(self):
        if hasattr(self, "run_network_generate_button"):
            self.run_network_generate_button.pack_forget()
        if hasattr(self, "p_ER_label"):
            # if new_network_model == "ER":
            self.p_ER_label.pack_forget()
            self.p_ER_entry.pack_forget()
            self.update_ER_button.pack_forget()
        if hasattr(self, "rp_size_label"):
            # if new_network_model == "RP":
            self.rp_size_label.pack_forget()
            self.rp_size_entry.pack_forget()
            self.rp_size_entry_2.pack_forget()
            self.p_within_label.pack_forget()
            self.p_within_entry.pack_forget()
            self.p_within_entry_2.pack_forget()
            self.p_between_label.pack_forget()
            self.p_between_entry.pack_forget()
            self.update_ER_button.pack_forget()
        if hasattr(self, "ba_m_label"):
            # if new_network_model == "BA":
            self.ba_m_label.pack_forget()
            self.ba_m_entry.pack_forget()
            self.update_ER_button.pack_forget()

    def increment_frow(self, increment=True, by=2):
        if increment:
            self.frow += by
        return self.frow

    def init_val(
        self,
        config_path,
    ):
        self.frow = 1
        hide = False

        self.network_model_to_string = {
            "Erdős–Rényi": "ER",
            "Barabási-Albert": "BA",
            "Random Partition": "RP",
        }

        self.string_to_network_mode = {
            "ER": "Erdős–Rényi",
            "BA": "Barabási-Albert",
            "RP": "Random Partition",
        }

        self.graph_values = ["Erdős–Rényi", "Barabási-Albert", "Random Partition"]

        self.config_path = config_path
        # self.tab_index = tab_index

        # User Configurations
        self.config_dict = load_config_as_dict(self.config_path)
        self.use_network_model = self.config_dict["NetworkModelParameters"][
            "use_network_model"
        ]
        self.host_size = self.config_dict["NetworkModelParameters"]["host_size"]

        self.path_network = self.config_dict["NetworkModelParameters"]["user_input"][
            "path_network"
        ]

        self.network_model = self.config_dict["NetworkModelParameters"][
            "randomly_generate"
        ]["network_model"]

        self.p_ER = self.config_dict["NetworkModelParameters"]["randomly_generate"][
            "ER"
        ]["p_ER"]

        temp_rp_size = self.config_dict["NetworkModelParameters"]["randomly_generate"][
            "RP"
        ]["rp_size"]
        if len(temp_rp_size) == 0:
            self.rp_size = [0, 0]
        elif len(temp_rp_size) == 2:
            self.rp_size = temp_rp_size
        else:
            raise ValueError("Invalid rp_size value in the config file.")
        temp_p_within = self.config_dict["NetworkModelParameters"]["randomly_generate"][
            "RP"
        ]["p_within"]
        if len(temp_p_within) == 0:
            self.p_within = [0, 0]
        elif len(temp_p_within) == 2:
            self.p_within = temp_p_within
        else:
            raise ValueError("Invalid p_within value in the config file.")
        self.p_between = self.config_dict["NetworkModelParameters"][
            "randomly_generate"
        ]["RP"]["p_between"]

        self.ba_m = self.config_dict["NetworkModelParameters"]["randomly_generate"][
            "BA"
        ]["ba_m"]

    def init_tab(self, parent, tab_parent, tab_title, tab_index, hide):
        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_index = tab_index
        # self.tab_parent.add(parent, text=tab_title)
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")
        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(padx=10, pady=10)


class NetworkModelGraph:
    def __init__(
        self, parent, tab_parent, network_graph_app, config_path, tab_index, tab_title
    ):
        self.parent = parent
        self.tab_parent = tab_parent
        self.config_path = config_path
        self.network_graph_app = network_graph_app
        # self.tab_index = tab_index
        self.config_dict = load_config_as_dict(self.config_path)
        self.wk_dir = self.config_dict["BasicRunConfiguration"]["cwdir"]
        self.network_file_path = os.path.join(self.wk_dir, "contact_network.adjlist")

        self.create_graph_frame()

    def update_graph(self, graph):
        self.network_graph_app = graph
        self.network_graph_app.plot_degree_distribution()

    def create_graph_frame(self):
        self.graph_frame = ttk.Frame(self.parent)
        self.graph_frame.pack(fill="both", expand=True)
        self.plot_degree_distribution([])

    def plot_degree_distribution(self, degrees):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
        if degrees:
            ax.hist(
                degrees,
                bins=range(min(degrees), max(degrees) + 1, 1),
                edgecolor="black",
            )
        elif os.path.exists(self.network_file_path) and self.wk_dir != "":
            G = nx.read_adjlist(self.network_file_path)
            degrees = [G.degree(n) for n in G.nodes()]
            ax.hist(
                degrees,
                bins=range(min(degrees), max(degrees) + 1, 1),
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
