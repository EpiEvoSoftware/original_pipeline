import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from utils import *


# TODO add line breaks to path rendering if too long, add None selected if path is empty


class Configurationv3:
    def __init__(
        self, parent, tab_parent, config_path, tab_title, tab_index, hide=False
    ):
        self.config_path = config_path
        self.cwd = load_config_as_dict(self.config_path)["BasicRunConfiguration"][
            "cwdir"
        ]
        self.n_replicates = load_config_as_dict(self.config_path)[
            "BasicRunConfiguration"
        ]["n_replicates"]
        self.random_number_seed = load_config_as_dict(self.config_path)[
            "BasicRunConfiguration"
        ]["random_number_seed"]
        self.ref_path = load_config_as_dict(self.config_path)["GenomeElement"][
            "ref_path"
        ]
        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_index = tab_index

        self.tab_parent.add(self.parent, text=tab_title)

        self.control_frame = ttk.Frame(self.parent, width=300)

        self.control_frame.pack(padx=10, pady=10)

        self.render_working_directory()
        self.render_ref_path_label()
        self.render_n_replicates()
        self.render_random_seed()

        render_next_button(self.tab_index, self.tab_parent, self.parent, self.update)

    # def render_next_button(self):
    #     def next_tab_fx():
    #         match update():
    #             case 1:
    #                 return
    #         go_to_next_tab(tab_index, tab_parent)

    #     next_button()

    def render_working_directory(self):
        def choose_directory_button():
            choose_directory_button = tk.Button(
                self.control_frame,
                text="Choose Directory",
                command=self.choose_directory,
            )
            choose_directory_button.grid(row=2, column=0, sticky="e")

        choose_directory_button()

    def update(self):
        error_messages = []
        self.update_n_replicates(error_messages)
        self.update_random_seed(error_messages)
        if len(error_messages) == 0:
            return 0
        else:
            error_message_str = "\n".join(error_messages)
            messagebox.showerror("Update Error", error_message_str)
            return 1
    def update_random_seed(self, error_messages):
        try:
            new_random_seed = int(self.random_seed_entry.get())
            config = load_config_as_dict(self.config_path)
            config["BasicRunConfiguration"]["random_number_seed"] = new_random_seed
            save_config(self.config_path, config)
        except ValueError:
            error_messages.append("Please enter a valid integer for the random seed.")
            
    def update_n_replicates(self, error_messages):
        """
        note: int() doesn't process scientific notation for strings but float() does
        """
        try:
            new_n_replicates = int(float(self.n_replicates_entry.get()))
            config = load_config_as_dict(self.config_path)
            config["BasicRunConfiguration"]["n_replicates"] = new_n_replicates
            save_config(self.config_path, config)
        except ValueError:
            error_messages.append(
                "Please enter a valid integer for the number of replicates."
            )

    def render_n_replicates(self):
        self.working_directory_label = ttk.Label(
            self.control_frame, text="Working Directory:", style="Bold.TLabel"
        )
        self.working_directory_label.grid(row=0, column=0, pady=5, sticky="w")
        CreateToolTip(self.working_directory_label, "hello world")
        if self.cwd == "":
            self.user_working_directory_label = ttk.Label(
                self.control_frame,
                text="None Selected",
                foreground="black",
                width=minwidth,
            )
        else:
            self.user_working_directory_label = ttk.Label(
                self.control_frame, text=self.cwd, foreground="black", width=minwidth
            )

        self.user_working_directory_label.grid(row=1, column=0, pady=5, sticky="w")

        self.n_replicates_label = ttk.Label(
            self.control_frame,
            text="Number of Simulation Replicates (Integer)",
            style="Bold.TLabel",
        )

        self.n_replicates_label.grid(row=7, column=0, sticky="w", pady=5)
        self.n_replicates_entry = ttk.Entry(
            self.control_frame, foreground="black", width=20
        )
        self.n_replicates_entry.grid(row=8, column=0, sticky="w", pady=5)
        self.n_replicates_entry.insert(0, self.n_replicates)
        
    def render_random_seed(self):
        random_seed_label = ttk.Label(self.control_frame, text="Random Seed (Integer)", style="Bold.TLabel")
        random_seed_label.grid(row=9, column=0, sticky="w", pady=5)
        self.random_seed_entry = ttk.Entry(self.control_frame, foreground="black", width=20)
        self.random_seed_entry.grid(row=10, column=0, sticky="w", pady=5)
        self.random_seed_entry.insert(0, str(self.random_number_seed))

    def render_ref_path_label(self):
        ref_path_label = ttk.Label(
            self.control_frame,
            text="Pathogen Reference Genome File (FASTA Format)",
            style="Bold.TLabel",
        )
        ref_path_label.grid(row=4, column=0, sticky="ew", pady=5)

        if self.ref_path == "":
            self.ref_path_label = ttk.Label(
                self.control_frame,
                text="None selected",
                foreground="black",
                width=minwidth,
            )
        else:
            self.ref_path_label = ttk.Label(
                self.control_frame,
                text=self.ref_path,
                foreground="black",
                width=minwidth,
            )

        self.ref_path_label.grid(row=5, column=0, pady=5, sticky="w")

        choose_ref_path_button = tk.Button(
            self.control_frame, text="Choose File", command=self.choose_ref_path
        )
        choose_ref_path_button.grid(row=6, column=0, sticky="e", pady=5)

    def choose_directory(self):
        chosen_directory = filedialog.askdirectory(title="Select a Directory")
        if chosen_directory:
            self.cwd = chosen_directory
            self.user_working_directory_label.config(
                text=f"{self.cwd}"
            )  # Update the label with the new directory
            config = load_config_as_dict(self.config_path)
            config["BasicRunConfiguration"]["cwdir"] = self.cwd
            save_config(self.config_path, config)

    def choose_ref_path(self):
        filetypes = (  # don't need to check if its genome file: or use python package jaehee said
            (
                "Genome files",
                (
                    "*.fasta",
                    "*.fa",
                    "*.gb",
                    "*.gtf",
                    "*.vcf",
                    "*.bam",
                    "*.sam",
                    "*.fna",
                ),
            ),
            ("All files", "*.*"),
        )
        # chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File", filetypes=filetypes)
        chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File")
        if chosen_file:
            self.ref_path = chosen_file
            self.ref_path_label.config(text=self.ref_path)
            config = load_config_as_dict(self.config_path)
            config["GenomeElement"]["ref_path"] = self.ref_path
            save_config(self.config_path, config)
