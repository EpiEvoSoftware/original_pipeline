import os
import subprocess
import shutil


#################### SEEDS GENRATION ################
def check_seedsvcf_input(vcf_path, seeds_size):
	## A function to check the format of the user-input seeds' vcf file
	## First check whether the file exists
	## Then check whether the file has the same number of columns as seeds_size specified
	## Lastly check the format of the vcf file (all the entries being 0 or 1)
	## Return error message for each problem
	## Return True or False
	### Input: vcf_path: Full path to the seeds' vcf file (one file)
	###		   seeds_size: how many seeds is needed
	### Output: Boolean value (True/False)
	return(True)

def split_seedvcf(seed_vcf_path, wk_dir, seeds_size):
	## A function that creates a directory (originalvcfs) in wk_dir, and splits the seeds' vcf into one vcf per seed
	## storing them in originalvcfs directory by the order of the seeds' vcf.
	## Input: seed_vcf_path: Full path to the seeds' vcf
	##        wk_dir: working directory
	##        seeds_size: how many seeds is needed
	## Output: No return value

	vcf_header = "##fileformat=VCFv4.2\n##source=SLiM\n##INFO=<ID=MID,Number=.,Type=Integer,Description=\"Mutation ID in SLiM\">\n##INFO=<ID=S,Number=.,Type=Float,Description=\"Selection Coefficient\">\n##INFO=<ID=DOM,Number=.,Type=Float,Description=\"Dominance\">\n##INFO=<ID=PO,Number=.,Type=Integer,Description=\"Population of Origin\">\n##INFO=<ID=TO,Number=.,Type=Integer,Description=\"Tick of Origin\">\n##INFO=<ID=MT,Number=.,Type=Integer,Description=\"Mutation Type\">\n##INFO=<ID=AC,Number=.,Type=Integer,Description=\"Allele Count\">\n##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total Depth\">\n##INFO=<ID=AA,Number=1,Type=String,Description=\"Ancestral Allele\">\n##INFO=<ID=NONNUC,Number=0,Type=Flag,Description=\"Non-nucleotide-based\">\n##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n"
	seeds_dir = os.path.join(wk_dir, "originalvcfs/")
	# If the directory exists, delete and regenerate it
	if os.path.exists(seeds_dir):
		shutil.rmtree(seeds_dir, ignore_errors=True)
	ref_allele = ["0|0", "0/0", "0", "."]
	vcf_info_col = 9
	alt_col = 4
	ref_col = 3
	vcf_info_col_plus1 = vcf_info_col + 1
	os.mkdir(seeds_dir)
	all_separate_vcfs = []
	for i in range(seeds_size):
		current_vcf = os.path.join(seeds_dir, f"seed.{i}.vcf")
		all_separate_vcfs.append(current_vcf)
		separate_vcf = open(os.path.join(current_vcf), "a")
		separate_vcf.write(vcf_header)
		separate_vcf.close()
	all_vcf = open(seed_vcf_path, "r")
	for line in all_vcf:
		if line.startswith("##"):
			continue
		elif line.startswith("#"):
			ll = line.rstrip("\n")
			l = ll.split("\t")
			for i in range(seeds_size):
				with open(all_separate_vcfs[i], "a") as newvcf:
					newvcf.write("\t".join(l[:vcf_info_col_plus1]) + "\n")
		else:
			ll = line.rstrip("\n")
			l = ll.split("\t")
			for i in range(seeds_size):
				if (l[vcf_info_col+i] not in ref_allele):
					ref = l[ref_col]
					if "|" in l[vcf_info_col+i]:
						geno_ = l[vcf_info_col+i].split("|")
					elif "/" in l[vcf_info_col+i]:
						geno_ = l[vcf_info_col+i].split("/")
					else:
						geno_ = [l[vcf_info_col+i]]
					geno = list(set([x for x in geno_ if x != "0"]))
					if len(geno) > 1:
						print("The genotype is a heterozygot, which is not permitted for a haploid pathogen genome")
					else:
						if len(l[alt_col]) > 1:
							alt = l[alt_col].split(",")
						else:
							alt = [l[alt_col]]
						with open(all_separate_vcfs[i], "a") as newvcf:
							newvcf.write("\t".join(l[:alt_col]) + "\t" + alt[int(geno[0])-1] + "\t1000\tPASS\tS=0;DOM=1;TO=1;MT=0;AC=1;DP=1000;AA=" + ref + "\tGT\t1\n")


