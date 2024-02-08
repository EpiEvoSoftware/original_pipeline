import os
import subprocess
import shutil
import inspect
import tskit
import random
import pyslim


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
	if os.path.exists(vcf_path):
		all_vcf = open(vcf_path, "r")
		for line in all_vcf:
			if line.startswith("##"):
				continue
			else:
				ll = line.rstrip("\n")
				l = ll.split("\t")
				if len(l) == 9 + seeds_size:
					return(True)
				else:
					print("The vcf provided doesn't have the correct number of individuals in it. Terminated.")
					return(False)
	else:
		print("Path to the provided vcf doesn't exist. Terminated.")
		return(False)


def check_seed_phylo_input(path_seeds_phylogeny, wk_dir):
	if os.file.exists(path_seeds_phylogeny):
		shutil.copyfile(path_seeds_phylogeny, os.path.join(wk_dir, "seeds.nwk"))
		## Should also check whether the newick format is correct, and the tip names are correct
	else:
		print("Path to the provided seeds' phylogeny doesn't exist")


def split_seedvcf(seed_vcf_path, wk_dir, seeds_size, method):
	## A function that creates a directory (originalvcfs) in wk_dir, and splits the seeds' vcf into one vcf per seed
	## storing them in originalvcfs directory by the order of the seeds' vcf.
	## Input: seed_vcf_path: Full path to the seeds' vcf
	##        wk_dir: working directory
	##        seeds_size: how many seeds is needed
	##        method: user or slim
	## Output: No return value

	vcf_header = "##fileformat=VCFv4.2\n##source=SLiM\n##INFO=<ID=MID,Number=.,Type=Integer,Description=\"Mutation ID in SLiM\">\n##INFO=<ID=S,Number=.,Type=Float,Description=\"Selection Coefficient\">\n##INFO=<ID=DOM,Number=.,Type=Float,Description=\"Dominance\">\n##INFO=<ID=PO,Number=.,Type=Integer,Description=\"Population of Origin\">\n##INFO=<ID=TO,Number=.,Type=Integer,Description=\"Tick of Origin\">\n##INFO=<ID=MT,Number=.,Type=Integer,Description=\"Mutation Type\">\n##INFO=<ID=AC,Number=.,Type=Integer,Description=\"Allele Count\">\n##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total Depth\">\n##INFO=<ID=AA,Number=1,Type=String,Description=\"Ancestral Allele\">\n##INFO=<ID=NONNUC,Number=0,Type=Flag,Description=\"Non-nucleotide-based\">\n##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n"
	seeds_dir = os.path.join(wk_dir, "originalvcfs/")
	# If the directory exists, delete and regenerate it
	if os.path.exists(seeds_dir):
		shutil.rmtree(seeds_dir, ignore_errors=True)
	ref_allele = ["0|0", "0/0", "0", "."]
	vcf_info_col = 9
	pos_col = 1
	alt_col = 4
	ref_col = 3
	vcf_info_col_plus1 = vcf_info_col + 1
	pos_col_plus1 = pos_col + 1
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
			if method=="slim":
				l[pos_col] = str(int(l[pos_col]) + 1)
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
							newvcf.write("\t".join(l[:pos_col]) + "\t" + l[pos_col] + "\t" + "\t".join(l[pos_col_plus1:alt_col]) + "\t" + alt[int(geno[0])-1] + "\t1000\tPASS\tS=0;DOM=1;TO=1;MT=0;AC=1;DP=1000;AA=" + ref + "\tGT\t1\n")


def seed_userinput(seed_vcf_path, seed_size, wk_dir, path_seeds_phylogeny):
	if check_seedsvcf_input(seed_vcf_path, seed_size):
		split_seedvcf(seed_vcf_path, wk_dir, seed_size, "user")
	if path_seeds_phylogeny!="":
		check_seed_phylo_input(path_seeds_phylogeny, wk_dir)


