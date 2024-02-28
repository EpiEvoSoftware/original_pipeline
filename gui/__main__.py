"""
An application for visualizing networks

This file is the main entry-point for the GUI application. 
"""
import argparse
import os.path

import tkinter as tk
from tkinter import ttk
from plot import NetworkGraphApp
import json


def load_config_as_dict(config_file):
    """
    Loads the configuration from a file into a dictionary.

    Parameters:
        config_file (str): The path to the configuration file

    Returns:
        dict: Dictionary containing the configuration settings.
    """
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuration file {config_file} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {config_file}.")
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
                        help='path to the configuration file', default="test/params_test.json")
    parser.add_argument('-v', '--view', action='store_true',
                        help='visualize network graph')
    return parser.parse_args()


def launch_gui(config_file):
    """
    Launches the gui application
    """

    root = tk.Tk()

    tab_parent = ttk.Notebook(root)
    tab1 = ttk.Frame(tab_parent)
    network_app = NetworkGraphApp(tab1, config_file)
    tab2 = ttk.Frame(tab_parent)
    tab_parent.add(tab1, text="Network Graph")
    tab_parent.add(tab2, text="Add New Tab")
    tab_parent.pack(expand=1, fill='both')

    root.mainloop()


def execute():
    """
    Executes the application, according to the command line arguments specified.
    """
    args = parse_args()
    config = load_config_as_dict(args.config_path)
    if config:
        launch_gui(config)
    else:
        print("A valid configuration file is required to run the application.")


execute()
