from base_func import *
import os
import statistics
import subprocess
from random import sample
import numpy as np
import pandas as pd


def seeds_trait_calc(wk_dir, dict_c_g):
	## A function to calculate trait values(trait value: sum of all mutation's effect sizes) of all seeds
	## of all the seeds
	## Attention: Has to be run after seeds_generator.py is run
	### Input: wk_dir: Working directory
	###		   dict_c_g: A dictionary that stores the genetic elements' effect sizes. 
	###                  Keys are gene names, values are lists, each list takes the form of
	###                  [start_pos(int), end_pos(int), effect_size(float)]
	### Output: A list of trait value (length = seed size)

	c = 0
	calc_sum = []
	seeds_vcf_dict = os.path.join(wk_dir, "originalvcfs/")
	if os.path.exists(seeds_vcf_dict):
		seeds = os.listdir(seeds_vcf_dict)
		for seed in seeds:
			calc_sum.append(0)
			with open(os.path.join(seeds_vcf_dict, seed), "r") as seed_vcf:
				for line in seed_vcf:
					if line.startswith("#"):
						continue
					else:
						ll = line.rstrip("\n")
						l = ll.split("\t")
						for gene in dict_c_g:
							if int(l[1]) >= dict_c_g[gene][0] and int(l[1]) <= dict_c_g[gene][1]:
								calc_sum[c] = calc_sum[c] + dict_c_g[gene][2]
				c = c + 1
	else:
		print("WARNING: seed_generator.py hasn't been run. If you want use seed sequence different than reference genome, please run seed_generator first.")
	
	return(calc_sum)



def generate_eff_vals(gff_, causal, es_low, es_high, wk_dir, n_gen, mut_rate, norm_or_not):
	## A function to randomly generate a set of effect sizes for some genes sampled from a gff-like annotation file.
	## Effect sizes will be uniformly sampled from [es_low, es_high], and can be normalized if needed.
	### Input: gff_: Full path to the gff-like file, that needs to take the form of a tab-delimed file,
	###              with each row representing one genetic element,
	###              the 4th column being the starting position, the 5th column being the ending position,
	###              the 9th column being the info column, which is ,delimted and the 3rd one is the name
	###        causal: Number of genetic elements that is going to be generated (int)
	###        es_low: Lower bound of the effect size that is going to be sampled (float)
	###		   es_high: Higher bound of the effect size that is going to be sampled (float)
	###        wk_dir: Working directory
	###        norm_or_not: Boolean variable, specifying whether the generated effect sizes will be normalized
	###        n_gen: Number of generations that is going to be simulated, only used when norm_or_not=T (int)
	###        mut_rate: Mutation rate, only used when norm_or_not=T (float)
	### Output: dict_causal_genes: A dictionary that stores the genetic elements' effect sizes. 
	###                            Keys are gene names, values are lists, each list takes the form of
	###                            [start_pos(int), end_pos(int), effect_size(float)]
	###         seeds_trait_vals: A list of trait values for each seed given the genetic elements' effect sizes generated
	g_len = 0
	with open(gff_, "r") as gff:
		for line in gff:
			if line.startswith("\n"):
				continue
			elif line.startswith("#"):
				continue
			else:
				g_len = g_len + 1
	genes = sample(range(int(g_len)), int(causal))

	dict_causal_genes = {}

	causal_length = []
	names = []
	starts = []
	ends = []
	coe = []

	with open(gff_, "r") as gff:
		index = 0
		for line in gff:
			if line.startswith("#") or line.startswith("\n") :
				continue
			else:
				if index in genes:
					ll = line.rstrip("\n")
					l = ll.split("\t")
					info = l[8].split(";")
					causal_length.append(int(l[4])-int(l[3])+1)
					dict_causal_genes[info[0].split("=")[1]] = [int(l[3]), int(l[4]), np.random.uniform(float(es_low), float(es_high), 1)[0]]
				index = index + 1
		if norm_or_not:
			dict_causal_genes = normalization_by_mutscounts(wk_dir, dict_causal_genes, n_gen, mut_rate)
	seeds_trait_vals = seeds_trait_calc(wk_dir, dict_causal_genes)

	return(dict_causal_genes, seeds_trait_vals)

