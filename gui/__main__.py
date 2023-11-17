"""
An application for visualizing networks

This file is the main entry-point for the GUI application. 
"""
# To handle command line options
import argparse
import os.path

def parse():
    """
    Returns: the command line arguments

    This function uses argparse to handle the command line arguments.  The benefit of
    argparse is the built-in error checking and help menu.
    """
    parser = argparse.ArgumentParser(prog='cluster',description='Application to view GUI')
    parser.add_argument('file', type=str, nargs='?', help='the data set to process')
    parser.add_argument('k', type=str, nargs='?', help='initial cluster size')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v','--view',  action='store_true',  help='visualize network graph')
    result = parser.parse_args()

    if not result.k is None:
        try:
            kval = result.k
            kval = int(kval)
            assert kval > 0
        except:
            parser.error('k must be an int > 0.')
    
    return result


def launch_gui(filename,k):
    """
    Launches the gui application
    """
    from plotter import Visualizer
    Visualizer.launch(filename,k)


def execute():
    """
    Executes the application, according to the command line arguments specified.
    """
    args = parse()
    filename = args.file
    try:
        kval = args.k
        kval = int(kval)
    except:
        kval = 3

    launch_gui(filename,kval)

execute()
