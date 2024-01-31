import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class EpiModel:
    def __init__(self, parent, tab_parent, config_file):

        self.parent = parent
        self.tab_parent = tab_parent

        # self.canvas = tk.Canvas(self.parent)
        # self.scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # # Place the canvas and the scrollbar in the parent frame
        # self.scrollbar.pack(side='right', fill='y')
        # self.canvas.pack(side='left', fill='both', expand=True)

        # # Create a frame inside the canvas
        # self.control_frame = ttk.Frame(self.canvas)

        # # Add the new frame to a window in the canvas
        # self.canvas_frame = self.canvas.create_window((0,0), window=self.control_frame, anchor='nw')
        
        # # Bind the frame's width to the canvas's width and configure the canvas's scrollregion
        # self.control_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # self.canvas.bind('<Configure>', self.frame_width) #fix

        self.control_frame = ttk.Frame(self.parent, width=300)
        self.control_frame.pack(fill='both', expand=True)  # Pack the frame

        self.surname_label = ttk.Label(self.control_frame, text="Model")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["SIR", "SEIR"], foreground="White")
        self.surname_combobox.pack()

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

        self.surname_label = ttk.Label(self.control_frame, text="Latency Probability")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="E->I")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="I->E")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="E->R")
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
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["On", "Off"], foreground="White")
        self.surname_combobox.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Number of Massive Sampling Event")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.name_label = ttk.Label(self.control_frame, text="Generation")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.name_label = ttk.Label(self.control_frame, text="Sample Probability")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.name_label = ttk.Label(self.control_frame, text="Recovery Probability Afterwards")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Treatment")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, values=["On", "Off"], foreground="White")
        self.surname_combobox.pack()

        self.name_label = ttk.Label(self.control_frame, text="Number of Epochs")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()

        self.surname_label = ttk.Label(self.control_frame, text="Start")
        self.surname_label.pack()
        self.surname_combobox = ttk.Combobox(self.control_frame, foreground="White")
        self.surname_combobox.pack()

        self.name_label = ttk.Label(self.control_frame, text="End")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.control_frame, foreground="White")
        self.name_entry.pack()
