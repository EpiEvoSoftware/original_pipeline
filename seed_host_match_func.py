import networkx as nx
import os
from random import sample

def check_user_matchingfile():
	### A function to check the format of the user-input seed-host matching file
	return(0)

def read_network(network_path):
	if os.path.exists(network_path):
		## Check format
		return(nx.read_adjlist(network_path))
	else:
		print("The provided network path doesn't exist.")


def match_random(ntwk_, unavail=[]):
	## A function to match one seed randomly to one available host (not yet matched)
	### Input: ntwk_: A network object
	###        unavail: a list of unavailable host id (already matched)
	node_list = list(range(nx.number_of_nodes(ntwk_)))
	node_list_avail = [x for x in node_list if x not in unavail]
	return(sample(node_list_avail, 1)[0])

def match_ranking(ntwk_, rank, unavail=[]):
	## A function to match one seed by rank to the host
	### Input: ntwk_: A network object
	###        unavail: a list of unavailable host id (already matched)
	###        rank: the desired rank of the host
	return(host_id)

def match_quantile(ntwk_, quantile, unavail=[]):
	## A function to match one seed by quantile to the host
	### Input: ntwk_: A network object
	###        unavail: a list of unavailable host id (already matched)
	###        rank: the desired rank of the host
	return(host_id)


def match_all_hosts(ntwk_, match_method, seed_size, ranking=[], quantile=[]):
	## A function to match each seed to one host given the matching method.
	## Attention: The matching will be executed for each seed subsequently (the seed with a smaller id will be matched earlier and other seed cannot take those matched hosts)
	### Input: ntwk_: A network object read by read_network()
	###		   match_method: Method of matching 
	###        seed_size: How many seeds should be matched (e.g. 5)
	###        rank: A list of integers that shows ranking of contact degree for each seed (having length = seed_size, e.g. [1, 250, 300, 400, 700])
	###        quantile: A list of lists that shows quantiles of contact degree for each seed (having length = seed_size, e.g. [[0, 25], [0, 25], [0, 25], [0, 25], [0, 25]])
	### Output: A dictionary of the matching (key: the host id, value: the seed id, e.g. {232:0, 256:1, 790:2, 4:3, 760:4})

	match_dict = {}
	if match_method=="random":
		unavail_id = []
		for i in range(seed_size):
			matched_host = match_random(ntwk_, unavail=unavail_id)
			match_dict[matched_host] = i
			unavail_id.append(matched_host)
	elif match_method=="ranking":
		unavail_id = []
		for i in range(seed_size):
			matched_host = match_random(match_ranking, ranking[i], unavail=unavail_id)
			match_dict[matched_host] = i
			unavail_id.append(matched_host)
	elif match_method=="quantile":
		unavail_id = []
		for i in range(seed_size):
			matched_host = match_random(match_ranking, quantile[i], unavail=unavail_id)
			match_dict[matched_host] = i
			unavail_id.append(matched_host)
	print(match_dict)
	return(match_dict)


def write_match(match_dict, wk_dir):
	## A function to write the matching to a csv file in the working directory
	## The order of writing is subject to the order of the chosen host id
	### Input: match_dict: A dictionary of the matching
	###        wk_dir: working directory
	### Output: no return value
	sorted_match = dict(sorted(match_dict.items()))
	with open(os.path.join(wk_dir, "seed_host_match.csv"), "w") as txt:
		for i in sorted_match:
			txt.write(",".join([str(i), str(sorted_match[i])]) + "\n")



################ Testing #######################
ntwk = read_network("/Users/px54/Documents/TB_software/V2_code/test/contact_network.adjlist")
############ To test other methods, change "random" here to "ranking" or "quantile", and specify the parameters for them
mtch = match_all_hosts(ntwk, "random", 5)
########### Change the directories to your own directory for testing
write_match(mtch, "/Users/px54/Documents/TB_software/V2_code/test")