def normalization_by_mutscounts(wk_dir, dict_c_g, n_gen, mut_rate):
	## A function to normalize the effect sizes based on the expected trait values at the end of the simulation
	### Input: wk_dir: Working directory
	###		   dict_c_g: A dictionary that stores the genetic elements' effect sizes. 
	###                  Keys are gene names, values are lists, each list takes the form of
	###                  [start_pos(int), end_pos(int), effect_size(float)]
	###        n_gen: Number of generations that is going to be simulated, only used when norm_or_not=T (int)
	###        mut_rate: Mutation rate, only used when norm_or_not=T (float)
	### Output: A normalized directory that stores the genetic elements' effect sizes. Same as input dict_c_g, only changed the value of the last element of each value
	avg_muts = statistics.mean(seeds_trait_calc(wk_dir, dict_c_g))
	total_sum = avg_muts
	for i in dict_c_g:
		total_sum = total_sum + (n_gen * mut_rate) * (dict_c_g[i][1] - dict_c_g[i][0]) * dict_c_g[i][2]
	k = 1 / total_sum
	for i in dict_c_g:
		dict_c_g[i][2] = k * dict_c_g[i][2]
	return(dict_c_g)


def generate_effsize_csv(trait_n, causal_sizes, es_lows, es_highs, gff_, wk_dir, n_gen, mut_rate, norm_or_not):
	## A function to generate a .csv file in the working directory that shows the full genetic element information for all traits
	## for the specified number of traits and their range. Generate a seeds' trait value at the same time
	### Input: trait_n: Number of traits that is going to be generated (has to be at least 1, int)
	###        causal_sizes: A list of the number of genetic elements that is going to be generated (list, length=trait_n)
	###        es_lows: Lower bound of the effect size that is going to be sampled (list, length=trait_n)
	###		   es_highs: Higher bound of the effect size that is going to be sampled (list, length=trait_n)
	###        gff_: Full path to the gff-like file, that needs to take the form of a tab-delimed file
	###        wk_dir: Working directory
	###        norm_or_not: Boolean variable, specifying whether the generated effect sizes will be normalized
	###        n_gen: Number of generations that is going to be simulated, only used when norm_or_not=T (int)
	###        mut_rate: Mutation rate, only used when norm_or_not=T (float)
	### Output: no return value
	traits_dict = []
	seeds_trait_vals = []
	for trait_id in range(sum(trait_n)):
		print(trait_id)
		curret_tdict, seed_vals = generate_eff_vals(gff_, causal_sizes[trait_id], es_lows[trait_id], es_highs[trait_id], wk_dir, n_gen, mut_rate, norm_or_not)
		traits_dict.append(curret_tdict)
		seeds_trait_vals.append(seed_vals)


	write_seeds_trait(wk_dir, seeds_trait_vals, trait_n)
	write_eff_size_csv(trait_n, traits_dict, wk_dir)


