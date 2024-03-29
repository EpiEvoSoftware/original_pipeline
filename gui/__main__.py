"""
An application for visualizing networks

This file is the main entry-point for the GUI application. 
"""
import argparse
import os.path
import tkinter as tk
from tkinter import ttk
import json

from tabs.t1_configuration import Configuration
from tabs.t1_configuration_v2 import Configurationv2
from tabs.t2_evolutionarymodel import EvolutionaryModel
from tabs.t3_networkmodel import NetworkModel
from tabs.t4_seeds_configuration import SeedsConfiguration
from tabs.t5_genome_element import GenomeElement
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


def parse_args():
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog='cluster', description='Application to view GUI')
    parser.add_argument('--config_path', type=str,
                        help='path to the configuration JSON file', default="config_templates/base_params_test.json")
    parser.add_argument('-v', '--view', action='store_true',
                        help='visualize network graph')
    parser.add_argument('--hide', action='store_true', help='Set hide to False, default is True')
    return parser.parse_args()


def launch_gui(config_path, hide = False):
    """
    Launches the gui application
    """

    root = tk.Tk()
    root.title("Epidemiology Evolution")

    tab_parent = ttk.Notebook(root)

    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)
    tab3 = ttk.Frame(tab_parent)
    tab4 = ttk.Frame(tab_parent)
    tab5 = ttk.Frame(tab_parent)
    tab6 = ttk.Frame(tab_parent)
    tab7 = ttk.Frame(tab_parent)
    tab8 = ttk.Frame(tab_parent)

    if hide:
        network_app = Configuration(tab1, tab_parent, config_path, "Basic Configuration", 0, hide = True)
        network_app = EpidemiologyModelv2(tab2, tab_parent, config_path, "Evolutionary Model", 1, hide = True)
        # network_app = Configurationv2(tab2, tab_parent, config_path, hide = True)
        network_graph_app = NetworkGraphApp(tab6, tab_parent, config_path, "Network Graph", 2, hide = True)
        network_model_app = NetworkModel(tab3, tab_parent, network_graph_app, config_path, "Network Model Parameters", 3, hide = True)
        network_app = Configurationv2(tab4, tab_parent, config_path, "Seeds Configuration", 4, hide = True)
        network_app = GenomeElement(tab5, tab_parent, config_path, "Genome Element", 5, hide = True)
        network_app = EpidemiologyModel(tab7, tab_parent, config_path, "Epidemiology Model", 6, hide = True)
        network_app = PostProcessing(tab8, tab_parent, config_path, "Post Processing Options", 7, hide = True)
    else:
        network_app = Configuration(tab1, tab_parent, config_path, "Basic Configuration", 0)
        network_app = EpidemiologyModelv2(tab2, tab_parent, config_path, "Evolutionary Model", 1)
        # network_app = Configurationv2(tab2, tab_parent, config_path)
        network_graph_app = NetworkGraphApp(tab6, tab_parent, config_path, "Network Graph", 2)
        network_model_app = NetworkModel(tab3, tab_parent, network_graph_app, config_path, "Network Model Parameters", 3)
        network_app = Configurationv2(tab4, tab_parent, config_path, "Seeds Configuration", 4)
        network_app = GenomeElement(tab5, tab_parent, config_path, "Genome Element", 5)
        network_app = EpidemiologyModel(tab7, tab_parent, config_path, "Epidemiology Model", 6)
        network_app = PostProcessing(tab8, tab_parent, config_path, "Post Processing Options", 7)

    # # network_app = EpidemiologyModelv3(tab1, tab_parent, config_path)
    # network_app = Configuration(tab1, tab_parent, config_path, "Basic Configuration", 0)
    # network_app = EpidemiologyModelv2(tab2, tab_parent, config_path, "Evolutionary Model", 1)
    # # network_app = Configurationv2(tab2, tab_parent, config_path)
    # network_graph_app = NetworkGraphApp(tab6, tab_parent, config_path, "Network Graph", 5)
    # network_model_app = NetworkModel(tab3, tab_parent, network_graph_app, config_path, "Network Model Parameters", 2)
    # network_app = Configurationv2(tab4, tab_parent, config_path, "Seeds Configuration", 3)
    # network_app = GenomeElement(tab5, tab_parent, config_path, "Genome Element", 4)
    # network_app = EpidemiologyModel(tab7, tab_parent, config_path, "Epidemiology Model", 6)
    # network_app = PostProcessing(tab8, tab_parent, config_path, "Post Processing Options", 7)

    tab_parent.pack(expand=1, fill='both')

    root.mainloop()


def execute():
    """
    Executes the application, according to the command line arguments specified.
    """
    args = parse_args()
    if args.config_path:
        launch_gui(args.config_path, args.hide)
    else:
        print("A valid configuration file is required to run the application.")


execute()
