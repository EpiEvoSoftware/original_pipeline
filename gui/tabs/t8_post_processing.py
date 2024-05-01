import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import shutil
import sys
from utils import *

current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.join(os.path.dirname(current_dir), '../codes')
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


class PostProcessing(TabBase):
    def __init__(
        self, parent, tab_parent, config_path, tab_title, tab_index, hide=False
    ):
        super().__init__(parent, tab_parent, config_path, tab_title, tab_index, hide)

        # generate_config_file Button
        generate_config_file_button = tk.Button(
            self.parent,
            text="Generate the configuration file",
            command=self.generate_config_file,
        )
        generate_config_file_button.pack()

    def generate_config_file(self):
        source = self.config_path
        cwdir = load_config_as_dict(self.config_path)["BasicRunConfiguration"]["cwdir"]
        target = os.path.join(cwdir, "config_file.json")

        try:
            shutil.copy(source, target)
            tk.messagebox.showinfo("Success", "Config file saved successfully")
        except IOError as e:
            print("Unable to copy file. %s" % e)

    def load_page(self):
        hide = False
        self.global_group_control = GroupControls()
        self.render_do_postprocess(None, None, hide, 0, 1)
        self.render_branch_color_trait(hide, 0, 1, 4)
        self.render_drug_resistance_heatmap(None, None, hide, 0, 6)

    def render_do_postprocess(
        self, to_rerender, to_derender, hide=True, column=None, frow=None, columnspan=1
    ):
        to_rerender = None
        to_derender = None
        keys_path = self.do_postprocess_keys_path
        text = "Do you want to run post-processing (plotting trajectories & transmission trees) after the simulation?"

        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)

        component = EasyRadioButton(
            keys_path,
            self.config_path,
            text,
            "do_postprocess",
            self.control_frame,
            column,
            frow,
            hide,
            to_rerender,
            to_derender,
            columnspan,
            radiobuttonselected,
        )

        self.visible_components.add(component)
        return component

    def render_branch_color_trait(self, hide, column, columnspan, frow):
        text = "Which trait do you want to use for coloring the branches in the transmission tree plot (integer)"
        keys_path = self.branch_color_trait_keys_path
        component = EasyEntry(
            keys_path,
            self.config_path,
            text,
            "branch_color_trait",
            self.control_frame,
            column,
            frow,
            "integer",
            hide,
            columnspan,
        )

        self.visible_components.add(component)
        return component

    def render_branch_color_trait_dep(self):
        """
        self.branch_color_trait = load_config_as_dict(self.config_path)['Postprocessing_options']['tree_plotting']['branch_color_trait']
        """

        def update():
            try:
                prev_val = self.branch_color_trait
                self.branch_color_trait = int(
                    float(self.branch_color_trait_entry.get())
                )
                config = load_config_as_dict(self.config_path)
                keys_path = [
                    "Postprocessing_options",
                    "tree_plotting",
                    "branch_color_trait",
                ]
                update_nested_dict(config, keys_path, self.branch_color_trait)
                save_config(self.config_path, config)
                if prev_val != self.branch_color_trait:
                    messagebox.showinfo("Success", "Updated successfully")
            except ValueError:
                messagebox.showerror("Update Error", "Please enter a valid number.")
            except Exception as e:
                messagebox.showerror("Update Error", str(e))

        self.branch_color_trait_label = ttk.Label(
            self.control_frame, text="branch_color_trait:"
        ).grid()
        self.branch_color_trait_entry = ttk.Entry(
            self.control_frame, foreground="black"
        )
        self.branch_color_trait_entry.grid()
        self.branch_color_trait_entry.insert(0, self.branch_color_trait)
        self.update_branch_color_trait_button = tk.Button(
            self.control_frame, text="Update branch_color_trait", command=update
        ).grid()

    def render_drug_resistance_heatmap(
        self, to_rerender, to_derender, hide=True, column=None, frow=None, columnspan=1
    ):
        to_rerender = None
        to_derender = None
        keys_path = self.drug_resistance_heatmap_keys_path
        text = "Do you want to plot the heatmap for drug-resistance of all sampled genomes in the transmission tree plot?"

        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)

        component = EasyRadioButton(
            keys_path,
            self.config_path,
            text,
            "do_postprocess",
            self.control_frame,
            column,
            frow,
            hide,
            to_rerender,
            to_derender,
            columnspan,
            radiobuttonselected,
        )

        self.visible_components.add(component)
        return component

    def render_drug_resistance_heatmap_dep(self):
        """
        self.drug_resistance_heatmap = load_config_as_dict(self.config_path)['Postprocessing_options']['tree_plotting']['drug_resistance_heatmap']
        """

        def update():
            prev_val = self.drug_resistance_heatmap
            self.drug_resistance_heatmap = string_to_bool_mapping[
                self.drug_resistance_heatmap_var.get()
            ]
            config = load_config_as_dict(self.config_path)
            keys_path = [
                "Postprocessing_options",
                "tree_plotting",
                "drug_resistance_heatmap",
            ]
            update_nested_dict(config, keys_path, self.drug_resistance_heatmap)
            save_config(self.config_path, config)
            if prev_val != self.drug_resistance_heatmap:
                messagebox.showinfo("Success", "Updated successfully")

        self.drug_resistance_heatmap_label = ttk.Label(
            self.control_frame, text="drug_resistance_heatmap:"
        ).grid()
        self.drug_resistance_heatmap_var = tk.StringVar(
            value=bool_to_string_mapping[self.drug_resistance_heatmap]
        )
        self.drug_resistance_heatmap_combobox = ttk.Combobox(
            self.control_frame,
            textvariable=self.drug_resistance_heatmap_var,
            values=["Yes", "No"],
            state="readonly",
        ).grid()
        self.update_drug_resistance_heatmap_button = tk.Button(
            self.control_frame, text="Update Method", command=update
        ).grid()

    def init_val(self, config_path):
        self.render_nb = False
        self.frow_val = 0

        self.config_path = config_path
        self.config_dict = load_config_as_dict(self.config_path)
        self.config_path = config_path

        self.cwdir = load_config_as_dict(self.config_path)["BasicRunConfiguration"][
            "cwdir"
        ]
        # Postprocessing_options Configurations
        self.do_postprocess = load_config_as_dict(self.config_path)[
            "Postprocessing_options"
        ]["do_postprocess"]
        self.do_postprocess_keys_path = ["Postprocessing_options", "do_postprocess"]
        self.branch_color_trait = load_config_as_dict(self.config_path)[
            "Postprocessing_options"
        ]["tree_plotting"]["branch_color_trait"]
        self.branch_color_trait_keys_path = [
            "Postprocessing_options",
            "tree_plotting",
            "branch_color_trait",
        ]
        self.drug_resistance_heatmap = load_config_as_dict(self.config_path)[
            "Postprocessing_options"
        ]["tree_plotting"]["drug_resistance_heatmap"]

        self.drug_resistance_heatmap_keys_path = [
            "Postprocessing_options",
            "tree_plotting",
            "drug_resistance_heatmap",
        ]
