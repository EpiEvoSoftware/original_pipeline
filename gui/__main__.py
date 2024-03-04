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
from tabs.t2_seeds import Seeds
from tabs.t3_networkmodel import NetworkModel
from tabs.t4_seeds_configuration import SeedsConfiguration
from tabs.t5_genome_element import GenomeElement
from tabs.t6_networkgraph import NetworkGraphApp


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
                        help='path to the configuration JSON file', default="codes/base_params.json")
    parser.add_argument('-v', '--view', action='store_true',
                        help='visualize network graph')
    return parser.parse_args()


def launch_gui(config_path):
    """
    Launches the gui application
    """

    root = tk.Tk()

    tab_parent = ttk.Notebook(root)
    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)
    tab3 = ttk.Frame(tab_parent)
    tab4 = ttk.Frame(tab_parent)
    tab5 = ttk.Frame(tab_parent)
    tab6 = ttk.Frame(tab_parent)
    network_app = Configuration(tab1, tab_parent, config_path)
    network_app = Seeds(tab2, tab_parent, config_path)
    network_app = NetworkModel(tab3, tab_parent, config_path)
    network_app = SeedsConfiguration(tab4, tab_parent, config_path)
    network_app = GenomeElement(tab5, tab_parent, config_path)
    network_app = NetworkGraphApp(tab6, tab_parent, config_path)
    tab_parent.add(tab1, text="Configuration")
    tab_parent.add(tab2, text="Seeds")
    tab_parent.add(tab3, text="Network Model Parameters")
    tab_parent.add(tab4, text="Seeds Configuration")
    tab_parent.add(tab5, text="Genome Element")
    tab_parent.add(tab6, text="Network Graph")

    tab_parent.pack(expand=1, fill='both')

    root.mainloop()


def execute():
    """
    Executes the application, according to the command line arguments specified.
    """
    args = parse_args()
    if args.config_path:
        launch_gui(args.config_path)
    else:
        print("A valid configuration file is required to run the application.")


execute()
