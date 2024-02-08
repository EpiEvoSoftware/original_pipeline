import networkx as nx
import os
from random import sample
import json
import pandas as pd
import unittest
from base_func import read_params
from collections import defaultdict
from pathlib import Path
from error_handling import CustomizedError
from typing import Union, Tuple

# The path for the working pipeline
PIPELINE_PATH = os.path.dirname(__file__)
# The relative path for the testing folder
TEST_DIR = "test/seed_host_match_func"

# avail problem

def _build_dict_edges_node(ntwk_):
	## A helper function that returns a dictionary with number of edges as keys
	## and a list of nodes of corresponding degrees as values
	dict_edges_node = defaultdict(list)
	for node, n_edges in ntwk_.degree:
		dict_edges_node[n_edges].append(node)
	return dict_edges_node

def _sort_node_by_edge(dict_edges_node):
	## A helper function that returns a list of nodes reversely sorted by their 
	## degrees and a list of their corresponding degrees
	nodes_sorted = []
	degree_sorted = []
	for degree in sorted(dict_edges_node.keys(), reverse = True):
		nodes = dict_edges_node[degree]
		nodes_sorted.extend(nodes)
		degree_sorted.extend([degree]*len(nodes))
	return nodes_sorted, degree_sorted

def _save_dict_to_csv(dict_matching, file_path):
	## A helper function that saves the matching dictionary as a specified file
	## with columns ['host_id', 'seed']
	df = pd.DataFrame(list(dict_matching.items()), columns = ['host_id', 'seed'])
	df.to_csv(file_path, index = False)
 
def _read_user_matchingfile_info_json(file):
	## TO DO: to check the contents of json
	return file

def _read_user_matchingfile_info_csv(file):
	## TO DO: to check the contents of csv
	return file

def read_user_matchingfile(file_path):
	## A function to check whether the user-input host-seed matching file is valid
	## Raise exceptions when given file path is invalid / when contents of file
	## does not satisfy the seed-host matching format.
	
	file_path = Path(file_path)
	if not file_path.exists():
		raise FileNotFoundError(f"File {file_path} not found")
	if file_path.suffix.lower() == ".json":
		try:
			with open(file_path, 'r') as file:
				matching = json.load(file)
				return _read_user_matchingfile_info_json(matching)
		except json.JSONDecodeError:
			raise ValueError(f"Invalid JSON format in {file_path}")
	elif file_path.suffix.lower() == ".csv":
		try:
			matching = pd.read_csv(file_path)
			return _read_user_matchingfile_info_csv(matching)
		except pd.errors.ParserError:
			raise ValueError(f"Invalid CSV format in {file_path}")
	else:
		raise ValueError("Host-seed matching file is not CSV or JSON")

def read_network(network_path):
	network_path = Path(network_path)
	if not network_path.exists():
		raise FileNotFoundError(f"The provided networkX path '{network_path}' doesn't exist")
	return(nx.read_adjlist(network_path, nodetype=int))

def match_random(nodes_sorted: list[int], unavail: list[int]) -> int:
	### A function to return one random available host to match one seed
	### Input: nodes_sorted: available hosts to match sorted by degree in reverse order
	### Output: host: An int for host id in the network graph
	if len(nodes_sorted) == 0: raise CustomizedError("All hosts already taken")
	for id in unavail:
		if id in nodes_sorted: nodes_sorted.remove(id)
	host = sample(nodes_sorted, 1)[0]
	nodes_sorted.remove(host)
	return host

def match_ranking(nodes_sorted: list[int], rank, unavail: list[int]) -> int:
	## A function to match one seed by rank (=degree of connectivity) to the host
	### Input: nodes_sorted: hosts sorted by degree in reverse order
	###        unavail: a list of unavailable host id (already matched)
	###        rank: the desired rank of the host
	### Output: host: An int for host id in the network graph
	if len(unavail) >= len(nodes_sorted): raise CustomizedError("All host already taken")
	host = nodes_sorted[rank - 1]
	if host in unavail: raise CustomizedError("Host of specified rank already taken")
	return host

