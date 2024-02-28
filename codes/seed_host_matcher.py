from base_func import *
from seed_host_match_func import *
import argparse
import json
import time


def main():
	parser = argparse.ArgumentParser(description='Match seeds and hosts.')
	parser.add_argument('-method',  action='store',dest='method', type=str, required=True, 
                     help="Methods of the seed host matching")
	parser.add_argument('-wkdir', action='store',dest='wkdir', type=str, required=True, 
                     help="Working directory")
	parser.add_argument('-n_seed', action='store',dest='num_seed', type=int, required=True, 
                     help="Number of seeds to be matched.")
    ### optional parameters
	parser.add_argument('-path_matching',  action='store',dest='path_matching', type=str, 
                     required=False, help="Path to the user-provided matching file", default="")
	parser.add_argument('-match_scheme',  action='store',dest='match_scheme', type=str, 
                     required=False, help="Scheme of matching", default="")
	parser.add_argument('-match_scheme_param', action='store', dest='match_scheme_param', 
                     type=str, required=False, help="Matching parameters for each seed", default="")

	args = parser.parse_args()
	method = args.method
	wkdir = args.wkdir
	num_seed = args.num_seed
	path_matching = args.path_matching
	match_scheme = args.match_scheme
	match_scheme_param = args.match_scheme_param

	run_seed_host_match(method=method, wkdir=wkdir, num_seed=num_seed, path_matching=path_matching, 
                     match_scheme=match_scheme, match_scheme_param=match_scheme_param)

if __name__ == "__main__":
    main()