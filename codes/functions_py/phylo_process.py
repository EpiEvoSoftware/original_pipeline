"""
Functions for dealing with trees (convert .trees to .nwk or rename .nwk file)

Author: Perry Xu
Date: November 6, 2023
"""

import tskit
import re

def rename_by_host(wkdir):
	"""
	Create a newick file for seeds' phylogeny with replaced seed ids.

	:param wkdir: The data directory of input seeds' phylogeny
	:type wkdir: str
	"""
	all_names = {}
	with open(wkdir + "seeds.name", "r") as names:
		for line in names:
			ll = line.rstrip("\n")
			l = ll.split(",p")
			all_names[l[0]] = l[1]
	nwk_ori = open(wkdir + "seeds.nwk", "r+")
	nwk_out = open(wkdir + "seeds.renamed.nwk", "a+")
	for tree_l in nwk_ori.readlines():
		take = 0
		index_now = ""
		new_line = ""
		for i in tree_l:
			if take==0:
				if i=="(" or i==",":
					take = 1
				new_line = new_line + i
			elif take==1:
				if i=="(":
					index_now = ""
					new_line = new_line + i
				elif i==":":
					take = 0
					new_line = new_line + all_names[index_now] + "_1:"
					index_now = ""
				else:
					index_now = index_now + i
	nwk_out.write(new_line)
	

####????????????????????????????????????????????
# I think the function below is the same as the one above, so I commented it out.
# def rename_by_host(wkdir):
# 	all_names = {}
# 	with open(wkdir + "seeds.name", "r") as names:
# 		for line in names:
# 			ll = line.rstrip("\n")
# 			l = ll.split(",p")
# 			all_names[l[0]] = l[1]
# 	nwk_ori = open(wkdir + "seeds.nwk", "r+")
# 	nwk_out = open(wkdir + "seeds.renamed.nwk", "a+")
# 	for tree_l in nwk_ori.readlines():
# 		take = 0
# 		index_now = ""
# 		new_line = ""
# 		for i in tree_l:
# 			if take==0:
# 				if i=="(" or i==",":
# 					take = 1
# 				new_line = new_line + i
# 			elif take==1:
# 				if i=="(":
# 					index_now = ""
# 					new_line = new_line + i
# 				elif i==":":
# 					take = 0
# 					new_line = new_line + all_names[index_now] + "_1:"
# 					index_now = ""
# 				else:
# 					index_now = index_now + i
# 	nwk_out.write(new_line)