def write_eff_size_csv(trait_n, traits_dict, wk_dir):
	all_dict = {}
	start_pos_dict = {}

	for trait_id in range(sum(trait_n)):
		t_dict = traits_dict[trait_id]
		for gene in t_dict:
			if gene in all_dict:
				while (len(all_dict[gene]) < 2 + trait_id):
					all_dict[gene].append(0)
				all_dict[gene].append(t_dict[gene][2])
			else:
				all_dict[gene] = t_dict[gene][:2]
				i = 0
				while (i < trait_id):
					all_dict[gene].append(0)
					i = i + 1
				all_dict[gene].append(t_dict[gene][2])
				start_pos_dict[all_dict[gene][0]] = gene
	for gene in all_dict:
		while len(all_dict[gene]) < 2 + sum(trait_n):
			all_dict[gene].append(0)

	myKeys = list(start_pos_dict.keys())
	myKeys.sort()
	sorted_dict = {i: start_pos_dict[i] for i in myKeys}
	sorted_all_dict = {start_pos_dict[i]: all_dict[start_pos_dict[i]] for i in sorted_dict}

	with open(os.path.join(wk_dir, "causal_gene_info.csv"), "w") as csv:
		header_csv = "gene_name,start,end,"
		for i in range(trait_n[0]):
			header_csv = header_csv + "eff_size_transmissibility" + str(i + 1) + ","
		for i in range(trait_n[1]):
			header_csv = header_csv + "eff_size_dr" + str(i + 1) + ","
		csv.write(header_csv[:-1] + "\n")
		for i in sorted_all_dict:
			csv.write(i + "," + ",".join([str(j) for j in sorted_all_dict[i]]) + "\n")


def write_seeds_trait(wk_dir, seeds_trait_vals, traits_num):
	## A function to write trait values(trait value: sum of all mutation's effect sizes) of all seeds into a csv file
	### Input: wk_dir: Working directory
	###		   seeds_trait_vals: A list (length=number of traits) where each element is a list (length=number or seeds), storing the trait value of each seeds
	### Output: no return values
	with open(os.path.join(wk_dir, "seeds_trait_values.csv"), "w") as csv_file:
		header_csv = "seed_id,"
		for i in range(traits_num[0]):
			header_csv = header_csv + "transmissibility_" + str(i + 1) + ","
		for i in range(traits_num[1]):
			header_csv = header_csv + "drugresist_" + str(i + 1) + ","
		csv_file.write(header_csv[:-1] + "\n")
		for i in range(len(seeds_trait_vals[0])):
			csv_file.write(str(i) + "," + ",".join([str(seeds_trait_vals[j][i]) for j in range(len(seeds_trait_vals))]) + "\n")


def read_effvals(wk_dir, effsize_path, traits_num):
	## A function to read a user-specified csv file of effect size, return the seeds' trait values accordingly
	### Input: wk_dir: Working directory
	###        effsize_path: Full path to the effect size file (.csv)
	### Needs to first check the format of the file
	### Output: seeds_trait_vals: A list (length=number of traits) where each element is a list (length=number or seeds), storing the trait value of each seeds
	############################## UNFINISHED ####################################
	if os.path.exists(effsize_path):
		### Check if the file format is right
		### If effsize_path for mat correct: do
		csv_df = pd.read_csv(effsize_path)
		traits_num_provided = len(csv_df.columns) - 3
		if sum(traits_num) != traits_num_provided:
			print("Format error, need to have at sum of traits number being the column of the effect size file provided.")
		else:
			gene_names = csv_df["gene_name"].tolist()
			start_pos = csv_df["start"].tolist()
			end_pos = csv_df["end"].tolist()
			traits = []
			traits_dict = []
			if traits_num[0] > 0:
				for i in range(traits_num[0]):
					traits.append(csv_df.iloc[:, 3 + i].tolist())
			if traits_num[1] > 0:
				for i in range(traits_num[1]):
					traits.append(csv_df.iloc[:, 3 + i + traits_num[0]].tolist())
			seeds_trait_vals = []
			#print(traits)
			for i in range(sum(traits_num)):
				dict_c_g = {}
				for j in range(len(gene_names)):
					dict_c_g[gene_names[j]] = [start_pos[j], end_pos[j], traits[i][j]]
				seeds_trait_vals.append(seeds_trait_calc(wk_dir, dict_c_g))
				traits_dict.append(dict_c_g)
			write_eff_size_csv(traits_num, traits_dict, wk_dir)
			return(seeds_trait_vals)



