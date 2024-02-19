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
# Magic numbers
HUNDRED = 100
ZERO = 0

def _build_dict_edges_node(ntwk_):
	## A helper function that returns a dictionary with degrees as keys
	## and a list of nodes of corresponding degrees as values
	## ntwk_: nx.Graph
	### Output: dict_edges_node: A dictionary with int as keys and int list as values dict[int, list[int]]
	dict_edges_node = defaultdict(list)
	[dict_edges_node[n_edges].append(node) for node, n_edges in ntwk_.degree]
	return dict_edges_node

def _sort_node_by_edge(dict_edges_node):
	## A helper function that returns a list of nodes reversely sorted by their 
	## degrees and a list of their corresponding degrees
	## dict_edges_node: dict[int, list[int]]
	### Output: nodes_sorted: A list of int list[int]
	### 		degree_sorted: A list of int list[int]
	nodes_sorted = []
	degree_sorted = []
	for degree in sorted(dict_edges_node.keys(), reverse = True):
		nodes = dict_edges_node[degree]
		nodes_sorted.extend(nodes)
		degree_sorted.extend([degree]*len(nodes))
	# degree_sorted is not used anywhere in the pipeline; we can delete it if we decide this is unnecessary
	return nodes_sorted, degree_sorted

def _save_dict_to_csv(dict_matching, file_path):
	## A helper function that saves the matching dictionary as a specified file
	## with columns ['seed', 'host_id']
	## dict_matching: dict[int, int]
	## file_path: str
	### Output: file_path: A string

	# changed the order of columns, it used to be ['host_id', 'seed']
	df = pd.DataFrame(list(dict_matching.items()), columns = ['seed', 'host_id'])
	df.to_csv(file_path, index = False)
 
def _read_user_matchingfile_info_json(file):
	## file: str
	## TO DO: to check the contents of json
	return file

def _read_user_matchingfile_info_csv(file):
	## file: str
	## TO DO: to check the contents of csv
	return file

def _percentile_to_index(percentile, node_per_percent):
	## A helper function that converts the percentile range to index range for the matching method ## 'percentile'
	## percentile: list[int, int]
	## node_per_percent: Union[float, int]
	### Output: A tuple of ints representing the range of indices to choose from Tuple[int, int]
	if len(percentile) != 2:
		raise CustomizedError(f"The percentile range {percentile} is not a list of two element.")
	l_per, h_per = percentile
	not_int = type(l_per) != int or type(h_per) != int
	not_0_100 = min(l_per, h_per) < ZERO or max(l_per, h_per) > HUNDRED
	if not_int or not_0_100:
		raise CustomizedError(f"The percentile range {percentile} is not a list of element of two 0 - 100 integers.")
	if h_per <= l_per:
		raise CustomizedError(f"The percentile range {percentile} is not a valid interval.")
	# round the index to make sure those are integers
	low_idx = math.ceil(node_per_percent * l_per)
	high_idx = math.floor(node_per_percent * h_per)
	return low_idx, high_idx

def read_user_matchingfile(file_path):
	## A function to check whether the user-input host-seed matching file is valid
	## Raise exceptions when given file path is invalid / when contents of file
	## does not satisfy the seed-host matching format.
	## file_path: str
	### Output: A dictionary of matching where seeds are the keys and host_id are the values
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
	## A function that read networks from a given path
	## network_path: str
	### Output: nx.Graph
	network_path = Path(network_path)
	if not network_path.exists():
		raise FileNotFoundError(f"The provided networkX path '{network_path}' doesn't exist. Please run network_generation first before running this script and make sure the given working directory is correct.")
	return nx.read_adjlist(network_path, nodetype=int)

def match_random(nodes_sorted, taken_hosts, param = None):
	### A function to return one random available host to match one seed
	## nodes_sorted: list[int]
	## taken_hosts: list[int]
	## param: None
	### Output: host: An int
	available_host = list(set(nodes_sorted).difference(set(taken_hosts)))
	host = sample(available_host, 1)[0]
	return host

def match_ranking(nodes_sorted: list[int], taken_hosts, rank):
	## A function to match one seed by rank (=degree of connectivity) to the host
	## nodes_sorted: list[int]
	## taken_hosts: list[int]
	## rank: int
	### Output: host: An int
	ntwk_size = len(nodes_sorted)
	if rank > ntwk_size:
		raise CustomizedError(f"Your provided ranking {rank} exceed host size {ntwk_size}.")
	host = nodes_sorted[rank - 1]
	if host in taken_hosts: 
		raise CustomizedError(f"Host of specified rank {rank} is already taken.")
	return host

def match_percentile(nodes_sorted, taken_hosts, percentile):
	## A function to match one seed by percentile to the host
	## nodes_sorted:  list[int]
	## taken_hosts: list[int]
	## percentile: list[int, int]
	### Output: host: An int
	node_per_percent = len(nodes_sorted) / 100
	low_idx, high_idx = _percentile_to_index(percentile, node_per_percent)
	if high_idx > low_idx:
		hosts_in_range = set(nodes_sorted[low_idx:high_idx])
		taken_hosts_in_range = hosts_in_range.intersection(taken_hosts)
		available_host = list(hosts_in_range.difference(taken_hosts_in_range))
		if available_host == []: 
			raise CustomizedError(f"There is no host left to match in the percentile {percentile}.")
		host = sample(available_host, 1)[0]
		return host
	raise CustomizedError(f"There is no host left to match in the range {percentile}%.")
	
