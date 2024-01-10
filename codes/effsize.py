import numpy as np
from random import sample
import statistics
import os
import argparse

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

### We already have the right format, just count the muts
def calc_sum_effsize_raw(mss, dict_c_g):
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
						if int(l[1]) >= dict_c_g[gene][0] and int(l[1]) <= dict_c_g[gene][1]:
							calc_sum[c] = calc_sum[c] + dict_c_g[gene][2]
			c = c + 1
	return(statistics.mean(calc_sum))



def generate_eff(gff_, causal, es_low, es_high, mss, n_gen, mut_rate, norm_or_not):
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
				causal_length.append(int(l[4])-int(l[3]))
				dict_causal_genes[info[2].split("=")[1]] = [int(l[3]), int(l[4]), np.random.uniform(float(es_low), float(es_high), 1)[0]]
			index = index + 1
		if norm_or_not:
			dict_causal_genes = normalization_by_mutscounts(mss, dict_causal_genes, n_gen, mut_rate)

	return(dict_causal_genes)

def normalization_by_mutscounts(mss, dict_c_g, n_gen, mut_rate):
	avg_muts = calc_sum_effsize_raw(mss, dict_c_g)
	total_sum = avg_muts
	for i in dict_c_g:
		total_sum = total_sum + (n_gen * mut_rate) * (dict_c_g[i][1] - dict_c_g[i][0]) * dict_c_g[i][2]
	k = 1 / total_sum
	for i in dict_c_g:
		dict_c_g[i][2] = k * dict_c_g[i][2]
	return(dict_c_g)


def generate_csv(trait_n, causal_sizes, es_lows, es_highs, gff_, mss, n_gen, mut_rate, norm_or_not):
	traits_dict = []
	for trait_id in range(trait_n):
		traits_dict.append(generate_eff(gff_, causal_sizes[trait_id], es_lows[trait_id], es_highs[trait_id], mss, n_gen, mut_rate, norm_or_not))

	all_dict = {}
	start_pos_dict = {}

	for trait_id in range(trait_n):
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
		while len(all_dict[gene]) < 2 + trait_n:
			all_dict[gene].append(0)

	myKeys = list(start_pos_dict.keys())
	myKeys.sort()
	sorted_dict = {i: start_pos_dict[i] for i in myKeys}
	sorted_all_dict = {start_pos_dict[i]: all_dict[start_pos_dict[i]] for i in sorted_dict}

	with open(mss + "causal_gene_info.csv", "w") as csv:
		header_csv = "gene_name,start,end,"
		for i in range(trait_n):
			header_csv = header_csv + "eff_size_t" + str(i + 1) + ","
		csv.write(header_csv[:-1] + "\n")
		for i in sorted_all_dict:
			csv.write(i + "," + ",".join([str(j) for j in sorted_all_dict[i]]) + "\n") #+ str(sorted_all_dict[i][0]) + "," + str(sorted_all_dict[i][1]) + "," + str(sorted_all_dict[i][2]) + "," + str(sorted_all_dict[i][3]) + "\n")




def main():
	parser = argparse.ArgumentParser(description='Generate the selection coefficient modifying part of the slim script.')
	parser.add_argument('-gff', action='store',dest='gff', required=True)
	parser.add_argument('-trait_num', action='store',dest='trait_num', required=True, type=int, help="Number of traits")
	parser.add_argument('-causal_size_each','--causal_size_each', nargs='+', help='Size of causal genes for each trait', required=True, type=int)
	parser.add_argument('-es_low','--es_low', nargs='+', help='Lower bounds of effect size for each trait', required=True, type=float)
	parser.add_argument('-es_high','--es_high', nargs='+', help='Higher bounds of effect size for each trait', required=True, type=float)
	parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)
	parser.add_argument('-normalize','--normalize', default=False, required=True, type=str2bool, help='Whether to normalize the effect size based on sim_generations and mut_rate')
	parser.add_argument('-sim_generation', action='store',dest='sim_generation', required=False, type=float, default=0)
	parser.add_argument('-mut_rate', action='store',dest='mut_rate', required=False, type=float, default=0)

	args = parser.parse_args()
	gff_in = args.gff
	trait_n = args.trait_num
	causal_sizes = args.causal_size_each
	es_lows = args.es_low
	es_highs = args.es_high
	mss = args.wk_dir
	n_gen = args.sim_generation
	mut_rate = args.mut_rate
	norm_or_not = args.normalize

	## Check inputs
	run_check = True
	if (len(es_lows)!=trait_n):
		print("The given length of the lower bounds doesn't equal to the number of traits")
		run_check = False
	if (len(es_highs)!=trait_n):
		print("The given length of the higher bounds doesn't equal to the number of traits")
		run_check = False
	if norm_or_not:
		if n_gen==0:
			print("Need to specify a number of generation that is bigger than 0 in normalization mode")
			run_check = False
		if mut_rate==0:
			print("Need to specify a mutation rate that is bigger than 0 in normalization mode")
			run_check = False

	if run_check:
		generate_csv(trait_n, causal_sizes, es_lows, es_highs, gff_in, mss, n_gen, mut_rate, norm_or_not)
	else:
		print("Terminated because of incorrect input")
    

if __name__ == "__main__":
	main()


