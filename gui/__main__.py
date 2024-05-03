"""
An application for visualizing networks

This file is the main entry-point for the GUI application. 
"""
import argparse
import os.path
import shutil
import tkinter as tk
from tkinter import ttk
import json
import tkinter.font as tkFont
import sys

enivol_dir = os.path.join(os.path.dirname(__file__), '../enivol_packaging/enivol')
if enivol_dir not in sys.path:
    sys.path.insert(0, enivol_dir)

from tabs.t1_configuration import Configuration
from tabs.t1_configuration_v2 import Configurationv2
from tabs.t1_configuration_v3 import Configurationv3
from tabs.t2_evolutionarymodel import EvolutionaryModel
from tabs.t3_networkmodel import NetworkModel
from tabs.t4_seeds_configuration import SeedsConfiguration
from tabs.t5_genome_element import GenomeElement
# from tabs.t5_genome_element_v2 import GenomeElementv2
from tabs.t6_networkgraph import NetworkGraphApp
from tabs.t7_epidemiology_model import EpidemiologyModel
from tabs.t7_epidemiology_model_v2 import EpidemiologyModelv2
from tabs.t7_epidemiology_model_v3 import EpidemiologyModelv3
from tabs.t8_post_processing import PostProcessing


def load_config(config_path):
    """
    loads configuration file into python from a path
    """
    with open(config_path, 'r') as file:
        return json.load(file)
    
def load_config_as_dict(config_file):
    """
    Loads the configuration from a file into a dictionary.

    Parameters:
        config_file (str): The path to the configuration file

    Returns:
        dict: Dictionary containing the configuration settings.
    """
    try:
        config_dict = {}
        with open(config_file, 'r') as file:
            for line in file:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    config_dict[key.strip()] = value.strip()
        return config_dict
    except FileNotFoundError:
        print(f"Configuration file {config_file} not found.")
        return None

def initialize_configuration(default_config_path, user_config_path):
    shutil.copy(default_config_path, user_config_path)
    return user_config_path

def parse_args():
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog='cluster', description='Application to view GUI')
    parser.add_argument('--config_path', type=str,
                        help='path to the configuration JSON file', default="enivol_packaging/enivol/config_template/user_config.json")
    parser.add_argument('-v', '--view', action='store_true',
                        help='visualize network graph')
    parser.add_argument('--hide', action='store_true', help='Set hide to False, default is True')
    return parser.parse_args()


def validate_input(P):
    if P.strip() in ["e", ".", ""]:
            return True
    return P.isdigit()
def launch_gui(default_config_path, user_config_path, hide=False):
    """
    Launches the gui application
    """
    root = tk.Tk()
    root.iconbitmap('')
    style = ttk.Style(root)
    if 'aqua' in style.theme_names():
        style.theme_use('aqua')
    root.title("EnivolCrossing: Simulation Framework for Genetic Epidemiology")
    
    if user_config_path == "enivol_packaging/enivol/config_template/user_config.json":
        config_path = initialize_configuration(default_config_path, user_config_path)
    else:
        config_path = user_config_path

    tab_parent = ttk.Notebook(root)
     
    style = ttk.Style()
    default_font = tkFont.nametofont("TkDefaultFont")

    font_family = default_font.cget("family")
    font_size = default_font.cget("size")
    style.configure("Bold.TLabel", font=(font_family, font_size, 'bold'))
    style.configure("Title.TLabel", font=(font_family, font_size+4, 'bold'))

    # if tk.Tcl().eval('set tcl_platform(threaded)'):
    #     print('Threading is enabled')
    # else:
    #     print('Threading is disabled, application might not run as expected. Please enable threading in your python installation.')
        


    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)
    tab3 = ttk.Frame(tab_parent)
    tab4 = ttk.Frame(tab_parent)
    tab5 = ttk.Frame(tab_parent)
    tab6 = ttk.Frame(tab_parent)
    tab7 = ttk.Frame(tab_parent)
    tab8 = ttk.Frame(tab_parent)

    network_app = Configurationv3(tab1, tab_parent, config_path, "Basic Configuration", 0, hide)
    network_app = EvolutionaryModel(tab2, tab_parent, config_path, "Evolutionary Model", 1, hide)
    network_graph_app = None
    network_model_app = NetworkModel(tab3, tab_parent, network_graph_app, config_path, "Network Model Parameters", 3, hide )
    network_app = SeedsConfiguration(tab4, tab_parent, config_path, "Seeds Configuration", 4, hide )
    network_app = GenomeElement(tab5, tab_parent, config_path, "Genome Element", 5, hide )
    network_graph_app = NetworkGraphApp(tab6, tab_parent, config_path, "Seed Host Matching", 2, hide )
    network_model_app.update_graph(network_graph_app)
    network_app = EpidemiologyModel(tab7, tab_parent, config_path, "Epidemiology Model", 6, hide )
    network_app = PostProcessing(tab8, tab_parent, config_path, "Post Processing Options", 7, hide)

    tab_parent.pack(expand=1, fill='both')
    root.configure(background='black')
    root.mainloop()


def execute():
    """
    Executes the application, according to the command line arguments specified.
    """
    args = parse_args()
    default_config_path = "enivol_packaging/enivol/config_template/default_config.json"
    launch_gui(default_config_path, args.config_path, args.hide)



execute()
