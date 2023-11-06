"""
Functions for generating contact networks.

Author: Perry Xu
Date: November 6, 2023
"""

import networkx as nx
import numpy as np
import random

def write_network(ntwk_, wk_dir, pop_size):
    """
    Create an adjlist file to store a given network.

    :param ntwk_: The given network.
    :type ntwk: ?
    :param wk_dir: The path to store network adjlist file.
    :type wk_dir: str
    :param pop_size: The population size of the network.
    :type pop_size: int
    """
    with open(wk_dir + "contact_network.adjlist.modified", "w") as adjl:
        for i in range(pop_size):
            int_list = list(ntwk_.adj[i])
            if len(int_list) > 0:
                adjl.write(str(i) + " " + " ".join([str(x) for x in int_list]) + "\n")
            else:
                adjl.write(str(i) + "\n")


def ER_generate(pop_size, p_ER):
    """
    Returns an Erdős-Rényi graph with specified parameters.

    :param pop_size: The population size of the network.
    :type pop_size: int
    :param p_ER: The probability of connection between two individuals.
    :type p_ER: float
    :return: The ER network.
    :rtype: ?
    """
        ## Generate an Erdős-Rényi graph with 1000 nodes and probability of edge generation being 0.15
    er_graph = nx.erdos_renyi_graph(pop_size, p_ER)

    return(er_graph)



def rp_generate(rp_size, p_within, p_between):
    """
    Returns a random partition graph of ? groups with sepcified parameters.
    
    :param rp_size: The population sizes of each group.
    :typr rp_size: list[int]
    :param p_within: The probabilities of within group connection.
    :type p_within: list[float]
    :param p_between: The probabilities of intergroup connection.
    :type p_between: list[float]
    :return: The RP network.
    :rtype: ?
    """
    ## Generate a random partition graph with 2 groups, each group having a probability of within-group edge, and there is a between-group edge probability
    rp_graph = nx.random_partition_graph(rp_size, p_within[1], p_between)
    if p_within[0]==p_within[1]:
        higher_density_group = list(rp_graph.graph['partition'][0])
        for i in higher_density_group:
            for j in range(i):
                if j in list(rp_graph.adj[i]):
                    continue
                else:
                    if np.random.uniform(0, 1, 1)[0] <= (p_within[0] - p_within[1]) / (1 - p_within[1]):
                        rp_graph.add_edge(i ,j)
    return(rp_graph)


def _random_subset(seq,m):
    """
    Returns randomly selected m objects from seq.

    :param seq: ?
    :type seq: ?
    :param m: ?
    :type m: int
    :return: ?
    :rtype: list[?]
    """
    targets=set()
    while len(targets)<m:
        x=random.choice(seq)
        targets.add(x)
    return targets

def ba_generate(pop_size, m):
    """
    Returns a Barabási-Albert graph with sepcified parameters.
    
    :param pop_size: The population size of the network.
    :type pop_size: int
    :param m:
    :type m:
    :return: The BA network.
    :rtype: ?
    """
    G=nx.empty_graph(m)
    G.name="barabasi_albert_graph(%s,%s)"%(pop_size,m)
    # Target nodes for new edges
    targets=list(range(m))
    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes=[]
    # Start adding the other n-m nodes. The first node is m.
    source=m
    while source<pop_size:
        G.add_edges_from(zip([source]*m,targets))
        repeated_nodes.extend(targets)
        repeated_nodes.extend([source]*m)
        targets = _random_subset(repeated_nodes,m)
        source += 1
    ba_graph = G
    return(ba_graph)