import os, networkx as nx, json, pandas as pd, math, argparse
from random import sample
from collections import defaultdict
from pathlib import Path
from error_handling import CustomizedError
from base_func import *

# Magic numbers
HUNDRED = 100
ZERO = 0

def _build_dict_edges_node(ntwk_):
	"""
	Returns a dictionary with degrees as keys and a list of notes 
	of corresponding degrees as values (dict[int, list[int]]).

	Parameters:
		ntwk_ (nx.Graph): The contact network.
	"""
	dict_edges_node = defaultdict(list)
	[dict_edges_node[n_edges].append(node) for node, n_edges in ntwk_.degree]
	return dict_edges_node

def _sort_node_by_edge(dict_edges_node):
	"""
	Returns a list of nodes reversely sorted by their degress (list[int])
	and a list of their corresponding degreses (list[int]).

	Parameters:
		dict_edges_node (dict[int, list[int]]): A dictionary with degrees
		as keys and a list of notes of corresponding degrees as values,
	"""
	nodes_sorted = []
	degree_sorted = []
	for degree in sorted(dict_edges_node.keys(), reverse = True):
		nodes = dict_edges_node[degree]
		nodes_sorted.extend(nodes)
		degree_sorted.extend([degree]*len(nodes))
	# degree_sorted is not used anywhere in the pipeline for now; 
	# we can delete it if we decide this is unnecessary
	return nodes_sorted, degree_sorted

def _save_dict_to_csv(dict_matching, file_path):
	"""
	Writes a CSV that stores the matching dictionary with columns ['seed', 'host_id'].

	Parameters:
		dict_matching (dict[int, int]): A dictionary with seeds as keys and hosts as keys
		file_path (str): Full path to write the desired CSV
	"""
	# changed the order of columns, it used to be ['host_id', 'seed']
	df = pd.DataFrame(list(dict_matching.items()), columns = ['seed', 'host_id'])
	df.to_csv(file_path, index = False)
 
def _read_user_matchingfile_info_json(file):
	"""
	Returns a dictionary of the matching and checks the user input JSON for matching.

	Parameters:
		file (str): Full path to the JSON
	"""
	## TODO: to check whether the contents of JSON satisfies the matching requirement
	return file

def _read_user_matchingfile_info_csv(file):
	"""
	Returns a dictionary of the matching and checks the user input CSV for matching.

	Parameters:
		file (str): Full path to the CSV
	"""
	## TODO: to check whether the contents of CSV satisfies the matching requirement
	return file

def _Percentile_to_index(Percentile, node_per_percent):
	"""
	Returns the two indices (int, int) corresponding to the given Percentile ranges.

	Parameters: 
		Percentile (list[int, int]): Percentile range for the node selection.
		node_per_percent: The number of nodes equivalent to a Percentile
	"""
	if len(Percentile) != 2:
		raise CustomizedError(f"The Percentile range {Percentile} is not a list of two element.")
	l_per, h_per = Percentile
	# check if the Percentiles are int
	if type(l_per) != int or type(h_per) != int:
		raise CustomizedError(f"The Percentile range {Percentile} is not a list of integers, please reset the range.")
	# check if the ends are out of bound
	if min(l_per, h_per) < ZERO or max(l_per, h_per) > HUNDRED:
		raise CustomizedError(f"The Percentile range {Percentile} is not within the closed 0-100 interval.")
	# check the relationship between the lower and higher ends
	if h_per <= l_per:
		raise CustomizedError(f"The Percentile range {Percentile} is not a valid interval.")
	# round the index to make sure those are integers
	low_idx = math.ceil(node_per_percent * l_per)
	high_idx = math.floor(node_per_percent * h_per)
	return low_idx, high_idx

def read_user_matchingfile(file_path):
	"""
	Raises exceptions when user given file path is invalid/ format does not satisfy
	the matching file requirements. Returns a dictionary of matching where seeds are 
	keys and host_ids are values.

	Parameters:
		file path (str): Full path to the user matchingfile
	"""
	file_path = Path(file_path)

	# check if file exists
	if not file_path.exists():
		raise FileNotFoundError(f"File {file_path} not found.")
	# check if the json file is a valid matching file
	if file_path.suffix.lower() == ".json":
		try:
			with open(file_path, 'r') as file:
				matching = json.load(file)
				return _read_user_matchingfile_info_json(matching)
		except json.JSONDecodeError:
			raise ValueError(f"Invalid JSON format in {file_path}.")
	# check if the csv file is a valid matching file
	elif file_path.suffix.lower() == ".csv":
		try:
			matching = pd.read_csv(file_path)
			return _read_user_matchingfile_info_csv(matching)
		except pd.errors.ParserError:
			raise ValueError(f"Invalid CSV format in {file_path}")
	raise ValueError("Host-seed matching file is not CSV or JSON.")