def effsize_generation_byconfig(all_config):
	## A function to generate effect size file and seeds' trait values based on a provided config file
	## Input: all_config: A dictionary of the configuration (read with read_params())
	## Output: No return value

	genetic_config = all_config["GenomeElement"]
	wk_dir = seeds_config["BasicRunConfiguration"]["cwdir"]
	effsize_method = genetic_config["effect_size"]["method"]

	if effsize_method=="user_input":
		run_effsize_generation(method="user_input", wk_dir=wk_dir, effsize_path=genetic_config["effect_size"]["user_input"]["path_effsize_table"])
	elif effsize_method=="randomly_generate":
		eff_params_config = genetic_config["randomly_generate"]
		run_effsize_generation(method="randomly_generate", wk_dir=wk_dir, trait_n=genetic_config["traits_num"], causal_sizes=eff_params_config["genes_num"], es_lows=eff_params_config["effsize_min"], es_highs=eff_params_config["effsize_max"], gff_in=eff_params_config["gff"], n_gen=all_config["EvolutionModel"]["n_generation"], mut_rate=all_config["EvolutionModel"]["mut_rate"], norm_or_not=eff_params_config["normalize"])
	else:
		print("Incorrect effect size method.")


def run_effsize_generation(method, wk_dir, effsize_path="", gff_in="", trait_n=[0,0], causal_sizes=[], es_lows=[], es_highs=[], norm_or_not=False, n_gen=0, mut_rate=0):
	## A function to run the effect size generation and do error control.
	print("trait_n ", trait_n)
	print("causal_sizes ", causal_sizes)

	run_check = True
	if method=="user_input":
		if effsize_path=="":
			print("Need to specify a path to the effect size csv file (-effsize_path) in user_input mode.")
			run_check = False
		elif len(trait_n)!=2:
			print("Wrong trait number format, need to have exactly two traits number (for transmissibility and drug resistance).")
			run_check = False
		elif sum(trait_n)<1:
			print("Please provide a list of number of trait (-trait_n) that sum up to at least 1.")
			run_check = False
	elif method=="randomly_generate":
		if sum(trait_n)<1:
			print("Please provide a list of number of trait (-trait_n) that sum up to at least 1.")
			run_check = False
		else:
			if len(trait_n)!=2:
				print("Wrong trait number format, need to have exactly two traits number (for transmissibility and drug resistance).")
				run_check = False
			if len(causal_sizes)!=sum(trait_n):
				print("The given length of the number of causal genetic elements (-causal_size_each) doesn't equal to the number of traits (Each trait has one number of causal genetic element)")
				run_check = False
			if len(es_lows)!=sum(trait_n):
				print("The given length of the lower bounds (-es_low) doesn't equal to the number of traits")
				run_check = False
			if len(es_highs)!=sum(trait_n):
				print("The given length of the higher (-es_high) bounds doesn't equal to the number of traits")
				run_check = False
			if norm_or_not:
				if n_gen==0:
					print("Need to specify a number of generation (-sim_generation) that is bigger than 0 in normalization mode")
					run_check = False
				if mut_rate==0:
					print("Need to specify a mutation rate (-mut_rate) that is bigger than 0 in normalization mode")
					run_check = False
			if gff_in=="":
				print("Need to specify a path to the gff file (-gff) in random generation mode.")
				run_check = False
	else:
		run_check = False
		print("Please provide a permitted method (-method): user_input/randomly_generate.")

	if run_check:
		if method=="user_input":
			print(trait_n, causal_sizes, es_lows, es_highs, gff_in, wk_dir, n_gen, mut_rate, norm_or_not)
			write_seeds_trait(wk_dir, read_effvals(wk_dir, effsize_path, trait_n), trait_n)
		elif method=="randomly_generate":
			print(trait_n, causal_sizes, es_lows, es_highs, gff_in, wk_dir, n_gen, mut_rate, norm_or_not)
			generate_effsize_csv(trait_n, causal_sizes, es_lows, es_highs, gff_in, wk_dir, n_gen, mut_rate, norm_or_not)
	else:
		print("Terminated because of incorrect input")









