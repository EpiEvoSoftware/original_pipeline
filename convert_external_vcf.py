import argparse


#### This is when we have a out-source vcf that doesn't meet our criterior, when count muts, we also change them into the vcf format SLiM can read
def convert_external_vcf(vcf, wkdir):
	with open(vcf, "r") as vcf_external:
		with open(wkdir + "seeds.vcf", "a") as newvcf:
			newvcf.write("##fileformat=VCFv4.2\n##INFO=<ID=S,Number=.,Type=Float,Description=\"Selection Coefficient\">\n##INFO=<ID=DOM,Number=.,Type=Float,Description=\"Dominance\">\n##INFO=<ID=PO,Number=.,Type=Integer,Description=\"Population of Origin\">\n##INFO=<ID=TO,Number=.,Type=Integer,Description=\"Tick of Origin\">\n##INFO=<ID=MT,Number=.,Type=Integer,Description=\"Mutation Type\">\n##INFO=<ID=AC,Number=.,Type=Integer,Description=\"Allele Count\">\n##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total Depth\">\n##INFO=<ID=AA,Number=1,Type=String,Description=\"Ancestral Allele\">\n##INFO=<ID=NONNUC,Number=0,Type=Flag,Description=\"Non-nucleotide-based\">\n##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n##source=GenomicsDBImport\n##source=SelectVariants\n##source=VariantFiltration\n")
			for line in vcf_external:
				if line.startswith("##"):
					continue
				elif line.startswith("#"):
					newvcf.write(line)
				else:
					ll = line.rstrip("\n")
					l = ll.split("\t")
					num_seeds = len(l) - 9
					ref = l[3]
					geno = l[9+i].split("|")[0]
					if len(l[4]) > 1:
						alt = l[4].split(",")
					new_line = "\t".join(l[:5]) + "\t1000\tPASS\tS=0;DOM=1;TO=1;MT=0;AC=1;DP=1000;AA=" + ref + "\tGT"
					for i in range(num_seeds):
						if (l[9+i]=="0|0" or l[9+i]=="0/0"):
							new_line = new_line + "\t0" 
						else:
							for j in range(1, len(alt)):
								if str(j) in l[9+i]:
									new_line = new_line + "\t" + str(j)
									break        
					newvcf.write(new_line + "\n")



def main():
	parser = argparse.ArgumentParser(description='Generate the selection coefficient modifying part of the slim script.')
	parser.add_argument('-vcf_path', action='store',dest='vcf_path', required=True)
	parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)

	args = parser.parse_args()
	vcf_ = args.vcf_path
	wkdir_ = args.wk_dir


	generate_eff(gff_in, csv_in, causal_size, effsize_low, effsize_high, mss)
    

if __name__ == "__main__":
	main()