def seed_WF(Ne, seed_size, ref_path, wk_dir, mu, n_gen):
	slim_script = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "burn_in_slim_scripts", "burnin_WF.slim")
	slim_stdout_path = os.path.join(wk_dir, "burn-in_slim.stdout")
	with open(slim_stdout_path, 'w') as fd:
		subprocess.run(["slim", "-d", f"Ne={Ne}", "-d", f"ref_path=\"{ref_path}\"", "-d", f"wk_dir=\"{wk_dir}\"", "-d", f"mu={mu}", "-d", f"n_gen={n_gen}", slim_script], stdout=fd)
	seeds_treeseq(wk_dir, seed_size)
	split_seedvcf(os.path.join(wk_dir, "seeds.vcf"), wk_dir, seed_size, "slim")

def seed_epi(wk_dir, seed_size, ref_path, mu, n_gen, host_size, seeded_host_id, S_IE_rate, E_I_rate=0, E_R_rate=0, latency_prob=0, I_R_rate=0, I_E_rate=0, R_S_rate=0):
	## A function to run the burn-in using the epidemiological model.
	## If user choose to run this method, they have to provide the network and all the parameters
	if os.path.exists(os.path.join(wk_dir, "burn_in_SEIR_trajectory.csv.gz")):
		os.remove(os.path.join(wk_dir, "burn_in_SEIR_trajectory.csv.gz"))
	slim_script = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "burn_in_slim_scripts", "burnin_epi.slim")
	slim_stdout_path = os.path.join(wk_dir, "burn-in_slim.stdout")
	with open(slim_stdout_path, 'w') as fd:
		subprocess.run(["slim", "-d", f"cwdir=\"{wk_dir}\"", "-d", f"ref_path=\"{ref_path}\"", "-d", f"contact_network_path=\"{os.path.join(wk_dir, "contact_network.adjlist")}\"", "-d", f"host_size={host_size}", "-d", f"mut_rate={mu}", "-d", f"n_generation={n_gen}", "-d", f"seeded_host_id=c({",".join([str(i) for i in seeded_host_id])})", "-d", f"S_IE_rate={S_IE_rate}", "-d", f"E_I_rate={E_I_rate}", "-d", f"E_R_rate={E_R_rate}", "-d", f"latency_prob={latency_prob}", "-d", f"I_R_rate={I_R_rate}", "-d", f"I_E_rate={I_E_rate}", "-d", f"R_S_rate={R_S_rate}", slim_script], stdout=fd)

	seeds_treeseq(wk_dir, seed_size)
	split_seedvcf(os.path.join(wk_dir, "seeds.vcf"), wk_dir, seed_size, "slim")



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


def seeds_treeseq(wk_dir, seed_size):
	## A function to read the seeds' treesequence file and output newick format from it.
	## Called when seed is generated by SLiM burn in.
	## Input: wk_dir: working directory
	## Output: No return value
	rscript_path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "seed_phylogeny_id_convert.r")

	ts = tskit.load(os.path.join(wk_dir, "seeds.trees"))

	if ts.tables.individuals.num_rows < seed_size:
		print("There's no enough genomes to choose seed from, please rerun the seed generation or adjust the parameters if needed.")
	else:
		sampled_inds = random.sample(range(ts.tables.individuals.num_rows), seed_size)
		seeds = [2 * i for i in sampled_inds]
		new_label = {}

		sampled_tree = ts.simplify(samples = seeds)
		sample_size = range(sampled_tree.tables.individuals.num_rows)

		all_tables = sampled_tree.tables
		table_ind = all_tables.individuals

		idx = 0
		for l_id in sample_size:
			subpop_now = table_ind[l_id].metadata["subpopulation"]
			new_label[l_id] = str(idx)
			idx = idx + 1
		roots_all = sampled_tree.first().roots

		phylo_path = os.path.join(wk_dir, "seeds_phylogeny_uncoalesced")
		if os.path.exists(phylo_path):
			shutil.rmtree(phylo_path)
		nwk_path = os.path.join(wk_dir, "seeds.nwk")
		if os.path.exists(nwk_path):
			os.remove(nwk_path)

		if len(roots_all)>1:
			os.mkdir(phylo_path)
			for root in roots_all:
				with open(os.path.join(phylo_path, str(root) + ".nwk"), "w") as nwk:
					nwk.write(sampled_tree.first().as_newick(root=root, node_labels = new_label))
		else:
			with open(nwk_path, "w") as nwk:
				nwk.write(sampled_tree.first().as_newick(root=roots_all[0], node_labels = new_label))
		
		f = open(os.path.join(wk_dir, "seeds.vcf"), "w")
		nu_ts = pyslim.convert_alleles(sampled_tree)
		nu_ts.write_vcf(f, individual_names=new_label.values())



