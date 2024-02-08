import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class EpiModel:
    def __init__(self, parent, tab_parent, config_file):
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