def write_match(match_dict, wk_dir):
	## A function to write the matching to a csv file in the working directory
	## match_dict: dict[int, int]
	## wk_dir: str
	sorted_match = dict(sorted(match_dict.items()))
	_save_dict_to_csv(sorted_match, os.path.join(wk_dir, "seed_host_match.csv"))

def match_all_hosts(ntwk_, match_method, param, num_seed):
	## A function to match each seed to one host given the matching method.
	## ntwk_: nx.Graph
	##  match_method: dict[int, str]
	## param: dict[int, Union[int, list[int, int], None]]
	## num_seed: int
	### Output: A dictionary of the matching (key: the seed, value: the host id, e.g. {0: 232, 1:256, 2:790, 3:4, 4:760}) dict[int, int]
	ntwk_size = ntwk_.number_of_nodes()
	if num_seed > ntwk_size:
		raise CustomizedError(f"It is not allowed to match {num_seed} seeds to {ntwk_size} hosts. Please reduce the number of seeds or increase the host population size.")
	
	# Preprocess the network
	dict_edges_node = _build_dict_edges_node(ntwk_)
	nodes_sorted, _ = _sort_node_by_edge(dict_edges_node)
	taken_hosts_id = []

    # Gather the nodes by their matching method
	dict_method_seeds = {'ranking': [], 'percentile': [], 'random': []}
	# for _ , (seed_id, method) in enumerate(match_method.items()):
	# 	if method not in ['ranking', 'percentile', 'random']:
	# 		raise CustomizedError(f"Please provide a valid matching method in ('ranking', 'percentile', 'random') instead of {method} for seed {seed_id}")
	# 	dict_method_seeds[method].append(seed_id)
	for seed_id in range(num_seed):
		idx_method = match_method.get(seed_id)
		if idx_method not in [None, 'ranking', 'percentile', 'random']:
			raise CustomizedError(f"Please provide a valid matching method in ('ranking', 'percentile', 'random') instead of {method} for seed {seed_id}")
		dict_method_seeds[idx_method].append(seed_id) if idx_method != None else dict_method_seeds["random"].append(seed_id)
	
	# Define the matching function by the method param and process methods in the specified order
	match_functions = {'ranking': match_ranking, 'percentile': match_percentile,'random': match_random}
	match_dict = {}
	for method in ['ranking', 'percentile', 'random']:
		match_function = match_functions[method]
		for seed_id in dict_method_seeds[method]:
			matched_host = match_function(nodes_sorted, taken_hosts_id, param.get(seed_id))
			match_dict[seed_id] = matched_host
			taken_hosts_id.append(matched_host)
	return match_dict

def read_config_and_match(file_path, num_seed):
	## A function to read from config file and do matching
	## file_path: str
	## num_seed: int
	config_all = read_params(file_path)
	config = config_all["SeedHostMatching"]["randomly_generated"]
	match_method = config["match_scheme"]
	match_method_param = config["match_scheme_param"]
	path_matching = config_all["SeedHostMatching"]["user_input"]["path_matching"]
	method = "user_input" if path_matching != "" else "randomly_generated"
	run_seed_host_match(method=method, wkdir=config_all["BasicRunConfiguration"]["cwdir"], num_seed=num_seed, path_matching=path_matching, match_scheme=match_method, match_scheme_param=match_method_param)

def run_seed_host_match(method, wkdir, num_seed, path_matching="", match_scheme="", match_scheme_param = ""):
	## A function that supports the execution of seed_host_match in command line and saves the matching file in the specified diretcory
	
	# Process the match_scheme and parameters if the scheme is 'random' for all seeds
	
	# Read network
	ntwk_path = os.path.join(wkdir, "contact_network.adjlist")
	
	# Process the parameters and save the matching results have we match all host
	try:
		if method=="user_input":
			if path_matching=="":
				raise CustomizedError("Path to the user-provided matching file (-path_matching) needs to be provided in user_provided mode.")
			elif os.path.exists(path_matching) == False:
				raise CustomizedError("Path to the user-provided matching file (-path_matching) doesn't exist.")
			else: 
				read_user_matchingfile(path_matching)
		elif method=="randomly_generate":
			if match_scheme == "random":
				match_scheme = {seed_id: "random" for seed_id in range(num_seed)}
				match_scheme_param = {seed_id: None for seed_id in range(num_seed)}
			else:
				try:
					match_scheme = json.loads(match_scheme)
				except json.decoder.JSONDecodeError:
					raise CustomizedError(f"The match_scheme is not a valid json format.")
				
			if list(set(match_scheme.values())) != ["random"]:
				try:
					match_scheme_param = json.loads(match_scheme_param)
				except json.decoder.JSONDecodeError: 
					raise CustomizedError(f"The match_scheme_param is not a valid json format.")

			write_match(match_all_hosts(ntwk_=read_network(ntwk_path), match_method = match_scheme, param = match_scheme_param, num_seed = num_seed), wkdir)
			print(f"The matching process has successfully terminated. Please see working directory {wkdir}/seed_host_match.csv for the seed host matching file.")
		else:
			raise CustomizedError(f"Please provide a permitted method (-method): user_input/randomly_generate instead of your current input {method}.")
	except (CustomizedError, FileNotFoundError, ValueError) as e:
		print(f"Seed and host match - A violation of input parameters occured: {e}")