def read_network(network_path):
	"""
	Return a network (nx.Graph) written in the input path.

	Parameters:
		network_path (str): Full path to the network to read
	"""
	network_path = Path(network_path)
	if not network_path.exists():
		raise FileNotFoundError(f"The provided networkX path '{network_path}' doesn't exist. \
							Please run network_generation first before running this script \
						  	and make sure the given working directory is correct.")
	return nx.read_adjlist(network_path, nodetype=int)

def match_Random(nodes_sorted, taken_hosts, param = None):
	"""
	Returns one Random available host (int) to match one seed.

	Parameters:
		nodes_sorted (list[int]): Hosts sorted in reverse order by degrees.
		taken_hosts (list[int]): Hosts already matched to a seed.
	"""
	available_host = list(set(nodes_sorted).difference(set(taken_hosts)))
	host = sample(available_host, 1)[0]
	return host

def match_Ranking(nodes_sorted, taken_hosts, rank):
	"""
	Returns one available host (int) of a specific rank (by degrees) to match one seed.

	Parameters:
		nodes_sorted (list[int]): Hosts sorted in reverse order by degrees.
		taken_hosts (list[int]): Hosts already matched to a seed.
	"""
	ntwk_size = len(nodes_sorted)
	if rank > ntwk_size:
		raise CustomizedError(f"Your provided Ranking {rank} exceed host size {ntwk_size}.")
	host = nodes_sorted[rank - 1]
	if host in taken_hosts: 
		raise CustomizedError(f"Host of specified rank {rank} is already taken.")
	return host

def match_Percentile(nodes_sorted, taken_hosts, Percentile):
	"""
	Returns one available host (int) within the 
	given Percentile range (by degrees) to match one seed.

	Parameters:
		nodes_sorted (list[int]): Hosts sorted in reverse order by degrees.
		taken_hosts (list[int]): Hosts already matched to a seed.
		Percentile (list[int]): Range for host selection, can only be of length two.
	"""
	node_per_percent = len(nodes_sorted) / HUNDRED
	low_idx, high_idx = _Percentile_to_index(Percentile, node_per_percent)
	if high_idx > low_idx:
		hosts_in_range = set(nodes_sorted[low_idx:high_idx])
		taken_hosts_in_range = hosts_in_range.intersection(taken_hosts)
		available_host = list(hosts_in_range.difference(taken_hosts_in_range))
		if available_host == []: 
			raise CustomizedError(f"There is no host left to match in the Percentile {Percentile}.")
		host = sample(available_host, 1)[0]
		return host
	raise CustomizedError(f"There is no host to match in the range {Percentile}%.")
	
def write_match(match_dict, wk_dir):
	"""
	Writes the matching to a CSV file sorted in ascending 
	order by host ids in the working directory.

	Parameters:
		match_dict (dict[int, int]): A dictionary of matching with seeds as keys and hosts as values.
		wk_dir (str): Full path to the working directory.
	"""
	sorted_match = dict(sorted(match_dict.items(), key=lambda x:x[1]))
	_save_dict_to_csv(sorted_match, os.path.join(wk_dir, "seed_host_match.csv"))

def match_all_hosts(ntwk_, match_method, param, num_seed):
	"""
	Returns matching in the form of dictionary where keys are seeds and values are hosts.
	E.g., {0: 232, 1:256, 2:790, 3:4, 4:760} (dict[int, int])

	Parameters:
		ntwk_ (nx.Graph): Contact network.
		match_method (dict[int, str]): A dictionary of hosts as keys and matching method as values.
		param (dict[int, Union[int, list[int, int], None]]): A dictionary of hosts as k
		eys and matching parameters as values.
		num_seed (int): Number of seeds. 
	"""
	ntwk_size = ntwk_.number_of_nodes()
	if num_seed > ntwk_size:
		raise CustomizedError(f"It is not allowed to match {num_seed} seeds to {ntwk_size} hosts. \
						Please reduce the number of seeds or increase the host population size.")
	
	# Preprocess the network
	dict_edges_node = _build_dict_edges_node(ntwk_)
	nodes_sorted, _ = _sort_node_by_edge(dict_edges_node)
	taken_hosts_id = []

    # Gather the nodes by their matching method
	dict_method_seeds = {'Ranking': [], 'Percentile': [], 'Random': []}

	for seed_id in range(num_seed):
		idx_method = match_method.get(str(seed_id))
		if idx_method not in [None, 'Ranking', 'Percentile', 'Random']:
			raise CustomizedError(f"Please provide a valid matching method in ('Ranking', \
						 'Percentile', 'Random') instead of {method} for seed {seed_id}")
		elif idx_method != None:
			dict_method_seeds[idx_method].append(seed_id) 
		else: 
			dict_method_seeds["Random"].append(seed_id)
	
	# Define the matching function by the method param and process methods in the specified order
	match_functions = {'Ranking': match_Ranking, 'Percentile': match_Percentile,'Random': match_Random}
	match_dict = {}
	for method in ['Ranking', 'Percentile', 'Random']:
		match_function = match_functions[method]
		for seed_id in dict_method_seeds[method]:
			matched_host = match_function(nodes_sorted, taken_hosts_id, param.get(str(seed_id)))
			match_dict[seed_id] = matched_host
			taken_hosts_id.append(matched_host)
	return match_dict

