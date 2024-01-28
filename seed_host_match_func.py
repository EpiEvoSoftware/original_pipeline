import networkx as nx
import os
from random import sample
import json
import pandas as pd
import unittest

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
	nodes_sorted = ntwk_.number_of_nodes*[None]
	degree_sorted = len(nodes_sorted)*[None]
	degrees = sorted(dict_edges_node.keys(), reverse = True)
	idx_acc = 0
	for d in degree_sorted:
		len_nodes = len(dict_edges_node[d])
		nodes_sorted[idx_acc: idx_acc + len_nodes] = dict_edges_node[d]
		degree_sorted[idx_acc: idx_acc + len_nodes] = [d]*len_nodes
		idx_acc += len_nodes
	return nodes_sorted, degree_sorted

def _save_dict_to_csv(dict_matching, file_path):
	## A helper function that saves the matching dictionary as a specified file
	df = pd.DataFrame(list(dict_matching.items()), columns = ['seed', 'host_id'])
	df.to_csv(file_path)
 
def _check_user_matchingfile_info_json(file):
	## To do: to check the contents of json
	pass

def _check_user_matchingfile_info_csv(file):
	## To do: to check the contents of csv
	pass

def check_user_matchingfile(file_path):
	## A function to check whether the user-input host-seed matching file is valid
	## If the file is not a json or csv, will throw an exception
	## If the matching contains conflicting information or lacks information, will
	## throw aother exception
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
		return(nx.read_adjlist(network_path))
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

def match_quantile(nodes_sorted, quantile, unavail=[]):
	## A function to match one seed by quantile to the host
	### Input: nodes_sorted: host sorted by degree in reverse order
	###        unavail: a list of unavailable host id (already matched)
	###        quantile: the desired rank of the host
	assert len(nodes_sorted) != len(unavail), "All hosts already taken"
	assert quantile in [[0, 25], [25, 50], [50, 75], [75, 100]], "Incorrect quantile input"
	assert len(nodes_sorted) >= 4, "Network size < 4; too small to use quantile"
	start, end = quantile
	start = int(round(start * len(nodes_sorted)))
	end = int(round(end * len(nodes_sorted)))
	cond = False
	host = None
	while cond == False:
		host = sample(nodes_sorted[start:end], 1)[0]
		if not host in unavail: cond = True
	if host == None: raise Exception("All hosts in specified quantitle already matched")
	return host

def match_all_hosts(ntwk_, match_method, seed_size, ranking=[], quantile=[]):
	## A function to match each seed to one host given the matching method.
	## Attention: The matching will be executed for each seed subsequently (the seed with a smaller id will be matched earlier and other seed cannot take those matched hosts)
	### Input: ntwk_: A networkX object read by read_network()
	###		   match_method: Method of matching
	###        seed_size: How many seeds should be matched (e.g. 5)
	###        rank: A list of integers that shows ranking of contact degree for each seed (having length = seed_size, e.g. [1, 250, 300, 400, 700])
	###        quantile: A list of lists that shows quantiles of contact degree for each seed (having length = seed_size, e.g. [[0, 25], [0, 25], [0, 25], [0, 25], [0, 25]])
	### Output: A dictionary of the matching (key: the host id, value: the seed id, e.g. {232:0, 256:1, 790:2, 4:3, 760:4})

	dict_edges_node = _build_dict_edges_node(ntwk_)
	nodes_sorted, degree_sorted = _sort_node_by_edge(ntwk_, dict_edges_node)
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
	for seed in dict_method_seeds['quantile']:
		matched_host = match_quantile(nodes_sorted, quantile[seed], unavail_id)
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
	_save_dict_to_csv(os.path.join(wk_dir, "seed_host_match.csv"))

	import unittest

class HostSeedMatch(unittest.TestCase):

    def test_check_user_matchingfile(self):
      pass
    
    def read_network(self):
      pass
    
    def match_random(self):
      pass

    def match_quantile(self):
      pass

    def match_ranking(self):
      pass

    def match_all_hosts(self):
      pass

    def write_match(self):
      pass

if __name__ == '__main__':
    unittest.main()

################ Testing #######################
ntwk = read_network("/Users/px54/Documents/TB_software/V2_code/test/contact_network.adjlist")
############ To test other methods, change "random" here to "ranking" or "quantile", and specify the parameters for them
mtch = match_all_hosts(ntwk, "random", 5)
########### Change the directories to your own directory for testing
write_match(mtch, "/Users/px54/Documents/TB_software/V2_code/test")
