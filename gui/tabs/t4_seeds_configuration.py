import tkinter as tk
from tkinter import ttk, messagebox, filedialog, PhotoImage
import json
import os
import sys
from PIL import Image, ImageTk
from utils import *
from seed_generator import *


# TODO: seed_size = len(seeded_host_id), validate
class SeedsConfiguration(TabBase):
    def __init__(
        self, parent, tab_parent, config_path, tab_title, tab_index, hide=False
    ):
        super().__init__(parent, tab_parent, config_path, tab_title, tab_index, hide)

    # def global_update(self):

    def init_val(self, config_path):
        self.config_path = config_path

        self.visible_components = set()

        self.frow_val = 0

        self.config_dict = load_config_as_dict(self.config_path)

        # SeedsConfiguration
        self.seed_size = self.config_dict["SeedsConfiguration"]["seed_size"]
        self.method = self.config_dict["SeedsConfiguration"]["method"]
        self.use_reference: bool = self.config_dict["SeedsConfiguration"]["use_reference"]

        # user_input
        self.path_seeds_vcf = self.config_dict["SeedsConfiguration"]["user_input"]["path_seeds_vcf"]
        self.path_seeds_phylogeny = self.config_dict["SeedsConfiguration"]["user_input"]["path_seeds_phylogeny"]

        # SLiM_burnin_WF
        self.burn_in_Ne = self.config_dict["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_Ne"]
        self.burn_in_generations_wf = self.config_dict["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_generations"]
        self.burn_in_mutrate_wf = self.config_dict["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_mutrate"]

        # SLiM_burnin_epi
        self.burn_in_generations_epi = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["burn_in_generations"]
        self.burn_in_mutrate_epi = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["burn_in_mutrate"]
        self.seeded_host_id = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["seeded_host_id"]
        self.S_IE_prob = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["S_IE_prob"]
        self.E_I_prob = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["E_I_prob"]
        self.E_R_prob = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["E_R_prob"]
        self.latency_prob = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["latency_prob"]
        self.I_R_prob = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["I_R_prob"]
        self.I_E_prob = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["I_E_prob"]
        self.R_S_prob = self.config_dict["SeedsConfiguration"]["SLiM_burnin_epi"]["R_S_prob"]

    def init_user_input_group(self, hide):
        # tab_t = self.render_tab_title(hide, 5+3, 0, 3)
        # path_seeds_vfc = self.render_path_seeds_vcf(hide, 5+3, 1, 1)
        # path_seeds_phyl = self.render_path_seeds_phylogeny(hide, 12, 1, 1)
        grpctrs = GroupControls()
        # grpctrs.add(tab_t)
        # todo
        grpctrs.add(self.display_burn_in_settings_label(hide, 1, 9))
        grpctrs.add(self.render_path_seeds_vcf(hide, 1, 11, 1))
        grpctrs.add(self.render_path_seeds_phylogeny(hide, 1, 14, 1))
        return grpctrs

    def init_wf_group(self, hide):
        """
        self.burn_in_Ne = self.config_dict['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_Ne']
        self.burn_in_generations_wf = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_generations']
        self.burn_in_mutrate_wf = load_config_as_dict(self.config_path)['SeedsConfiguration']['SLiM_burnin_WF']['burn_in_mutrate']
        """
        wf_grpctrls = GroupControls()
        # wf_grpctrls.add(self.render_tab_title(hide, 5+3, 0, 3))
        wf_grpctrls.add(self.display_burn_in_settings_label(hide, 1, 9))
        wf_grpctrls.add(self.render_burn_in_ne(hide, 1, 11))
        wf_grpctrls.add(self.render_burn_in_generations_wf(hide, 2, 11))
        wf_grpctrls.add(self.render_subst_model_parameterization_wf(hide, 1, 13))
        self.burn_in_mutrate_wf_control = self.render_burn_in_mutrate_wf(hide, 1, 15)
        self.burn_in_mutrate_matrix_wf_control = self.render_burn_in_mutrate_matrix_wf(hide, 2, 15)
        wf_grpctrls.add(self.burn_in_mutrate_wf_control)
        wf_grpctrls.add(self.burn_in_mutrate_matrix_wf_control)
        wf_grpctrls.add(self.render_burn_in_load_mutrate_wf(hide, 1, 19))
        return wf_grpctrls

    def init_epi_group(self, hide):
        epi_grpctrls = GroupControls()
        # epi_grpctrls.add(self.render_tab_title(hide, 5+3, 0, 3))
        epi_grpctrls.add(self.display_burn_in_settings_label(hide, 0, 9))
        epi_grpctrls.add(self.render_seeded_host_id(hide, 0, 11))
        epi_grpctrls.add(self.render_burn_in_generations_epi(hide, 1, 11))
        epi_grpctrls.add(self.render_subst_model_parameterization_epi(hide, 2, 11))
        self.burn_in_mutrate_epi_control = self.render_burn_in_mutrate_epi(hide, 2, 13)
        self.burn_in_mutrate_matrix_epi_control = self.render_burn_in_mutrate_matrix_epi(hide, 3, 13)
        epi_grpctrls.add(self.burn_in_mutrate_epi_control)
        epi_grpctrls.add(self.burn_in_mutrate_matrix_epi_control)
        epi_grpctrls.add(self.render_burn_in_load_mutrate_epi(hide, 2, 16))
        
        epi_grpctrls.add(self.render_S_IE_prob(hide, 0, 13))
        epi_grpctrls.add(self.render_E_I_prob(hide, 0, 15))
        epi_grpctrls.add(self.render_latency_prob(hide, 1, 13))
        epi_grpctrls.add(self.render_E_R_prob(hide, 1, 15))
        epi_grpctrls.add(self.render_I_E_prob(hide, 0, 17))
        epi_grpctrls.add(self.render_R_S_prob(hide, 0, 19))
        epi_grpctrls.add(self.render_I_R_prob(hide, 0, 21))
        epi_grpctrls.add(
            self.render_image(
                "gui/assets/t4.png",
                550,
                255,
                hide,
                self.control_frame,
                frow=18,
                column=1,
                columnspan=2,
                rowspan=10,
            )
        )

        return epi_grpctrls

    def render_tab_title(self, hide=True, column=None, frow=None, columnspan=1):
        # self.render_tab_title(user_input_components, 5+3, 0, 3)

        self.render_t4_title_text = "Burn-in Settings:"
        component = EasyTitle(
            self.render_t4_title_text,
            self.control_frame,
            column,
            frow,
            hide,
            columnspan,
        )
        self.visible_components.add(component)
        return component

    def render_seeds_size(self, hide, column, columnspan, frow):
        text = "Number of Seeding Pathogens (Integer)"
        keys_path = ["SeedsConfiguration", "seed_size"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            text,
            "Number of Seeding Pathogens",
            self.control_frame,
            column,
            frow,
            "integer",
            hide,
            columnspan,
        )

        self.visible_components.add(component)
        return component

        self.seed_size_label = ttk.Label(
            self.control_frame, text=self.render_seeds_size_title, style="Bold.TLabel"
        )
        self.seed_size_label.grid(row=1, column=1, columnspan=3, sticky="w", pady=5)
        self.seed_size_entry = ttk.Entry(
            self.control_frame, foreground="black", width=20
        )
        self.seed_size_entry.insert(0, self.seed_size)
        self.seed_size_entry.grid(row=2, column=1, columnspan=3, sticky="w", pady=5)

        self.render_seeds_size_components = []
        self.render_seeds_size_components.append(self.seed_size_label)
        self.render_seeds_size_components.append(self.seed_size_entry)

    def render_path_seeds_vcf(self, hide=True, column=None, frow=None, columnspan=1):
        """
        self.path_seeds_vcf = load_config_as_dict(self.config_path)['SeedsConfiguration']['user_input']['path_seeds_vcf']
        """
        self.render_path_seeds_vcf_text = (
            "The vcf file of the seeding pathogen sequences (VCF format)"
        )
        keys_path = ["SeedsConfiguration", "user_input", "path_seeds_vcf"]
        component = EasyPathSelector(
            keys_path,
            self.config_path,
            self.render_path_seeds_vcf_text,
            self.control_frame,
            column,
            hide,
            frow,
            columnspan,
        )

        self.visible_components.add(component)
        return component

        def update():
            chosen_file = filedialog.askopenfilename(title="Select a File")
            if chosen_file:
                self.path_seeds_vcf = chosen_file
                self.path_seeds_vcf_value_label.config(text=self.path_seeds_vcf)
                config = load_config_as_dict(self.config_path)
                config["SeedsConfiguration"]["user_input"]["path_seeds_vcf"] = (
                    self.path_seeds_vcf
                )
                save_config(self.config_path, config)

        self.render_path_seeds_vcf_text = (
            "The vcf file of the seeding pathogen sequences (VCF format)"
        )
        self.path_seeds_vcf_var = tk.StringVar(value=self.path_seeds_vcf)
        self.path_seeds_vcf_label = ttk.Label(
            self.control_frame,
            text=self.render_path_seeds_vcf_text,
            style="Bold.TLabel",
        )

        if self.path_seeds_vcf == "":
            self.path_seeds_vcf_value_label = ttk.Label(
                self.control_frame, text="None selected", foreground="black"
            )
        else:
            self.path_seeds_vcf_value_label = ttk.Label(
                self.control_frame, text=self.path_seeds_vcf, foreground="black"
            )

        self.path_seeds_vcf_button = tk.Button(
            self.control_frame, text="Choose File", command=update
        )
        # self.delete_path_seeds_vcf_button = tk.Button(self.control_frame, text="Delete File", command=update)

        self.path_seeds_vcf_label.grid(row=9, column=1, sticky="w", pady=5)
        self.path_seeds_vcf_value_label.grid(row=10, column=1, sticky="w", pady=5)
        self.path_seeds_vcf_button.grid(row=11, column=1, sticky="e", pady=5)
        # self.delete_path_seeds_vcf_button.grid(row=11, column=1, sticky='w', pady=5)

        components.add(self.path_seeds_vcf_label)
        components.add(self.path_seeds_vcf_value_label)
        components.add(self.path_seeds_vcf_button)
        # components.add(self.delete_path_seeds_vcf_button)

    def render_path_seeds_phylogeny(
        self, hide=True, column=None, frow=None, columnspan=1
    ):
        """
        self.path_seeds_phylogeny = load_config_as_dict(self.config_path)['SeedsConfiguration']['user_input']["path_seeds_phylogeny"]
        """

        text = "The phylogeny of the seeding sequences (nwk format, optional)"
        keys_path = ["SeedsConfiguration", "user_input", "path_seeds_phylogeny"]
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

        def update():
            chosen_file = filedialog.askopenfilename(title="Select a File")
            if chosen_file:
                self.path_seeds_phylogeny = chosen_file
                self.path_seeds_phylogeny_value_label.config(
                    text=self.path_seeds_phylogeny
                )
                config = load_config_as_dict(self.config_path)
                config["SeedsConfiguration"]["user_input"]["path_seeds_phylogeny"] = (
                    self.path_seeds_phylogeny
                )
                save_config(self.config_path, config)

        self.render_path_seeds_phylogeny_text = (
            "The phylogeny of the seeding sequences (nwk format, optional)"
        )
        self.path_seeds_phylogeny_var = tk.StringVar(value=self.path_seeds_phylogeny)
        self.path_seeds_phylogeny_label = ttk.Label(
            self.control_frame,
            text=self.render_path_seeds_phylogeny_text,
            style="Bold.TLabel",
        )

        if self.path_seeds_phylogeny == "":
            self.path_seeds_phylogeny_value_label = ttk.Label(
                self.control_frame, text="None selected", foreground="black"
            )
        else:
            self.path_seeds_phylogeny_value_label = ttk.Label(
                self.control_frame, text=self.path_seeds_phylogeny, foreground="black"
            )

        self.path_seeds_phylogeny_button = tk.Button(
            self.control_frame, text="Choose File", command=update
        )
        # self.delete_path_seeds_phylogeny_button = tk.Button(self.control_frame, text="Delete File", command=update)

        self.path_seeds_phylogeny_label.grid(row=12, column=1, sticky="w", pady=5)
        self.path_seeds_phylogeny_value_label.grid(row=13, column=1, sticky="w", pady=5)
        self.path_seeds_phylogeny_button.grid(row=14, column=1, sticky="e", pady=5)
        # self.delete_path_seeds_phylogeny_button.grid(row=11, column=1, sticky='w', pady=5)

        components.add(self.path_seeds_phylogeny_label)
        components.add(self.path_seeds_phylogeny_value_label)
        components.add(self.path_seeds_phylogeny_button)
        # components.add(self.delete_path_seeds_phylogeny_button)

    def render_use_reference(
        self, to_rerender, to_derender, hide=True, column=None, frow=None, columnspan=1
    ):
        keys_path = ["SeedsConfiguration", "use_reference"]
        text = "Do you want to use the same sequence (reference genome) as seeding sequences?"

        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)
            if var.get():
                to_derender()
            else:
                to_rerender()

        component = EasyRadioButton(
            keys_path,
            self.config_path,
            text,
            "use_reference",
            self.control_frame,
            column,
            frow,
            hide,
            to_rerender,
            to_derender,
            columnspan,
            radiobuttonselected,
        )

        component.update_rb_false_text(
            "No (Run the burn-in process or provide seeding sequences)"
        )

        self.visible_components.add(component)
        return component

        def update():
            keys_path = ["SeedsConfiguration", "use_reference"]
            no_validate_update(
                self.within_host_reproduction_var, self.config_path, keys_path
            )
            use_ref_local = get_dict_val(
                load_config_as_dict(self.config_path), keys_path
            )
            if use_ref_local:
                self.use_method_grid_configs = derender_components(
                    self.use_method_components
                )
                self.user_input_grid_configs = derender_components(
                    self.user_input_components
                )
                self.wf_grid_configs = derender_components(self.wf_components)
                self.epi_grid_configs = derender_components(self.epi_components)
            else:
                rerender_components(
                    self.use_method_components, self.use_method_grid_configs
                )
                rerender_components(
                    self.user_input_components, self.user_input_grid_configs
                )
                keys_path = ["SeedsConfiguration", "method"]
                use_method_local = get_dict_val(
                    load_config_as_dict(self.config_path), keys_path
                )
                match use_method_local:
                    case "user_input":
                        rerender_components(
                            self.user_input_components, self.user_input_grid_configs
                        )
                    case "SLiM_burnin_WF":
                        rerender_components(self.wf_components, self.wf_grid_configs)
                    case "SLiM_burnin_epi":
                        rerender_components(self.epi_components, self.epi_grid_configs)

        self.render_use_reference_text = "Do you want to use the same sequence (reference genome) as seeding sequences?"
        self.within_host_reproduction_var = tk.BooleanVar(value=self.use_reference)
        self.within_host_reproduction_label = ttk.Label(
            self.control_frame, text=self.render_use_reference_text, style="Bold.TLabel"
        )
        self.within_host_reproduction_label.grid(row=3, column=1, sticky="w", pady=5)

        self.rb_true = ttk.Radiobutton(
            self.control_frame,
            text="Yes",
            variable=self.within_host_reproduction_var,
            value=True,
            command=update,
        )
        self.rb_true.grid(row=4, column=1, columnspan=3, sticky="w", pady=5)

        self.rb_false = ttk.Radiobutton(
            self.control_frame,
            text="No (Run the burn-in process or provide seeding sequences)",
            variable=self.within_host_reproduction_var,
            value=False,
            command=update,
        )
        self.rb_false.grid(row=5, column=1, columnspan=3, sticky="w", pady=5)

    def render_use_method(
        self,
        column=None,
        frow=None,
        to_rerender=None,
        to_derender=None,
        hide=True,
        width=20,
        column_span=20,
    ):
        text = "Method to Generate Sequences of the Seeding Pathogens"
        keys_path = ["SeedsConfiguration", "method"]

        def comboboxselected(var, to_rerender, to_derender):
            local_var = var.get()
            converted_var = render_to_val_ui_wf_epi_mapping.get(local_var, "")
            # self.set_var(converted_var)
            no_validate_update_val(converted_var, self.config_path, keys_path)
            renders = [self.use_method_controls, self.run_button_control]

            match converted_var:
                case "user_input":
                    renders.append(self.user_input_group_controls)
                case "SLiM_burnin_WF":
                    renders.append(self.wf_group_controls)
                case "SLiM_burnin_epi":
                    renders.append(self.epi_group_controls)
                case _:
                    raise ValueError("Invalid method")

            use_reference_to_rerender = GroupControls(renders).rerender_itself
            use_reference_to_derender = GroupControls(renders).derender_itself
            self.use_reference_control.set_to_rerender(use_reference_to_rerender)
            self.use_reference_control.set_to_derender(use_reference_to_derender)
            match converted_var:
                case "user_input":
                    derender = [self.wf_group_controls, self.epi_group_controls]
                    self.use_method_controls.set_to_derender(
                        GroupControls(derender).derender_itself
                    )
                    self.use_method_controls.set_to_rerender(
                        self.user_input_group_controls.rerender_itself
                    )

                    # renders.append(self.user_input_group_controls)
                case "SLiM_burnin_WF":
                    derender = [self.user_input_group_controls, self.epi_group_controls]
                    self.use_method_controls.set_to_derender(
                        GroupControls(derender).derender_itself
                    )
                    self.use_method_controls.set_to_rerender(
                        self.wf_group_controls.rerender_itself
                    )
                case "SLiM_burnin_epi":
                    derender = [self.user_input_group_controls, self.wf_group_controls]
                    self.use_method_controls.set_to_derender(
                        GroupControls(derender).derender_itself
                    )
                    self.use_method_controls.set_to_rerender(
                        self.epi_group_controls.rerender_itself
                    )
                case _:
                    raise ValueError("Invalid method")
                
            to_derender()
            to_rerender()

        component = EasyCombobox(
            keys_path,
            self.config_path,
            text,
            self.control_frame,
            column,
            frow,
            ui_wf_epi_values,
            to_rerender,
            to_derender,
            comboboxselected,
            hide,
            width,
            column_span,
            val_to_render_ui_wf_epi_mapping,
        )
        # render_to_val_generate_genetic_architecture_method)

        self.visible_components.add(component)

        return component

        def update(event):
            keys_path = ["SeedsConfiguration", "method"]
            no_validate_update(
                self.use_method_var,
                self.config_path,
                keys_path,
                mapping=render_to_val_ui_wf_epi_mapping,
            )
            match get_dict_val(load_config_as_dict(self.config_path), keys_path):
                case "user_input":
                    self.wf_grid_configs = derender_components(self.wf_components)
                    self.epi_grid_configs = derender_components(self.epi_components)
                    rerender_components(
                        self.user_input_components, self.user_input_grid_configs
                    )
                case "SLiM_burnin_WF":
                    self.epi_grid_configs = derender_components(self.epi_components)
                    self.user_input_grid_configs = derender_components(
                        self.user_input_components
                    )
                    rerender_components(self.wf_components, self.wf_grid_configs)
                case "SLiM_burnin_epi":
                    self.wf_grid_configs = derender_components(self.wf_components)
                    self.user_input_grid_configs = derender_components(
                        self.user_input_components
                    )
                    rerender_components(self.epi_components, self.epi_grid_configs)

        self.render_use_method_title = (
            "Method to Generate Sequences of the Seeding Pathogens"
        )
        self.use_method_label = ttk.Label(
            self.control_frame, text=self.render_use_method_title, style="Bold.TLabel"
        )
        self.use_method_label.grid(row=6, column=1, columnspan=3, sticky="w", pady=5)
        local_use_method_var = val_to_render_ui_wf_epi_mapping.get(self.method, "")
        self.use_method_var = tk.StringVar(value=local_use_method_var)
        combobox_vals = list(render_to_val_ui_wf_epi_mapping.keys())
        self.use_method_combobox = ttk.Combobox(
            self.control_frame,
            textvariable=self.use_method_var,
            values=combobox_vals,
            state="readonly",
            width=50,
        )
        self.use_method_combobox.grid(row=7, column=1, columnspan=3, sticky="w", pady=5)
        self.use_method_combobox.bind("<<ComboboxSelected>>", update)

        use_method_components = set()
        use_method_components.add(self.use_method_label)
        use_method_components.add(self.use_method_combobox)
        return use_method_components

    def display_burn_in_settings_label(self, hide=True, column=None, frow=None):
        component = EasyTitle(
            "Burn-in Settings: ", self.control_frame, column, frow, hide, 1
        )
        self.visible_components.add(component)
        return component

    def render_burn_in_ne(self, hide=True, column=None, frow=None):
        columnspan = 1
        self.render_burn_in_ne_text = "Effective Population Size (Integer)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_WF", "burn_in_Ne"]

        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_burn_in_ne_text,
            "Effective Population Size",
            self.control_frame,
            column,
            frow,
            "integer",
            hide,
            columnspan,
        )

        self.visible_components.add(component)
        return component

        self.burn_in_Ne_label = ttk.Label(
            self.control_frame, text=self.render_burn_in_ne_text, style="Bold.TLabel"
        )
        self.burn_in_Ne_entry = ttk.Entry(self.control_frame, foreground="black")
        self.burn_in_Ne_entry.insert(0, self.burn_in_Ne)
        # self.update_burn_in_Ne_button = tk.Button(self.control_frame, text="Update burn_in_Ne", command=self.update_burn_in_Ne)

        self.burn_in_Ne_label.grid(row=9, column=1, sticky="w", pady=5)
        self.burn_in_Ne_entry.grid(row=10, column=1, sticky="w", pady=5)
        # no east
        components.add(self.burn_in_Ne_label)
        components.add(self.burn_in_Ne_entry)

    def render_burn_in_generations_wf(self, hide=True, column=None, frow=None):
        columnspan = 1
        self.render_burn_in_generations_wf_text = (
            "Number of Burn-in Generations (Integer)"
        )
        keys_path = ["SeedsConfiguration", "SLiM_burnin_WF", "burn_in_generations"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_burn_in_generations_wf_text,
            "Number of Burn-in Generations (WF)",
            self.control_frame,
            column,
            frow,
            "integer",
            hide,
            columnspan,
        )
        self.visible_components.add(component)
        return component
    
    def render_subst_model_parameterization_wf(self, hide=True, column=None, frow=None):
        def comboboxselected(var, to_rerender, to_derender):
            local_var = var.get()
            no_validate_update_val(local_var, self.config_path, keys_path)
            if local_var == "mutation rate (single)":
                self.burn_in_mutrate_wf_control.label.config(state="normal")
                self.burn_in_mutrate_wf_control.entry.config(state="normal", foreground="black")
                self.burn_in_mutrate_matrix_wf_control.label.config(state="disabled")
                for i in range(4):
                    for j in range(4):
                        self.burn_in_mutrate_matrix_wf_control.matrix_entries[i][j].config(state="disabled", foreground="light grey")
            elif local_var == "mutation rate matrix":
                self.burn_in_mutrate_wf_control.label.config(state="disabled")
                self.burn_in_mutrate_wf_control.entry.config(state="disabled", foreground="light grey")
                self.burn_in_mutrate_matrix_wf_control.label.config(state="normal")
                for i in range(4):
                    for j in range(4):
                        if i != j:
                            self.burn_in_mutrate_matrix_wf_control.matrix_entries[i][j].config(state="normal", foreground="black")

        text = "Substitution Model Parameterization"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_WF", "subst_model_parameterization"]
        to_rerender, to_derender = None, None
        width = 20
        column_span = 1
        component = EasyCombobox(
            keys_path,
            self.config_path,
            text,
            self.control_frame,
            column,
            frow,
            ["mutation rate (single)", "mutation rate matrix"],
            to_rerender,
            to_derender,
            comboboxselected,
            hide,
            width,
            column_span
        )

        self.visible_components.add(component)

        return component

    def render_burn_in_mutrate_wf(self, hide=True, column=None, frow=None):
        columnspan = 1
        text = "Mutation Rate (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_WF", "burn_in_mutrate"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            text,
            "Mutation Rate",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            columnspan=columnspan,
            sticky="wn",
            disabled=True
        )
        self.visible_components.add(component)
        return component

    def render_burn_in_mutrate_matrix_wf(self, hide=True, column=None, frow=None):
        columnspan = 1
        self.render_burn_in_mutrate_wf_text = "Mutation Rate Matrix (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_WF", "burn_in_mutrate_matrix"]
        component = EasyEntryMatrix(
            keys_path,
            self.config_path,
            self.render_burn_in_mutrate_wf_text,
            "Mutation Rate Matrix (WF)",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            columnspan=columnspan,
            disabled=True
        )
        
        self.visible_components.add(component)
        return component
    
    def render_burn_in_load_mutrate_wf(self, hide=True, column=None, frow=None):
        def click():
            config = load_config_as_dict(self.config_path)["EvolutionModel"]
            self.burn_in_mutrate_wf_control.entry.delete(0, tk.END)
            self.burn_in_mutrate_wf_control.entry.insert(0, str(config["mut_rate"]))
            for i in range(4):
                for j in range(4):
                    self.burn_in_mutrate_matrix_wf_control.matrix_entries[i][j].delete(0, tk.END)
                    self.burn_in_mutrate_matrix_wf_control.matrix_entries[i][j].insert(0, str(config["mut_rate_matrix"][i][j]))

        text = "Load mut. rate(s) \n from Evolutionary Model"
        component = EasyButton(
            text,
            self.control_frame,
            column,
            frow,
            click,
            hide,
            sticky="w"
        )
        
        self.visible_components.add(component)
        return component

    ##########################################################################
    ####### startofepi
    ##########################################################################

    def render_burn_in_generations_epi(self, hide=True, column=None, frow=None):
        self.render_burn_in_generations_epi_text = (
            "Number of Burn-in Generations (Integer)"
        )
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "burn_in_generations"]

        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_burn_in_generations_epi_text,
            "Number of Burn-in Generations (epi)",
            self.control_frame,
            column,
            frow,
            "integer",
            hide,
            1,
        )
        self.visible_components.add(component)
        return component

        self.burn_in_generations_epi_label = ttk.Label(
            self.control_frame,
            text=self.render_burn_in_generations_epi_text,
            style="Bold.TLabel",
        )
        self.burn_in_generations_epi_entry = ttk.Entry(
            self.control_frame, foreground="black"
        )
        self.burn_in_generations_epi_entry.insert(0, self.burn_in_generations_epi)

        self.burn_in_generations_epi_label.grid(row=6 + 3, column=0, sticky="w", pady=5)
        self.burn_in_generations_epi_entry.grid(row=7 + 3, column=0, sticky="w", pady=5)

        # self.render_burn_in_generations_epi_components = []
        epi_components.add(self.burn_in_generations_epi_label)
        epi_components.add(self.burn_in_generations_epi_entry)

        # self.update_burn_in_generations_epi_button = tk.Button(self.control_frame, text="Update burn_in_generations", command=self.update_burn_in_generations_epi)
        # self.update_burn_in_generations_epi_button.grid()

        # self.t4_title.grid(row=7, column=0, sticky='w', pady=5)

    def render_subst_model_parameterization_epi(self, hide=True, column=None, frow=None):
        def comboboxselected(var, to_rerender, to_derender):
            local_var = var.get()
            no_validate_update_val(local_var, self.config_path, keys_path)
            if local_var == "mutation rate (single)":
                self.burn_in_mutrate_epi_control.label.config(state="normal")
                self.burn_in_mutrate_epi_control.entry.config(state="normal", foreground="black")
                self.burn_in_mutrate_matrix_epi_control.label.config(state="disabled")
                for i in range(4):
                    for j in range(4):
                        self.burn_in_mutrate_matrix_epi_control.matrix_entries[i][j].config(state="disabled", foreground="light grey")
            elif local_var == "mutation rate matrix":
                self.burn_in_mutrate_epi_control.label.config(state="disabled")
                self.burn_in_mutrate_epi_control.entry.config(state="disabled", foreground="light grey")
                self.burn_in_mutrate_matrix_epi_control.label.config(state="normal")
                for i in range(4):
                    for j in range(4):
                        if i != j:
                            self.burn_in_mutrate_matrix_epi_control.matrix_entries[i][j].config(state="normal", foreground="black")

        text = "Substitution Model Parameterization"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "subst_model_parameterization"]
        to_rerender, to_derender = None, None
        width = 20
        column_span = 1
        component = EasyCombobox(
            keys_path,
            self.config_path,
            text,
            self.control_frame,
            column,
            frow,
            ["mutation rate (single)", "mutation rate matrix"],
            to_rerender,
            to_derender,
            comboboxselected,
            hide,
            width,
            column_span
        )

        self.visible_components.add(component)

        return component

    def render_burn_in_mutrate_epi(self, hide=True, column=None, frow=None):
        self.render_burn_in_mutrate_epi_text = "Mutation Rate (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "burn_in_mutrate"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_burn_in_mutrate_epi_text,
            "Mutation Rate (epi)",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            1,
            disabled=True
        )
        self.visible_components.add(component)
        return component

        self.burn_in_mutrate_epi_label = ttk.Label(
            self.control_frame,
            text=self.render_burn_in_mutrate_epi_text,
            style="Bold.TLabel",
        )
        self.burn_in_mutrate_epi_entry = ttk.Entry(
            self.control_frame, foreground="black"
        )
        self.burn_in_mutrate_epi_entry.insert(0, self.burn_in_mutrate_epi)

        self.burn_in_mutrate_epi_label.grid(row=6 + 3, column=1, sticky="w", pady=5)
        self.burn_in_mutrate_epi_entry.grid(row=7 + 3, column=1, sticky="w", pady=5)

        # self.render_burn_in_mutrate_epi_components = []
        epi_components.add(self.burn_in_mutrate_epi_label)
        epi_components.add(self.burn_in_mutrate_epi_entry)
        # self.update_burn_in_mutrate_epi_button = tk.Button(self.control_frame, text="Update burn_in_mutrate_epi", command=self.update_burn_in_mutrate_epi)
        # self.update_burn_in_mutrate_epi_button.grid()
    
    def render_burn_in_mutrate_matrix_epi(self, hide=True, column=None, frow=None):
        columnspan = 1
        text = "Mutation Rate Matrix (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "burn_in_mutrate_matrix"]
        component = EasyEntryMatrix(
            keys_path,
            self.config_path,
            text,
            "Mutation Rate Matrix (epi)",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            columnspan=columnspan,
            disabled=True
        )
        
        self.visible_components.add(component)
        return component
    
    def render_burn_in_load_mutrate_epi(self, hide=True, column=None, frow=None):
        def click():
            config = load_config_as_dict(self.config_path)["EvolutionModel"]
            self.burn_in_mutrate_epi_control.entry.delete(0, tk.END)
            self.burn_in_mutrate_epi_control.entry.insert(0, str(config["mut_rate"]))
            for i in range(4):
                for j in range(4):
                    self.burn_in_mutrate_matrix_epi_control.matrix_entries[i][j].delete(0, tk.END)
                    self.burn_in_mutrate_matrix_epi_control.matrix_entries[i][j].insert(0, str(config["mut_rate_matrix"][i][j]))

        text = "Load mut. rate(s) \n from Evolutionary Model"
        component = EasyButton(
            text,
            self.control_frame,
            column,
            frow,
            click,
            hide,
            sticky="w"
        )
        
        self.visible_components.add(component)
        return component

    def render_seeded_host_id(self, hide=True, column=None, frow=None):
        self.render_seeded_host_id_text = "Seeded Host ID(s) (Integer)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "seeded_host_id"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_seeded_host_id_text,
            "Seeded Host IDs",
            self.control_frame,
            column,
            frow,
            "list",
            hide,
            columnspan=1,
        )
        self.visible_components.add(component)
        return component

        self.seeded_host_id_label = ttk.Label(
            self.control_frame,
            text=self.render_seeded_host_id_text,
            style="Bold.TLabel",
        )
        self.seeded_host_id_entry = ttk.Entry(self.control_frame, foreground="black")
        self.seeded_host_id_entry.insert(0, str(self.seeded_host_id))

        self.seeded_host_id_label.grid(row=6 + 3, column=2, sticky="w", pady=5)
        self.seeded_host_id_entry.grid(row=7 + 3, column=2, sticky="w", pady=5)

        # self.render_seeded_host_id_components = []
        epi_components.add(self.seeded_host_id_label)
        epi_components.add(self.seeded_host_id_entry)
        # self.update_seeded_host_id_button = tk.Button(self.control_frame, text="Update seeded_host_id", command=self.update_seeded_host_id)
        # self.update_seeded_host_id_button.grid()

    def render_S_IE_prob(self, hide=True, column=None, frow=None):
        self.render_S_IE_prob_text = "Transmission Prob. \u03b2 (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "S_IE_prob"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_S_IE_prob_text,
            "Transmission Prob.",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            1,
        )
        self.visible_components.add(component)
        return component

        self.S_IE_prob_label = ttk.Label(
            self.control_frame, text=self.render_S_IE_prob_text, style="Bold.TLabel"
        )
        self.S_IE_prob_entry = ttk.Entry(self.control_frame, foreground="black")
        self.S_IE_prob_entry.insert(0, self.S_IE_prob)

        self.S_IE_prob_label.grid(row=8 + 3, column=0, sticky="w", pady=5)
        self.S_IE_prob_entry.grid(row=9 + 3, column=0, sticky="w", pady=5)

        # self.render_S_IE_prob_components = []
        epi_components.add(self.S_IE_prob_label)
        epi_components.add(self.S_IE_prob_entry)

    def render_E_R_prob(self, hide=True, column=None, frow=None):
        self.render_E_R_prob_text = "Latent Recovery Prob. \u03c4 (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "E_R_prob"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_E_R_prob_text,
            "Latent Recovery Prob.",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            1,
        )
        self.visible_components.add(component)
        return component

        self.E_R_prob_label = ttk.Label(
            self.control_frame, text=self.render_E_R_prob_text, style="Bold.TLabel"
        )
        self.E_R_prob_entry = ttk.Entry(self.control_frame, foreground="black")
        self.E_R_prob_entry.insert(0, self.E_R_prob)

        self.E_R_prob_label.grid(row=8 + 3, column=2, sticky="w", pady=5)
        self.E_R_prob_entry.grid(row=9 + 3, column=2, sticky="w", pady=5)

        # self.render_E_R_prob_components = []
        epi_components.add(self.E_R_prob_label)
        epi_components.add(self.E_R_prob_entry)

    def render_latency_prob(self, hide=True, column=None, frow=None):
        self.render_latency_prob_text = "Latency Prob. p (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "latency_prob"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_latency_prob_text,
            "Latency Prob. p",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            1,
        )
        self.visible_components.add(component)
        return component

        self.latency_prob_label = ttk.Label(
            self.control_frame, text=self.render_latency_prob_text, style="Bold.TLabel"
        )
        self.latency_prob_entry = ttk.Entry(self.control_frame, foreground="black")
        self.latency_prob_entry.insert(0, self.latency_prob)

        self.latency_prob_label.grid(row=8 + 3, column=1, sticky="w", pady=5)
        self.latency_prob_entry.grid(row=9 + 3, column=1, sticky="w", pady=5)

        # self.render_latency_prob_components = []
        epi_components.add(self.latency_prob_label)
        epi_components.add(self.latency_prob_entry)

    def render_E_I_prob(self, hide=True, column=None, frow=None):
        self.render_E_I_prob_text = "Activation Prob. v (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "E_I_prob"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_E_I_prob_text,
            "Activation Prob.",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            1,
        )
        self.visible_components.add(component)
        return component

        self.E_I_prob_label = ttk.Label(
            self.control_frame, text=self.render_E_I_prob_text, style="Bold.TLabel"
        )
        self.E_I_prob_entry = ttk.Entry(self.control_frame, foreground="black")
        self.E_I_prob_entry.insert(0, self.E_I_prob)

        self.E_I_prob_label.grid(row=10 + 3, column=0, sticky="w", pady=5)
        self.E_I_prob_entry.grid(row=11 + 3, column=0, sticky="w", pady=5)

        epi_components.add(self.E_I_prob_label)
        epi_components.add(self.E_I_prob_entry)

    def render_I_E_prob(self, hide=True, column=None, frow=None):
        self.render_I_E_prob_text = "De-activation Prob. \u03c6 (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "I_E_prob"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_I_E_prob_text,
            "De-activation Prob.",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            columnspan=1,
        )
        self.visible_components.add(component)
        return component

        self.I_E_prob_label = ttk.Label(
            self.control_frame, text=self.render_I_E_prob_text, style="Bold.TLabel"
        )

        self.I_E_prob_entry = ttk.Entry(self.control_frame, foreground="black")
        self.I_E_prob_entry.insert(0, self.I_E_prob)

        self.I_E_prob_label.grid(row=12 + 3, column=0, sticky="w", pady=5)
        self.I_E_prob_entry.grid(row=13 + 3, column=0, sticky="w", pady=5)

        # self.render_I_E_prob_components = []
        epi_components.add(self.I_E_prob_label)
        epi_components.add(self.I_E_prob_entry)

    def render_R_S_prob(self, hide=True, column=None, frow=None):
        self.render_R_S_prob_text = "Immunity Loss Prob. \u03c9 (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "R_S_prob"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_R_S_prob_text,
            "Immunity Loss Prob.",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            columnspan=1,
        )
        self.visible_components.add(component)
        return component

        self.R_S_prob_entry = ttk.Entry(self.control_frame, foreground="black")
        self.R_S_prob_entry.insert(0, self.R_S_prob)

        self.R_S_prob_label.grid(row=14 + 3, column=0, sticky="w", pady=5)
        self.R_S_prob_entry.grid(row=15 + 3, column=0, sticky="w", pady=5)

        # self.render_R_S_prob_components = []
        epi_components.add(self.R_S_prob_label)
        epi_components.add(self.R_S_prob_entry)

    def render_I_R_prob(self, hide=True, column=None, frow=None):
        self.render_I_R_prob_text = "Active Recovery Prob. \u03b3 (Numerical)"
        keys_path = ["SeedsConfiguration", "SLiM_burnin_epi", "I_R_prob"]
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_I_R_prob_text,
            "Active Recovery Prob.",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            columnspan=1,
        )
        self.visible_components.add(component)
        return component
        self.I_R_prob_label = ttk.Label(
            self.control_frame, text=self.render_I_R_prob_text, style="Bold.TLabel"
        )

        self.I_R_prob_entry = ttk.Entry(self.control_frame, foreground="black")
        self.I_R_prob_entry.insert(0, self.I_R_prob)

        self.I_R_prob_label.grid(row=16 + 3, column=0, sticky="w", pady=5)
        self.I_R_prob_entry.grid(row=17 + 3, column=0, sticky="w", pady=5)

        # self.render_I_R_prob_components = []
        epi_components.add(self.I_R_prob_label)
        epi_components.add(self.I_R_prob_entry)

    def render_image(
        self,
        image_path,
        desired_width,
        desired_height,
        hide,
        control_frame,
        frow,
        column,
        columnspan,
        rowspan,
    ):
        component = EasyImage(
            image_path,
            desired_width,
            desired_height,
            hide,
            control_frame,
            frow,
            column,
            columnspan,
            rowspan,
        )

        return component

    def render_run_button(self, hide):
        def seed_generation():
            if self.global_update() == 1:
                return
            
            self.global_update()
            config = load_config_as_dict(self.config_path)
            cwdir = config["BasicRunConfiguration"]["cwdir"]
            seed_size = config["SeedsConfiguration"]["seed_size"]
            method = config["SeedsConfiguration"]["method"]
            ref_path = get_dict_val(config, ["GenomeElement", "ref_path"])
            rand_seed = config["BasicRunConfiguration"]["random_number_seed"]

            try:
                if method == "SLiM_burnin_WF":
                    Ne = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_Ne"]
                    n_gen = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_generations"]
                    mu = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_mutrate"]
                    if config["SeedsConfiguration"]["SLiM_burnin_WF"]["subst_model_parameterization"] == "":
                        messagebox.showerror("Error", "Please select a substitution model parameterization")
                        return
                    use_subst_matrix = config["SeedsConfiguration"]["SLiM_burnin_WF"]["subst_model_parameterization"] == "mutation rate matrix"
                    mu_matrix = config["SeedsConfiguration"]["SLiM_burnin_WF"]["burn_in_mutrate_matrix"]
                    mu_matrix = json.dumps({"A": mu_matrix[0], "C": mu_matrix[1], "G": mu_matrix[2], "T": mu_matrix[3]})
                    error = run_seed_generation(
                        method=method,
                        wk_dir=cwdir,
                        seed_size=seed_size,
                        Ne=Ne,
                        mu=mu,
                        n_gen=n_gen,
                        ref_path=ref_path,
                        rand_seed=rand_seed,
                        use_subst_matrix=use_subst_matrix, 
                        mu_matrix=mu_matrix
                    )
                elif method == "SLiM_burnin_epi":
                    seeded_host_id = config["SeedsConfiguration"]["SLiM_burnin_epi"]["seeded_host_id"]
                    n_gen = config["SeedsConfiguration"]["SLiM_burnin_epi"]["burn_in_generations"]
                    mu = config["SeedsConfiguration"]["SLiM_burnin_epi"]["burn_in_mutrate"]
                    if config["SeedsConfiguration"]["SLiM_burnin_epi"]["subst_model_parameterization"] == "":
                        messagebox.showerror("Error", "Please select a substitution model parameterization")
                        return
                    use_subst_matrix = config["SeedsConfiguration"]["SLiM_burnin_epi"]["subst_model_parameterization"] == "mutation rate matrix"
                    mu_matrix = config["SeedsConfiguration"]["SLiM_burnin_epi"]["burn_in_mutrate_matrix"]
                    mu_matrix = json.dumps({"A": mu_matrix[0], "C": mu_matrix[1], "G": mu_matrix[2], "T": mu_matrix[3]})
                    S_IE_prob = config["SeedsConfiguration"]["SLiM_burnin_epi"]["S_IE_prob"]
                    E_I_prob = config["SeedsConfiguration"]["SLiM_burnin_epi"]["E_I_prob"]
                    E_R_prob = config["SeedsConfiguration"]["SLiM_burnin_epi"]["E_R_prob"]
                    latency_prob = config["SeedsConfiguration"]["SLiM_burnin_epi"]["latency_prob"]
                    I_R_prob = config["SeedsConfiguration"]["SLiM_burnin_epi"]["I_R_prob"]
                    I_E_prob = config["SeedsConfiguration"]["SLiM_burnin_epi"]["I_E_prob"]
                    R_S_prob = config["SeedsConfiguration"]["SLiM_burnin_epi"]["R_S_prob"]
                    host_size = config["NetworkModelParameters"]["host_size"]

                    error = run_seed_generation(
                        method=method,
                        wk_dir=cwdir,
                        seed_size=seed_size,
                        use_subst_matrix=use_subst_matrix, 
                        mu=mu,
                        mu_matrix=mu_matrix,
                        n_gen=n_gen,
                        seeded_host_id=seeded_host_id,
                        S_IE_prob=S_IE_prob,
                        E_I_prob=E_I_prob,
                        E_R_prob=E_R_prob,
                        latency_prob=latency_prob,
                        I_R_prob=I_R_prob,
                        I_E_prob=I_E_prob,
                        R_S_prob=R_S_prob,
                        host_size=host_size,
                        ref_path=ref_path,
                        rand_seed=rand_seed
                    )

                elif method == "user_input":
                    path_seeds_vcf = config["SeedsConfiguration"]["user_input"]["path_seeds_vcf"]
                    path_seeds_phylogeny = config["SeedsConfiguration"]["user_input"]["path_seeds_phylogeny"]
                    error = run_seed_generation(
                        method=method,
                        wk_dir=cwdir,
                        seed_size=seed_size,
                        seed_vcf=path_seeds_vcf,
                        path_seeds_phylogeny=path_seeds_phylogeny,
                        rand_seed=rand_seed
                    )

                if error is not None:
                    raise Exception(error)
                
                messagebox.showinfo("Success", "Seed generation completed successfully!")

            except Exception as e:
                messagebox.showerror("Seed Generation Error", str(e))

        column = 1
        frow = 100
        component = EasyButton(
            "Run Seed Generation",
            self.control_frame,
            column,
            frow,
            seed_generation,
            hide,
            "ew",
        )
        self.visible_components.add(component)
        return component

    def load_page(self):
        to_renderer, to_derenderer = None, None

        self.render_seeds_size(False, column=1, columnspan=3, frow=1)
        self.use_reference_control = self.render_use_reference(
            to_renderer, to_derenderer, False, column=1, frow=4, columnspan=3
        )

        if self.use_reference:
            hide = True
            self.use_method_controls = self.render_use_method(
                column=1,
                frow=7,
                to_rerender=to_renderer,
                to_derender=to_derenderer,
                hide=hide,
                width=20,
                column_span=3,
            )
            self.user_input_group_controls = self.init_user_input_group(hide)
            self.wf_group_controls = self.init_wf_group(hide)
            self.epi_group_controls = self.init_epi_group(hide)
            self.run_button_control = self.render_run_button(hide)

        else:
            hide = False

            self.use_method_controls = self.render_use_method(
                column=1,
                frow=7,
                to_rerender=to_renderer,
                to_derender=to_derenderer,
                hide=hide,
                width=20,
                column_span=3,
            )
            
            match self.method:
                case "user_input":
                    # self.burn_in_settings_label = self.display_burn_in_settings_label(hide, column=1, frow=9)
                    self.user_input_group_controls = self.init_user_input_group(hide)
                    self.wf_group_controls = self.init_wf_group(not hide)
                    self.epi_group_controls = self.init_epi_group(not hide)
                    self.run_button_control = self.render_run_button(hide)
                case "SLiM_burnin_WF":
                    # self.burn_in_settings_label = self.display_burn_in_settings_label(hide, column=1, frow=9)
                    self.wf_group_controls = self.init_wf_group(hide)
                    self.user_input_group_controls = self.init_user_input_group(not hide)
                    self.epi_group_controls = self.init_epi_group(not hide)
                    self.run_button_control = self.render_run_button(hide)
                case "SLiM_burnin_epi":
                    # self.burn_in_settings_label = self.display_burn_in_settings_label(hide, column=0, frow=9)
                    self.epi_group_controls = self.init_epi_group(hide)
                    self.user_input_group_controls = self.init_user_input_group(not hide)
                    self.wf_group_controls = self.init_wf_group(not hide)
                    self.run_button_control = self.render_run_button(hide)
                case _:
                    raise ValueError("Invalid method")

        match self.method:
            case "user_input":
                derender = [
                    self.wf_group_controls,
                    self.epi_group_controls,
                    self.epi_group_controls,
                ]
                self.use_method_controls.set_to_derender(GroupControls(derender).derender_itself)
                self.use_method_controls.set_to_rerender(self.user_input_group_controls.rerender_itself)
            case "SLiM_burnin_WF":
                derender = [
                    self.user_input_group_controls,
                    self.epi_group_controls,
                    self.epi_group_controls,
                ]
                self.use_method_controls.set_to_derender(GroupControls(derender).derender_itself)
                self.use_method_controls.set_to_rerender(self.wf_group_controls.rerender_itself)
            case "SLiM_burnin_epi":
                derender = [
                    self.user_input_group_controls,
                    self.wf_group_controls,
                    self.epi_group_controls,
                ]
                self.use_method_controls.set_to_derender(
                    GroupControls(derender).derender_itself
                )
                self.use_method_controls.set_to_rerender(
                    self.epi_group_controls.rerender_itself
                )
            case _:
                raise ValueError("Invalid method")

        renders = [self.use_method_controls, self.run_button_control]

        match self.method:
            case "user_input":
                renders.append(self.user_input_group_controls)
            case "SLiM_burnin_WF":
                renders.append(self.wf_group_controls)
            case "SLiM_burnin_epi":
                renders.append(self.epi_group_controls)
            case _:
                raise ValueError("Invalid method")

        use_reference_to_rerender = GroupControls(renders).rerender_itself
        use_reference_to_derender = GroupControls(renders).derender_itself
        self.use_reference_control.set_to_rerender(use_reference_to_rerender)
        self.use_reference_control.set_to_derender(use_reference_to_derender)

        # use_references = [
        #     self.wf_group_controls,
        #     self.epi_group_controls,
        #     self.user_input_group_controls
        # ]
        # use_reference_to_derender = GroupControls(use_references).derender_itself


#
# return


# if not self.use_reference:
#     rerender_components(self.use_method_components, self.use_method_grid_configs)

# self.user_input_components = self.init_user_input_group()
# self.user_input_grid_configs = derender_components(self.user_input_components)

# self.wf_components = self.init_wf_group()
# self.wf_grid_configs = derender_components(self.wf_components)

# self.epi_components = self.init_epi_group()
# self.epi_grid_configs = derender_components(self.epi_components)

# match self.method:
#     case "user_input":
#         rerender_components(self.user_input_components, self.user_input_grid_configs)
#     case "SLiM_burnin_WF":
#         rerender_components(self.wf_components, self.wf_grid_configs)
#     case "SLiM_burnin_epi":
#         rerender_components(self.epi_components, self.epi_grid_configs)
