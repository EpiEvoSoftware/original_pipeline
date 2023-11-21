# import networkx as nx
# import numpy as np
# import argparse
# import random
# import sys, os, os.path
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# import codes.network_generate as network_generate


# write_network = network_generate.write_network()
# """
# Function for writing network
# """
# # def write_network(ntwk_, wk_dir, pop_size):
# #     with open(wk_dir + "contact_network.adjlist.modified", "w") as adjl:
# #         for i in range(pop_size):
# #             int_list = list(ntwk_.adj[i])
# #             if len(int_list) > 0:
# #                 adjl.write(str(i) + " " +
# #                            " ".join([str(x) for x in int_list]) + "\n")
# #             else:
# #                 adjl.write(str(i) + "\n")


# ER_generate = network_generate.ER_generate()
# """
# Function for generating Erdős-Rényi graph
# """
# # def ER_generate(pop_size, p_ER):

# #     # Generate an Erdős-Rényi graph with 1000 nodes and probability of edge generation being 0.15
# #     er_graph = nx.erdos_renyi_graph(pop_size, p_ER)

# #     return (er_graph)


# RP_generate = network_generate.rp_generate()
# """
# Function for generating random partition graph
# """

# # def rp_generate(rp_size, p_within, p_between):
# #     # Generate a random partition graph with 2 groups, each group having a probability of within-group edge, and there is a between-group edge probability
# #     rp_graph = nx.random_partition_graph(rp_size, p_within[1], p_between)
# #     if p_within[0] == p_within[1]:
# #         higher_density_group = list(rp_graph.graph['partition'][0])
# #         for i in higher_density_group:
# #             for j in range(i):
# #                 if j in list(rp_graph.adj[i]):
# #                     continue
# #                 else:
# #                     if np.random.uniform(0, 1, 1)[0] <= (p_within[0] - p_within[1]) / (1 - p_within[1]):
# #                         rp_graph.add_edge(i, j)
# #     return (rp_graph)


# BA_generate = network_generate.ba_generate()
# """
# Function for generating barabasi albert graph
# """

# # def ba_generate(pop_size, m):
# #     G = nx.empty_graph(m)
# #     G.name = "barabasi_albert_graph(%s,%s)" % (pop_size, m)
# #     # Target nodes for new edges
# #     targets = list(range(m))
# #     # List of existing nodes, with nodes repeated once for each adjacent edge
# #     repeated_nodes = []
# #     # Start adding the other n-m nodes. The first node is m.
# #     source = m
# #     while source < pop_size:
# #         G.add_edges_from(zip([source]*m, targets))
# #         repeated_nodes.extend(targets)
# #         repeated_nodes.extend([source]*m)
# #         targets = _random_subset(repeated_nodes, m)
# #         source += 1
# #     ba_graph = G
# #     return (ba_graph)