import tkinter as tk
from tkinter import messagebox
import os
import shutil
import sys
from utils import *

current_dir = os.path.dirname(os.path.abspath(__file__))
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
        config = load_config_as_dict(self.config_path)

        if config["Postprocessing_options"]["do_postprocess"]:
            try:
                val = int(self.branch_color_trait_control.entry.get())
            except ValueError:
                messagebox.showerror("Value Error", "Please enter a valid integer for trait number")
                return
            
            config["Postprocessing_options"]["tree_plotting"]["branch_color_trait"] = val
            save_config(self.config_path, config)

        cwdir = config["BasicRunConfiguration"]["cwdir"]
        target = os.path.join(cwdir, "config_file.json")

        try:
            shutil.copy(self.config_path, target)
            messagebox.showinfo("Success", "Config file saved successfully")
        except IOError as e:
            print("Unable to copy file. %s" % e)

    def load_page(self):
        hide = False
        self.render_do_postprocess(hide, 0, 1)
        self.render_branch_color_trait(hide, 0, 4)
        self.render_heatmap(hide, 0, 6)
        self.render_vcf(hide, 0, 8)
        self.render_fasta(hide, 0, 11)

    def render_do_postprocess(self, hide=True, column=None, frow=None, columnspan=1):
        to_rerender = None
        to_derender = None
        keys_path = self.do_postprocess_keys_path
        text = "Do you want to run post-processing after the simulation?\n"\
            "(Plotting trajectories & transmission trees, and outputting VCF/FASTA files.)"

        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)
            if var.get():
                self.render_branch_color_trait(hide, 0, 4, disabled=False)
                self.render_heatmap(hide, 0, 6, disabled=False)
                self.render_vcf(hide, 0, 8, disabled=False)
                self.render_fasta(hide, 0, 11, disabled=False)
            else:
                self.render_branch_color_trait(hide, 0, 4, disabled=True)
                self.render_heatmap(hide, 0, 6, disabled=True)
                self.render_vcf(hide, 0, 8, disabled=True)
                self.render_fasta(hide, 0, 11, disabled=True)

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

    def render_branch_color_trait(self, hide, column, frow, columnspan=1, disabled=False):
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
            disabled,
        )

        self.visible_components.add(component)
        self.branch_color_trait_control = component
        return component

    def render_heatmap(
        self,
        hide=True,
        column=None,
        frow=None,
        columnspan=1,
        disabled=False,
    ):
        def comboboxselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)
            
        to_rerender = None
        to_derender = None
        keys_path = self.heatmap_keys_path
        text = "Plot a heatmap for a fitness effect of all sampled genomes in the transmission tree plot?"
        width = 20

        component = EasyCombobox(
            keys_path,
            self.config_path,
            text,
            self.control_frame,
            column,
            frow,
            ["none", "transmissibility", "drug resistance"],
            to_rerender,
            to_derender,
            comboboxselected,
            hide,
            width,
            columnspan,
        )

        if disabled:
            component.label.configure(state="disabled")
            component.combobox.configure(state="disabled")

        self.visible_components.add(component)
        return component
    
    def render_vcf(
        self,
        hide=True,
        column=None,
        frow=None,
        columnspan=1,
        disabled=False,
    ):
        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)
        
        to_rerender = None
        to_derender = None
        keys_path = ["Postprocessing_options", "sequence_output", "vcf"]
        text = "Output a VCF file for sampled pathogens?"

        component = EasyRadioButton(
            keys_path,
            self.config_path,
            text,
            "output_vcf",
            self.control_frame,
            column,
            frow,
            hide,
            to_rerender,
            to_derender,
            columnspan,
            radiobuttonselected,
            disabled,
        )

        self.visible_components.add(component)
        return component
    
    def render_fasta(
        self,
        hide=True,
        column=None,
        frow=None,
        columnspan=1,
        disabled=False,
    ):
        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)

        to_rerender = None
        to_derender = None
        keys_path = ["Postprocessing_options", "sequence_output", "fasta"]
        text = "Output a FASTA file of concatenated SNPs for sampled pathogens?"

        component = EasyRadioButton(
            keys_path,
            self.config_path,
            text,
            "output_fasta",
            self.control_frame,
            column,
            frow,
            hide,
            to_rerender,
            to_derender,
            columnspan,
            radiobuttonselected,
            disabled,
        )

        self.visible_components.add(component)
        return component

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
        self.heatmap = load_config_as_dict(self.config_path)[
            "Postprocessing_options"
        ]["tree_plotting"]["heatmap"]

        self.heatmap_keys_path = [
            "Postprocessing_options",
            "tree_plotting",
            "heatmap",
        ]
