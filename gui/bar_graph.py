import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

def create_plot():
    mu, sigma = -846700, 100  
    s = np.random.normal(mu, sigma, 1000)

    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.hist(s, 30, density=True, alpha=0.75, color='blue', edgecolor='black')
    plot.set_xlabel('posterior')
    plot.set_ylabel('frequency')

    return fig