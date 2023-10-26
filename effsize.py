import numpy as np
from random import sample
import os
import argparse


### We already have the right format, just count the muts
def count_muts(mss):
	c = 0
	counts = []
	seeds = os.listdir(mss)
	for seed in seeds:
		with open(mss + seed, "r") as seed_vcf:
			counts.append(0)
			for line in seed_vcf:
				if line.startswith("#"):
					continue
				else:
					counts[c] = counts[c] + 1
			c = c + 1
	return(max(counts))

def modify_vcf(starts, ends, coe, mss, causal_size, k):
	seeds = os.listdir(mss)
	for seed in seeds:
		with open(mss + seed, "r") as seed_vcf:
			with open(mss + seed.rstrip(".vcf") + ".coe.vcf", "w") as out_vcf:
				for line in seed_vcf:
					in_causal = False
					if line.startswith("#"):
						out_vcf.write(line)
					else:
						ll = line.rstrip("\n")
						l = ll.split("\t")
						for i in range(causal_size):
							if int(l[1])>=int(starts[i]) and int(l[1])<=int(ends[i]):
								out_vcf.write("\t".join(l[:7]) + "\t" + "S=" + str(k * coe[i]) + ";DOM=1;TO=1;MT=" +str(i+1) + ";AC=1;DP=1000;AA=" + l[3] + "\tGT\t1\n")
								in_causal = True
								break
						if in_causal==False:
							out_vcf.write(line)



def generate_eff(gff_, causal, es_low, es_high, mss):
	g_len = 0
	with open(gff_, "r") as gff:
		for line in gff:
			if line.startswith("\n"):
				continue
			else:
				g_len = g_len + 1

	genes = sample(range(int(g_len)), int(causal))

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
				names.append(info[2].split("=")[1])
				coe.append(np.random.uniform(float(es_low), float(es_high), 1)[0])
				causal_length.append(int(l[4])-int(l[3]))
				starts.append(l[3])
				ends.append(l[4])
			index = index + 1
	#print(coe)
	max_muts = count_muts(mss)
	total_sum = 0
	for i in range(causal):
		total_sum = total_sum + (((max_muts + 100 * 1.6e-6) * causal_length[i]) / 4411532 ) * coe[i]
	k = 1 / total_sum
	#print(k)

	with open("causal_gene_info.csv", "w") as csv:
		csv.write("gene_name,start,end,eff_size\n")
		for i in range(causal):
			csv.write(names[i] + "," + starts[i] + "," + ends[i] + "," + str(k * coe[i]) + "\n")
			index = index + 1

	modify_vcf(starts, ends, coe, mss, causal, k)

	


def main():
	parser = argparse.ArgumentParser(description='Generate the selection coefficient modifying part of the slim script.')
	parser.add_argument('-gff', action='store',dest='gff', required=True)
	parser.add_argument('-causal', action='store',dest='causal', required=True, type=int)
	parser.add_argument('-es_low', action='store',dest='es_low', required=True, type=float)
	parser.add_argument('-es_high', action='store',dest='es_high', required=True, type=float)
	parser.add_argument('-seeds_dir', action='store',dest='seeds_dir', required=True)

	args = parser.parse_args()
	gff_in = args.gff
	causal_size = args.causal
	effsize_low = args.es_low
	effsize_high = args.es_high
	mss = args.seeds_dir


	generate_eff(gff_in, causal_size, effsize_low, effsize_high, mss)
    

if __name__ == "__main__":
	main()


