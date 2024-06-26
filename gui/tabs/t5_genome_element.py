import tkinter as tk
from tkinter import ttk, messagebox
from utils import *
from genetic_effect_generator import run_effsize_generation


# TODO: fix ui for next button
class GenomeElement(TabBase):
    def __init__(
        self, parent, tab_parent, config_path, tab_title, tab_index, hide=False
    ):
        super().__init__(parent, tab_parent, config_path, tab_title, tab_index, hide)

    def load_page(self):
        render_next_button_v2(
            self.tab_index,
            self.tab_parent,
            self.parent,
            None,
            self.global_update,
        )
        ui_selected = self.generate_genetic_architecture_method == "user_input"
        rg_selected = self.generate_genetic_architecture_method == "randomly_generate"
        hide = not self.use_genetic_model
        self.global_group_control = GroupControls()
        self.init_landing_group(hide=False)
        self.init_num_traits_group(hide=hide)
        self.init_user_input_group(ui_selected, hide=hide)
        self.init_random_generate_group(rg_selected, hide=hide)

    def init_landing_group(self, hide=False):
        self.render_simulation_settings_title(False, 0, self.frow_val, 1)
        self.use_genetic_model_component = self.render_use_genetic_model(
            None, None, hide, 0, self.frow_val + 1, 1
        )

    def init_num_traits_group(self, hide=False):
        number_of_traits_title = self.render_number_of_traits_title(
            hide, 0, self.frow_val + 4
        )
        transmissibility = self.render_transmissibility(hide, 0, self.frow_val + 5)
        drug_resistance = self.render_drug_resistance(hide, 1, self.frow_val + 5)

        self.generate_genetic_architecture_method = (
            self.render_generate_genetic_architecture_method(
                50, 0, self.frow_val + 7, None, None, hide, 30
            )
        )

        num_traits_group_control = [
            number_of_traits_title,
            transmissibility,
            drug_resistance,
            self.generate_genetic_architecture_method,
        ]

        self.num_traits_group_control = GroupControls()
        for control in num_traits_group_control:
            self.num_traits_group_control.add(control)
        self.global_group_control.add(self.num_traits_group_control)
    
    def init_user_input_group(self, ui_selected, hide=False):
        hide: bool
        if not hide:
            if ui_selected:
                hide = False
            else:
                hide = True

        self.user_input_group_control = self.render_path_eff_size_table(
            hide, 0, self.frow_val + 9, 2
        )
        self.global_group_control.add(self.user_input_group_control)

    def init_random_generate_group(self, rg_selected, hide=False):
        if not hide:
            if rg_selected:
                hide = False
            else:
                hide = True

        gff = self.render_gff(hide, 0, self.frow_val + 9, 1)

        genes_num = self.render_genes_num(hide, 0, self.frow_val + 12)

        effsize_min = self.render_effsize_min(hide, 0, self.frow_val + 14)

        effsize_max = self.render_effsize_max(hide, 0, self.frow_val + 16)

        normalize = self.render_normalize(hide, 1, self.frow_val + 9)

        normalize_f_trait = self.render_normalize_f_trait(hide, 1, self.frow_val + 12)
        self.f_trait_control = normalize_f_trait

        run_button = self.render_run_button(hide, 0, self.frow_val + 31)

        random_generate_group_control = [
            gff,
            genes_num,
            effsize_min,
            effsize_max,
            normalize,
            normalize_f_trait,
            run_button,
        ]

        self.random_generate_group_control = GroupControls()
        for control in random_generate_group_control:
            self.random_generate_group_control.add(control)
        self.global_group_control.add(self.random_generate_group_control)

    def render_gff(self, hide=True, column=None, frow=None, columnspan=1):
        keys_path = ["GenomeElement", "effect_size", "randomly_generate", "gff"]
        config_path = self.config_path
        render_text = "Please provide the genome annotation in a gff-like format:"
        control_frame = self.control_frame
        component = EasyPathSelector(
            keys_path,
            config_path,
            render_text,
            control_frame,
            column,
            hide,
            frow,
            columnspan,
        )

        if not hide:
            self.visible_components.add(component)
        return component

    def render_simulation_settings_title(self, hide=True, column=None, frow=None, columnspan=1):
        self.render_simulation_settings_title_text = "Simulation Settings"
        self.number_of_traits_label = EasyTitle(
            self.render_simulation_settings_title_text,
            self.control_frame,
            column,
            frow,
            hide,
            columnspan,
        )

    def render_number_of_traits_title(self, hide=True, column=None, frow=None):
        self.render_number_of_traits_text = "Number of traits (Integer):"
        component = EasyLabel(
            self.render_number_of_traits_text, self.control_frame, column, frow, hide
        )
        self.visible_components.add(component)
        return component

    def render_transmissibility(self, hide=True, column=None, frow=None):
        keys_path = ["GenomeElement", "traits_num", "transmissibility"]
        self.render_transmissibility_text = "Transmissibility"
        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_transmissibility_text,
            "transmissibility",
            self.control_frame,
            column,
            frow,
            "integer",
            hide,
            columnspan=1,
        )
        self.visible_components.add(component)
        return component

    def render_drug_resistance(self, hide=True, column=None, frow=None):
        keys_path = ["GenomeElement", "traits_num", "drug_resistance"]
        self.render_drug_resistance_text = "Drug-Resistance"

        component = EasyEntry(
            keys_path,
            self.config_path,
            self.render_drug_resistance_text,
            "drug-resistance",
            self.control_frame,
            column,
            frow,
            "integer",
            hide,
            columnspan=1,
        )
        self.visible_components.add(component)
        return component

    def render_generate_genetic_architecture_method(
        self,
        columnspan,
        column=None,
        frow=None,
        to_rerender=None,
        to_derender=None,
        hide=True,
        width=20,
    ):
        """
        generate_genetic_architecture_method
        """
        keys_path = ["GenomeElement", "effect_size", "method"]
        text = ("Method to Generate the Genetic Architecture")

        def comboboxselected(var, to_rerender, to_derender):
            converted_var = render_to_val_generate_genetic_architecture_method.get(
                var.get(), ""
            )
            no_validate_update_val(converted_var, self.config_path, keys_path)
            match converted_var:
                case "user_input":
                    self.generate_genetic_architecture_method.set_to_rerender(
                        self.user_input_group_control.rerender_itself
                    )
                    self.generate_genetic_architecture_method.set_to_derender(
                        self.random_generate_group_control.derender_itself
                    )
                case "randomly_generate":
                    self.generate_genetic_architecture_method.set_to_rerender(
                        self.random_generate_group_control.rerender_itself
                    )
                    self.generate_genetic_architecture_method.set_to_derender(
                        self.user_input_group_control.derender_itself
                    )
                case _:
                    raise ValueError("Invalid method specified")
            if to_rerender:
                to_rerender()
            if to_derender:
                to_derender()

        component = EasyCombobox(
            keys_path,
            self.config_path,
            text,
            self.control_frame,
            column,
            frow,
            generate_genetic_architecture_method_values,
            to_rerender,
            to_derender,
            comboboxselected,
            hide,
            width,
            columnspan,
            val_to_render_generate_genetic_architecture_method,
        )
        self.visible_components.add(component)
        return component

    def render_genes_num(self, hide=True, column=None, frow=None):
        keys_path = ["GenomeElement", "effect_size", "randomly_generate", "genes_num"]
        render_text = "Number of Genomic Regions for each trait (list integer)"

        component = EasyEntry(
            keys_path,
            self.config_path,
            render_text,
            "genes_num",
            self.control_frame,
            column,
            frow,
            "list",
            hide,
            columnspan=1,
        )
        self.visible_components.add(component)
        return component

    def render_use_genetic_model(
        self, to_rerender, to_derender, hide=True, column=None, frow=None, columnspan=1
    ):
        keys_path = ["GenomeElement", "use_genetic_model"]
        render_use_genetic_model_text = "Do you want to use genetic architecture "
        "for traits (transmissibility/Drug-resistance)?"

        def radiobuttonselected(var, to_rerender, to_derender):
            no_validate_update(var, self.config_path, keys_path)
            if var.get():
                self.use_genetic_model = True
                self.global_group_control.rerender_itself()
            else:
                self.use_genetic_model = False
                self.global_group_control.derender_itself()

        component = EasyRadioButton(
            keys_path,
            self.config_path,
            render_use_genetic_model_text,
            "use_genetic_model",
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

    def render_effsize_min(self, hide=True, column=None, frow=None):
        keys_path = ["GenomeElement", "effect_size", "randomly_generate", "effsize_min"]
        render_text = (
            "Minimum Effect Size of each region for each trait (list numerical)"
        )
        component = EasyEntry(
            keys_path,
            self.config_path,
            render_text,
            "effsize_min",
            self.control_frame,
            column,
            frow,
            "list",
            hide,
            columnspan=1,
        )
        self.visible_components.add(component)
        return component

    def render_effsize_max(self, hide=True, column=None, frow=None):
        keys_path = ["GenomeElement", "effect_size", "randomly_generate", "effsize_max"]
        render_text = (
            "Maximum Effect Size of each region for each trait (list numerical)"
        )
        component = EasyEntry(
            keys_path,
            self.config_path,
            render_text,
            "effsize_min",
            self.control_frame,
            column,
            frow,
            "list",
            hide,
            columnspan=1,
        )
        self.visible_components.add(component)
        return component

    def render_normalize(
        self,
        hide=True,
        column=None,
        frow=None,
        to_rerender=None,
        to_derender=None,
        columnspan=1,
    ):
        def update(var, to_rerender, to_derender):
            if var.get():
                self.f_trait_control.label.configure(state="normal")
                self.f_trait_control.entry.configure(state="normal")
            else:
                self.f_trait_control.label.configure(state="disabled")
                self.f_trait_control.label.configure(state="disabled")
            
            config = load_config_as_dict(self.config_path)
            config["GenomeElement"]["effect_size"]["randomly_generate"]["normalize"] = var.get()
            save_config(self.config_path, config)

        render_text = "Whether to normalize randomly-selected effect sizes \nby the expected number of mutations?"
        keys_path = ["GenomeElement", "effect_size", "randomly_generate", "normalize"]
        component = EasyRadioButton(
            keys_path,
            self.config_path,
            render_text,
            "normalize",
            self.control_frame,
            column,
            frow,
            hide,
            to_rerender,
            to_derender,
            columnspan,
            update,
        )
        self.visible_components.add(component)
        return component
    
    def render_normalize_f_trait(self, hide=True, column=None, frow=None):
        keys_path = ["GenomeElement", "effect_size", "randomly_generate", "final_trait"]
        text = "Final trait normalization factor (Numerical)"
        component = EasyEntry(
            keys_path,
            self.config_path,
            text,
            "Final trait normalization factor",
            self.control_frame,
            column,
            frow,
            "numerical",
            hide,
            disabled=True,
            columnspan=1,
        )
        if not hide:
            self.visible_components.add(component)
        return component

    def render_path_eff_size_table(
        self, hide=True, column=None, frow=None, columnspan=1
    ):
        render_generate_genetic_architecture_file_text = (
            "Please provide the Genetic Architecture File in csv format:"
        )
        keys_path = ["GenomeElement", "effect_size", "randomly_generate", "gff"]
        config_path = self.config_path
        control_frame = self.control_frame

        filetype = (("CSV files", "*.csv"), ("All files", "*.*"))
        component = EasyPathSelector(
            keys_path,
            config_path,
            render_generate_genetic_architecture_file_text,
            control_frame,
            column,
            hide,
            frow,
            columnspan,
            filetype,
        )
        if not hide:
            self.visible_components.add(component)
        return component

    def effect_size_generation(self):
        if self.global_update_no_success_message() == 1:
            return

        config = load_config_as_dict(self.config_path)

        method = config["GenomeElement"]["effect_size"]["method"]
        wk_dir = config["BasicRunConfiguration"]["cwdir"]
        n_gen = config["EvolutionModel"]["n_generation"]
        num_seed = config["SeedsConfiguration"]["seed_size"]
        use_subst_matrix = config["EvolutionModel"]["subst_model_parameterization"] == "mutation rate matrix"
        mut_rate = config["EvolutionModel"]["mut_rate"]
        mu_matrix_values = config["EvolutionModel"]["mut_rate_matrix"]
        mu_matrix = json.dumps({"A": mu_matrix_values[0], "C": mu_matrix_values[1], 
                                "G": mu_matrix_values[2], "T": mu_matrix_values[3]})

        trait_n = config["GenomeElement"]["traits_num"]
        rand_seed = config["BasicRunConfiguration"]["random_number_seed"]
        ref = config["GenomeElement"]["ref_path"]

        if method == "user_input":
            effsize_path = config["GenomeElement"]["effect_size"]["user_input"]["path_effsize_table"]
        elif method == "randomly_generate":
            effsize_path = ""
            gff_in = config["GenomeElement"]["effect_size"]["randomly_generate"]["gff"]
            causal_sizes = config["GenomeElement"]["effect_size"]["randomly_generate"]["genes_num"]
            es_lows = config["GenomeElement"]["effect_size"]["randomly_generate"]["effsize_min"]
            es_highs = config["GenomeElement"]["effect_size"]["randomly_generate"]["effsize_max"]
            norm_or_not = config["GenomeElement"]["effect_size"]["randomly_generate"]["normalize"]
            final_T = config["GenomeElement"]["effect_size"]["randomly_generate"]["final_trait"]

            if norm_or_not:
                if n_gen <= 0:
                    messagebox.showerror("Value Error", "Number of Generations (Evolutionary Model) has to be a positive integer"
                                         " if normalization is turned on.")
                    return
                if not use_subst_matrix and mut_rate == 0:
                    messagebox.showerror("Value Error", "Mutation rate (Evolutionary Model) has to be a positive number"
                                         " if normalization is turned on.")
                    return
                if use_subst_matrix:
                    if sum(sum(lst) for lst in mu_matrix_values) == 0:
                        messagebox.showerror("Value Error", "Mutation rate matrix (Evolutionary Model) cannot be"
                                             " all 0s if normalization is turned on and using substitution matrix")
                        return
                    if ref == "":
                        messagebox.showerror("Value Error", "Pathogen Reference Genome File (Basic Configuration) must be provided"
                                            " if normalization is turned on and if using substitution matrix.")
                        return
        else:
            messagebox.showerror("Value Error", "Please select a method to generate the genetic architecture.")
            return

    
        err = run_effsize_generation(
            method,
            wk_dir,
            effsize_path=effsize_path,
            gff_in=gff_in,
            trait_n=trait_n,
            causal_sizes=causal_sizes,
            es_lows=es_lows,
            es_highs=es_highs,
            norm_or_not=norm_or_not,
            n_gen=n_gen,
            num_seed=num_seed,
            use_subst_matrix=use_subst_matrix,
            mut_rate=mut_rate,
            mu_matrix=mu_matrix,
            rand_seed=rand_seed,
            ref=ref,
            final_T=final_T
        )
        if err:
            messagebox.showerror("Generation Error", "Generation Error: " + str(err))
        else:
            messagebox.showinfo("Success", "Effect size generation completed successfully!")

    def render_run_button(self, hide=True, column=None, frow=None):
        button_text = "Run Effect Size Generation"
        run_button_component = EasyButton(
            button_text,
            self.control_frame,
            column,
            frow,
            self.effect_size_generation,
            hide,
        )
        if not hide:
            self.visible_components.add(run_button_component)
        return run_button_component

    def init_val(self, config_path):
        self.frow_val = 0

        self.render_nb = False
        self.config_path = config_path
        self.config_dict = load_config_as_dict(self.config_path)
        self.use_genetic_model = self.config_dict["GenomeElement"]["use_genetic_model"]
        self.transmissibility = self.config_dict["GenomeElement"]["traits_num"][
            "transmissibility"
        ]
        self.drug_resistance = self.config_dict["GenomeElement"]["traits_num"][
            "drug_resistance"
        ]

        self.generate_genetic_architecture_method = self.config_dict["GenomeElement"][
            "effect_size"
        ]["method"]
        self.path_effsize_table = self.config_dict["GenomeElement"]["effect_size"][
            "user_input"
        ]["path_effsize_table"]
        self.gff = self.config_dict["GenomeElement"]["effect_size"][
            "randomly_generate"
        ]["gff"]
        self.genes_num = self.config_dict["GenomeElement"]["effect_size"][
            "randomly_generate"
        ]["genes_num"]
        self.effsize_min = self.config_dict["GenomeElement"]["effect_size"][
            "randomly_generate"
        ]["effsize_min"]
        self.effsize_max = self.config_dict["GenomeElement"]["effect_size"][
            "randomly_generate"
        ]["effsize_max"]
        self.normalize = self.config_dict["GenomeElement"]["effect_size"][
            "randomly_generate"
        ]["normalize"]
