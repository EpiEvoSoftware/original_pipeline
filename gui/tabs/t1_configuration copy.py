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