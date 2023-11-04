import networkx as nx
import numpy as np
import argparse
import random

def write_network(ntwk_, wk_dir, pop_size):
    with open(wk_dir + "contact_network.adjlist.modified", "w") as adjl:
        for i in range(pop_size):
            int_list = list(ntwk_.adj[i])
            if len(int_list) > 0:
                adjl.write(str(i) + " " + " ".join([str(x) for x in int_list]) + "\n")
            else:
                adjl.write(str(i) + "\n")


def ER_generate(pop_size, p_ER):
     
        ## Generate an Erdős-Rényi graph with 1000 nodes and probability of edge generation being 0.15
    er_graph = nx.erdos_renyi_graph(pop_size, p_ER)

    return(er_graph)
    ## Read the adjascent list and write them into a matrix
    #with open(wk_dir + "contact_network.adjlist.modified", "w") as adjl:
    #    for i in range(pop_size):
    #        int_list = list(er_graph.adj[i])
    #        adjl.write(str(i) + " " + " ".join([str(x) for x in int_list]) + "\n")



def rp_generate(rp_size, p_within, p_between):
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
    #with open(wk_dir + "contact_network.adjlist.modified", "w") as adjl:
    #    for i in range(sum(rp_size)):
    #        int_list = list(rp_graph.adj[i])
    #        adjl.write(str(i) + " " + " ".join([str(x) for x in int_list]) + "\n")

def _random_subset(seq,m):

    targets=set()
    while len(targets)<m:
        x=random.choice(seq)
        targets.add(x)
    return targets

def ba_generate(pop_size, m):
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
    #with open(wk_dir + "contact_network.adjlist.modified", "w") as adjl:
    #    for i in range(pop_size):
    #        int_list = list(ba_graph.adj[i])
    #        adjl.write(str(i) + " " + " ".join([str(x) for x in int_list]) + "\n")
    #adj_mx = np.zeros((pop_size,pop_size))
    #for i in adj:
    #    a = int(i)
    #    for j in adj[i]:
    #        b = int(j)
    #        adj_mx[a,b] = 1
    #        adj_mx[b,a] = 1

    #with open(wk_dir + "contact_network.csv", "w") as csv:
    #    for i in range(len(adj_mx[0,:])):
    #        csv.write(",".join(map(str, adj_mx[i,:])) + "\n")

    #with open(wk_dir + "contact_network.csv", "w") as csv:
    #    for i in range(len(adj_mx[0,:])):
    #        csv.write(",".join(map(str, adj_mx[i,:])) + "\n")


def main():
    parser = argparse.ArgumentParser(description='Generate a contact network for the population size specified and conver it to a .csv file')
    parser.add_argument('-popsize', action='store',dest='popsize', required=False, type=int)
    parser.add_argument('-wkdir', action='store',dest='wkdir', required=True)
    parser.add_argument('-method', action='store',dest='method', required=True)
    parser.add_argument('-p_ER', action='store',dest='p_ER', required=False, type=float)
    parser.add_argument('-rp_size','--rp_size', nargs='+', help='Size of random partition graph groups', required=False, type=int)
    #parser.add_argument('-p_within', action='store',dest='p_within', required=False, type=float)
    parser.add_argument('-p_within','--p_within', nargs='+', help='probability of edges for different groups (descending order), take 2 elements rn', required=False, type=float)
    parser.add_argument('-p_between', action='store',dest='p_between', required=False, type=float)
    parser.add_argument('-m', action='store',dest='m', required=False, type=int)
    
    args = parser.parse_args()
    pop_size = args.popsize
    wk_dir = args.wkdir
    mtd = args.method
    p_ER = args.p_ER
    rp_size = args.rp_size
    p_within = args.p_within
    p_between = args.p_between
    m = args.m
    
    if mtd == "ER":
        write_network(ER_generate(pop_size, wk_dir, p_ER), wk_dir, pop_size)

    elif mtd == "rd_part":
        write_network(rp_generate(rp_size, wk_dir, p_within, p_between), wk_dir, pop_size)

    elif mtd=="ba":
         write_network(ba_generate(wk_dir, pop_size, m), wk_dir, pop_size)

    else:
        print("Illegal method provided!")

    

if __name__ == "__main__":
	main()
