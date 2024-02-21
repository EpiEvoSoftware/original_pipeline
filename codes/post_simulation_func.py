import os
import tskit
import pyslim
import shutil
import subprocess
import inspect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm


def read_tseq(each_wk_dir_):
	ts = tskit.load(os.path.join(each_wk_dir_, "sampled_genomes.trees"))
	n_gens = ts.metadata["SLiM"]["tick"]
	sample_size = range(ts.tables.individuals.num_rows)
	sampled_tree = ts.simplify(samples = [2 * i for i in sample_size])
	return(ts, sampled_tree, sample_size, n_gens)


def find_label(tseq_smp, sim_gen, sample_size):
	## Find the labels for every tip, labeled as ${tick}.${host_id}
	all_tables = tseq_smp.tables
	leaf_time = sim_gen - all_tables.nodes.time[sample_size].astype(int)
	leaf_id = all_tables.nodes.individual[sample_size]
	leaf_label = []
	table_ind = all_tables.individuals
	real_name = {}
	for l_id in sample_size:
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
			if line.startswith("seed"):
				continue
			else:
				ll = line.rstrip("\n")
				l = ll.split(",")
				match_dict[int(l[1])] = int(l[0])
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	else:
		shutil.rmtree(output_path)           # Removes all the subdirectories!
		os.makedirs(output_path)
	for root in roots_all:
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

def color_by_seed(tseq_smp, trvs_order, seed_host_match_path):
	roots_all = tseq_smp.first().roots
	table_ind = tseq_smp.tables.individuals
	match_dict = {}
	node_size = tseq_smp.tables.nodes.num_rows
	trait_val_now = {j:0 for j in range(node_size)}
	tree_first = tseq_smp.first()
	
	with open(seed_host_match_path, "r") as in_csv:
		for line in in_csv:
			if line.startswith("seed"):
				continue
			else:
				ll = line.rstrip("\n")
				l = ll.split(",")
				match_dict[int(l[1])] = int(l[0])
	cmap = cm.get_cmap('viridis')
	values = np.linspace(0, 1, len(match_dict))
	colors = cmap(values)
	hex_codes = [mcolors.to_hex(color) for color in colors]

	for root in roots_all:
		seed_id = match_dict[table_ind[root].metadata["subpopulation"]]
		trait_val_now[root] = hex_codes[seed_id]
	for u in trvs_order:
		if u not in roots_all:
			trait_val_now[u] = trait_val_now[tree_first.parent(u)]
	return(trait_val_now)


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
	vcf_path = os.path.join(wk_dir_, "sampled_pathogen_sequences.vcf.tmp")
	f = open(vcf_path, "w")
	nu_ts = pyslim.convert_alleles(sampled_ts)
	nu_ts.write_vcf(f, individual_names=real_label.values())
	f.close()
	with open(vcf_path, "r") as in_vcf:
		with open(os.path.join(wk_dir_, "sampled_pathogen_sequences.vcf"), "w") as outvcf:
			for line in in_vcf:
				if line.startswith("#"):
					outvcf.write(line)
				else:
					ll = line.split("\t")
					new_line = ll[0] + "\t" + str(int(ll[1]) + 1) + "\t" + "\t".join(ll[2:])
					outvcf.write(new_line)
	os.remove(vcf_path)




def run_per_data_processing(wk_dir_, gen_model, runid, n_trait, seed_host_match_path, color_trait=1):
    ## wk_dir: working directory (all)
    ## gen_model: whether to calculate trait values
    ## color_trait: which trait to color the tree
    ## runid
    each_wk_dir = os.path.join(wk_dir_, str(runid))
    full_ts, sampled_ts, sample_size, sim_gen = read_tseq(each_wk_dir)
    real_label = find_label(sampled_ts, sim_gen, sample_size)
    nwk_output(sampled_ts, real_label, each_wk_dir, seed_host_match_path)
    if color_trait==0:
        gen_model== False
    if gen_model==True:
        traits_num_values, trvs_order = trait_calc_tseq(wk_dir_, sampled_ts, n_trait)
        if color_trait>0:
            trait_color = color_by_trait_normalized(traits_num_values[color_trait - 1], trvs_order)
        else:
            trait_color = color_by_seed(sampled_ts, trvs_order, seed_host_match_path)
        mtdata = metadta_generate(sample_size, trvs_order, sampled_ts, sim_gen, traits_num_values, trait_color)
        write_metadata(mtdata, each_wk_dir, n_trait, color_trait)
    output_tseq_vcf(each_wk_dir, real_label, sampled_ts)



############################## PLOTTING ##################################

def plot_per_transmission_tree(each_wk_dir_, seed_size, slim_config_path, n_traits, seed_phylo_path):
	rscript_path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "plot_tree.R")
	subprocess.run(["Rscript", rscript_path, each_wk_dir_, str(seed_size), slim_config_path, str(n_traits[0]), str(n_traits[1]), seed_phylo_path])
	return(0)


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


def plot_all_strain_trajectory(wk_dir_, seed_size, host_size, n_generation, run_success):

	if len(run_success)>0:
		each_wk_dir_ = os.path.join(wk_dir_, str(run_success[0]))
		strain_df = pd.read_csv(os.path.join(each_wk_dir_, "strain_trajectory.csv.gz"), header=None, names=[str(i) for i in range(seed_size)])
		strain_df = pd.concat([pd.DataFrame({str(i): [1] for i in range(seed_size)}), strain_df]).reset_index(drop=True)
		strain_df_normalized = strain_df.div(strain_df.sum(axis=1), axis=0)

		ax = strain_df_normalized.plot(kind='line', figsize=(10, 6), cmap='viridis', alpha=0.4)
		eff_size_sum = strain_df_normalized

		for runid in run_success[1:]:
			each_wk_dir_ = os.path.join(wk_dir_, str(runid))
			strain_df = pd.read_csv(os.path.join(each_wk_dir_, "strain_trajectory.csv.gz"), header=None, names=[str(i) for i in range(seed_size)])
			strain_df = pd.concat([pd.DataFrame({str(i): [1] for i in range(seed_size)}), strain_df]).reset_index(drop=True)
			strain_df_normalized = strain_df.div(strain_df.sum(axis=1), axis=0)
			ax = strain_df_normalized.plot(ax = ax, kind='line', cmap='viridis', legend=None, alpha=0.4)
			eff_size_sum = eff_size_sum.add(strain_df_normalized, fill_value=0)

		eff_size_avg = eff_size_sum.div(len(run_success))
		ax = eff_size_avg.plot(ax = ax, kind='line', cmap='viridis', legend=None, linewidth=3)

		plt.xlabel('Generations')
		plt.ylabel('Proportion of strain')
		plt.title('Change of the Proportion of Different strains Through Time')
		plt.xlim(0, n_generation)


		plt.tight_layout()

		plt.savefig(os.path.join(wk_dir_, "all_strains_trajectory.png"))
		plt.close()

		