def match_percentile(nodes_sorted, percentile, unavail_id):
	## A function to match one seed by percentile to the host
	### Input: nodes_sorted: host sorted by degree in reverse order
	###        unavail: a list of unavailable host id (already matched)
	###        percentile: the desired percentile for host selection
	pass
	

def match_all_hosts(ntwk_: nx.Graph, match_method: dict[int, str], param: list[Union[int, Tuple[int, int]]] = []) -> dict[int, int]:
	## A function to match each seed to one host given the matching method.
	### Input: ntwk_: A networkX object
	###		   match_method: A dictionary with seed id as key and matching method as value
	###        param: A list of int for seeds with rankding or (int, int) for seeds with percentile interval (None for seed with 'random' as matching method)

	### Output: A dictionary of the matching (key: the host id, value: the seed id, e.g. {232:0, 256:1, 790:2, 4:3, 760:4})

	dict_edges_node = _build_dict_edges_node(ntwk_)
	nodes_sorted, _ = _sort_node_by_edge(dict_edges_node)
	unavail_id = []

	dict_method_seeds = {}
	for idx in match_method:
		if match_method[idx] in dict_method_seeds:
			dict_method_seeds[match_method[idx]] += [idx]
		else:
			dict_method_seeds[match_method[idx]] = [idx]
	match_dict = {}

	for seed in dict_method_seeds['ranking']:
		matched_host = match_ranking(nodes_sorted, param[seed], unavail_id)
		unavail_id.append(matched_host)
		match_dict[matched_host] = seed
	# for seed in dict_method_seeds['percentile']:
	# 	matched_host = match_percentile(nodes_sorted, percentile[seed], unavail_id)
	# 	unavail_id.append(matched_host)
	# 	match_dict[matched_host] = seed
	for seed in dict_method_seeds['random']:
		matched_host = match_random(nodes_sorted, unavail_id)
		unavail_id.append(matched_host)
		match_dict[matched_host] = seed
	return match_dict

# TO DO: Read Config and match
def read_config(file_path, ntwk_):
	## A function to read from config file and do matching
	### Input: file_path: A string for the absolute config file path
	###		   ntwk_: A networkX object
	config = read_params(file_path)
	params = config["SeedHostMatching"]["randomly_generate"]
	match_method = params["method"]
	seed_size = len(match_method)
	percentile = params["percentile"]
	ranking = params["percentile"]
	match_all_hosts(ntwk_, match_method, seed_size, percentile, ranking)

def write_match(match_dict, wk_dir):
	## A function to write the matching to a csv file in the working directory
	## The order of writing is subject to the order of the chosen host id
	### Input: match_dict: A dictionary of the matching
	###        wk_dir: working directory
	### Output: no return value
	sorted_match = dict(sorted(match_dict.items()))
	# with open(os.path.join(wk_dir, "seed_host_match.txt"), "w") as txt:
	# 	for i in sorted_match:
	# 		txt.write(",".join([str(i), str(sorted_match[i])]) + "\n")
	_save_dict_to_csv(sorted_match, os.path.join(wk_dir, "seed_host_match.csv"))

