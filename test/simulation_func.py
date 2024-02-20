import os
import shutil
import inspect
import subprocess
#from multiprocessing import Pool

import tskit
import pyslim
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from base_func import *


def writebinary(v):
	if v:
		return("T")
	else:
		return("")

def append_files(file1_path, file2_path):
	## Append file1 to file2
    with open(file1_path, 'r') as file1:
        with open(file2_path, 'a') as file2:
            shutil.copyfileobj(file1, file2)


def create_slimconfig(all_config):
	### A function to create a SLiM-readable config file that includes the SLiM-needed parameters from the big config file
	## Input: all_config: dictionary of the big config file, read by read_config()
	## Output: A one-layer dictionary for all the parameters in SLiM
	slim_pars = {}
	with open(os.path.join(all_config["BasicRunConfiguration"]["cwdir"], "slim.params"), "w") as out_config:
		slim_pars["cwdir"] = all_config["BasicRunConfiguration"]["cwdir"]
		out_config.write("cwdir:" + slim_pars["cwdir"] + "\n")
		slim_pars["n_replicates"] = all_config["BasicRunConfiguration"]["n_replicates"]
		out_config.write("n_replicates:" + str(slim_pars["n_replicates"]) + "\n")

		slim_pars["n_generation"] = all_config["EvolutionModel"]["n_generation"]
		out_config.write("n_generation:" + str(slim_pars["n_generation"]) + "\n")
		slim_pars["mut_rate"] = all_config["EvolutionModel"]["mut_rate"]
		out_config.write("mut_rate:" + str(slim_pars["mut_rate"]) + "\n")
		slim_pars["trans_type"] = all_config["EvolutionModel"]["trans_type"]
		out_config.write("trans_type:" + slim_pars["trans_type"] + "\n")
		slim_pars["dr_type"] = all_config["EvolutionModel"]["dr_type"]
		out_config.write("dr_type:" + slim_pars["dr_type"] + "\n")
		slim_pars["within_host_reproduction"] = all_config["EvolutionModel"]["within_host_reproduction"]
		out_config.write("within_host_reproduction:" + writebinary(slim_pars["within_host_reproduction"]) + "\n")
		slim_pars["cap_withinhost"] = all_config["EvolutionModel"]["cap_withinhost"]
		out_config.write("cap_withinhost:" + str(slim_pars["cap_withinhost"]) + "\n")

		slim_pars["seed_size"] = all_config["SeedsConfiguration"]["seed_size"]
		out_config.write("seed_size:" + str(slim_pars["seed_size"]) + "\n")
		slim_pars["ref_path"] = all_config["GenomeElement"]["ref_path"]
		out_config.write("ref_path:" + slim_pars["ref_path"] + "\n")
		slim_pars["use_genetic_model"] = all_config["GenomeElement"]["use_genetic_model"]
		out_config.write("use_genetic_model:" + writebinary(slim_pars["use_genetic_model"]) + "\n")
		slim_pars["use_network_model"] = all_config["NetworkModelParameters"]["use_network_model"]
		out_config.write("use_network_model:" + writebinary(slim_pars["use_network_model"]) + "\n")

		slim_pars["epi_model"] = all_config["EpidemiologyModel"]["model"]
		out_config.write("epi_model:" + slim_pars["epi_model"] + "\n")
		slim_pars["n_epoch"] = all_config["EpidemiologyModel"]["epoch_changing"]["n_epoch"]
		out_config.write("n_epoch:" + str(slim_pars["n_epoch"]) + "\n")
		if slim_pars["n_epoch"]>1:
			slim_pars["epoch_changing_generation"] = all_config["EpidemiologyModel"]["epoch_changing"]["epoch_changing_generation"]
			out_config.write("epoch_changing_generation:" + ",".join([str(x) for x in slim_pars["epoch_changing_generation"]]) + "\n")
		slim_pars["transmissibility_effsize"] = all_config["EpidemiologyModel"]["genetic_architecture"]["transmissibility"]
		out_config.write("transmissibility_effsize:" + ",".join([str(x) for x in slim_pars["transmissibility_effsize"]]) + "\n")
		slim_pars["cap_transmissibility"] = all_config["EpidemiologyModel"]["genetic_architecture"]["cap_transmissibility"]
		out_config.write("cap_transmissibility:" + ",".join([str(x) for x in slim_pars["cap_transmissibility"]]) + "\n")
		slim_pars["drugresistance_effsize"] = all_config["EpidemiologyModel"]["genetic_architecture"]["drug_resistance"]
		out_config.write("drugresistance_effsize:" + ",".join([str(x) for x in slim_pars["drugresistance_effsize"]]) + "\n")
		slim_pars["cap_drugresist"] = all_config["EpidemiologyModel"]["genetic_architecture"]["cap_drugresist"]
		out_config.write("cap_drugresist:" + ",".join([str(x) for x in slim_pars["cap_drugresist"]]) + "\n")
		slim_pars["S_IE_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["S_IE_rate"]
		out_config.write("S_IE_rate:" + ",".join([str(x) for x in slim_pars["S_IE_rate"]]) + "\n")
		slim_pars["I_R_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["I_R_rate"]
		out_config.write("I_R_rate:" + ",".join([str(x) for x in slim_pars["I_R_rate"]]) + "\n")
		slim_pars["R_S_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["R_S_rate"]
		out_config.write("R_S_rate:" + ",".join([str(x) for x in slim_pars["R_S_rate"]]) + "\n")
		slim_pars["latency_prob"] = all_config["EpidemiologyModel"]["transiton_rate"]["latency_prob"]
		out_config.write("latency_prob:" + ",".join([str(x) for x in slim_pars["latency_prob"]]) + "\n")
		slim_pars["E_I_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["E_I_rate"]
		out_config.write("E_I_rate:" + ",".join([str(x) for x in slim_pars["E_I_rate"]]) + "\n")
		slim_pars["I_E_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["I_E_rate"]
		out_config.write("I_E_rate:" + ",".join([str(x) for x in slim_pars["I_E_rate"]]) + "\n")
		slim_pars["E_R_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["E_R_rate"]
		out_config.write("E_R_rate:" + ",".join([str(x) for x in slim_pars["E_R_rate"]]) + "\n")
		slim_pars["sample_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["sample_rate"]
		out_config.write("sample_rate:" + ",".join([str(x) for x in slim_pars["sample_rate"]]) + "\n")
		slim_pars["recovery_prob_after_sampling"] = all_config["EpidemiologyModel"]["transiton_rate"]["recovery_prob_after_sampling"]
		out_config.write("recovery_prob_after_sampling:" + ",".join([str(x) for x in slim_pars["recovery_prob_after_sampling"]]) + "\n")

		slim_pars["n_massive_sample"] = all_config["EpidemiologyModel"]["massive_sampling"]["event_num"]
		out_config.write("n_massive_sample:" + str(slim_pars["n_massive_sample"]) + "\n")
		if slim_pars["n_massive_sample"]>0:
			slim_pars["massive_sample_generation"] = all_config["EpidemiologyModel"]["massive_sampling"]["generation"]
			out_config.write("massive_sample_generation:" + ",".join([str(x) for x in slim_pars["massive_sample_generation"]]) + "\n")
			slim_pars["massive_sample_prob"] = all_config["EpidemiologyModel"]["massive_sampling"]["sampling_prob"]
			out_config.write("massive_sample_prob:" + ",".join([str(x) for x in slim_pars["massive_sample_prob"]]) + "\n")
			slim_pars["massive_sample_recover_prob"] = all_config["EpidemiologyModel"]["massive_sampling"]["recovery_prob_after_sampling"]
			out_config.write("massive_sample_recover_prob:" + ",".join([str(x) for x in slim_pars["massive_sample_recover_prob"]]) + "\n")

		slim_pars["super_infection"] = all_config["EpidemiologyModel"]["super_infection"]
		out_config.write("super_infection:" + writebinary(slim_pars["n_massive_sample"]) + "\n")

		slim_pars["cap_withinhost"] = all_config["EvolutionModel"]["cap_withinhost"]
		out_config.write("cap_withinhost:" + str(slim_pars["cap_withinhost"]) + "\n")
		slim_pars["within_host_reproduction"] = all_config["EvolutionModel"]["within_host_reproduction"]
		out_config.write("within_host_reproduction:" + writebinary(slim_pars["within_host_reproduction"]) + "\n")

		if slim_pars["use_genetic_model"]:
			out_config.write("causal_gene_path:" + os.path.join(slim_pars["cwdir"], "causal_gene_info.csv") + "\n")
		else:
			out_config.write("causal_gene_path:" + "\n")
		slim_pars["seed_host_matching_path"] = os.path.join(slim_pars["cwdir"], "seed_host_match.csv")
		out_config.write("seed_host_matching_path:" + slim_pars["seed_host_matching_path"] + "\n")

		if slim_pars["use_network_model"]:
			slim_pars["host_size"] = all_config["NetworkModelParameters"]["host_size"]
			out_config.write("host_size:" + str(slim_pars["host_size"]) + "\n")
			out_config.write("contact_network_path:" + os.path.join(slim_pars["cwdir"], "contact_network.adjlist") + "\n")

		if slim_pars["within_host_reproduction"]:
			slim_pars["within_host_reproduction_rate"] = all_config["EvolutionModel"]["within_host_reproduction_rate"]
			out_config.write("within_host_reproduction_rate:" + str(slim_pars["within_host_reproduction_rate"]) + "\n")
		else:
			out_config.write("host_size:" + str(slim_pars["host_size"]) + "\n")

		if all_config["Postprocessing_options"]["do_postprocess"]:
			post_processing_config = all_config["Postprocessing_options"]
			post_processing_config["n_trait"] = all_config["GenomeElement"]["traits_num"]
		else:
			post_processing_config = {}
		

	return(slim_pars, post_processing_config)


def check_all_params(slim_pars):
	### A function that takes in all parameters needed for the simulation (A dictionary) and check whether it's legit

	## Return T/F
	return(True)


def check_prerequisites(wk_dir, use_genetic_model=True, use_network_model=True):
	### A function that takes in the parameters and check whether the required prerequisites files are already in the working directory
	pres_met = True
	if os.path.exists(os.path.join(wk_dir, "originalvcfs"))==False:
		print("No seed file is provided in the working directory, please run seed_generator module before running the simulation.")
		pres_met = False
	if use_network_model:
		if os.path.exists(os.path.join(wk_dir, "contact_network.adjlist"))==False:
			print("No network file is provided in the working directory under network model, please run network_generator module before running the simulation or use a no-network model.")
			pres_met = False
		if os.path.exists(os.path.join(wk_dir, "seed_host_match.csv"))==False:
			print("No seed-host matching file file is provided in the working directory under network model, please run seed_host_matcher module before running the simulation.")
			pres_met = False
	if use_genetic_model:
		if os.path.exists(os.path.join(wk_dir, "causal_gene_info.csv"))==False:
			print("No causal gene effect size file is provided in the working directory under network model, please run genetic_effect_generator module before running the simulation or use a no-genetic-effect model.")
			pres_met = False
	return(pres_met)



def create_slimscript(slim_pars):
	### A function that create a SLiM script in the working directory according to the config
	### The script should take in SLiM config file and the current output directory (related to n_replicates) as parameters
	### No return value
	
	code_path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "slim_scripts")
	mainslim_path = os.path.join(slim_pars["cwdir"], "simulation.slim")

	if os.path.exists(mainslim_path):
		os.remove(mainslim_path)

	## Create a slim file in working directory
	f = open(mainslim_path, "w")
	f.close()


	## Get trait calculation functions ready
	append_files(os.path.join(code_path, "trait_calc_function.slim"), mainslim_path)

	## Initialization
	append_files(os.path.join(code_path, "initialization_pt1.slim"), mainslim_path)
	append_files(os.path.join(code_path, "read_config.slim"), mainslim_path)
	append_files(os.path.join(code_path, "initialization_pt2.slim"), mainslim_path)
	if slim_pars["use_genetic_model"]:
		append_files(os.path.join(code_path, "genomic_element_init_effsize.slim"), mainslim_path)
	else:
		append_files(os.path.join(code_path, "genomic_element_init.slim"), mainslim_path)
	append_files(os.path.join(code_path, "initialization_pt3.slim"), mainslim_path)

	## Mutation block (for m1)
	if slim_pars["use_genetic_model"]:
		append_files(os.path.join(code_path, "mutation_effsize.slim"), mainslim_path)

	## Block control 1first()
	append_files(os.path.join(code_path, "block_control.slim"), mainslim_path)

	## Seed's read in and network read in
	if slim_pars["use_network_model"]:
		append_files(os.path.join(code_path, "seeds_read_in_network.slim"), mainslim_path)
		append_files(os.path.join(code_path, "contact_network_read_in.slim"), mainslim_path)

	## Epoch changing
	if slim_pars["n_epoch"]>1:
		append_files(os.path.join(code_path, "change_epoch.slim"), mainslim_path)

	## Self reproduction
	append_files(os.path.join(code_path, "self_reproduce.slim"), mainslim_path)

	## Transmission reproduction
	if slim_pars["use_genetic_model"] == False:
		append_files(os.path.join(code_path, "transmission_nogenetic.slim"), mainslim_path)
	else:
		if slim_pars["trans_type"]=="additive":
			append_files(os.path.join(code_path, "transmission_additive.slim"), mainslim_path)
		elif slim_pars["trans_type"]=="bialleleic":
			append_files(os.path.join(code_path, "transmission_bialleleic.slim"), mainslim_path)
		if any(idx == 0 for idx in slim_pars["transmissibility_effsize"]):
			append_files(os.path.join(code_path, "transmission_nogenetic.slim"), mainslim_path)

	## Within-host reproduction
	if slim_pars["within_host_reproduction"]:
		append_files(os.path.join(code_path, "within_host_reproduce.slim"), mainslim_path)

	## Kill old pathogens
	append_files(os.path.join(code_path, "kill_old_pathogens.slim"), mainslim_path)

	## State transition for exposed hosts
	if slim_pars["epi_model"]=="SEIR":
		append_files(os.path.join(code_path, "Exposed_process.slim"), mainslim_path)

	## State transition for infected hosts
	if any(idx != 0 for idx in slim_pars["drugresistance_effsize"]):
		if slim_pars["trans_type"] == "additive":
			append_files(os.path.join(code_path, "Infected_process_additive.slim"), mainslim_path)
		elif slim_pars["trans_type"] == "bialleleic":
			append_files(os.path.join(code_path, "Infected_process_additive.slim"), mainslim_path)
	if any(idx == 0 for idx in slim_pars["drugresistance_effsize"]):
		append_files(os.path.join(code_path, "Infected_process_nogenetic.slim"), mainslim_path)

	## Massive sampling events
	if slim_pars["n_massive_sample"] > 0:
		append_files(os.path.join(code_path, "massive_sampling.slim"), mainslim_path)

	## New infections
	if slim_pars["super_infection"] > 0:
		append_files(os.path.join(code_path, "New_infection_process.slim"), mainslim_path)
	else:
		append_files(os.path.join(code_path, "New_infection_process_superinfection.slim"), mainslim_path)

	## Recovered individuals
	if any(rate != 0 for rate in slim_pars["R_S_rate"]):
		append_files(os.path.join(code_path, "Recovered_process.slim"), mainslim_path)

	## Logging all things
	append_files(os.path.join(code_path, "log.slim"), mainslim_path)

	## Finish simulation
	append_files(os.path.join(code_path, "finish_simulation.slim"), mainslim_path)



	return(0)


def run_per_slim_simulation(slim_config_path, wk_dir, runid):
	### A function that run the SLiM script generated by create_slimscript().
	### It creates subfolders in the working directory and run them (in parallel ideally).
	### And run post data processing for each folder.
	### No return value
	#slim_config_path, wk_dir, runid = tuple_arg
	output_path = os.path.join(wk_dir, str(runid))
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	else:
		shutil.rmtree(output_path)           # Removes all the subdirectories!
		os.makedirs(output_path)

	script_path = os.path.join(wk_dir, "simulation.slim")
	slim_stdout_path = os.path.join(output_path, "slim.stdout")
	with open(slim_stdout_path, 'w') as fd:
		subprocess.run(["slim", "-d", f"config_path=\"{slim_config_path}\"", "-d", f"runid={runid}", script_path], stdout=fd)
	return(0)


def all_slim_simulation_by_config(all_config):
	### A function that run the SLiM script generated by create_slimscript().
	### It creates subfolders in the working directory and run them (in parallel ideally).
	### And run post data processing for each folder.
	### No return value
	slim_pars, dataprocess_pars = create_slimconfig(all_config)
	create_slimscript(slim_pars)
	wk_dir = slim_pars["cwdir"]
	run_all_slim_simulation(slim_config_path = os.path.join(wk_dir, "slim.params"), slim_pars = slim_pars, dataprocess_pars=dataprocess_pars)
	

def run_all_slim_simulation(slim_config_path="", slim_pars={}, dataprocess_pars={}):
	## Not parallel for now (sequentially)
	if slim_config_path=="":
		slim_config_path = os.path.join(slim_pars["cwdir"], "slim.params")

	run_check = True
	if check_all_params(slim_pars)==False:
		print("Checking slim configuration not passed, please check for the error message to adjust for the parameters.")
		run_check = False
	if check_prerequisites(slim_pars["cwdir"], use_genetic_model=slim_pars["use_genetic_model"], use_network_model=slim_pars["use_network_model"])==False:
		print("Prerequisites for your specified slim configuration isn't met, please see the error message and run the pre-simulation steps as suggested.")
		run_check = False

	#lst = [(slim_config_path, slim_pars["cwdir"], runid) for runid in range(1, slim_pars["n_replicates"] + 1)]

	if run_check:
		run_success = []
		for runid in range(1,slim_pars["n_replicates"] + 1):
			run_per_slim_simulation(slim_config_path, slim_pars["cwdir"], runid)
			if os.path.exists(os.path.join(slim_pars["cwdir"], str(runid), "sampled_genomes.trees")):
				if len(dataprocess_pars) > 0:
					each_wkdir = os.path.join(slim_pars["cwdir"], str(runid))
					run_per_data_processing(slim_pars["cwdir"], slim_pars["use_genetic_model"], runid, dataprocess_pars["n_trait"], slim_pars["seed_host_matching_path"], slim_pars["seed_size"], dataprocess_pars["tree_plotting"]["branch_color_trait"])
					#plot_per_transmission_tree(each_wkdir, slim_pars["seed_size"], slim_config_path, dataprocess_pars["n_trait"], os.path.join(slim_pars["cwdir"], "seeds.nwk"))
					plot_strain_distribution_trajectory(each_wkdir, slim_pars["seed_size"], slim_pars["n_generation"])
					if os.path.exists(os.path.join(each_wkdir, "SEIR_trajectory.csv.gz")):
						plot_SEIR_trajectory(each_wkdir, slim_pars["seed_size"], slim_pars["host_size"], slim_pars["n_generation"])
						run_success.append(runid)
			else:
				print(f"There's no sampled genome in replicate {runid}. Either the simulation failed or the sampling rate is too low. Please check your config file.")
		plot_all_SEIR_trajectory(slim_pars["cwdir"], slim_pars["seed_size"], slim_pars["host_size"], slim_pars["n_generation"], run_success)
	return(0)


#################### POST-SIMULATION DATA PROCESSING ##############################

def read_tseq(each_wk_dir_, seed_size, subsample_prob=1):
	ts = tskit.load(os.path.join(each_wk_dir_, "sampled_genomes.trees"))
	n_gens = ts.metadata["SLiM"]["tick"]
	print(ts.first().roots)
	sample_size = [i for i, x in enumerate(np.random.binomial(n=1, p=0.5, size=ts.tables.individuals.num_rows)) if x == 1]
	sampled_tree = ts.simplify(samples = [2 * i for i in sample_size], keep_input_roots=True)
	print(sampled_tree.first().roots)
	return(ts, sampled_tree, sample_size, n_gens)


def find_label(tseq_smp, sim_gen, sample_size):
	## Find the labels for every tip, labeled as ${tick}.${host_id}
	all_tables = tseq_smp.tables
	leaf_time = sim_gen - all_tables.nodes.time[range(len(sample_size))].astype(int)
	leaf_id = all_tables.nodes.individual[range(len(sample_size))]
	leaf_label = []
	table_ind = all_tables.individuals
	real_name = {}
	for l_id in range(len(sample_size)):
		subpop_now = table_ind[l_id].metadata["subpopulation"]
		leaf_label.append(subpop_now)
		real_name[l_id] = str(leaf_time[l_id]) + "." + str(subpop_now)
	return(real_name)


def nwk_output(tseq_smp, real_name, each_wk_dir_, seed_host_match_path):
	##### Don't name with roots, but name with seed id?
	roots_all = tseq_smp.first().roots
	output_path = os.path.join(each_wk_dir_, "transmission_tree")
	table_ind = tseq_smp.tables.individuals
	match_dict = {}
	with open(seed_host_match_path, "r") as in_csv:
		for line in in_csv:
			ll = line.rstrip("\n")
			l = ll.split(",")
			match_dict[int(l[0])] = int(l[1])
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	else:
		shutil.rmtree(output_path)           # Removes all the subdirectories!
		os.makedirs(output_path)
	print(roots_all)
	for root in roots_all:
		#print(table_ind)
		print(match_dict)
		print(root)
		print(table_ind[root].metadata["subpopulation"])
		root_subpop = table_ind[root].metadata["subpopulation"]
		with open(os.path.join(output_path, str(match_dict[root_subpop]) + ".nwk"), "w") as nwk:
			nwk.write(tseq_smp.first().as_newick(root = root, node_labels = real_name) + "\n")


def trait_calc_tseq(wk_dir_, tseq_smp, n_trait):
	eff_size = pd.read_csv(os.path.join(wk_dir_, "causal_gene_info.csv"))
	num_trait = sum(n_trait)
	search_intvls = []
	for i in range(eff_size.shape[0]):
		search_intvls.append(eff_size["start"][i])
		search_intvls.append(eff_size["end"][i])
	## Prepare mutation data for each node
	node_pluses = []
	pos_values = []
	node_ids = []
	node_size = tseq_smp.tables.nodes.num_rows
	muts_size = tseq_smp.tables.mutations.num_rows
	tree_first = tseq_smp.first()
	trvs_order = list(tree_first.nodes(order="preorder"))

	for j in range(muts_size):
		mut = tseq_smp.mutation(j)
		pos_values.append(tseq_smp.site(mut.site).position + 1)
		node_ids.append(mut.node)
		intvs = np.searchsorted(search_intvls, pos_values)
		which_m2 = np.where(intvs % 2 == 1)[0]
	colnames_df = eff_size.columns
	for j in range(num_trait):
		node_pluses.append({i:0 for i in range(node_size)})
		for i in which_m2:
			node_pluses[j][node_ids[i]] += eff_size[colnames_df[j + 3]][intvs[i] // 2]
	real_traits_vals = []
	for i in range(num_trait):
		node_plus = node_pluses[i]
		muts_nodes = {}
		for key, value in node_plus.items():
			if value > 0:
				muts_nodes[key] = value
		trait_val_now = {j:0 for j in range(node_size)}
		trait_val_now[-1]=0
		for u in trvs_order:
			trait_val_now[u] = trait_val_now[tree_first.parent(u)] + node_plus[u]
		trait_val_now.pop(-1)
		real_traits_vals.append(trait_val_now)
	return(real_traits_vals, trvs_order)

def floats_to_colors_via_matplotlib(float_values):
	cmap = mcolors.LinearSegmentedColormap.from_list("", ["blue", "red"])
	colors = [cmap(value) for value in float_values]
	hex_colors = [mcolors.to_hex(color) for color in colors]
	return(hex_colors)


def color_by_trait_normalized(trait_val_now, trvs_order):
	all_traits = np.array(list(trait_val_now.values()))
	normalized_traits = (all_traits-np.min(all_traits))/(np.max(all_traits)-np.min(all_traits))
	color_map_nodes = floats_to_colors_via_matplotlib(normalized_traits)
	color_map_dict = {i:color_map_nodes[i] for i in range(len(trvs_order))}
	return(color_map_dict)


def metadta_generate(sample_size, trvs_order, sampled_ts, sim_gen, traits_num_values, trait_color):
	a_big_df = {}
	sample_size_max = len(sample_size)
	nodes_table = sampled_ts.tables.nodes
	inds_table = sampled_ts.tables.individuals
	tree_first = sampled_ts.first()
	traits_num = len(traits_num_values)
	for u in trvs_order:
		node_id = str(u)
		node_time = str(sim_gen - nodes_table.time[u].astype(int))
		if u < sample_size_max:
			subpop_id = str(inds_table[u].metadata["subpopulation"])
			name = ".".join([node_time, subpop_id])
		else:
			subpop_id = str(-1)
			name = "."
		parent_id = str(tree_first.parent(u))
		color_by_trait = str(trait_color[u])
		a_big_df[u] = [node_id, name, node_time, subpop_id, parent_id, color_by_trait]
		for i in range(traits_num):
			a_big_df[u].append(str(traits_num_values[i][u]))
	return(a_big_df)


def write_metadata(mtdata, each_wk_dir_, n_trait, color_trait):
	with open(os.path.join(each_wk_dir_, "transmission_tree_metadata.csv"), "w") as csv:
		if color_trait <= n_trait[0]:
			color_trait_id = color_trait
		else:
			color_trait_id = color_trait - n_trait[0]
		header = "node_id,name,node_time,subpop_id,parent_id,color_trait_" + str(color_trait_id)
		for i in range(n_trait[0]):
			header = header + "," + "transmissibility_" + str(i + 1)
		for i in range(n_trait[1]):
			header = header + "," + "drug_resistance_" + str(i + 1)
		csv.write(header + "\n")
		for i in mtdata:
			csv.write(",".join(mtdata[i]) + "\n")


def output_tseq_vcf(wk_dir_, real_label, sampled_ts):
	f = open(os.path.join(wk_dir_, "sampled_pathogen_sequences.vcf"), "w")
	nu_ts = pyslim.convert_alleles(sampled_ts)
	nu_ts.write_vcf(f, individual_names=real_label.values())


def run_per_data_processing(wk_dir_, gen_model, runid, n_trait, seed_host_match_path, seed_size, color_trait=1, subsample_prob = 1):
    ## wk_dir: working directory (all)
    ## gen_model: whether to calculate trait values
    ## color_trait: which trait to color the tree
    ## runid
    each_wk_dir = os.path.join(wk_dir_, str(runid))
    full_ts, sampled_ts, sample_size, sim_gen = read_tseq(each_wk_dir, seed_size, subsample_prob)
    real_label = find_label(sampled_ts, sim_gen, sample_size)
    nwk_output(sampled_ts, real_label, each_wk_dir, seed_host_match_path)
    if color_trait==0:
    	gen_model== False
    if gen_model==True:
        traits_num_values, trvs_order = trait_calc_tseq(wk_dir_, sampled_ts, n_trait)
        trait_color = color_by_trait_normalized(traits_num_values[color_trait - 1], trvs_order)
        mtdata = metadta_generate(sample_size, trvs_order, sampled_ts, sim_gen, traits_num_values, trait_color)
        write_metadata(mtdata, each_wk_dir, n_trait, color_trait)
    output_tseq_vcf(each_wk_dir, real_label, sampled_ts)
    #sampled_ts.write_fasta("output.fa")




############################## PLOTTING ##################################

#def plot_per_transmission_tree(each_wk_dir_, seed_size, slim_config_path, n_traits, seed_phylo_path):
#	rscript_path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "plot_tree.r")
#	subprocess.run(["Rscript", rscript_path, each_wk_dir_, str(seed_size), slim_config_path, str(n_traits[0]), str(n_traits[1]), seed_phylo_path])
#	return(0)


def plot_strain_distribution_trajectory(each_wk_dir_, seed_size, n_generation):
	eff_size = pd.read_csv(os.path.join(each_wk_dir_, "strain_trajectory.csv.gz"), header=None, names=range(seed_size), compression = "gzip")
	eff_size = pd.concat([pd.DataFrame({i: [1] for i in range(seed_size)}), eff_size]).reset_index(drop=True)

	eff_size_normalized = eff_size.div(eff_size.sum(axis=1), axis=0)

	ax = eff_size_normalized.plot(kind='area', stacked=True, figsize=(10, 6), cmap='viridis')

	plt.xlabel('Generations')
	plt.ylabel('Proportion of strain')
	plt.title('Change of the Proportion of Different strains Through Time')
	plt.ylim(0, 1)
	plt.xlim(0, n_generation)
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

	plt.tight_layout()
	plt.savefig(os.path.join(each_wk_dir_, "strain_trajectory.png"))


def plot_SEIR_trajectory(each_wk_dir_, seed_size, host_size, n_generation):
	seir = pd.read_csv(os.path.join(each_wk_dir_, "SEIR_trajectory.csv.gz"), header=None, names=["S", "E", "I", "R"])
	seir = pd.concat([pd.DataFrame({"S": [host_size - seed_size], "E": [0], "I": [seed_size], "R": [0]}), seir]).reset_index(drop=True)

	seir.plot(kind='line', figsize=(10, 6), cmap='viridis')

	plt.xlabel('Generations')
	plt.ylabel('number of hosts')
	plt.title('SEIR Trajectory')
	plt.ylim(0, host_size)
	plt.xlim(0, n_generation)

	plt.tight_layout()

	plt.savefig(os.path.join(each_wk_dir_, "SEIR_trajectory.png"))
	plt.close()



def plot_all_SEIR_trajectory(wk_dir_, seed_size, host_size, n_generation, run_success):

	if len(run_success)>0:
		each_wk_dir_ = os.path.join(wk_dir_, str(run_success[0]))
		seir = pd.read_csv(os.path.join(each_wk_dir_, "SEIR_trajectory.csv.gz"), header=None, names=["S", "E", "I", "R"])
		seir = pd.concat([pd.DataFrame({"S": [host_size - seed_size], "E": [0], "I": [seed_size], "R": [0]}), seir]).reset_index(drop=True)
		ax = seir.plot(kind='line', figsize=(10, 6), cmap='viridis', alpha=0.4)
		seir_sum = seir

		for runid in run_success[1:]:
			each_wk_dir_ = os.path.join(wk_dir_, str(runid))
			seir = pd.read_csv(os.path.join(each_wk_dir_, "SEIR_trajectory.csv.gz"), header=None, names=["S", "E", "I", "R"])
			seir = pd.concat([pd.DataFrame({"S": [host_size - seed_size], "E": [0], "I": [seed_size], "R": [0]}), seir]).reset_index(drop=True)
			ax = seir.plot(ax = ax, kind='line', cmap='viridis', legend=None, alpha=0.4)
			seir_sum = seir_sum.add(seir, fill_value=0)

		seir_avg = seir_sum.div(len(run_success))
		ax = seir_avg.plot(ax = ax, kind='line', cmap='viridis', legend=None, linewidth=3)

		plt.xlabel('Generations')
		plt.ylabel('number of hosts')
		plt.title('SEIR Trajectory')
		plt.ylim(0, host_size)
		plt.xlim(0, n_generation)


		plt.tight_layout()

		plt.savefig(os.path.join(wk_dir_, "all_SEIR_trajectory.png"))
		plt.close()