def seeds_generation_byconfig(all_config):
	## A function to run different seeds generation/modification based on a provided config file
	## Input: all_config: A dictionary of the configuration (read with read_params())
	## Output: No return value

	seeds_config = all_config["SeedsConfiguration"]
	wk_dir = seeds_config["BasicRunConfiguration"]["cwdir"]
	method = seeds_config["method"]
	seed_size = seeds_config["seeds_size"]
	seed_vcf = seeds_config["user_input"]["path_seeds_vcf"]
	path_seeds_phylogeny = seeds_config["user_input"]["path_seeds_phylogeny"]
	Ne = seeds_config["SLiM_burnin_WF"]["burn_in_Ne"]
	ref_path = all_config["GenomeElement"]["ref_path"]
	if method=="user_input":
		n_gen = 0
	elif seed_method=="SLiM_burnin_WF":
		n_gen = seeds_config["SLiM_burnin_WF"]["burn_in_generations"]
		mu = seeds_config["SLiM_burnin_WF"]["burn_in_Ne"]
	elif seed_method=="SLiM_burnin_epi":
		n_gen = seeds_config["SLiM_burnin_epi"]["burn_in_generations"]
		mu = seeds_config["SLiM_burnin_epi"]["burn_in_Ne"]

	host_size = all_config["NetworkModelParameters"]["host_size"]
	seeded_host_id = seeds_config["SLiM_burnin_epi"]["seeded_host_id"]
	S_IE_rate = seeds_config["user_input"]["S_IE_rate"]
	E_I_rate = seeds_config["SLiM_burnin_epi"]["E_I_rate"]
	E_R_rate = seeds_config["SLiM_burnin_epi"]["E_R_rate"]
	latency_prob = seeds_config["SLiM_burnin_epi"]["latency_prob"]
	I_R_rate = seeds_config["SLiM_burnin_epi"]["I_R_rate"]
	I_E_rate = seeds_config["SLiM_burnin_epi"]["I_E_rate"]
	R_S_rate = seeds_config["SLiM_burnin_epi"]["R_S_rate"]

	run_seed_generation(method=method, wk_dir=wk_dir, seed_size=seed_size, seed_vcf=seed_vcf, Ne=Ne, ref_path=ref_path, mu=mu, n_gen=n_gen, path_seeds_phylogeny=path_seeds_phylogeny, host_size=host_size, seeded_host_id=seeded_host_id, S_IE_rate=S_IE_rate, E_I_rate=E_I_rate, E_R_rate=E_R_rate, latency_prob=latency_prob, I_R_rate=I_R_rate, I_E_rate=I_E_rate, R_S_rate=R_S_rate)