class HostSeedMatch(unittest.TestCase):

	def test_read_user_matchingfile(self):
		## TO DO: Test the helper functions _check_user_matchingfile_info_json
		## 		and _check_user_matchingfile_info_csv
		pass

	def test_read_user_matchingfile_info_json(file):
		## TO DO: check json file
		pass

	def test_read_user_matchingfile_info_csv(file):
		## TO DO: check csv file
		pass

	def test_read_network(self):
		file_path_network_r = os.path.join(PIPELINE_PATH, TEST_DIR, "test_read_network.adjlist")
		file_path_network_error = os.path.join(PIPELINE_PATH, TEST_DIR, "test_read_network_error.adjlist")
		G = nx.path_graph(4)
		F = nx.path_graph(4)
		nx.write_adjlist(G, file_path_network_r)

		nw = read_network(file_path_network_r)
		self.assertEqual(nx.utils.misc.graphs_equal(G, nw), True)

	def test_match_random(self):
		nodes_0 = [0]
		host_0 = match_random(nodes_0, [])
		self.assertEqual(host_0, 0)

		nodes_1 = [0, 1]
		host_1 = match_random(nodes_1, [0])
		self.assertEqual(host_1, 1)

		nodes_2 = [0, 1, 2]
		host_2 = match_random(nodes_2, [0, 1])
		self.assertEqual(host_2, 2)

	def test_match_percentile(self):
		pass

	def test_match_ranking(self):
		nodes_0 = [0]
		host_0 = match_ranking(nodes_0, 1, [])
		self.assertEqual(host_0, 0)

		nodes_1 = [0, 1]
		host_1 = match_ranking(nodes_1, 2, [])
		self.assertEqual(host_1, 1)

		nodes_2 = [0, 1, 2]
		host_2 = match_ranking(nodes_2, 3, [])
		self.assertEqual(host_2, 2)

	def test_match_all_hosts(self):
		G = nx.Graph()
		G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (6, 7), (6, 8), (6, 9), (6, 10), (11, 12), (11, 13), (11, 14), (15, 16), (15, 17), (18, 19)])
		match_method_0 = {0: 'ranking', 1: 'ranking', 2: 'ranking', 3: 'ranking', 4: 'random'}
		param_0 = list(range(1, 5)) + [None]
		match_0 = match_all_hosts(G, match_method_0, param_0)
		print(match_0)
		self.assertEqual(match_0[0], 0)
		self.assertEqual(match_0[6], 1)
		self.assertEqual(match_0[11], 2)
		self.assertEqual(match_0[15], 3)

	def test_write_match(self):
		pass

	def test_build_dict_edges_node(self):
		# 0 edge
		G = nx.Graph()
		self.assertEqual(_build_dict_edges_node(G), {})
		# 1 edge
		G.add_edge(0, 1)
		self.assertEqual(_build_dict_edges_node(G), {1: [0, 1]})
		# 2 edges
		G.add_edges_from([(1, 3)])
		G.add_node(2)
		self.assertEqual(_build_dict_edges_node(G), {0: [2], 1: [0, 3], 2:[1]})

	def test_sort_node_by_edge(self):
		# 0 edge
		G = nx.Graph()
		dict_edges_node_0 = _build_dict_edges_node(G)
		self.assertEqual(_sort_node_by_edge(dict_edges_node_0), ([], []))
		# 1 edge
		G.add_edge(0, 1)
		dict_edges_node_1 = _build_dict_edges_node(G)
		self.assertEqual(_sort_node_by_edge(dict_edges_node_1), ([0, 1], [1, 1]))
		# 2 edges
		G.add_edges_from([(1, 3)])
		G.add_node(2)
		dict_edges_node_2 = _build_dict_edges_node(G)
		self.assertEqual(_sort_node_by_edge(dict_edges_node_2), ([1, 0, 3, 2], [2, 1, 1, 0]))

	def test_save_dict_to_csv(self):
		dict_matching_empty = {}
		file_path_empty = os.path.join(PIPELINE_PATH, TEST_DIR, "empty_dict_to_csv.csv")
		_save_dict_to_csv(dict_matching_empty, file_path_empty)
		df_empty = pd.read_csv(file_path_empty)
		self.assertEqual(df_empty.columns.tolist(), ['host_id', 'seed'])

		dict_matching_one = {0: 0}
		file_path_one = os.path.join(PIPELINE_PATH, TEST_DIR, "one_dict_to_csv.csv")
		_save_dict_to_csv(dict_matching_one, file_path_one)
		df_one = pd.read_csv(file_path_one)
		self.assertEqual(df_one['host_id'][0], 0)
		self.assertEqual(df_one['host_id'][0], 0)

		dict_matching_two = {0: 1, 1: 0}
		file_path_two = os.path.join(PIPELINE_PATH, TEST_DIR, "two_dict_to_csv.csv")
		_save_dict_to_csv(dict_matching_two, file_path_two)
		df_two = pd.read_csv(file_path_two)
		self.assertEqual(df_two['host_id'][0], 0)
		self.assertEqual(df_two['seed'][1], 0)