def seed_userinput(seed_vcf_path, seed_size, wk_dir):
	if check_seedsvcf_input(seed_vcf_path, seed_size):
		split_seedvcf(seed_vcf_path, wk_dir, seed_size)

def seed_WF(Ne, seed_size, ref_path, wk_dir, mu, n_gen):
	subprocess.run(["slim", "-d", f"Ne={Ne}", "-d", f"seed_size={seed_size}", "-d", f"ref_path=\"{ref_path}\"", "-d", f"wk_dir=\"{wk_dir}\"", "-d", f"mu={mu}", "-d", f"n_gen={n_gen}", "burnin_WF.slim"])
	split_seedvcf(os.path.join(wk_dir, "seeds.vcf"), wk_dir, seed_size)

def seed_epi():
	## A function to run the burn-in using the epidemiological model.
	## If user choose to run this method, they have to provide the network and all the parameters
	return 0


def seeds_tree_scaling(tree_path, scale_factor, wk_dir):
	## A function to scale the seeds' phylogeny and store in working directory
	## First check whether the tree is a valid newick format single root tree, is so, 
	## The branch lengths of the scaled tree will be {scale_factor} times of the original tree.
	## If not, print error.
	## Input: tree_path: Path to the seeds' phylogeny
	##        scale_factor: Scaling factor of the phylogeny (seed to transmission tree)
	##        wk_dir: working directory
	## Output: No return value
	return 0


def seeds_treeseq(wk_dir):
	## A function to read the seeds' treesequence file and output newick format from it.
	## Called when seed is generated by SLiM burn in.
	## Input: wk_dir: working directory
	## Output: No return value
	return 0


def seeds_generation_byconfig(all_config):
	## A function to run different seeds generation/modification based on a provided config file
	## Input: all_config: A dictionary of the configuration (read with read_params())
	## Output: No return value

	seeds_config = all_config["SeedsConfiguration"]
	wk_dir = seeds_config["BasicRunConfiguration"]["cwdir"]
	seed_method = seeds_config["seeds_vcf"]["method"]

	if seed_method=="user_input":
		seed_vcf_path = seeds_config["seeds_vcf"]["user_input"]["path_seeds_vcf"]
		seed_generation_userinput(seed_vcf_path, seeds_config["seeds_size"], wk_dir)
		if os.path.exists(seeds_config["path_seeds_phylogeny"]):
			seeds_tree_scaling(seeds_config["path_seeds_phylogeny"], seeds_config["scaling_factor"], wk_dir)
	elif seed_method=="SLiM_burnin_WF":
		slim_param = seeds_config["SLiM_burnin_WF"]
		seed_generation_WF(slim_param["burn_in_Ne"], seeds_config["seeds_size"], all_config["GenomeElement"]["ref_path"], wk_dir, slim_param["burn_in_mutrate"], slim_param["burn_in_generations"])
		seeds_tree_scaling(os.path.join(wk_dir, "seeds.nwk"), seeds_config["scaling_factor"], wk_dir)
	elif seed_method=="SLiM_burnin_epi":
		slim_param = seeds_config["SLiM_burnin_epi"]
		seed_generation_epi() ################################ UNFINISHED #########################
	else:
		print("Please use the correct generation method")


def run_seed_generation(method, wk_dir, seed_size, seed_vcf="", Ne=0, ref_path="", mu=0, n_gen=0):
	run_check = True
	if method=="user_input":
		if seed_vcf=="":
			print("Need to specify a path to the seeds' vcf file in user_input mode.")
			run_check = False
	elif method=="SLiM_burnin_WF":
		if Ne==0:
			print("Need to specify an effective population size bigger than 0 in SLiM burn-in mode.")
			run_check = False
		elif ref_path=="":
			print("Need to specify a path to the reference genome in SLiM burn-in mode.")
			run_check = False
		elif mu==0:
			print("Need to specify a mutation rate bigger than 0 in SLiM burn-in mode.")
			run_check = False
		elif n_gen==0:
			print("Need to specify a burn-in generation bigger than 0 in SLiM burn-in mode.")
			run_check = False
	else:
		run_check = False
		print("Please provide a permitted method.")

	# Actually run
	if run_check:
		if method=="user_input":
			seed_userinput(seed_vcf, seed_size, wk_dir)
		elif method=="SLiM_burnin_WF":
			seed_WF(Ne, seed_size, ref_path, wk_dir, mu, n_gen)
	else:
		print("Terminated because of incorrect input") 









		