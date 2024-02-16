import unittest
from seed_host_match_func import read_network, match_random, match_ranking, match_percentile, match_all_hosts, write_match, _build_dict_edges_node, _sort_node_by_edge, _save_dict_to_csv
import os
import networkx as nx
import pandas as pd
# The path for the working pipeline
PIPELINE_PATH = os.path.dirname(__file__)
# The relative path for the testing folder
TEST_DIR = "test/seed_host_match_func"


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
		nodes_0 = [0]
		host_0 = match_percentile(nodes_0, [], [0, 100])
		self.assertEqual(host_0, 0)

		nodes_1 = [0, 1]
		host_1 = match_percentile(nodes_1, [], [50, 100])
		self.assertEqual(host_1, 1)

		nodes_2 = [0, 1, 2]
		host_2 = match_percentile(nodes_2, [], [30, 70])
		self.assertEqual(host_2, 1)

	def test_match_ranking(self):
		nodes_0 = [0]
		host_0 = match_ranking(nodes_0, [], 1)
		self.assertEqual(host_0, 0)

		nodes_1 = [0, 1]
		host_1 = match_ranking(nodes_1, [], 2)
		self.assertEqual(host_1, 1)

		nodes_2 = [0, 1, 2]
		host_2 = match_ranking(nodes_2, [], 3)
		self.assertEqual(host_2, 2)

	def test_match_all_hosts(self):
		G = nx.Graph()
		G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (6, 7), (6, 8), (6, 9), (6, 10), (11, 12), (11, 13), (11, 14), (15, 16), (15, 17), (18, 19)])
		match_method_0 = {0: 'ranking', 1: 'ranking', 2: 'ranking', 3: 'ranking', 4: 'random'}
		param_0 = {0: 1, 1: 2, 2:3, 3:4, 4: None}
		# param_0 = {0: 1, 1: 2, 2:3, 3:4}
		match_0 = match_all_hosts(G, match_method_0, param_0, 5)
		self.assertEqual(match_0[0], 0)
		self.assertEqual(match_0[1], 6)
		self.assertEqual(match_0[2], 11)
		self.assertEqual(match_0[3], 15)

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
		self.assertEqual(df_empty.columns.tolist(), ['seed', 'host_id'])

		dict_matching_one = {0: 0}
		file_path_one = os.path.join(PIPELINE_PATH, TEST_DIR, "one_dict_to_csv.csv")
		_save_dict_to_csv(dict_matching_one, file_path_one)
		df_one = pd.read_csv(file_path_one)
		self.assertEqual(df_one['host_id'][0], 0)

		dict_matching_two = {0: 1, 1: 0}
		file_path_two = os.path.join(PIPELINE_PATH, TEST_DIR, "two_dict_to_csv.csv")
		_save_dict_to_csv(dict_matching_two, file_path_two)
		df_two = pd.read_csv(file_path_two)
		self.assertEqual(df_two['host_id'][0], 1)
		self.assertEqual(df_two['seed'][1], 1)

if __name__ == '__main__':
    unittest.main()