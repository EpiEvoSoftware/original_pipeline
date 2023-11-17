import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.figure import Figure

def create_plot(graph):
    """
    Creates the plot
    """
    degrees = [d for n, d in graph.degree()]
    
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.hist(degrees, bins=np.arange(min(degrees), max(degrees) + 1, 1), density=True, alpha=0.75, color='blue', edgecolor='black')
    plot.set_xlabel('Degree')
    plot.set_ylabel('Frequency')
    plot.set_title('Degree Distribution')   
    return fig


def empty_figure():
    """
    Creates an empty default network graph
    """
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.set_xlabel('Degree')
    plot.set_ylabel('Frequency')
    plot.set_title('Degree Distribution')  
    return fig