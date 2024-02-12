import networkx as nx
import os
from random import sample
import json
import pandas as pd
from base_func import read_params
from collections import defaultdict
from pathlib import Path
from error_handling import CustomizedError
from typing import Union, Tuple
import math

# The path for the working pipeline
PIPELINE_PATH = os.path.dirname(__file__)
# The relative path for the testing folder
TEST_DIR = "test/seed_host_match_func"

def _build_dict_edges_node(ntwk_: nx.Graph) -> dict[int, list[int]]:
	## A helper function that returns a dictionary with number of edges as keys
	## and a list of nodes of corresponding degrees as values
	### Output: dict_edges_node: A dictionary with int as keys and int list as values
	dict_edges_node = defaultdict(list)
	[dict_edges_node[n_edges].append(node) for node, n_edges in ntwk_.degree]
	return dict_edges_node

def _sort_node_by_edge(dict_edges_node: dict[int, list[int]]) -> Tuple[list[int], list[int]]:
	## A helper function that returns a list of nodes reversely sorted by their 
	## degrees and a list of their corresponding degrees
	### Output: nodes_sorted: A list of int
	### 		degree_sorted: A list of int
	nodes_sorted = []
	degree_sorted = []
	for degree in sorted(dict_edges_node.keys(), reverse = True):
		nodes = dict_edges_node[degree]
		nodes_sorted.extend(nodes)
		degree_sorted.extend([degree]*len(nodes))
	return nodes_sorted, degree_sorted

def _save_dict_to_csv(dict_matching: dict[int, int], file_path: str):
	## A helper function that saves the matching dictionary as a specified file
	## with columns ['host_id', 'seed']
	### Output: file_path: A string
	df = pd.DataFrame(list(dict_matching.items()), columns = ['host_id', 'seed'])
	df.to_csv(file_path, index = False)
 
def _read_user_matchingfile_info_json(file: str):
	## TO DO: to check the contents of json
	return file

def _read_user_matchingfile_info_csv(file: str):
	## TO DO: to check the contents of csv
	return file

def read_user_matchingfile(file_path: str):
	## A function to check whether the user-input host-seed matching file is valid
	## Raise exceptions when given file path is invalid / when contents of file
	## does not satisfy the seed-host matching format.
	file_path = Path(file_path)
	if not file_path.exists():
		raise FileNotFoundError(f"File {file_path} not found.")
	if file_path.suffix.lower() == ".json":
		try:
			with open(file_path, 'r') as file:
				matching = json.load(file)
				return _read_user_matchingfile_info_json(matching)
		except json.JSONDecodeError:
			raise ValueError(f"Invalid JSON format in {file_path}.")
	elif file_path.suffix.lower() == ".csv":
		try:
			matching = pd.read_csv(file_path)
			return _read_user_matchingfile_info_csv(matching)
		except pd.errors.ParserError:
			raise ValueError(f"Invalid CSV format in {file_path}")
	else:
		raise ValueError("Host-seed matching file is not CSV or JSON.")

def read_network(network_path: str) -> nx.Graph:
	## A function that read networks from a given path
	network_path = Path(network_path)
	if not network_path.exists():
		raise FileNotFoundError(f"The provided networkX path '{network_path}' doesn't exist. Please run network_generation first before running this script and make sure the given working directory is correct.")
	return nx.read_adjlist(network_path, nodetype=int)

def match_random(nodes_sorted: list[int], taken_hosts: list[int], param = None) -> int:
	### A function to return one random available host to match one seed
	### Output: host: An int
	if len(nodes_sorted) == 0: 
		raise CustomizedError("There is no host left to match for random method.")
	available_host = list(set(nodes_sorted).difference(set(taken_hosts)))
	host = sample(available_host, 1)[0]
	taken_hosts.append(host)
	return host

def match_ranking(nodes_sorted: list[int], taken_hosts: list[int], rank: int) -> int:
	## A function to match one seed by rank (=degree of connectivity) to the host
	### Output: host: An int
	if len(taken_hosts) == len(nodes_sorted): 
		raise CustomizedError("There is no host left to match for ranking method.")
	if rank > len(nodes_sorted):
		raise CustomizedError(f"Your provided ranking {rank} exceed host size {len(nodes_sorted)}.")
	host = nodes_sorted[rank - 1]
	if host in taken_hosts: 
		raise CustomizedError(f"Host of specified rank {rank} is already taken.")
	taken_hosts.append(host)
	return host

