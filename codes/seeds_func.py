import os, subprocess, shutil, inspect, tskit, random, pyslim
from error_handling import CustomizedError
import ete3 as Tree

NUM_VCF_FORMAT_COLUMNS = 9
POS_COL = 1
ALT_COL = 4
REF_COL = 3
VCF_STR_HA = "\t1000\tPASS\tS=0;DOM=1;TO=1;MT=0;AC=1;DP=1000;AA="
VCF_STR_HB = "\tGT\t1\n"

PHYLO_PREFIX = "seeds_phylogeny_uncoalesced"
NEWICK_SUFFIX = ".nwk"
NEWICK_NAME = "seeds.nwk"
VCF_NAME = "seeds.vcf"

VCF_HEAD = """\
	##fileformat=VCFv4.2\n##source=SLiM
	##INFO=<ID=MID,Number=.,Type=Integer,Description=\"Mutation ID in SLiM\">
	##INFO=<ID=S,Number=.,Type=Float,Description=\"Selection Coefficient\">
	##INFO=<ID=DOM,Number=.,Type=Float,Description=\"Dominance\">
	##INFO=<ID=PO,Number=.,Type=Integer,Description=\"Population of Origin\">
	##INFO=<ID=TO,Number=.,Type=Integer,Description=\"Tick of Origin\">
	##INFO=<ID=MT,Number=.,Type=Integer,Description=\"Mutation Type\">
	##INFO=<ID=AC,Number=.,Type=Integer,Description=\"Allele Count\">
	##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total Depth\">
	##INFO=<ID=AA,Number=1,Type=String,Description=\"Ancestral Allele\">
	##INFO=<ID=NONNUC,Number=0,Type=Flag,Description=\"Non-nucleotide-based\">
	##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">
	"""

def _create_seeds_directory(wk_dir):
	"""
	Returns new directory storing the seed vcf files

	Parameters:
		wk_dir (str): Working directory
	"""
	seeds_dir = os.path.join(wk_dir, "originalvcfs/")
	# Remove if the directory already exists
	if os.path.exists(seeds_dir):
		shutil.rmtree(seeds_dir, ignore_errors=True)
	os.mkdir(seeds_dir)
	return seeds_dir

def _copy_vcf_headers(all_separate_vcfs):
	"""
	Writes header information into each VCF.

	Parameters:
		all_separate_vcfs (list[str]): File paths of VCF files.
	"""
	for vcf in all_separate_vcfs:
		with open(vcf, "a") as a_vcf:
			a_vcf.write(VCF_HEAD)

def _write_column_names(all_separate_vcfs, header_line, vcf_info_col_plus1):
	"""
	Writes the column names into each VCF.

	Parameters: 
		all_separate_vcfs (list[str]): File paths of VCF files.
		header_line (str): The column line of the shared seed VCF.
		vcf_info_col_plus1 (int): The index of info column for the second seed.
	"""
	col_names = header_line.rstrip("\n").split("\t")
	for newvcf in all_separate_vcfs:
		with open(newvcf, "a") as vcf_file:
			# Only include the column name for the first seed, 
			# because in each vcf file we will only have one seed
			vcf_file.write("\t".join(col_names[:vcf_info_col_plus1]) + "\n")

def _process_data_lines(seed_vcf_path, all_separate_vcfs, method):
	"""
	Writes non-header lines into individual VCF files.

	Parameters:
		seed_vcf_path (str): File path of the input seed VCF file.
		all_separate_vcfs (list[str]): File path of the seeds' VCF files.
		method (str): the burn-in method (e.g., slim).
	"""
	# Define the reference allele
	ref_allele = ["0|0", "0/0", "0", "."]
	with open(seed_vcf_path, "r") as all_vcf:
		for line in all_vcf:
			if line.startswith("#"):
				_write_column_names(all_separate_vcfs, line, NUM_VCF_FORMAT_COLUMNS + 1)
			elif not line.startswith("##"):
				# Encounter a row of information
				fields = line.rstrip("\n").split("\t")
				if method == "slim":
					# SLiM use index 1 instead of 0
					fields[POS_COL] = str(int(fields[POS_COL]) + 1)
				for i, newvcf in enumerate(all_separate_vcfs):
					idx = NUM_VCF_FORMAT_COLUMNS + i
					if fields[idx] not in ref_allele:
						ref = fields[REF_COL]
						# Get the base of this seed
						geno = fields[idx].split("|") if "|" in fields[idx] else fields[idx].split("/")
						geno = list(set([x for x in geno if x != "0"]))
						if len(geno) <= 1:
							# Write to the vcf file
							alt = fields[ALT_COL].split(",") if len(fields[ALT_COL]) > 1 else [fields[ALT_COL]]
							with open(newvcf, "a") as vcf_file:
								vcf_file.write("\t".join(fields[:ALT_COL]) + 
											alt[int(geno[0])-1] + VCF_STR_HA + ref + VCF_STR_HB)
						else:
							raise CustomizedError("The genotype is a heterozygote, \
												which is not permitted for a haploid pathogen genome.")
						
