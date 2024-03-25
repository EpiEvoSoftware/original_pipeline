import networkx as nx, os, argparse
from base_func import *
from error_handling import CustomizedError


def write_network(ntwk_, wk_dir):
    """
    Writes a network to the workding directory.
    
    Parameters:
        wk_dir (str): Working directory.
        ntwk_ (nx.Graph): Contact network.
    """
    nx.write_adjlist(ntwk_, os.path.join(wk_dir, "contact_network.adjlist"))


def ER_generate(pop_size, p_ER):
    """
    Returns an Erdos_renyi graph with specified parameters.
    
    Parameters:
        p_ER (str): The probability of existing edges between two nodes.
        pop_size (int): Population size.
    """
    if not 0 < p_ER <= 1: 
        raise CustomizedError("You need to specify a p>0 (-p_ER) in Erdos-Renyi graph.")
    er_graph = nx.erdos_renyi_graph(pop_size, p_ER)
    return er_graph

def rp_generate(pop_size, rp_size, p_within, p_between):
    """
    Returns a random partition graph with n groups, each group having a probability of \
        within-group edge, and there is a global between-group edge probability.
    
    Parameters:
        rp_size (list[int]): The sizes of partitions.
        pop_size (int): Population size.
        p_within (list[float]): The probability of edges within each partition.
        p_between (float): The probability of edges among partitions.
    """
    block_size = len(rp_size)
    prob_size = len(p_within)

    # Check for validity of inputs
    if sum(rp_size) != pop_size:
        raise CustomizedError(f"Size of the partitions (-rp_size {rp_size}) has \
                              to add up to the whole population size (-popsize {pop_size}). ")
    if prob_size != block_size: 
        raise CustomizedError(f"The number of partitions ({block_size}) does \
                              not match the number of given within partition connection \
                              probabilities ({prob_size}).")
    if p_between == 0: 
        print("WARNING: You didn't specify a between partition connection probability (-p_between) \
              or have set it to 0. This will lead to two completely isolated partitions.")
    
    # Construct contact probability matrix
    p = [[p_between for _ in range(block_size)] for _ in range(block_size)]
    for k in range(block_size):
        p[k][k] = p_within[k]

    # Generate random partition graph
    rp_graph = nx.stochastic_block_model(rp_size, p)
    return rp_graph


def ba_generate(pop_size, m):
    """
    Returns a random graph using Barabasi-Albert preferential attachement.
    
    Parameters:
        pop_size (int): Population size.
        m (int): Number of edges to attach from a new node to existing nodes.
    """
    ba_graph = nx.barabasi_albert_graph(pop_size, m)
    return ba_graph

def copy_input_network(wk_dir, path_network, pop_size):
    """
    Checks the format of the input network and copy it in the working directory.
    
    Parameters:
        wk_dir (str): Working directory.
        path_network (str): Path to the network file.
        pop_size (int): Population size.
    """
    if path_network == "":
        raise CustomizedError(f"You need to specify a path to the user-provided network (-path_network).")    
    elif not os.path.exists(path_network):
        raise FileNotFoundError(f"The provided network path ({path_network}) doesn't exist.")

    ntwk = nx.read_adjlist(path_network)
    if len(ntwk) != pop_size:
        raise CustomizedError(f"The provided network doesn't have the same number of nodes \
                              ({len(ntwk)}) as the host population size ({pop_size}) specified.")

    write_network(ntwk, wk_dir)


def run_network_generation(pop_size, wk_dir, method, model="", path_network="", p_ER=0, rp_size=[], p_within=[], p_between=0, m=0):
    """
    Generates the contact network given parameters.
    
    Parameters:
        wk_dir (str): Working directory.
        path_network (str): Path to the network file.
        pop_size (int): Population size.
        method (str): Method to acquire the contact network.
        model (str): The network model to construct contact network.
        p_ER (float): param for ER graph.
        rp_size (float): param for RP graph.
        p_within (list[float]): param for RP graph.
        p_between (float): param for RP graph.
        m (int): param for BA graph.
    """
    try: 
        ntwk = None
        if method == "user_input":
            copy_input_network(wk_dir, path_network, pop_size)
    
        elif method=="randomly_generate":
            if not model in ["ER", "BP", "BA"]: 
                raise CustomizedError("You need to specify a random graph model (-model) in random \
                                      generate mode. (Supported model: ER/RP/BA)")
            if model == "ER": 
                write_network(ER_generate(pop_size, p_ER), wk_dir)
            elif model == "RP": 
                write_network(rp_generate(pop_size, rp_size, p_within, p_between), wk_dir)
            else:
                write_network(ba_generate(pop_size, m), wk_dir)
        else:
            CustomizedError("Please provide a permitted method (user_input/randomly_generate).")
        print("******************************************************************** \n" +
              "                   CONTACT NETWORK GENERATED                         \n" +
              "******************************************************************** \n")
        
    except Exception as e:
        raise CustomizedError(f"Contact network generation - A violation of input parameters occured {e}.")

def network_generation_byconfig(all_config):
    ntwk_config = all_config["NetworkModelParameters"]
    wk_dir = all_config["BasicRunConfiguration"]["cwdir"]
    # shared params
    ntwk_method = ntwk_config["method"]
    pop_size = ntwk_config["host_size"]
    # user_input params
    path_network = ntwk_config["user_input"]["path_network"]
    # randomly generated network params
    model = ntwk_config["randomly_generate"]["network_model"]
    # ER param
    p_ER = ntwk_config["randomly_generate"]["ER"]["p_ER"]
    # RP params
    rp_params = ntwk_config["randomly_generate"]["RP"]
    rp_size = rp_params["rp_size"]
    p_within = rp_params["p_within"]
    p_between = rp_params["p_between"]
    # BA params
    ba_m=ntwk_config["randomly_generate"]["BA"]["ba_m"]

    run_network_generation(pop_size = pop_size, wk_dir = wk_dir, method = ntwk_method, 
                           path_network = path_network, model = model, p_ER = p_ER, 
                           p_within = p_within, p_between = p_between, 
                           rp_size = rp_size, ba_m = ba_m)

def main():
    parser = argparse.ArgumentParser(description='Generate a contact network for the population \
                                     size specified and store it in the working directory as an adjacency list.')
    parser.add_argument('-popsize', action='store',dest='popsize', required=True, type=int)
    parser.add_argument('-wkdir', action='store',dest='wkdir', required=True, type=str)
    parser.add_argument('-method', action='store',dest='method', required=True, type=str)
    parser.add_argument('-model', action='store',dest='model', required=False, type=str, default="")
    parser.add_argument('-path_network', action='store',dest='path_network', required=False, type=str, default="")
    parser.add_argument('-p_ER', action='store',dest='p_ER', required=False, type=float, default=0)
    parser.add_argument('-rp_size','--rp_size', nargs='+', help='Size of random partition graph groups', 
                        required=False, type=int, default=[])
    parser.add_argument('-p_within','--p_within', nargs='+', help='probability of edges for different groups \
                        (descending order), take 2 elements rn', required=False, type=float, default=[])
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
    
    run_network_generation(pop_size=pop_size, wk_dir=wk_dir, method=method, model=model, path_network=path_network, 
                           p_ER=p_ER, rp_size=rp_size, p_within=p_within, p_between=p_between, m=m)


if __name__ == "__main__":
	main()