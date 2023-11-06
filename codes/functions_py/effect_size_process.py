"""
Functions for generating the effect size of selected genes in genomes.

Author: Perry Xu
Date: November 6, 2023
"""
import numpy as np
from random import sample
import statistics
import os


### We already have the right format, just count the muts
def calc_sum_effsize_raw(mss, dict_c_g):
    """
    Returns the average effect size of seeds according to mutations 
    on selected genes of individual seeds.

    :param mss: The data directory for seed vcf access.
    :type mss: str
    :param dict_c_g: The dictionary that stores [starting position, ending position, effect size] (values) of selected genes (keys).
    :type dict_c_g: dict[?, [int, int, float]]
    :return: The average effect size of seeds.
    :rtype: float
    """
    c = 0
    calc_sum = []
    seeds = os.listdir(mss + "originalvcfs/")
    for seed in seeds:
        calc_sum.append(0)
        with open(mss + "originalvcfs/" + seed, "r") as seed_vcf:
            for line in seed_vcf:
                if line.startswith("#"):
                    continue
                else:
                    ll = line.rstrip("\n")
                    l = ll.split("\t")
                    for gene in dict_c_g:
                        ##@@
                        # print(f"gene is of type {type(gene)}")
                        # print(f"dictionary values are {dict_c_g[gene]}")
                        ##@@
                        if int(l[1]) >= dict_c_g[gene][0] and int(l[1]) <= dict_c_g[gene][1]:
                            calc_sum[c] = calc_sum[c] + dict_c_g[gene][2]
                    #counts[c] = counts[c] + 1
            c = c + 1
    return(statistics.mean(calc_sum))



def generate_eff(gff_, causal, es_low, es_high, mss, n_gen, mut_rate):
    """
    Returns a dictionary of genes (keys) and their corresponding [starting position, ending position, effect size] (values).

    :param gff_: The path to the annotation file (a tab-delimited file containing non-overlapping genes).
    :type gff_: str
    :param causal: The number of selected genes.
    :type causal: int
    :param es_low: The minimum effect size allowed.
    :type es_low: float
    :param es_high:The maximum effect size allowed.
    :type es_high: float
    :param mss: The data directory for seed vcf access.
    :type mss: str
    :param n_gen: The number of generation to run for SLiM simulation.
    :type n_gen: int
    :param mut_rate: The mutation rate per generation for SLiM simulation.
    :type mut_rate:float
    :return: The dictionary documenting selected genes (keys) and corresponding [starting, ending positions, effect size] (values).
    :rtype: dict[?, [int, int, float]]
    """
    
    g_len = 0
    with open(gff_, "r") as gff:
        for line in gff:
            if line.startswith("\n"):
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
            if index in genes:
                ll = line.rstrip("\n")
                l = ll.split("\t")
                info = l[8].split(";")
                #names.append(info[2].split("=")[1])
                #coe.append(np.random.uniform(float(es_low), float(es_high), 1)[0])
                causal_length.append(int(l[4])-int(l[3]))
                #starts.append(l[3])
                #ends.append(l[4])
                dict_causal_genes[info[2].split("=")[1]] = [int(l[3]), int(l[4]), np.random.uniform(float(es_low), float(es_high), 1)[0]]
            index = index + 1
        dict_causal_genes = normalization_by_mutscounts(mss, dict_causal_genes, n_gen, mut_rate)
    return(dict_causal_genes)

def normalization_by_mutscounts(mss, dict_c_g, n_gen, mut_rate):
    """
    Returns a dictionary of selected genes (keys) and their corresponding [starting position, ending position, normalized effect size] (values).

    :param mss: The data directory for seed vcf access.
    :type mss: str
    :param dict_c_g: The dictionary that stores starting & ending positions (values) of selected genes (keys).
    :type dict_c_g: dict[?, [int, float, float]]
    :param n_gen: The number of generation to run for SLiM simulation.
    :type n_gen: int
    :param mut_rate: The mutation rate per generation for SLiM simulation.
    :type mut_rate:float
    :return: The dictionary documenting selected genes (keys) and corresponding [starting, ending positions, normalized effect size] (values)
    :rtype: dict[?, [int, int, float]]
    """
    avg_muts = calc_sum_effsize_raw(mss, dict_c_g)
    total_sum = avg_muts
    for i in dict_c_g:
        total_sum = total_sum + (n_gen * mut_rate) * (dict_c_g[i][1] - dict_c_g[i][0]) * dict_c_g[i][2]
    k = 1 / total_sum
    for i in dict_c_g:
        dict_c_g[i][2] = k * dict_c_g[i][2]
    return(dict_c_g)



def generate_csv(t1_causal, t2_causal, t1_es_low, t2_es_low, t1_es_high, t2_es_high, gff_, mss, n_gen, mut_rate):
    """
    Create a csv file storing selected genes' information with columns: gene name, starting position, ending position, effect size of trait 1, effect size of trait 2. For example, trait 1 can be related to transmissibility, while trait 2 is drug resistance.

    :param t1_causal: The number of causal genes related to trait 1
    :type t1_causal: int
    :param t2_causal: The number of causal genes related to trait 2
    :type t2_causal: int
    :param t1_es_low: The minimum effect size of trait 1 allowed.
    :type t1_es_low: float
    :param t2_es_low: The minimum effect size of trait 2 allowed.
    :type t2_es_low: float
    :param t1_es_high: The maximum effect size of trait 1 allowed.
    :type t1_es_high: float
    :param t2_es_high: The maximum effect size of trait 2 allowed.
    :type t2_es_high: float
    :param gff_: The path to the annotation file (a tab-delimited file containing non-overlapping genes).
    :type gff_: str
    :param mss: The data directory for seed vcf access.
    :type mss: str
    :param n_gen: The number of generation to run for SLiM simulation.
    :type n_gen: int
    :param mut_rate: The mutation rate per generation for SLiM simulation.
    :type mut_rate:float
    """
    t1_dict = generate_eff(gff_, t1_causal, t1_es_low, t1_es_high, mss, n_gen, mut_rate)
    t2_dict = generate_eff(gff_, t2_causal, t2_es_low, t2_es_high, mss, n_gen, mut_rate)

    all_dict = {}
    start_pos_dict = {}
    overlap = set(t1_dict.keys()).intersection(set(t2_dict.keys()))
    for gene in t1_dict:
        if gene in overlap:
            all_dict[gene] = t1_dict[gene]
            all_dict[gene].append(t2_dict[gene][2])
            start_pos_dict[all_dict[gene][0]] = gene
        else:
            all_dict[gene] = t1_dict[gene]
            all_dict[gene].append(0)
            start_pos_dict[all_dict[gene][0]] = gene
    for gene in t2_dict:
        if gene in overlap:
            continue
        else:
            all_dict[gene] = t2_dict[gene][:2]
            all_dict[gene].append(0)
            all_dict[gene].append(t2_dict[gene][2])
            start_pos_dict[all_dict[gene][0]] = gene
    myKeys = list(start_pos_dict.keys())
    myKeys.sort()
    sorted_dict = {i: start_pos_dict[i] for i in myKeys}
    sorted_all_dict = {start_pos_dict[i]: all_dict[start_pos_dict[i]] for i in sorted_dict}

    with open("causal_gene_info.csv", "w") as csv:
        csv.write("gene_name,start,end,eff_size_t1,eff_size_t2\n")
        for i in sorted_all_dict:
            csv.write(i + "," + str(sorted_all_dict[i][0]) + "," + str(sorted_all_dict[i][1]) + "," + str(sorted_all_dict[i][2]) + "," + str(sorted_all_dict[i][3]) + "\n")