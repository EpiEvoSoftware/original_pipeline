"""
Visualization App
"""
import matplotlib
import numpy
import math
import traceback
matplotlib.use('TkAgg')

# Modules to embed matplotlib in a custom Tkinter window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import networkx as nx

# File support to load data files
import tkinter as tk
from tkinter import font, filedialog, messagebox
import sys, os, os.path

# The graph implementation
import bar_graph
import tools
import create_graph
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import codes.network_generate as network_generate


class Visualizer(object):
    """
    A class providing a visualization app.

    This class has many attributes for GUI widgets (buttons and labels). We do not list 
    all of them here.
    """
    # INSTANCE ATTRIBUTES:
    
    # Maximum allowable m value
    MAX_VAL = 20

    @classmethod
    def launch(cls,filename,k):
        """
        Launches the visualizer and starts the application loop.

        Parameter filename: The name of the initial dataset
        Precondition: filename is a valid file path OR None.

        Parameter k: The initial number of clusters
        Precondition: k is an int
        """
        cls(filename,k)
        tk.mainloop()

    def __init__(self, filename=None, k=3):
        """
        Initializes a visualization app.

        The initial dataset and k value are optional.  By default, it will
        choose the first dataset from the dataset directory.

        Parameter filename: The name of the initial dataset
        Precondition: filename is a valid file path OR None.

        Parameter k: The initial number of clusters
        Precondition: k is an int
        """
        self._network_dict = {
            "Erdős–Rényi": "ER",
            "Barabási-Albert": "BA", 
            "Random Partition": "RP"
        }
        
        self._root = tk.Tk()
        self._root.wm_title("Network Visualizer")
        self._dset  = None
        self._kmean = None

        # Start the application
        # empty_figure = create_graph.empty_figure()
        # self._config_canvas(empty_figure, is_empty=True)

        er_graph = network_generate.ER_generate(pop_size=1000, p_ER=0.15)
        fig = create_graph.create_plot(er_graph)
        fig

        self._config_canvas(fig, is_empty=False)
        self._network_type = "ER"
        # setting init to Erdos network
        self._config_control()
        if not k is None:
            self._kval.set(k)

        if filename:
            self._select_data(filename,False)
        else:
            self._select_data()
        self._canvas.draw()

    def _config_canvas(self, figure, is_empty=False):
        """
        Loads the MatPlotLib drawing code
        """
        self._canvas = FigureCanvasTkAgg(figure, master=self._root)
        self._canvas._tkcanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def _config_control(self):
        """
        Creates the control panel on the right hand side
        """
        panel = tk.Frame(master=self._root)
        panel.columnconfigure(0,pad=3)
        panel.columnconfigure(1,pad=3,minsize=150)
        panel.rowconfigure(0,pad=3)
        panel.rowconfigure(1,pad=0)
        panel.rowconfigure(2,pad=23)
        panel.rowconfigure(3,pad=3)
        panel.rowconfigure(4,pad=3)
        panel.rowconfigure(5,pad=3)
        panel.rowconfigure(6,pad=3)
        panel.rowconfigure(7,pad=13)
        panel.columnconfigure(2,minsize=20)

        title = tk.Label(master=panel,text='Network',height=3)
        wfont = font.Font(font=title['font'])
        wfont.config(weight='bold',size=20)
        title.grid(row=0,columnspan=2, sticky='we')
        title.config(font=wfont)

        divider = tk.Frame(master=panel,height=2, bd=1, relief=tk.SUNKEN)
        divider.grid(row=1,columnspan=2, sticky='we')


        label = tk.Label(master=panel,text='Network: ',height=2)
        wfont = font.Font(font=label['font'])
        wfont.config(weight='bold')
        label.config(font=wfont)
        label.grid(row=2,column=0, sticky='e')

        self._kfile = tk.StringVar(master=self._root)
        self._kfile.set("Erdős–Rényi")
        # options = tk.OptionMenu(panel,self._kfile,*["Erdős–Rényi", "Barabási-Albert", "Random Partition"],command=self._reset)
        options = tk.OptionMenu(panel,self._kfile,*["Erdős–Rényi", "Barabási-Albert", "Random Partition"])

        options.grid(row=2,column=1,sticky='w')

        # Label and option menu to select m-value
        label = tk.Label(master=panel,text='M Value: ',height=2,font=wfont)
        label.grid(row=3,column=0,sticky='e')

        self._kval = tk.IntVar(master=self._root)
        options = tk.OptionMenu(panel,self._kval,*range(1,self.MAX_VAL+1),command=self._reset)
        options.grid(row=3,column=1,sticky='w')

        # visualize button
        button = tk.Button(master=panel, text='Visualize', width=6, command=self._visualize)
        button.grid(row=10, column=1)


        panel.pack(side=tk.RIGHT, fill=tk.Y)


    def _plot(self):
        """
        Plots the data as it can.
        
        This function replots the data any time that it changes.
        """  
        self._canvas.draw()

    def _select_data(self,file=None,local=True):
        """
        Selects a data set, either from the data directory or user choice
        
        Parameter file: The (local) file for the data set
        Precondition: file is a string.  It is either '<select file>', the name
        of a file, or a prefix of a 2d data set in the data directory.
        
        Parameter local: Whether to chose the file from the data directory
        Precondition: local is a boolean
        """
        if file is None:
            file = self._kfile.get()
        if file == '<select file>':
            filename = filedialog.askopenfilename(initialdir='.',title='Select a Data File',
                                                    filetypes=[('CSV Data Files', '.csv')])
            self._kfile.set(self._shortname(filename))
        elif local:
            filename = os.path.join(os.path.split(__file__)[0],'data',file+'-2d.csv')
        else:
            filename = file
            self._kfile.set(self._shortname(filename))
        
        try:
            contents = tools.data_for_file(filename)
            message  = None
            if len(contents) == 0 or len(contents[0]) == 0:
                messagebox.showwarning('Load','The dataset is empty')
                return
            elif len(contents[0]) == 1:
                for pos in range(len(contents)):
                    contents[pos] = (contents[pos][0],0.5)
            elif len(contents[0]) > 2:
                for pos in range(len(contents)):
                    contents[pos] = contents[pos][:2]
            self._load_data(contents)
            if message:
                messagebox.showwarning('Load',message)
        except AssertionError as e:
            messagebox.showwarning('Load',str(e))
        except:
            traceback.print_exc()
            messagebox.showwarning('Load','ERROR: An unknown error occurred.')

    def _load_data(self, contents):
        """
        Loads a data set file into a Dataset object.
        
        Parameter contents: The contents of the dataset
        Precondition: contents is a 2d rectangular table
        """
        try:
            self._dset = "TODO: Implement"
            if not self._dset.getContents():
                raise RuntimeError()
            #self._filebutton.configure(text=shortname)
            self._kmean = None
            self._reset()
            # self._plot()
        except RuntimeError:
            messagebox.showwarning('Load','ERROR: Runtime Error.')
        except:
            traceback.print_exc()
            messagebox.showwarning('Load','ERROR: An unknown error occurred.')

    def _reset(self,k=None):
        """
        Resets GUI
        """
        # TODO: Implement
        if k is None:
            k = self._kval.get()
        if self._dset is None:
            messagebox.showwarning('Reset','ERROR: Ignore this Error')

        self._count = 0
        self._countlabel.configure(text='0')
        self._finished = False
        self._finishlabel.configure(text='False')


    def _visualize(
            self, 
            network_type="ER",
            pop_size=1000, 
            p_ER=0.15, 
            m = 2,
            rp_size = [400, 600], 
            p_within = [0.1, 0.07], 
            p_between = 0.02
            ):
        """
        Visualizes Network Graph
        """
        selected_option = self._kfile.get()
        selected_network_model = self._network_dict[selected_option]
        
        if network_type is None:
            tk.messagebox.showwarning('Visualize','ERROR: No network type was specified.')
        if selected_network_model == "BA":
            tk.messagebox.showwarning('Visualize','BA')
        #     # tk.messagebox.showwarning('Visualize','BA.')
        #     plot = network_generate.ba_generate(pop_size, m)
        #     figure = create_graph.create_plot(plot)
        #     self._canvas = FigureCanvasTkAgg(figure, master=self._root)
        #     # self._canvas._tkcanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        #     self._network_type = "BA"
        #     self._canvas.draw()
            # tk.messagebox.showwarning('Visualize','ER.')
            plot = network_generate.ba_generate(pop_size, m)
            figure = create_graph.create_plot(plot)
            self._canvas = FigureCanvasTkAgg(figure, master=self._root)
            # self._canvas._tkcanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

            self._config_canvas(figure, is_empty=False)
            # setting init to Erdos network
            # self._config_control()
            self._canvas.draw()

            return
        if selected_network_model == "ER":
            # tk.messagebox.showwarning('Visualize','ER.')
            plot = network_generate.ER_generate(pop_size, p_ER)
            figure = create_graph.create_plot(plot)
            self._canvas = FigureCanvasTkAgg(figure, master=self._root)
            # self._canvas._tkcanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            self._network_type = "ER"
            self._canvas.draw()
            return
        # elif selected_network_model == "BA":
        #     # tk.messagebox.showwarning('Visualize','BA.')
        #     plot = network_generate.ba_generate(pop_size, m)
        #     figure = create_graph.create_plot(plot)
        #     self._canvas = FigureCanvasTkAgg(figure, master=self._root)
        #     # self._canvas._tkcanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        #     self._network_type = "BA"
        #     self._canvas.draw()
            return
        elif selected_network_model == "RP":
            # tk.messagebox.showwarning('Visualize','RP.')
            plot = network_generate.rp_generate(rp_size, p_within, p_between)
            figure = create_graph.create_plot(plot)
            self._canvas = FigureCanvasTkAgg(figure, master=self._root)
            # self._canvas._tkcanvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            self._network_type = "RP"
            self._canvas.draw()
            return
        elif selected_option == "button":
            tk.messagebox.showwarning('Visualize','buantsoijasfidspecified.')
            return "Hello Button Pressed"
        else:
            tk.messagebox.showwarning('Visualize','ERROR: Unsupported network type was specified.')

        # self._plot(draw)

        
        self._count = self._count+1
        self._countlabel.configure(text=str(self._count))
        self._finished = self._kmean.step()
        self._finishlabel.configure(text=str(self._finished))
        
        # self._plot()

    def _shortname(self,filename):
        """
        Returns the short name of a file.
        
        This is used to display the active file, when possible. It removes any
        parent directories, any file type information, and shortens the name to
        10 characters.
        
        Parameter filename: The name of the file
        Precondition: filename is a string representing a valid file path
        """
        name = os.path.split(filename)[1]
        name = os.path.splitext(name)[0]
        if (len(name) > 10):
            name = name[0:10]+'...'
        return name