def _generate_sample_indices(ts, seed_size):
    """
    Generate sample indices for simplification.

    Parameters:
        ts (tskit.TreeSequence): The treesequence.
        seed_size (int): The number of seeds.

    Returns:
        list: List of sample indices.
    """
    if ts.tables.individuals.num_rows < seed_size:
        raise ValueError("Not enough genomes to choose seeds from. Please rerun the seed generation or adjust parameters.")
    sampled_inds = random.sample(range(ts.tables.individuals.num_rows), seed_size)
    return [2 * i for i in sampled_inds]


def check_seedsvcf_input(vcf_path, seeds_size):
	"""
	Checks the format of the user-input seeds' VCF file.
	
	Parameters:
		vcf_path (str): Full path to the seeds' VCF file.
		seeds_size (int): Number of seeds needed.
	"""
	# Check if the file exists
	if not os.path.exists(vcf_path):
		raise FileNotFoundError(f"Path to the provided VCF ({vcf_path}) doesn't exist.")
	
	# Check if the number of columns align with the number of seeds
	with open(vcf_path, "r") as all_vcf:
		for line in all_vcf:
			if line.startswith("##"):
				continue
			else:
				line_stp = line.rstrip("\n").split("\t")
				if len(line_stp) != NUM_VCF_FORMAT_COLUMNS + seeds_size:
					raise CustomizedError(f"The vcf provided doesn't 
						   have the correct number of individuals ({seeds_size}) in it.")
	
	return True


def copy_seed_phylo_input(path_seeds_phylogeny, wk_dir):
	"""
	Checks and copies the seeds' phylogenies into working directory.

	Parameters:
		path_seeds_phylogeny (str): Full path to the seeds' phylogeny VCF.
		wk_dir (str): Working directory.
	"""
	if not os.path.exists(path_seeds_phylogeny):
		raise CustomizedError(f"Path to the provided seeds' 
						phylogeny ({path_seeds_phylogeny}) doesn't exist.")
	## Should also check whether the newick format is correct, and the tip names are correct
	phylo = Tree(path_seeds_phylogeny, "newick")
	tips = sorted([leaf.name for leaf in phylo])
	if tips != list(range(len(tips))):
		raise CustomizedError("Seed phylogeny tip labels must be consecutive integers \
						starting from 0.")
	shutil.copyfile(path_seeds_phylogeny, os.path.join(wk_dir, "seeds.nwk"))


def split_seedvcf(seed_vcf_path, wk_dir, seeds_size, method):
	"""
	Splits the one shared seed vcf into individual seed's VCF.

	Parameters:
		seed_vcf_path (str): Full path to the shared seed VCF
		wk_dir (str): Working directory to write the new VCFs into
		seeds_size (int): Number of seeds
		method (str): the burn-in method (e.g., slim)
	"""
	seeds_dir = _create_seeds_directory(wk_dir)
	all_separate_vcfs = [os.path.join(seeds_dir, f"seed.{i}.vcf") for i in range(seeds_size)]
	_copy_vcf_headers(all_separate_vcfs)
	_process_data_lines(seed_vcf_path, all_separate_vcfs, method)


def seed_userinput(seed_vcf_path, seed_size, wk_dir, path_seeds_phylogeny):
	"""
	Check and/or copy user input seeds' information

	Parameters:
		seed_vcf_path (str): Full path to the shared seed VCF
		seed_size (int): Number of seeds
		wk_dir: Working directory
		path_seeds_phylogeny (str): Full path to the seeds' phylogeny if opt to use
	"""
	# Check shared seed vcf
	if check_seedsvcf_input(seed_vcf_path, seed_size):
		split_seedvcf(seed_vcf_path, wk_dir, seed_size, "user")
	# Copy shared seed phylogeny newick file into working directory
	if path_seeds_phylogeny != "":
		copy_seed_phylo_input(path_seeds_phylogeny, wk_dir)


def seed_WF(Ne, seed_size, ref_path, wk_dir, mu, n_gen):
	slim_script = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "burn_in_slim_scripts", "burnin_WF.slim")
	slim_stdout_path = os.path.join(wk_dir, "burn-in_slim.stdout")
	with open(slim_stdout_path, 'w') as fd:
		subprocess.run(["slim", "-d", f"Ne={Ne}", "-d", f"ref_path=\"{ref_path}\"", "-d", f"wk_dir=\"{wk_dir}\"", "-d", f"mu={mu}", "-d", f"n_gen={n_gen}", slim_script], stdout=fd)
	seeds_treeseq(wk_dir, seed_size)
	split_seedvcf(os.path.join(wk_dir, "seeds.vcf"), wk_dir, seed_size, "slim")
	os.remove(os.path.join(wk_dir, "seeds.vcf"))

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

	# Load the tree sequence
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









		