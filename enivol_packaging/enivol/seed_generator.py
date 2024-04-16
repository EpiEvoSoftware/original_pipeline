import os, subprocess, shutil, tskit, pyslim, numpy as np
from error_handling import CustomizedError
from base_func import *
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

NODES_PER_IND = 2
NW_PRE = ".nwk"
NW_PATH = "seeds.nwk"
VCF_PATH = "seeds.vcf"

SLIM_DIR = "burn_in_slim_scripts"
WF_SLIM = "burnin_WF.slim"
EPI_SLIM = "burnin_epi.slim"
OUT_SLIM = "burn-in_slim.stdout"
TRAJ = "burn_in_SEIR_trajectory.csv.gz"

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
			if line.startswith("#CHROM"):
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
								vcf_file.write("\t".join(fields[:ALT_COL]) + "\t" +
											alt[int(geno[0])-1] + VCF_STR_HA + ref + VCF_STR_HB)
						else:
							raise CustomizedError("The genotype is a heterozygote, "
												"which is not permitted for a haploid pathogen genome")
						
def _generate_sample_indices(ts, seed_size):
	"""
	Generates sample indices for simplification.

	Parameters:
		ts (tskit.TreeSequence): The treesequence.
		seed_size (int): The number of seeds.

	Returns:
		list: List of sample indices.
	"""
	if ts.tables.individuals.num_rows < seed_size:
		raise ValueError("Not enough genomes to choose seeds from. "
						 "Please rerun the seed generation or adjust parameters.")
	sampled_inds = np.random.choice(ts.tables.individuals.num_rows, seed_size, replace = False)
	genome_ids = [NODES_PER_IND * i for i in sampled_inds]
	return genome_ids

def _write_newick_file(wk_dir, sampled_tree, node_labels):
	"""
    Writes Newick files and return the node labels for consistent subsequent VCF outputs.

    Parameters:
        wk_dir (str): Working directory.
        sampled_tree (tskit.Tree): The sampled tree.
		node_labels (dict): Dictionary mapping ints  to strs.
    """
	# Get roots and set up interested path/dir
	roots = sampled_tree.first().roots
	phylo_path = os.path.join(wk_dir, PHYLO_PREFIX)
	nwk_path = os.path.join(wk_dir, NEWICK_NAME)

	# Remove existing dirs/paths, which might be from previous unsuccessful runs
	if os.path.exists(phylo_path):
		shutil.rmtree(phylo_path)
	if os.path.exists(nwk_path):
		os.remove(nwk_path)

	# Write newicks depending on whether this is a multi-root tree
	if len(roots) > 1:
		for r in roots:
			os.mkdir(phylo_path)
			with open(os.path.join(phylo_path, str(r) + NEWICK_SUFFIX), "w") as nwk:	
				nwk.write(sampled_tree.first().as_newick(root=r, node_labels = node_labels))
	else:
		with open(nwk_path, "w") as nwk:
			nwk.write(sampled_tree.first().as_newick(root=roots[0], node_labels = node_labels))
	
def _write_vcf_file(wk_dir, sampled_tree, node_labels):
	"""
    Write VCF file for seeds.

    Parameters:
        wk_dir (str): Working directory.
        sampled_tree (tskit.Tree): The sampled tree.
        node_labels (dict): Dictionary mapping ints  to strs.
    """
	with open(os.path.join(wk_dir, VCF_NAME), "w") as f:
		nu_ts = pyslim.convert_alleles(sampled_tree)
		# indidviduals = sample IDs, NEWLY ADDED to make sure the node ids and strings match
		nu_ts.write_vcf(f, individuals = list(node_labels.keys()), \
				  individual_names = list(node_labels.values()))

def check_seedsvcf_input(vcf_path, seeds_size):
	"""
	Checks the format of the user-input seeds' VCF file.
	
	Parameters:
		vcf_path (str): Full path to the seeds' VCF file.
		seeds_size (int): Number of seeds needed.
	"""
	# Check if the file exists
	if not os.path.exists(vcf_path):
		raise FileNotFoundError(f"Path to the provided VCF ({vcf_path}) doesn't exist")
	
	# Check if the number of columns align with the number of seeds
	with open(vcf_path, "r") as all_vcf:
		for line in all_vcf:
			if line.startswith("##"):
				continue
			else:
				line_stp = line.rstrip("\n").split("\t")
				if len(line_stp) != NUM_VCF_FORMAT_COLUMNS + seeds_size:
					raise CustomizedError("The vcf provided doesn't "
						   f"have the correct number of individuals ({seeds_size}) in it.")
	
	return True