def run_seed_host_match(method, wkdir, seed_size, host_size, path_matching="", match_scheme="", ranking=[], percentile=[]):
	run_check = True

	ntwk_path = os.path.join(wkdir, "contact_network.adjlist")
	if os.path.exists(ntwk_path)==False:
		print("Doesn't detect a contact network file in the working directory. Please run network_generation first before running this script and make sure using the consistent working directory.")
		run_check = False

	if method=="user_input":
		if path_matching=="":
			print("Path to the user-provided matching file (-path_matching) needs to be provided in user_provided mode.")
			run_check = False
		elif os.path.exists(path_matching)==False:
			print("Path to the user-provided matching file (-path_matching) doesn't exist.")
			run_check = False
	elif method=="randomly_generate":
		if match_scheme=="random":
			run_check = True
		elif match_scheme=="ranking":
			if ranking==[]:
				print("Please provide a rank of contact degree of hosts (-ranking) for each seed.")
				run_check = False
			elif len(ranking)!=seed_size:
				print("Please provide a rank of contact degree of hosts (-ranking) for each seed. (Length doesn't match)")
				run_check = False
			elif max(ranking) >= host_size:
				print("Ranking cannot exceed host size.")
				run_check = False
			else:
				ranking_regen = {i: ranking[i] for i in range(seed_size)}
		elif match_scheme=="percentile":
			if percentile==[]:
				print("Please provide a percentile of contact degree of hosts (-percentile) for each seed.")
				run_check = False
			elif len(percentile) != 2 * seed_size:
				print("Length of the percentiles provided (-percentile) has to be at 2 times the seed size, as the lower bound and higher bound of percentage for each seed needs to be specified.")
				run_check = False
			elif any(percentile[2 * i] > percentile[2 * i + 1] for i in range(seed_size)):
				print("For each seed's percentile (-percentile), the lower bound needs to be ahead of the higher bound. And each seed has to be specified in order.")
				run_check = False
			elif max(percentile)>100:
				print("For each seed's percentile (-percentile), it has to be a number between 0 and 100.")
				run_check = False
			else:
				percentile_regen = {i: (percentile[2 * i], percentile[2 * i + 1]) for i in range(seed_size)}
		else:
			print("Please provided a permitted matching scheme (-match_scheme: random/ranking/percentile).")
			run_check = False
	else:
		run_check = False
		print("Please provide a permitted method (-method): user_input/randomly_generate.")

	if run_check:
		if method=="user_input":
			if check_user_matchingfile(path_matching):
				print("UNFINISHED")  ##################################################### UNFINISHED ###############################################
		elif method=="randomly_generate":
			if match_scheme=="random":
				match_all_hosts(ntwk_=read_network(ntwk_path), match_method = {i:match_scheme for i in range(seed_size)})
			elif match_scheme=="ranking":
				match_all_hosts(read_network(ntwk_path), match_method = {i:match_scheme for i in range(seed_size)}, param=ranking_regen)
			elif match_scheme=="percentile":
				match_all_hosts(ntwk_=read_network(ntwk_path), match_method = {i:match_scheme for i in range(seed_size)}, param=percentile_regen)
	else:
		print("Terminated because of incorrect input")
#
#if __name__ == '__main__':
 #   unittest.main()

# ################ Testing #######################
# ntwk = read_network("/Users/px54/Documents/TB_software/V2_code/test/contact_network.adjlist")
# ############ To test other methods, change "random" here to "ranking" or "percentile", and specify the parameters for them
# mtch = match_all_hosts(ntwk, "random", 5)
# ########### Change the directories to your own directory for testing
# write_match(mtch, "/Users/px54/Documents/TB_software/V2_code/test")