def match_percentile(nodes_sorted: list[int], taken_hosts: list[int], percentile: Tuple[int, int]) -> int:
	## A function to match one seed by percentile to the host
	### Output: host: An int
	if len(taken_hosts) == len(nodes_sorted): 
		raise CustomizedError("There is no host left to match for percentile method.")
	if len(percentile) != 2:
		raise CustomizedError(f"The percentile range {percentile} is not a tuple.")
	l_per, h_per = percentile
	not_int = type(l_per) != int or type(h_per) != int
	not_0_100 = min(l_per, h_per) < 0 or max(l_per, h_per) > 100
	if not_int or not_0_100:
		raise CustomizedError(f"The percentile range {percentile} is not a tuple of two 0 - 100 integer.")
	if h_per <= l_per:
		raise CustomizedError(f"The percentile range {percentile} is not a valid interval.")
	node_per_percent = len(nodes_sorted) / 100
	l_per, h_per = percentile
	low_idx = math.ceil(node_per_percent * l_per)
	high_idx = math.floor(node_per_percent * h_per)
	if high_idx > low_idx: 
		hosts_in_range = set(nodes_sorted[low_idx:high_idx])
		taken_hosts_in_range = hosts_in_range.intersection(taken_hosts)
		available_host = list(hosts_in_range.difference(taken_hosts_in_range))
		if available_host == []: 
			raise CustomizedError(f"There is no host left to match in the range {percentile}%.")
		host = sample(available_host, 1)[0]
		taken_hosts.append(host)
		return host
	else:
		raise CustomizedError(f"There is no host left to match in the range {percentile}%")
	
def write_match(match_dict: dict[int, int], wk_dir: str):
	## A function to write the matching to a csv file in the working directory
	sorted_match = dict(sorted(match_dict.items()))
	_save_dict_to_csv(sorted_match, os.path.join(wk_dir, "seed_host_match.csv"))

def match_all_hosts(ntwk_: nx.Graph, match_method: dict[int, str], param: dict[int, Union[int, Tuple[int, int], None]], num_seed: int) -> dict[int, int]:
	## A function to match each seed to one host given the matching method.
	### Output: A dictionary of the matching (key: the host id, value: the seed id, e.g. {232:0, 256:1, 790:2, 4:3, 760:4})

	if num_seed != len(param.keys()): 
		raise CustomizedError(f"Please provide a matching parameter for each seed. (Length of matching parameter {len(param.keys())} doesn't match number of seed {num_seed})")
	if num_seed != len(match_method.keys()): 
		raise CustomizedError(f"Please provide a matching method for each seed. (Length of matching method {len(match_method.keys())} doesn't match number of seed {num_seed})")
	dict_edges_node = _build_dict_edges_node(ntwk_)
	nodes_sorted, _ = _sort_node_by_edge(dict_edges_node)
	taken_hosts_id = []

    # Dictionary mapping matching method to corresponding match function
	match_functions = {'ranking': match_ranking, 'percentile': match_percentile,'random': match_random}
	dict_method_seeds = {'ranking': [], 'percentile': [], 'random': []}
	for _ , (seed_id, method) in enumerate(match_method.items()):
		dict_method_seeds[method].append(seed_id)	
	
	# max_rank = max(dict_method_seeds['ranking'])
	# if max_rank > ntwk_.number_of_nodes():
	# 	raise CustomizedError(f"The lowest given rank {max_rank} for matching is larger than the host population size.")
	match_dict = {}
	# Processing methods in the specified order
	for method in ['ranking', 'percentile', 'random']:
		match_function = match_functions[method]
		for seed_id in dict_method_seeds[method]:
			matched_host = match_function(nodes_sorted, taken_hosts_id, param[seed_id])
			match_dict[matched_host] = seed_id
	return match_dict

def read_config_and_match(file_path: str, method: str, ntwk_: nx.Graph, num_seed: int):
	## A function to read from config file and do matching
	config = read_params(file_path)["SeedHostMatching"]["randomly_generated"]
	method_random_y = config["method"]
	match_params_path = config["path_csv"]
	if method_random_y in ["random", "percentile", "ranking"]:
		match_all_hosts(ntwk_, {seed: method_random_y for seed in range(num_seed)}, {seed: None for seed in range(num_seed)})
	else:
		df = pd.read_csv(match_params_path)
		match_method = dict(zip(df['seed'], df['match_method']))
		param = dict(zip(df['seed'], df['param']))
		match_all_hosts(ntwk_, match_method, param)

def run_seed_host_match(method, wkdir, num_seed, path_matching="", match_scheme="", match_scheme_param = ""):

	ntwk_path = os.path.join(wkdir, "contact_network.adjlist")

	try:
		if method=="user_input":
			if path_matching=="":
				raise CustomizedError("Path to the user-provided matching file (-path_matching) needs to be provided in user_provided mode.")
			elif os.path.exists(path_matching) == False:
				raise FileNotFoundError("Path to the user-provided matching file (-path_matching) doesn't exist.")
			else: 
				read_user_matchingfile(path_matching)

		elif method=="randomly_generate":
			# if not match_scheme in ["ranking", "random", "percentile"]:
			# 	raise CustomizedError("Please provided a permitted matching scheme (-match_scheme: random/ranking/random/percentile/customized.")
			write_match(match_all_hosts(ntwk_=read_network(ntwk_path), match_method = match_scheme, param = match_scheme_param, num_seed = num_seed), wkdir)

		else:
			raise CustomizedError(f"Please provide a permitted method (-method): user_input/randomly_generate instead of your current input {method}.")
	except CustomizedError as e:
		print(f"Seed and host match - An error occured: {e.message}")



