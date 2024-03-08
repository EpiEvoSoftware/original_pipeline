from base_func import *
from network_func import *
import argparse


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