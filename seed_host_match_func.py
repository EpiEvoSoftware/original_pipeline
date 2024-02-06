import networkx as nx
import os
from random import sample
import unittest


### SHENNI's

def _build_dict_edges_node(ntwk_):
	## A helper function that returns a dictionary with number of edges as keys
	## and nodes as values
	dict_edges_node = {}
	for node, n_edges in ntwk_.degree:
		if n_edges not in dict_edges_node:
			dict_edges_node[n_edges] = [node]
		else:
			dict_edges_node[n_edges] += [node]
	return dict_edges_node


def _sort_node_by_edge(ntwk_, dict_edges_node):
	## A helper function that returns a list of nodes reversely sorted by their 
	## degrees and a list of corresponding degrees
	nodes_sorted = ntwk_.number_of_nodes()*[None]
	degree_sorted = len(nodes_sorted)*[None]
	degrees = sorted(dict_edges_node.keys(), reverse = True)
	idx_acc = 0
	for d in degrees:
		len_nodes = len(dict_edges_node[d])
		nodes_sorted[idx_acc: idx_acc + len_nodes] = dict_edges_node[d]
		degree_sorted[idx_acc: idx_acc + len_nodes] = [d]*len_nodes
		idx_acc += len_nodes
	return nodes_sorted, degree_sorted

def _save_dict_to_csv(dict_matching, file_path):
	## A helper function that saves the matching dictionary as a specified file
	## with columns ['host_id', 'seed']
	df = pd.DataFrame(list(dict_matching.items()), columns = ['host_id', 'seed'])
	df.to_csv(file_path, index = False)
 
def _check_user_matchingfile_info_json(file):
	## To do: to check the contents of json
	pass

def _check_user_matchingfile_info_csv(file):
	## To do: to check the contents of csv
	pass


def check_user_matchingfile(file_path):
	## A function to check whether the user-input host-seed matching file is valid
	## Raise exceptions when given file path is invalid / when contents of file
	## does not satisfy the seed-host matching format.
	if file_path.lower().endswith('.json'):
		try:
			with open(file_path, 'r') as file:
				matching = json.load(file)
				return _check_user_matchingfile_info_json(matching)
		except (json.JSONDecodeError, FileNotFoundError):
			raise ("Invalid json format or path for host-seed matching")
	elif file_path.lower().endswith('.csv'):
		try:
			matching = pd.read_csv(file_path)
			return _check_user_matchingfile_info_csv(matching)
		except (UnicodeDecodeError, FileNotFoundError):
			raise ("Invalid csv format or path for host-seed matching")
	else:
		raise ("Host-seed matching file is not csv or json")

def read_network(network_path):
	if os.path.exists(network_path):
		## Check format
		return(nx.read_adjlist(network_path, nodetype=int))
	else:
		raise ("The provided networkX path doesn't exist")

def match_random(nodes_sorted, unavail=[]):
	### A function to return one random available host to match one seed
	### Input: nodes_sorted: hosts sorted by degree in reverse order
	###        unavail: a list of unavailable host id (already matched)
	assert nodes_sorted != len(unavail), "All hosts already taken"
	cond = False
	host = None
	while cond == False:
		host = sample(nodes_sorted, 1)[0]
		if not host in unavail: cond = True
	return host

def match_ranking(nodes_sorted, rank, unavail=[]):
	## A function to match one seed by rank (=degree of connectivity) to the host
	### Input: nodes_sorted: hosts sorted by degree in reverse order
	###        unavail: a list of unavailable host id (already matched)
	###        rank: the desired rank of the host
	assert nodes_sorted != len(unavail), "All hosts already taken"
	host = nodes_sorted[rank - 1]
	if host in unavail: raise ("Host of specified rank already taken")
	return host

def match_percentile(nodes_sorted, percentile, unavail=[]):
	## A function to match one seed by percentile to the host
	### Input: nodes_sorted: host sorted by degree in reverse order
	###        unavail: a list of unavailable host id (already matched)
	###        percentile: the desired percentile for host selection
	assert len(nodes_sorted) != len(unavail), "All hosts already taken"
	assert percentile in [[0, 25], [25, 50], [50, 75], [75, 100]], "Incorrect percentile input"
	assert len(nodes_sorted) >= 4, "Network size < 4; too small to use percentile"
	start, end = percentile
	start = int(round(start * len(nodes_sorted)))
	end = int(round(end * len(nodes_sorted)))
	cond = False
	host = None
	while cond == False:
		host = sample(nodes_sorted[start:end], 1)[0]
		if not host in unavail: cond = True
	if host == None: raise Exception("All hosts in specified quantitle already matched")
	return host