def run_seed_host_match(method, wkdir, num_seed, path_matching="", match_scheme="", match_scheme_param = ""):
	"""
	Executes seed host matching process in command line and write the matching file 
	in the specified directory.

	Parameters:
		method (str): "user_input" for user-provided matching or "Randomly_generated".
		wkdir (str): Full path to the workding directory.
		num_seed (int): Number of seeds for matching.
		path_matching (str): Full path to the user-provided matching file.
		match_scheme (str): JSON string of matching methods for seeds.
		match_scheme_param (str): JSON string of matching parameters for seeds.
	"""		
	# Generate network path
	ntwk_path = os.path.join(wkdir, "contact_network.adjlist")
	seed_vs_host = {}
	# Process the parameters and save the matching results have we match all host
	try:
		if method=="user_input":
			if path_matching=="":
				raise CustomizedError("Path to the user-provided matching file (-path_matching) \
						  needs to be provided in user_provided mode.")
			elif os.path.exists(path_matching) == False:
				raise CustomizedError("Path to the user-provided matching file (-path_matching) \
						  doesn't exist.")
			else: 
				read_user_matchingfile(path_matching)
		elif method=="Randomly_generate":
			if match_scheme == "" and match_scheme_param == "":
				match_scheme = {seed_id: "Random" for seed_id in range(num_seed)}
				match_scheme_param = {seed_id: None for seed_id in range(num_seed)}
			else:
				try:
					match_scheme = json.loads(match_scheme)
				except json.decoder.JSONDecodeError:
					raise CustomizedError(f"The matching methods {match_scheme} is \
						   not a valid json format.")
				try:
					match_scheme_param = json.loads(match_scheme_param)
				except json.decoder.JSONDecodeError:
					if list(set(match_scheme.values())) != ["Random"]:
						raise CustomizedError(f"The matching parameters {match_scheme_param} is \
	 			    not a valid json format.")
					elif match_scheme_param == "": 
						raise CustomizedError(f"Please specify the matching parameters (-match_scheme_param) for " \
						   "'Ranking' or 'Percentile'.")
					match_scheme_param = {seed_id: None for seed_id in range(num_seed)}
			seed_vs_host = match_all_hosts(ntwk_=read_network(ntwk_path), match_method = match_scheme, 
							   param = match_scheme_param, num_seed = num_seed)
			write_match(seed_vs_host, wkdir)
			print("The matching process has successfully terminated. Please see working \n"
		f"directory {wkdir}/seed_host_match.csv \nfor the seed host matching file.")
		else:
			raise CustomizedError(f"Please provide a permitted method (-method): "
						"user_input/Randomly_generate instead of your current input {method}.")
		print("******************************************************************** \n" +
              "                         SEEDS HOSTS MACTHED                         \n" +
              "******************************************************************** \n")
		return seed_vs_host
	except Exception as e:
		print(f"Seed and host match - A violation of input parameters occured: {e}")

def read_config_and_match(file_path, num_seed):
	"""
	Write matching file given the configuration file.

	Parameters:
		file_path (str): Full path to the configuration file.
		num_seed (int): Number of seeds.
	"""
	config_all = read_params(file_path)
	config = config_all["SeedHostMatching"]["Randomly_generated"]
	match_method = config["match_scheme"]
	match_method_param = config["match_scheme_param"]
	path_matching = config_all["SeedHostMatching"]["user_input"]["path_matching"]
	method = "user_input" if path_matching != "" else "Randomly_generated"
	run_seed_host_match(method=method, wkdir=config_all["BasicRunConfiguration"]["cwdir"], 
					 num_seed=num_seed, path_matching=path_matching, 
	match_scheme=match_method, match_scheme_param=match_method_param)

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