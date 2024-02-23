import networkx as nx
import os
import numpy as np
import argparse
import random
from base_func import *

def write_network(ntwk_, wk_dir):
    ## Writes a network to the workding directory
    ## ntwk_: nx.Graph
    ## wk_dir: str
    nx.write_adjlist(ntwk_, os.path.join(wk_dir, "contact_network.adjlist"))


def ER_generate(pop_size, p_ER):
    ## Returns an Erdos_renyi graph with specified parameters
    ## pop_size: int
    ## p_ER: float/int
    er_graph = nx.erdos_renyi_graph(pop_size, p_ER)
    return er_graph


def rp_generate(rp_size, p_within, p_between):
    ## Returns a random partition graph with 2 groups, each group having a probability of within-group edge, and there is a between-group edge probability
    ## rp_size: list[int], length of the list is 2
    ## p_within: list[float], length of the list is 2
    rp_graph = nx.random_partition_graph(rp_size, max(p_within), p_between)
    if p_within[0]!=p_within[1]:
        higher_density_group = list(rp_graph.graph['partition'][0])
        for i in higher_density_group:
            for j in range(i):
                if j in list(rp_graph.adj[i]):
                    continue
                else:
                    if np.random.uniform(0, 1, 1)[0] <= abs(p_within[0] - p_within[1]) / (1 - p_within[1]):
                        rp_graph.add_edge(i ,j)
    return rp_graph


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

def check_input_network(wk_dir, path_network, pop_size):
    # A function to check format of the input network and store it to the working directory
    if os.path.exists(path_network):
        ntwk = nx.read_adjlist(path_network)
        if len(ntwk)!=pop_size:
            print(f"The provided network doesn't have the same number of nodes ({len(ntwk)}) as the host population size ({pop_size}) specified.")
        else:
            write_network(ntwk, wk_dir)
    else:
        print("The provided network path doesn't exist. Terminated.")


def network_generation_byconfig(all_config):
    ntwk_config = all_config["NetworkModelParameters"]
    wk_dir = seeds_config["BasicRunConfiguration"]["cwdir"]
    ntwk_method = ntwk_config["method"]

    if ntwk_method=="user_input":
        run_network_generation(pop_size=ntwk_config["host_size"], wk_dir=wk_dir, method="user_input", path_network=ntwk_config["user_input"]["path_network"])
    elif ntwk_method=="randomly_generate":
        model = ntwk_config["randomly_generate"]["network_model"]
        if model=="ER":
            run_network_generation(pop_size=ntwk_config["host_size"], wk_dir=wk_dir, method="randomly_generate", model=model, p_ER=ntwk_config["randomly_generate"]["ER"]["p_ER"])
        elif model=="RP":
            run_network_generation(pop_size=ntwk_config["host_size"], wk_dir=wk_dir, method="randomly_generate", model=model, rp_size=ntwk_config["randomly_generate"]["RP"]["rp_size"], p_within=ntwk_config["randomly_generate"]["RP"]["p_within"], p_between=ntwk_config["randomly_generate"]["RP"]["p_between"])
        elif model=="BA":
            run_network_generation(pop_size=ntwk_config["host_size"], wk_dir=wk_dir, method="randomly_generate", model=model, ba_m=ntwk_config["randomly_generate"]["BA"]["ba_m"])


def run_network_generation(pop_size, wk_dir, method, model="", path_network="", p_ER=0, rp_size=[], p_within=[], p_between=0, m=0):
    run_check = True
    if method=="user_input":
        if path_network=="":
            print("Need to specify a path to the user-provided network (-path_network).")
            run_check = False
    elif method=="randomly_generate":
        if model == "":
            print("Need to specify a random graph model (-model) in random generate mode.")
            run_check = False
        elif model == "ER":
            if p_ER==0:
                print("Need to specify a p>0 (-p_ER) in Erdos-Renyi graph.")
                run_check = False
        elif model == "RP":
            if len(rp_size)!=2:
                print("Need to specify size of the 2 partitions (-rp_size) in random partition graph.")
                run_check = False
            elif sum(rp_size)!=pop_size:
                print("Size of the 2 partitions (-rp_size) has to add up to the whole population size (-popsize).")
                run_check = False
            elif len(p_within)==0:
                print("Need to specify the connection probability within two partitions (-p_within).")
                run_check = False
            elif len(p_within)!=len(rp_size):
                print("The parameter p within each partition (-p_within) needs to 2 numbers, each for one partition.")
                run_check = False
            elif p_between==0:
                print("WARNING: You didn't specify a between partition connection probability (-p_between) or have set it to 0. This will lead to two isolating partitions, which isn't usually desired. Please make sure this is what you want.")
            elif len(p_between)!=len(rp_size) - 1:
                print("The parameter p between each partition needs to be 1 number (-p_between)")
                run_check = False
        elif model=="BA":
            if m==0:
                print("Need to specify a m>0 (-m) in Barabasi-Albert graph.")
                run_check = False
        else:
            run_check = False
            print("Illegal network model specified! (Supported model: ER/RP/BA)")
    else:
        run_check = False
        print("Please provide a permitted method (user_input/randomly_generate).")

    if run_check:
        if method=="user_input":
            check_input_network(wk_dir, path_network, pop_size)
        elif method=="randomly_generate":
            if model == "ER":
                write_network(ER_generate(pop_size, p_ER), wk_dir)
            elif model == "RP":
                write_network(rp_generate(rp_size, p_within, p_between), wk_dir)
            elif model=="BA":
                write_network(ba_generate(pop_size, m), wk_dir)
    else:
        print("Terminated because of incorrect input")

###################################
def main():
    parser = argparse.ArgumentParser(description='Generate a contact network for the population size specified and store it in the working directory as an adjacency list.')
    parser.add_argument('-popsize', action='store',dest='popsize', required=True, type=int)
    parser.add_argument('-wkdir', action='store',dest='wkdir', required=True, type=str)
    parser.add_argument('-method', action='store',dest='method', required=True, type=str)
    parser.add_argument('-model', action='store',dest='model', required=False, type=str, default="")
    parser.add_argument('-path_network', action='store',dest='path_network', required=False, type=str, default="")
    parser.add_argument('-p_ER', action='store',dest='p_ER', required=False, type=float, default=0)
    parser.add_argument('-rp_size','--rp_size', nargs='+', help='Size of random partition graph groups', required=False, type=int, default=[])
    parser.add_argument('-p_within','--p_within', nargs='+', help='probability of edges for different groups (descending order), take 2 elements rn', required=False, type=float, default=[])
    parser.add_argument('-p_between', action='store',dest='p_between', required=False, type=float, default=0)
    parser.add_argument('-m', action='store',dest='m', required=False, type=int, default=0)
    
    args = parser.parse_args()
    pop_size = args.popsize
    wk_dir = args.wkdir
    method = args.method
    model = args.model
    path_network = args.path_network
    p_ER = args.p_ER
    rp_size = args.rp_size
    p_within = args.p_within
    p_between = args.p_between
    m = args.m
    
    run_network_generation(pop_size=pop_size, wk_dir=wk_dir, method=method, model=model, path_network=path_network, p_ER=p_ER, rp_size=rp_size, p_within=p_within, p_between=p_between, m=m)

    

if __name__ == "__main__":
	main()