def match_all_hosts(ntwk_, match_method, seed_size, ranking=[], percentile=[]):
	## A function to match each seed to one host given the matching method.
	## Attention: The matching will be executed for each seed subsequently (the seed with a smaller id will be matched earlier and other seed cannot take those matched hosts)
	### Input: ntwk_: A networkX object read by read_network()
	###		   match_method: Method of matching
	###        seed_size: How many seeds should be matched (e.g. 5)
	###        rank: A list of integers or None that shows ranking of contact degree for each seed (having length = seed_size, e.g. [1, 250, 300, 400, , None, 700])
	###        percentile: A list of lists that shows percentiles of contact degree for each seed (having length = seed_size, e.g. [[0, 25], [0, 25], None, [0, 25], [0, 25], [0, 25]])
	### Output: A dictionary of the matching (key: the host id, value: the seed id, e.g. {232:0, 256:1, 790:2, 4:3, 760:4})

	dict_edges_node = _build_dict_edges_node(ntwk_)
	nodes_sorted, _ = _sort_node_by_edge(ntwk_, dict_edges_node)
	unavail_id = []

	dict_method_seeds = {}
	for idx in match_method:
		if match_method[idx] in dict_method_seeds:
			dict_method_seeds[match_method[idx]] = [idx]
		else:
			dict_method_seeds[match_method[idx]] += [idx]
	match_dict = {}

	for seed in dict_method_seeds['ranking']:
		matched_host = match_ranking(nodes_sorted, ranking[seed], unavail_id)
		unavail_id.append(matched_host)
		match_dict[matched_host] = seed
	for seed in dict_method_seeds['percentile']:
		matched_host = match_percentile(nodes_sorted, percentile[seed], unavail_id)
		unavail_id.append(matched_host)
		match_dict[matched_host] = seed
	for seed in dict_method_seeds['random']:
		matched_host = match_random(nodes_sorted, unavail_id)
		unavail_id.append(matched_host)
		match_dict[matched_host] = seed
	return match_dict

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

	def test_check_user_matchingfile(self):
		## TO DO: Test the helper functions _check_user_matchingfile_info_json
		## 		and _check_user_matchingfile_info_csv
		pass

	def test_check_user_matchingfile_info_json(file):
		## TO DO: check json file
		pass

	def test_check_user_matchingfile_info_csv(file):
		## TO DO: check csv file
		pass

	def test_read_network(self):
		file_path_network_r = os.path.join(script_path, TEST_DIR, "test_read_network.adjlist")
		file_path_network_error = os.path.join(script_path, TEST_DIR, "test_read_network_error.adjlist")
		G = nx.path_graph(4)
		F = nx.path_graph(4)
		nx.write_adjlist(G, file_path_network_r)

		nw = read_network(file_path_network_r)
		print(nw.adj)
		print(G.adj)
		self.assertEqual(nx.utils.misc.graphs_equal(G, nw), True)



		

	def test_match_random(self):
		pass

	def test_match_percentile(self):
		pass

	def test_match_ranking(self):
		pass

	def test_match_all_hosts(self):
		pass

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
		self.assertEqual(_sort_node_by_edge(G, dict_edges_node_0), ([], []))
		# 1 edge
		G.add_edge(0, 1)
		dict_edges_node_1 = _build_dict_edges_node(G)
		self.assertEqual(_sort_node_by_edge(G, dict_edges_node_1), ([0, 1], [1, 1]))
		# 2 edges
		G.add_edges_from([(1, 3)])
		G.add_node(2)
		dict_edges_node_2 = _build_dict_edges_node(G)
		self.assertEqual(_sort_node_by_edge(G, dict_edges_node_2), ([1, 0, 3, 2], [2, 1, 1, 0]))

	def test_save_dict_to_csv(self):
		dict_matching_empty = {}
		file_path_empty = os.path.join(script_path, TEST_DIR, "empty_dict_to_csv.csv")
		_save_dict_to_csv(dict_matching_empty, file_path_empty)
		df_empty = pd.read_csv(file_path_empty)
		self.assertEqual(df_empty.columns.tolist(), ['host_id', 'seed'])

		dict_matching_one = {0: 0}
		file_path_one = os.path.join(script_path, TEST_DIR, "one_dict_to_csv.csv")
		_save_dict_to_csv(dict_matching_one, file_path_one)
		df_one = pd.read_csv(file_path_one)
		self.assertEqual(df_one['host_id'][0], 0)
		self.assertEqual(df_one['host_id'][0], 0)

		dict_matching_two = {0: 1, 1: 0}
		file_path_two = os.path.join(script_path, TEST_DIR, "two_dict_to_csv.csv")
		_save_dict_to_csv(dict_matching_two, file_path_two)
		df_two = pd.read_csv(file_path_two)
		self.assertEqual(df_two['host_id'][0], 0)
		self.assertEqual(df_two['seed'][1], 0)


##### PERRY's

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
				percentile_regen = [[percentile[2 * i], percentile[2 * i + 1]] for i in range(seed_size)]
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
			match_all_hosts(read_network(ntwk_path), {i:match_scheme for i in range(seed_size)}, seed_size, ranking, percentile)
	else:
		print("Terminated because of incorrect input")


