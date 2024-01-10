import tskit
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import pyslim
import argparse
import os


## Read tree and write nwk file
def read_tseq(wk_dir_):
    ts = tskit.load(os.path.join(wk_dir_, "sampled_genomes.trees"))
    n_gens = ts.metadata["SLiM"]["tick"]
    sample_size = range(ts.tables.individuals.num_rows)
    sampled_tree = ts.simplify(samples = [2 * i for i in sample_size])
    return(ts, sampled_tree, sample_size, n_gens)

## Find the labels for every tip, labeled as ${tick}.${host_id}
def find_label(tseq_smp, sim_gen, sample_size):
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

## Store the nwk format of the tree for each root to the output directory (nwk named by the treesequence id, will have to be changed later)
def nwk_output(tseq_smp, real_name, wk_dir_):
    roots_all = tseq_smp.first().roots
    for root in roots_all:
        with open(os.path.join(wk_dir_, "transmission_tree/", str(root) + ".nwk"), "w") as nwk:
            nwk.write(tseq_smp.first().as_newick(root = root, node_labels = real_name))

## Calculate trait value for all the tips and nodes
def trait_calc_tseq(wk_dir_, tseq_smp):
    eff_size = pd.read_csv(os.path.join(wk_dir_, "causal_gene_info.csv"))
    num_trait = eff_size.shape[1] - 3
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
        pos_values.append(tseq_smp.site(mut.site).position)
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

## Create a dataframe that stores all the coloring information
def metadta_generate(sample_size, trvs_order, sampled_ts, sim_gen, traits_num_values, transmissibility_color):
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
        color_by_t1 = str(transmissibility_color[u])
        a_big_df[u] = [node_id, name, node_time, subpop_id, parent_id, color_by_t1]
        for i in range(traits_num):
            a_big_df[u].append(str(traits_num_values[i][u]))
    return(a_big_df)

def write_metadata(mtdata, wk_dir_):
    with open(os.path.join(wk_dir_, "transmission_tree_metadata.csv"), "w") as csv:
        header = "node_id,name,node_time,subpop_id,parent_id,color_by_transmissibility,transmissibility"
        dr_num = len(mtdata[0])-7
        for i in range(dr_num):
            header = header + "," + "drug_resistance_" + str(i + 1)
        csv.write(header + "\n")
        for i in mtdata:
            csv.write(",".join(mtdata[i]) + "\n")

def output_tseq_vcf(wk_dir_, real_label, sampled_ts):
    f = open(os.path.join(wk_dir_, "sampled_pathogen_sequences.vcf"), "w")
    nu_ts = pyslim.convert_alleles(sampled_ts)
    nu_ts.write_vcf(f, individual_names=real_label.values())

def main():
    parser = argparse.ArgumentParser(description='Processing the treesequence file produced by SLiM.')
    parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)
    parser.add_argument('-gen_model', action='store',dest='gen_model', default=False, type = bool, help="If true, then calculate trait values")

    args = parser.parse_args()
    wk_dir_ = args.wk_dir
    gen_model_ = args.gen_model
    print(gen_model_)

    full_ts, sampled_ts, sample_size, sim_gen = read_tseq(wk_dir_)
    real_label = find_label(sampled_ts, sim_gen, sample_size)
    nwk_output(sampled_ts, real_label, wk_dir_)
    if gen_model_==True:
        traits_num_values, trvs_order = trait_calc_tseq(wk_dir_, sampled_ts)
        transmissibility_color = color_by_trait_normalized(traits_num_values[0], trvs_order)
        mtdata = metadta_generate(sample_size, trvs_order, sampled_ts, sim_gen, traits_num_values, transmissibility_color)
        write_metadata(mtdata, wk_dir_)
    output_tseq_vcf(wk_dir_, real_label, sampled_ts)


if __name__ == "__main__":
    main()