def run_seed_generation(method, wk_dir, seed_size, seed_vcf="", Ne=0, ref_path="", mu=0, n_gen=0, path_seeds_phylogeny="", host_size=0, seeded_host_id=[], S_IE_rate=0, E_I_rate=0, E_R_rate=0, latency_prob=0, I_R_rate=0, I_E_rate=0, R_S_rate=0):
	run_check = True
	if os.path.exists(wk_dir)==False:
		print("The working directory path provided doesn't exist.")
		run_check = False
	if method=="user_input":
		if seed_vcf=="":
			print("Need to specify a path to the seeds' vcf (-seed_vcf) file in user_input mode.")
			run_check = False
	elif method=="SLiM_burnin_WF":
		if Ne==0:
			print("Need to specify an effective population size (-Ne) bigger than 0 in SLiM WF burn-in mode.")
			run_check = False
		elif ref_path=="":
			print("Need to specify a path to the reference genome (-ref_path) in SLiM burn-in mode.")
			run_check = False
		elif os.path.exists(ref_path)== False:
			print("Path to the reference genome provided doesn't exist.")
			run_check = False
		elif mu==0:
			print("Need to specify a mutation rate (-mu) bigger than 0 in SLiM burn-in mode.")
			run_check = False
		elif n_gen==0:
			print("Need to specify a burn-in generation (-n_gen) bigger than 0 in SLiM burn-in mode.")
			run_check = False
	elif method == "SLiM_burnin_epi":
		if ref_path=="":
			print("Need to specify a path to the reference genome (-ref_path) in SLiM burn-in mode.")
			run_check = False
		elif os.path.exists(ref_path)== False:
			print("Path to the reference genome provided doesn't exist.")
			run_check = False
		elif mu==0:
			print("Need to specify a mutation rate (-mu) bigger than 0 in SLiM burn-in mode.")
			run_check = False
		elif n_gen==0:
			print("Need to specify a burn-in generation (-n_gen) bigger than 0 in SLiM burn-in mode.")
			run_check = False
		elif os.path.exists(os.path.join(wk_dir, "contact_network.adjlist"))==False:
			print("Contact network file in the working directory isn't detected, please run network generation before running seeds' burn-in in SLiM epi model burn-in mode.")
			run_check = False
		elif len(seeded_host_id)==0:
			print("Need to specify at least one host id (-seeded_host_id) to be seeded in SLiM epi model burn-in mode.")
			run_check = False
		elif host_size < len(seeded_host_id):
			print("Need to specify a host population size (-host_size) bigger than the size of the seeded hosts in SLiM epi model burn-in mode.")
			run_check = False
		elif max(seeded_host_id) >= host_size:
			print("All the host ids to be seeded has to be smaller than host population size.")
			run_check = False
		elif S_IE_rate==0:
			print("An infection rate (-S_IE_rate, Susceptible to infected/exposed rate) bigger than 0 needs to be provided in SLiM epi model burn-in mode.")
			run_check = False
		elif latency_prob>0:
			if E_I_rate==0 and E_R_rate==0:
				print("WARNING: You activated an SEIR model, in which exposed compartment exists, but you doesn't specify any transition from exposed compartment, which will lead to exposed hosts being locked (never recovered and cannot infect others). Please make sure this is what you want.")
		elif I_R_rate==0:
			print("WARNING: You activated a S(E)I model by setting I>R rate = 0, where recovered component doesn't exists, meaning that all infected hosts never recovered. Please make sure this is what you want.")
		elif R_S_rate==0:
			print("WARNING: You activated a S(E)IR model with Recovered individuals are fully immune, they don't go back to recovered state. This can probably lead to the outbreak ending before the specified burn-in generation and makes the seeds' sampling fail. Please make sure this is what you want.")
	else:
		run_check = False
		print(f"{method} isn't a valid method. Please provide a permitted method. (user_input/SLiM_burnin_WF/SLiM_burnin_epi)")

	# Actually run
	if run_check:
		if method=="user_input":
			seed_userinput(seed_vcf, seed_size, wk_dir, path_seeds_phylogeny)

		elif method=="SLiM_burnin_WF":
			seed_WF(Ne, seed_size, ref_path, wk_dir, mu, n_gen)

		elif method == "SLiM_burnin_epi":
			seed_epi(wk_dir, seed_size, ref_path, mu, n_gen, host_size, seeded_host_id, S_IE_rate, E_I_rate, E_R_rate, latency_prob, I_R_rate, I_E_rate, R_S_rate)

	else:
		print("Terminated because of incorrect input") 









		