def copy_seed_phylo_input(path_seeds_phylogeny, wk_dir):
	"""
	Checks and copies the seeds' phylogenies into working directory.

	Parameters:
		path_seeds_phylogeny (str): Full path to the seeds' phylogeny NWK.
		wk_dir (str): Working directory.
	"""
	if not os.path.exists(path_seeds_phylogeny):
		raise CustomizedError("Path to the provided seeds' "
						f"phylogeny ({path_seeds_phylogeny}) doesn't exist")
	## Should also check whether the newick format is correct, and the tip names are correct
	phylo = Tree(path_seeds_phylogeny, "newick")
	tips = sorted([leaf.name for leaf in phylo])
	if tips != list(range(len(tips))):
		raise CustomizedError("Seed phylogeny tip labels must be consecutive integers "
						"starting from 0.")
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
	Checks and/or copy user input seeds' information

	Parameters:
		seed_vcf_path (str): Full path to the shared seed VCF
		seed_size (int): Number of seeds
		wk_dir: Working directory
		path_seeds_phylogeny (str): Full path to the seeds' phylogeny if opt to use
	"""
	if seed_vcf_path == "":
		raise CustomizedError("You need to specify a path to the seeds' vcf "
						"(-seed_vcf) file in user_input mode")
	# Check shared seed vcf
	if check_seedsvcf_input(seed_vcf_path, seed_size):
		split_seedvcf(seed_vcf_path, wk_dir, seed_size, "user")
	# Copy shared seed phylogeny newick file into working directory
	if path_seeds_phylogeny != "":
		copy_seed_phylo_input(path_seeds_phylogeny, wk_dir)


def seeds_treeseq(wk_dir, seed_size):
	"""
    Read the seeds' treesequence file and output newick/VCF format from it.

    Parameters:
        wk_dir (str): Working directory.
        seed_size (int): Number of seeds.
    """
	# Load the tree sequence
	ts = tskit.load(os.path.join(wk_dir, "seeds.trees"))
	# Sample nodes
	sampled_inds = _generate_sample_indices(ts, seed_size)
	sampled_tree = ts.simplify(samples = sampled_inds)
	# Node labels from int to strings
	new_labels = {node : str(node) for node in sampled_tree.samples()}
	# Write NWK/VCF
	_write_newick_file(wk_dir, sampled_tree, new_labels)
	_write_vcf_file(wk_dir, sampled_tree, new_labels)

def seed_WF(Ne, seed_size, ref_path, wk_dir, mu, n_gen, rand_seed = None):
	"""
	Burn-in w/ Wright-Fisher model for seed generations and write the VCF/NWK of seeds to working diretory.

	Parameters:
        Ne (int): Effective population size.
        seed_size (int): Number of seeds.
        ref_path (str): Path to the reference genome.
        wk_dir (str): Working directory.
        mu (float): Mutation rate.
        n_gen (int): Number of generations.
		rand_seed (int): Random number generator.
	"""
	
	slim_script = os.path.join(os.path.dirname(__file__), SLIM_DIR, WF_SLIM)
	slim_stdout_path = os.path.join(wk_dir, OUT_SLIM)
	# Run SLiM

	with open(slim_stdout_path, 'w') as fd:
		if rand_seed == None:
			subprocess.run(["slim", "-d", f"Ne={Ne}", "-d", f"ref_path=\"{ref_path}\"", "-d", \
					f"wk_dir=\"{wk_dir}\"", "-d", f"mu={mu}", "-d", f"n_gen={n_gen}", slim_script], stdout=fd)
		else:
			subprocess.run(["slim", "-d", f"Ne={Ne}", "-d", f"ref_path=\"{ref_path}\"", "-d", \
					f"wk_dir=\"{wk_dir}\"", "-d", f"mu={mu}", "-d", f"n_gen={n_gen}", "-d", f"seed={rand_seed}", slim_script], stdout=fd)
	# VCF/NWK
	seeds_treeseq(wk_dir, seed_size)
	split_seedvcf(os.path.join(wk_dir, VCF_NAME), wk_dir, seed_size, "slim")
	# Remove the seeds aggregation VCF because tskit use different indexing for base positions than we and SLiM do.
	os.remove(os.path.join(wk_dir, VCF_NAME))

def seed_epi(wk_dir, seed_size, ref_path, mu, n_gen, host_size, seeded_host_id, S_IE_rate, \
			 E_I_rate=0, E_R_rate=0, latency_prob=0, I_R_rate=0, I_E_rate=0, R_S_rate=0, rand_seed = None):
	"""
	Burn-in w/ an epidemiological model for seed generations and write the VCF/NWK of seeds to working directory.
	Note: The network and all epidemiological parameters must be available for this burn-in method.

	Parameters:
		wk_dir (str): Working directory.
        seed_size (int): Number of seeds.
        ref_path (str): Path to the reference genome.
        mu (float): Mutation rate.
        n_gen (int): Number of generations.
        host_size (int): Total number of hosts in the simulation.
        seeded_host_id (list): List of IDs of initially infected hosts.
        S_IE_rate (float): Rate of transition from susceptible to exposed.
        E_I_rate (float, optional): Rate of transition from exposed to infected.
        E_R_rate (float, optional): Rate of transition from exposed to recovered.
        latency_prob (float, optional): Probability of latency.
        I_R_rate (float, optional): Rate of transition from infected to recovered.
        I_E_rate (float, optional): Rate of transition from infected to exposed.
        R_S_rate (float, optional): Rate of transition from recovered to susceptible.
    """
	if len(seeded_host_id) == 0:
		raise CustomizedError("You need to specify at least one host id (-seeded_host_id) "
						"to be seeded in SLiM epi model burn-in mode")
	elif host_size < len(seeded_host_id):
		raise CustomizedError("You need to specify a host population size (-host_size) "
						"bigger than the size of the seeded hosts in SLiM epi model burn-in mode")
	elif max(seeded_host_id) >= host_size:
		raise CustomizedError("All the host ids to be seeded has to be smaller than host population size")
	elif S_IE_rate <= 0:		
		raise CustomizedError("An infection rate (-S_IE_rate, Susceptible to infected/exposed rate) bigger than 0 needs "
						"to be provided in SLiM epi model burn-in mode")
	elif latency_prob > 0 and E_I_rate == 0 and E_R_rate == 0:
		print("WARNING: You activated an SEIR model, in which exposed compartment exists, "
			"but you doesn't specify any transition from exposed compartment, which will lead "
			"to exposed hosts being locked (never recovered and cannot infect others). Please "
			"make sure this is what you want.")
	elif I_R_rate == 0:
		print("WARNING: You activated a S(E)I model by setting I>R rate = 0, where recovered "
		"component doesn't exists, meaning that all infected hosts never recovered. Please make sure "
		"this is what you want.")
	elif R_S_rate == 0:
		print("WARNING: You activated a S(E)IR model with Recovered individuals are fully immune, "
		"they don't go back to recovered state. This can probably lead to the outbreak ending before "
		"the specified burn-in generation and makes the seeds' sampling fail. Please make sure this "
		"is what you want.")	
	# Remove the trajectory file if it already exists
	trajectory = os.path.join(wk_dir, TRAJ)
	if os.path.exists(trajectory): os.remove(trajectory)

	slim_script = os.join(os.path.dirname(__file__), SLIM_DIR, EPI_SLIM)
	slim_stdout_path = os.path.join(wk_dir, OUT_SLIM)
	# Run SLiM
	with open(slim_stdout_path, 'w') as fd:
		if rand_seed == None:
			subprocess.run(["slim", "-d", f"cwdir=\"{wk_dir}\"", "-d", f"ref_path=\"{ref_path}\"", "-d", \
					f"contact_network_path=\"{os.path.join(wk_dir, "contact_network.adjlist")}\"", "-d", \
						f"host_size={host_size}", "-d", f"mut_rate={mu}", "-d", f"n_generation={n_gen}", "-d", \
						f"seeded_host_id=c({",".join([str(i) for i in seeded_host_id])})", "-d", \
						f"S_IE_rate={S_IE_rate}", "-d", f"E_I_rate={E_I_rate}", "-d", \
						f"E_R_rate={E_R_rate}", "-d", f"latency_prob={latency_prob}", "-d", \
						f"I_R_rate={I_R_rate}", "-d", f"I_E_rate={I_E_rate}", "-d", f"R_S_rate={R_S_rate}", \
						slim_script], stdout=fd)
		else:
			subprocess.run(["slim", "-d", f"cwdir=\"{wk_dir}\"", "-d", f"ref_path=\"{ref_path}\"", "-d", \
					f"contact_network_path=\"{os.path.join(wk_dir, "contact_network.adjlist")}\"", "-d", \
						f"host_size={host_size}", "-d", f"mut_rate={mu}", "-d", f"n_generation={n_gen}", "-d", \
						f"seeded_host_id=c({",".join([str(i) for i in seeded_host_id])})", "-d", \
						f"S_IE_rate={S_IE_rate}", "-d", f"E_I_rate={E_I_rate}", "-d", \
						f"E_R_rate={E_R_rate}", "-d", f"latency_prob={latency_prob}", "-d", \
						f"I_R_rate={I_R_rate}", "-d", f"I_E_rate={I_E_rate}", "-d", f"R_S_rate={R_S_rate}", "-d", \
						f"seed={rand_seed}", slim_script], stdout=fd)


	# VCF/NWK
	seeds_treeseq(wk_dir, seed_size)
	split_seedvcf(os.path.join(wk_dir, VCF_NAME), wk_dir, seed_size, "slim")
	# Remove the seeds aggregation VCF because tskit use different indexing for base positions than we and SLiM do.
	os.remove(os.path.join(wk_dir, VCF_NAME))

def seeds_tree_scaling(tree_path, scale_factor, wk_dir):
	"""
	Checks whether the given phylogeny has a single root; if so, rescale the branch length by {scale_factor}.

	Parameters:
		tree_path (str): Full path to the seeds' phylogeny.
		scale_factor (int/float): Scaling factor of the phylogeny.
		wk_dir: Working directory.
	"""
	# This should be only called after copy_seed_phylo_input, so that tree_path must exists.
	phylo = Tree(tree_path, "newick")
	# Here I am assuming any tree with non-binary in the outer most parenthese are not rooted.
	if len(phylo.children) != 2:
		raise CustomizedError("The phylogeny is not rooted")
	for node in phylo.traverse():
		node.dist *= scale_factor
	
	phylo.write(outfile=os.path.join(wk_dir, "seeds.nwk"))

def run_seed_generation(method, wk_dir, seed_size, seed_vcf="", Ne=0, ref_path="", mu=0, n_gen=0, \
						path_seeds_phylogeny="", host_size=0, seeded_host_id=[], S_IE_rate=0, E_I_rate=0, \
						E_R_rate=0, latency_prob=0, I_R_rate=0, I_E_rate=0, R_S_rate=0, rand_seed = None):
	"""
	Generate seeds's phylogeny and individual VCFs.

	Parameters:
		method (str): Seed generation method, can be burn-in ("SLiM_burnin_WF" or "SLiM_burnin_epi") or user input.
		wk_dir (str): Working directory.
        seed_size (int): Number of seeds.
		seed_vcf (str): Full path to the congregate seeds' VCF.
		Ne (int): Effective population size.
        ref_path (str): Path to the reference genome.
        mu (float): Mutation rate.
        n_gen (int): Number of generations.
		path_seeds_phylogeny (str): Full path to the seeds' phylogeny VCF.
        host_size (int): Total number of hosts in the simulation.
        seeded_host_id (list[int]): List of IDs of initially infected hosts.
        S_IE_rate (float): Rate of transition from susceptible to exposed.
        E_I_rate (float, optional): Rate of transition from exposed to infected.
        E_R_rate (float, optional): Rate of transition from exposed to recovered.
        latency_prob (float, optional): Probability of latency.
        I_R_rate (float, optional): Rate of transition from infected to recovered.
        I_E_rate (float, optional): Rate of transition from infected to exposed.
        R_S_rate (float, optional): Rate of transition from recovered to susceptible.

		Returns:
			error_message (str): Error message.
    """
	if rand_seed != None:
		np.random.seed(rand_seed)
	error_message = None
	try:	
		if not os.path.exists(wk_dir):
			raise CustomizedError(f"The provided working ({wk_dir}) doesn't exist")
		# User input
		if method == "user_input":
			seed_userinput(seed_vcf, seed_size, wk_dir, path_seeds_phylogeny)
		elif method == "SLiM_burnin_WF" or method == "SLiM_burnin_epi": # assuming SLiM burn-in (currently just WF and epi), checking violation of parameters for all SLiM burn-in
			if Ne <= 0: 
				raise CustomizedError("You need to specify an effective population size (-Ne) "
						f"bigger than 0 instead of {Ne} in SLiM WF burn-in mode")
			if ref_path == "":
				raise CustomizedError("You need to specify a path to the reference genome "
						"(-ref_path) in SLiM burn-in mode")
			elif not os.path.exists(ref_path):
				raise FileNotFoundError(f"The path to the reference genome {ref_path} provided doesn't exist")
			if mu <= 0:
				raise CustomizedError("You need to specify a mutation rate (-mu) bigger than 0 "
						f"instead of {mu} in SLiM burn-in mode")
			if n_gen <= 0:
				raise CustomizedError("You need to specify a burn-in generation (-n_gen) bigger than 0 "
						f"instead of {n_gen} in SLiM burn-in mode")
			if method == "SLiM_burnin_WF":
				seed_WF(Ne, seed_size, ref_path, wk_dir, mu, n_gen)
			else:
				seed_epi(wk_dir, seed_size, ref_path, mu, n_gen, host_size, seeded_host_id, S_IE_rate, \
				E_I_rate, E_R_rate, latency_prob, I_R_rate, I_E_rate, R_S_rate)
		else: # the given method is invalid
			raise CustomizedError(f"{method} isn't a valid method. Please provide a permitted method. "
							"(user_input/SLiM_burnin_WF/SLiM_burnin_epi)")
		print("******************************************************************** \n" +
				"                   	    SEEDS GENERATED		                        \n" +
				"******************************************************************** \n")
	except Exception as e:
		print(f"Seed sequences generation - A error occured: {e}.")
		error_message = e
	
	return error_message


def seeds_generation_byconfig(all_config):
	"""
	Generate seed sequences and phylogenies given the configuration file.

	Parameters:
		file_path (str): Full path to the configuration file.
	"""
	# Read parameters
	# all_config = read_params(file_path, "base_params.json")
	seeds_config = all_config["SeedsConfiguration"]

	# reference then pass the function
	refer = seeds_config["use_reference"]
	if refer: # do nothing
		pass
	wk_dir = all_config["BasicRunConfiguration"]["cwdir"]
	method = seeds_config["method"]
	seed_size = seeds_config["seed_size"]
	seed_vcf = seeds_config["user_input"]["path_seeds_vcf"]
	path_seeds_phylogeny = seeds_config["user_input"]["path_seeds_phylogeny"]
	Ne = seeds_config["SLiM_burnin_WF"]["burn_in_Ne"]
	ref_path = all_config["GenomeElement"]["ref_path"]
	if method== "user_input":
		n_gen = 0
	n_gen = seeds_config[method]["burn_in_generations"]
	mu = seeds_config[method]["burn_in_mutrate"]

	host_size = all_config["NetworkModelParameters"]["host_size"]
	seeded_host_id = seeds_config["SLiM_burnin_epi"]["seeded_host_id"]
	S_IE_rate = seeds_config["SLiM_burnin_epi"]["S_IE_rate"]
	E_I_rate = seeds_config["SLiM_burnin_epi"]["E_I_rate"]
	E_R_rate = seeds_config["SLiM_burnin_epi"]["E_R_rate"]
	latency_prob = seeds_config["SLiM_burnin_epi"]["latency_prob"]
	I_R_rate = seeds_config["SLiM_burnin_epi"]["I_R_rate"]
	I_E_rate = seeds_config["SLiM_burnin_epi"]["I_E_rate"]
	R_S_rate = seeds_config["SLiM_burnin_epi"]["R_S_rate"]
	random_number_seed = all_config["BasicRunConfiguration"].get("random_number_seed", None)

	# Run simulation for seed generation
	error = run_seed_generation(method=method, wk_dir=wk_dir, seed_size=seed_size, seed_vcf=seed_vcf, Ne=Ne, \
					 	ref_path=ref_path, mu=mu, n_gen=n_gen, path_seeds_phylogeny=path_seeds_phylogeny, \
						host_size=host_size, seeded_host_id=seeded_host_id, S_IE_rate=S_IE_rate, \
						E_I_rate=E_I_rate, E_R_rate=E_R_rate, latency_prob=latency_prob, 
						I_R_rate=I_R_rate, I_E_rate=I_E_rate, R_S_rate=R_S_rate, rand_seed = random_number_seed)
	return error

def main():
	parser = argparse.ArgumentParser(description='Generate or modify seeds.')
	parser.add_argument('-method', action='store',dest='method', type=str, required=True, help="Method of the seed generation")
	parser.add_argument('-wkdir', action='store',dest='wkdir', type=str, required=True, help="Working directory")
	parser.add_argument('-seed_size', action='store',dest='seed_size', type=int, required=True, help="How many seeds is required")
	parser.add_argument('-seed_vcf', action='store',dest='seed_vcf', type=str, required=False, help="Path to the user-provided seeds' vcf", default="")
	parser.add_argument('-Ne', action='store',dest='Ne', type=int, required=False, help="Ne for a WF model, required in WF burn-in mode", default=0)
	parser.add_argument('-ref_path', action='store',dest='ref_path', type=str, required=False, help="Reference genome path, required in SLiM burn-in", default="")
	parser.add_argument('-mu', action='store',dest='mu', type=float, required=False, help="Mutation rate, required in SLiM burn-in", default=0)
	parser.add_argument('-n_gen', action='store',dest='n_gen', type=int, required=False, help="Number of generations of the burn-in process, required in SLiM burn-in", default=0)
	parser.add_argument('-path_seeds_phylogeny', action='store',dest='path_seeds_phylogeny', type=str, required=False, help="Phylogeny of the provided seeds", default="")
	parser.add_argument('-host_size', action='store',dest='host_size', type=int, required=False, help="Size of the host population", default=0)
	parser.add_argument('-seeded_host_id','--seeded_host_id', nargs='+', help='IDs of the host(s) that are seeded', required=False, type=int, default=[])
	parser.add_argument('-S_IE_rate', action='store',dest='S_IE_rate', type=float, required=False, help="Probability of transmission for each contact pair per generation", default=0)
	parser.add_argument('-E_I_rate', action='store',dest='E_I_rate', type=float, required=False, help="Probability of activation (E>I) for each infected host per generation", default=0)
	parser.add_argument('-E_R_rate', action='store',dest='E_R_rate', type=float, required=False, help="Probability of recovery (E>R) for each exposed host per generation", default=0)
	parser.add_argument('-latency_prob', action='store',dest='latency_prob', type=float, required=False, help="Probability of being a latent infection per infection event", default=0)
	parser.add_argument('-I_R_rate', action='store',dest='I_R_rate', type=float, required=False, help="Probability of recovery (I>R) for each infected host per generation", default=0)
	parser.add_argument('-I_E_rate', action='store',dest='I_E_rate', type=float, required=False, help="Probability of deactivation (I>E) for each infected host per generation", default=0)
	parser.add_argument('-R_S_rate', action='store',dest='R_S_rate', type=float, required=False, help="Probability of immunity loss (R>S) for each recovered host per generation", default=0)
	parser.add_argument('-random_seed', action = 'store', dest = 'random_seed', required = False, type = int, default = None)



	args = parser.parse_args()

	method = args.method
	wk_dir = args.wkdir
	seed_size = args.seed_size
	seed_vcf = args.seed_vcf
	Ne = args.Ne
	ref_path = args.ref_path
	mu = args.mu
	n_gen = args.n_gen
	path_seeds_phylogeny = args.path_seeds_phylogeny
	host_size = args.host_size
	seeded_host_id = args.seeded_host_id
	S_IE_rate = args.S_IE_rate
	E_I_rate = args.E_I_rate
	E_R_rate = args.E_R_rate
	latency_prob = args.latency_prob
	I_R_rate = args.I_R_rate
	I_E_rate = args.I_E_rate
	R_S_rate = args.R_S_rate
	rand_seed = args.random_seed


	run_seed_generation(method=method, wk_dir=wk_dir, seed_size=seed_size, seed_vcf=seed_vcf, Ne=Ne, \
					ref_path=ref_path, mu=mu, n_gen=n_gen, path_seeds_phylogeny=path_seeds_phylogeny, \
					host_size=host_size, seeded_host_id=seeded_host_id, S_IE_rate=S_IE_rate, \
					E_I_rate=E_I_rate, E_R_rate=E_R_rate, latency_prob=latency_prob, I_R_rate=I_R_rate, \
					I_E_rate=I_E_rate, R_S_rate=R_S_rate, rand_seed = rand_seed)


if __name__ == "__main__":
    main()


