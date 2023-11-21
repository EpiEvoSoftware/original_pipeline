"""
An application for visualizing networks

This file is the main entry-point for the GUI application. 
"""
# To handle command line options
import argparse
import os.path
import tkinter as tk

def load_config_as_dict(config_file = "../codes/params.config"):
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
    parser = argparse.ArgumentParser(prog='cluster', description='Application to view GUI')
    parser.add_argument('config_path', type=str, help='path to the configuration file')
    parser.add_argument('-v', '--view', action='store_true', help='visualize network graph')
    return parser.parse_args()
    
def launch_gui(config_file):
    """
    Launches the gui application
    """
    from plot import NetworkGraphApp
    root = tk.Tk()
    app = NetworkGraphApp(root, config_file)
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