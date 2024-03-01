import os
import shutil
import inspect
import subprocess
#from multiprocessing import Pool

import tskit
import pyslim


from base_func import *
from post_simulation_func import *


def writebinary(v):
	if v:
		return("T")
	else:
		return("")

def append_files(file1_path, file2_path):
	## Append file1 to file2
    with open(file1_path, 'r') as file1:
        with open(file2_path, 'a') as file2:
            shutil.copyfileobj(file1, file2)

def create_slimconfig(all_config):
	### A function to create a SLiM-readable config file that includes the SLiM-needed parameters from the big config file
	## Input: all_config: dictionary of the big config file, read by read_config()
	## Output: A one-layer dictionary for all the parameters in SLiM
	print("********************************************************************")
	print("                    CHECKING THE CONFIGURATION")
	print("********************************************************************")

	print("Checking \"BasicRunConfiguration\"...... ")
	slim_pars = {}
	slim_pars["cwdir"] = all_config["BasicRunConfiguration"]["cwdir"]
	if os.path.exists(slim_pars["cwdir"])== False:
		raise Exception(f"The working directory specified {slim_pars["cwdir"]} doesn't exist.")
	else:
		out_config = open(os.path.join(all_config["BasicRunConfiguration"]["cwdir"], "slim.params"), "w")
		out_config.write("cwdir:" + slim_pars["cwdir"] + "\n")

		slim_pars["n_replicates"] = all_config["BasicRunConfiguration"]["n_replicates"]
		if slim_pars["n_replicates"].is_integer()==False:
			raise Exception("Number of replicates (\"n_replicates\") has to be an integer")
		else:
			if int(slim_pars["n_replicates"]) < 1:
				raise Exception("You have to at least run one replicate (\"n_replicates\").")
			else:
				out_config.write("n_replicates:" + str(slim_pars["n_replicates"]) + "\n")
		print("\"BasicRunConfiguration\" checked.")

		print("Checking \"EvolutionModel\"...... ")
		slim_pars["n_generation"] = all_config["EvolutionModel"]["n_generation"]
		if slim_pars["n_generation"].is_integer()==False:
			raise Exception("Number of ticks (\"n_generation\") has to be an integer")
		else:
			if int(slim_pars["n_generation"]) < 1:
				raise Exception("You have to at least run 1 tick (\"n_generation\") (and still not recommended).")
			else:
				out_config.write("n_generation:" + str(slim_pars["n_generation"]) + "\n")
		
		slim_pars["mut_rate"] = all_config["EvolutionModel"]["mut_rate"]
		if type(slim_pars["mut_rate"])!=float:
			raise Exception("Mutation rate (\"mut_rate\") has to be a float number.")
		else:
			out_config.write("mut_rate:" + str(slim_pars["mut_rate"]) + "\n")

		slim_pars["trans_type"] = all_config["EvolutionModel"]["trans_type"]
		if slim_pars["trans_type"] not in ["additive", "bialleleic"]:
			raise Exception("Model for transmissibility (\"trans_type\") has to be one of the two models: additive / bialleleic.")
		else:
			out_config.write("trans_type:" + slim_pars["trans_type"] + "\n")

		slim_pars["dr_type"] = all_config["EvolutionModel"]["dr_type"]
		if slim_pars["dr_type"] not in ["additive", "bialleleic"]:
			raise Exception("Model for drug-resistance (\"dr_type\") has to be one of the two models: additive / bialleleic.")
		else:
			out_config.write("dr_type:" + slim_pars["dr_type"] + "\n")

		slim_pars["within_host_reproduction"] = all_config["EvolutionModel"]["within_host_reproduction"]
		if type(slim_pars["within_host_reproduction"])!=bool:
			raise Exception("Please specify \"true\" or \"false\" for within-host reproduction (\"within_host_reproduction\").")
		else:
			out_config.write("within_host_reproduction:" + writebinary(slim_pars["within_host_reproduction"]) + "\n")
		
		slim_pars["cap_withinhost"] = all_config["EvolutionModel"]["cap_withinhost"]
		if slim_pars["cap_withinhost"].is_integer()==False:
			raise Exception("Capacity within host (\"cap_withinhost\") has to be an integer")
		elif slim_pars["within_host_reproduction"]:
			if slim_pars["cap_withinhost"] < 1:
				raise Exception("Capacity within host (\"cap_withinhost\") has to be at least 1")
			elif slim_pars["cap_withinhost"] == 1:
				print("WARNING: Within-host reproduction is turned on, but the capacity within-host is 1, which will be no different from within-host evolution being turned off.")
				out_config.write("cap_withinhost:" + str(slim_pars["cap_withinhost"]) + "\n")
			else:
				out_config.write("cap_withinhost:" + str(slim_pars["cap_withinhost"]) + "\n")
			slim_pars["within_host_reproduction_rate"] = all_config["EvolutionModel"]["within_host_reproduction_rate"]
			if type(slim_pars["within_host_reproduction_rate"])!=float:
				raise Exception("Within-host reproduction probability (\"within_host_reproduction_rate\") has to be a float number.")
			elif slim_pars["within_host_reproduction_rate"]<=0 or slim_pars["within_host_reproduction_rate"]>1:
				raise Exception("Within-host reproduction probability (\"within_host_reproduction_rate\") should be between 0 and 1.")
			else:
				out_config.write("within_host_reproduction_rate:" + str(slim_pars["within_host_reproduction_rate"]) + "\n")
		else:
			out_config.write("cap_withinhost:" + str(slim_pars["cap_withinhost"]) + "\n")
		print("\"EvolutionModel\" Checked. ")

		print("Checking \"SeedsConfiguration\"...... ")
		slim_pars["seed_size"] = all_config["SeedsConfiguration"]["seed_size"]
		if slim_pars["seed_size"].is_integer()==False:
			raise Exception("Number of seeds (\"seed_size\") has to be an integer")
		elif slim_pars["seed_size"] < 1:
			raise Exception("Number of seeds (\"seed_size\") has to be at least 1")
		else:
			out_config.write("seed_size:" + str(slim_pars["seed_size"]) + "\n")
		slim_pars["use_reference"] = all_config["SeedsConfiguration"]["use_reference"]
		if type(slim_pars["use_reference"])!=bool:
			raise Exception("Please specify \"true\" or \"false\" for using reference genome for seeds (\"use_reference\").")
		else:
			out_config.write("use_genetic_model:" + writebinary(slim_pars["use_reference"]) + "\n")

		if slim_pars["use_reference"]==False:
			if os.path.exists(os.path.join(slim_pars["cwdir"], "originalvcfs"))==False:
				raise Exception("Reference genome isn't used for seed sequences, but SeedGenerator hasn't been run. Please run SeedGenerator before running this program or specify use_reference=true.")
		if os.path.exists(os.path.join(slim_pars["cwdir"], "seed_host_match.csv"))==False:
			raise Exception("HostSeedMatcher hasn't been run. Please run HostSeedMatcher before running this program.")
		else:
			slim_pars["seed_host_matching_path"] = os.path.join(slim_pars["cwdir"], "seed_host_match.csv")
			out_config.write("seed_host_matching_path:" + slim_pars["seed_host_matching_path"] + "\n")
		print("\"SeedsConfiguration\" Checked. ")
		
		print("Checking \"GenomeElement\"...... ")
		slim_pars["ref_path"] = all_config["GenomeElement"]["ref_path"]
		if os.path.exists(slim_pars["ref_path"])==False:
			raise Exception("The provided reference genome path doesn't exist.")
		else:
			out_config.write("ref_path:" + slim_pars["ref_path"] + "\n")
		slim_pars["use_genetic_model"] = all_config["GenomeElement"]["use_genetic_model"]
		if type(slim_pars["use_genetic_model"])!=bool:
			raise Exception("Please specify \"true\" or \"false\" for whether to use a genetic model (\"use_genetic_model\").")
		elif slim_pars["use_genetic_model"]:
			if os.path.exists(os.path.join(slim_pars["cwdir"], "causal_gene_info.csv"))==False:
				raise Exception("Genetic model for trait is used, but GeneticElementGenerator hasn't been run. Please run GeneticElementGenerator before running this program.")
			else:
				out_config.write("causal_gene_path:" + os.path.join(slim_pars["cwdir"], "causal_gene_info.csv") + "\n")
		else:
			out_config.write("causal_gene_path:" + "\n")
		out_config.write("use_genetic_model:" + writebinary(slim_pars["use_genetic_model"]) + "\n")
		if type(all_config["GenomeElement"]["traits_num"])!=list:
			raise Exception("Number of traits (\"traits_num\") has to be a list [] of length 2.")
		elif len(all_config["GenomeElement"]["traits_num"])!=2:
			raise Exception("Number of traits (\"traits_num\") has to be a list [] of length 2, showing number of effect size sets (traits) for transmissibility and drug-resistance.")
		elif any([type(i) != int for i in all_config["GenomeElement"]["traits_num"]]):
			raise Exception("Number of traits (\"traits_num\") has to be a list [] of ints.")
		print("\"GenomeElement\" Checked. ")

		print("Checking \"NetworkModelParameters\"...... ")
		slim_pars["use_network_model"] = all_config["NetworkModelParameters"]["use_network_model"]
		if type(slim_pars["use_network_model"])!=bool:
			raise Exception("Please specify \"true\" for whether to use the network model (\"use_network_model\").")
		elif slim_pars["use_network_model"]==False:
			raise Exception("Please specify \"true\" for whether to use the network model (\"use_network_model\").")
		else:
			out_config.write("use_network_model:" + writebinary(slim_pars["use_network_model"]) + "\n")
			slim_pars["host_size"] = all_config["NetworkModelParameters"]["host_size"]
			if slim_pars["host_size"].is_integer()==False:
				raise Exception("Number of seeds (\"host_size\") has to be an integer")
			elif slim_pars["host_size"] < 1:
				raise Exception("Number of hosts (\"host_size\") has to be at least 1")
			else:
				if os.path.exists(os.path.join(slim_pars["cwdir"], "contact_network.adjlist"))==False:
					raise Exception("NetworkGenerator hasn't been run. Please run NetworkGenerator before running this program.")
				else:
					out_config.write("contact_network_path:" + os.path.join(slim_pars["cwdir"], "contact_network.adjlist") + "\n")
				out_config.write("host_size:" + str(slim_pars["host_size"]) + "\n")
		print("\"NetworkModelParameters\" Checked. ")
			
		print("Checking \"EpidemiologyModel\"...... ")
		slim_pars["epi_model"] = all_config["EpidemiologyModel"]["model"]
		if slim_pars["epi_model"] not in ["SIR", "SEIR"]:
			raise Exception("Compartmental model (\"model\") has to be SIR or SEIR.")
		out_config.write("epi_model:" + slim_pars["epi_model"] + "\n")
		slim_pars["n_epoch"] = all_config["EpidemiologyModel"]["epoch_changing"]["n_epoch"]
		if slim_pars["n_epoch"].is_integer()==False:
			raise Exception("Number of epochs (\"n_epoch\") has to be an integer")
		elif slim_pars["n_epoch"] < 1:
			raise Exception("Number of epochs (\"n_epoch\") has to be at least 1")

		out_config.write("n_epoch:" + str(slim_pars["n_epoch"]) + "\n")
		if slim_pars["n_epoch"]>1:
			slim_pars["epoch_changing_generation"] = all_config["EpidemiologyModel"]["epoch_changing"]["epoch_changing_generation"]
			if type(slim_pars["epoch_changing_generation"])!=list:
				raise Exception("Ticks to change epochs (\"epoch_changing_generation\") has to be a list [].")
			elif len(slim_pars["epoch_changing_generation"])!=slim_pars["n_epoch"]-1:
				raise Exception("Ticks to change epochs (\"epoch_changing_generation\") has to have length of the number of epochs - 1.")
			elif any([i>slim_pars["n_generation"] or i<1 for i in slim_pars["epoch_changing_generation"]]):
				raise Exception(f"Ticks to change epoch (\"massive_sample_generation\") has to in a tick that is valid (1..{slim_pars["n_generation"]}).")
			else:
				out_config.write("epoch_changing_generation:" + ",".join([str(x) for x in slim_pars["epoch_changing_generation"]]) + "\n")

		slim_pars["transmissibility_effsize"] = all_config["EpidemiologyModel"]["genetic_architecture"]["transmissibility"]
		slim_pars["cap_transmissibility"] = all_config["EpidemiologyModel"]["genetic_architecture"]["cap_transmissibility"]
		slim_pars["drugresistance_effsize"] = all_config["EpidemiologyModel"]["genetic_architecture"]["drug_resistance"]
		slim_pars["cap_drugresist"] = all_config["EpidemiologyModel"]["genetic_architecture"]["cap_drugresist"]
		slim_pars["S_IE_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["S_IE_rate"]
		slim_pars["I_R_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["I_R_rate"]
		slim_pars["R_S_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["R_S_rate"]
		slim_pars["latency_prob"] = all_config["EpidemiologyModel"]["transiton_rate"]["latency_prob"]
		slim_pars["E_I_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["E_I_rate"]
		slim_pars["I_E_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["I_E_rate"]
		slim_pars["E_R_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["E_R_rate"]
		slim_pars["sample_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["sample_rate"]
		slim_pars["recovery_prob_after_sampling"] = all_config["EpidemiologyModel"]["transiton_rate"]["recovery_prob_after_sampling"]

		for param in ["S_IE_rate", "I_R_rate", "R_S_rate", "latency_prob", "E_I_rate", "I_E_rate", "E_R_rate", "sample_rate", "recovery_prob_after_sampling"]:
			if type(slim_pars[param])!=list:
				raise Exception(f"(\"{param}\") has to be a list [].")
			elif len(slim_pars[param])!=slim_pars["n_epoch"]:
				raise Exception("Ticks to change epochs (\"epoch_changing_generation\") has to have length of the number of epochs.")
			elif any([type(i) not in [float, int] for i in slim_pars[param]]):
				raise Exception(f"The probability of event (\"{param}\") has to be a list of floats")
			elif any([i>1 or i<0 for i in slim_pars[param]]):
				raise Exception(f"(\"{param}\") has to be a list of probability, thus between 0 and 1.")
			else:
				out_config.write(param + ":" + ",".join([str(x) for x in slim_pars[param]]) + "\n")

		for param in ["cap_transmissibility", "cap_drugresist"]:
			if type(slim_pars[param])!=list:
				raise Exception(f"(\"{param}\") has to be a list [].")
			elif len(slim_pars[param])!=slim_pars["n_epoch"]:
				raise Exception(f"Cap of the trait value for each epoch (\"{param}\") has to have length of the number of epochs.")
			elif any([type(i) not in [float, int] for i in slim_pars[param]]):
				raise Exception(f"Cap of the trait value for each epoch (\"{param}\") has to be a list of numerical values")
			else:
				out_config.write(param + ":" + ",".join([str(x) for x in slim_pars[param]]) + "\n")

		for param in ["transmissibility_effsize", "drugresistance_effsize"]:
			if type(slim_pars[param])!=list:
				raise Exception(f"(\"{param}\") has to be a list [].")
			elif len(slim_pars[param])!=slim_pars["n_epoch"]:
				raise Exception(f"The effect size set being used in each epoch (\"{param}\") has to have length of the number of epochs.")
			elif any([type(i) != int for i in slim_pars[param]]):
				raise Exception(f"The effect size set being used in each epoch (\"{param}\") has to be a list of integer")
			else:
				out_config.write(param + ":" + ",".join([str(x) for x in slim_pars[param]]) + "\n")
		if any([i>all_config["GenomeElement"]["traits_num"][0] for i in slim_pars["transmissibility_effsize"]]):
			raise Exception(f"(\"transmissibility_effsize\") has to be chosen from {list(range(all_config["GenomeElement"]["traits_num"][0]))}.")
		if any([i>all_config["GenomeElement"]["traits_num"][1]for i in slim_pars["drugresistance_effsize"]]):
			raise Exception(f"(\"drugresistance_effsize\") has to be chosen from {list(range(all_config["GenomeElement"]["traits_num"][1]))}.")
		

		slim_pars["n_massive_sample"] = all_config["EpidemiologyModel"]["massive_sampling"]["event_num"]
		if slim_pars["n_massive_sample"].is_integer()==False:
			raise Exception("Number of massive sampling events (\"n_massive_sample\") has to be an integer")
		out_config.write("n_massive_sample:" + str(slim_pars["n_massive_sample"]) + "\n")
		if slim_pars["n_massive_sample"]>0:
			slim_pars["massive_sample_generation"] = all_config["EpidemiologyModel"]["massive_sampling"]["generation"]
			if type(slim_pars["massive_sample_generation"])!=list:
				raise Exception("Ticks to do massive sampling (\"massive_sample_generation\") has to be a list [].")
			elif len(slim_pars["massive_sample_generation"])!=slim_pars["n_massive_sample"]:
				raise Exception("Ticks to do massive sampling (\"massive_sample_generation\") has to have length of the number of massive sampling events.")
			elif any([i>slim_pars["n_generation"] or i<1 for i in slim_pars["massive_sample_generation"]]):
				raise Exception(f"Ticks to do massive sampling (\"massive_sample_generation\") has to in a tick that is valid (1..{slim_pars["n_generation"]}).")
			else:
				out_config.write("massive_sample_generation:" + ",".join([str(x) for x in slim_pars["massive_sample_generation"]]) + "\n")
			slim_pars["massive_sample_prob"] = all_config["EpidemiologyModel"]["massive_sampling"]["sampling_prob"]
			slim_pars["massive_sample_recover_prob"] = all_config["EpidemiologyModel"]["massive_sampling"]["recovery_prob_after_sampling"]
			for param in ["massive_sample_prob", "massive_sample_recover_prob"]:
				if type(slim_pars[param])!=list:
					raise Exception(f"(\"{param}\") has to be a list [].")
				elif len(slim_pars[param])!=slim_pars["n_massive_sample"]:
					raise Exception(f"The probability (\"{param}\") for each massive sampling event has to have length of the number of massive sampling events.")
				elif any([type(i) not in [float, int] for i in slim_pars[param]]):
					raise Exception(f"The probability (\"{param}\")  for each massive sampling event has to be a list of floats")
				elif any([i>1 or i<0 for i in slim_pars[param]]):
					raise Exception(f"(\"{param}\") has to be a list of probability, thus between 0 and 1.")
				else:
					out_config.write(param + ":" + ",".join([str(x) for x in slim_pars[param]]) + "\n")
			
		slim_pars["super_infection"] = all_config["EpidemiologyModel"]["super_infection"]
		if type(slim_pars["super_infection"])!=bool:
			raise Exception("Please specify \"true\" or \"false\" for super-infection (\"super_infection\").")
		else:
			out_config.write("super_infection:" + writebinary(slim_pars["n_massive_sample"]) + "\n")
			if slim_pars["super_infection"] and slim_pars["cap_withinhost"]==1:
				print("WARNING: Though super-infection is activated, you specified the capacity within-host being only 1, thus super-infection actually cannot happen.l")
		print("\"EpidemiologyModel\" Checked. ")
		
		
		print("Checking \"Postprocessing_options\"...... ")
		if type(all_config["Postprocessing_options"]["do_postprocess"])!=bool:
			raise Exception("Please specify \"true\" or \"false\" for whether to do postprocessing (\"do_postprocess\").")
		elif all_config["Postprocessing_options"]["do_postprocess"]:
			post_processing_config = all_config["Postprocessing_options"]
			post_processing_config["n_trait"] = all_config["GenomeElement"]["traits_num"]
			print("Post-simulation data processing will be done.")
			if type(post_processing_config["tree_plotting"]["branch_color_trait"])!=int:
				raise Exception("How to color the branches of the tree (branch_color_trait) should be an integer.")
			elif post_processing_config["tree_plotting"]["branch_color_trait"]<0 or post_processing_config["tree_plotting"]["branch_color_trait"]>sum(post_processing_config["n_trait"]):
				raise Exception(f"How to color the branches of the tree (branch_color_trait) should be an integer chosen from (0: color by seed, 1..{sum(post_processing_config["n_trait"])}: trait id.")
			else:
				if post_processing_config["tree_plotting"]["branch_color_trait"]==0:
					print("The tree will be colored by which seed is its ancestor")
				else:
					print(f"The tree will be colored by its trait {post_processing_config["tree_plotting"]["branch_color_trait"]}")
		else:
			print("Post-simulation data processing won't be done.")
			post_processing_config = {}
		print("\"Postprocessing_options\" Checked. ")
		

	return(slim_pars, post_processing_config)





def create_slimscript(slim_pars):
	### A function that create a SLiM script in the working directory according to the config
	### The script should take in SLiM config file and the current output directory (related to n_replicates) as parameters
	### No return value

	print("********************************************************************")
	print("                       CREATING SLIM SCRIPT")
	print("********************************************************************")
	
	code_path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "slim_scripts")
	mainslim_path = os.path.join(slim_pars["cwdir"], "simulation.slim")

	if os.path.exists(mainslim_path):
		os.remove(mainslim_path)

	## Create a slim file in working directory
	f = open(mainslim_path, "w")
	f.close()

	## Get trait calculation functions ready
	append_files(os.path.join(code_path, "trait_calc_function.slim"), mainslim_path)

	## Initialization
	append_files(os.path.join(code_path, "initialization_pt1.slim"), mainslim_path)
	append_files(os.path.join(code_path, "read_config.slim"), mainslim_path)
	append_files(os.path.join(code_path, "initialization_pt2.slim"), mainslim_path)
	if slim_pars["use_genetic_model"]:
		append_files(os.path.join(code_path, "genomic_element_init_effsize.slim"), mainslim_path)
	else:
		append_files(os.path.join(code_path, "genomic_element_init.slim"), mainslim_path)
	append_files(os.path.join(code_path, "initialization_pt3.slim"), mainslim_path)

	## Mutation block (for m1)
	if slim_pars["use_genetic_model"]:
		append_files(os.path.join(code_path, "mutation_effsize.slim"), mainslim_path)

	## Block control 1first()
	append_files(os.path.join(code_path, "block_control.slim"), mainslim_path)

	## Seed's read in and network read in
	if slim_pars["use_network_model"]:
		if slim_pars["use_reference"]:
			append_files(os.path.join(code_path, "seeds_read_in_noburnin.slim"), mainslim_path)
		else:
			append_files(os.path.join(code_path, "seeds_read_in_network.slim"), mainslim_path)
		append_files(os.path.join(code_path, "contact_network_read_in.slim"), mainslim_path)

	## Epoch changing
	if slim_pars["n_epoch"]>1:
		append_files(os.path.join(code_path, "change_epoch.slim"), mainslim_path)

	## Self reproduction
	append_files(os.path.join(code_path, "self_reproduce.slim"), mainslim_path)

	## Transmission reproduction
	if slim_pars["use_genetic_model"] == False:
		append_files(os.path.join(code_path, "transmission_nogenetic.slim"), mainslim_path)
	else:
		if slim_pars["trans_type"]=="additive":
			append_files(os.path.join(code_path, "transmission_additive.slim"), mainslim_path)
		elif slim_pars["trans_type"]=="bialleleic":
			append_files(os.path.join(code_path, "transmission_bialleleic.slim"), mainslim_path)
		if any(idx == 0 for idx in slim_pars["transmissibility_effsize"]):
			append_files(os.path.join(code_path, "transmission_nogenetic.slim"), mainslim_path)

	## Within-host reproduction
	if slim_pars["within_host_reproduction"]:
		append_files(os.path.join(code_path, "within_host_reproduce.slim"), mainslim_path)

	## Kill old pathogens
	append_files(os.path.join(code_path, "kill_old_pathogens.slim"), mainslim_path)

	## State transition for exposed hosts
	if slim_pars["epi_model"]=="SEIR":
		append_files(os.path.join(code_path, "Exposed_process.slim"), mainslim_path)

	## State transition for infected hosts
	if any(idx != 0 for idx in slim_pars["drugresistance_effsize"]):
		if slim_pars["trans_type"] == "additive":
			append_files(os.path.join(code_path, "Infected_process_additive.slim"), mainslim_path)
		elif slim_pars["trans_type"] == "bialleleic":
			append_files(os.path.join(code_path, "Infected_process_additive.slim"), mainslim_path)
	if any(idx == 0 for idx in slim_pars["drugresistance_effsize"]):
		append_files(os.path.join(code_path, "Infected_process_nogenetic.slim"), mainslim_path)

	## Massive sampling events
	if slim_pars["n_massive_sample"] > 0:
		append_files(os.path.join(code_path, "massive_sampling.slim"), mainslim_path)

	## New infections
	if slim_pars["super_infection"] == False:
		append_files(os.path.join(code_path, "New_infection_process.slim"), mainslim_path)
	else:
		append_files(os.path.join(code_path, "New_infection_process_superinfection.slim"), mainslim_path)

	## Recovered individuals
	if any(rate != 0 for rate in slim_pars["R_S_rate"]):
		append_files(os.path.join(code_path, "Recovered_process.slim"), mainslim_path)

	## Logging all things
	append_files(os.path.join(code_path, "log.slim"), mainslim_path)

	## Finish simulation
	append_files(os.path.join(code_path, "finish_simulation.slim"), mainslim_path)



	return(0)


def run_per_slim_simulation(slim_config_path, wk_dir, runid):
	### A function that run the SLiM script generated by create_slimscript().
	### It creates subfolders in the working directory and run them (in parallel ideally).
	### And run post data processing for each folder.
	### No return value
	#slim_config_path, wk_dir, runid = tuple_arg
	output_path = os.path.join(wk_dir, str(runid))
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	else:
		shutil.rmtree(output_path)           # Removes all the subdirectories!
		os.makedirs(output_path)

	script_path = os.path.join(wk_dir, "simulation.slim")
	slim_stdout_path = os.path.join(output_path, "slim.stdout")
	with open(slim_stdout_path, 'w') as fd:
		subprocess.run(["slim", "-d", f"config_path=\"{slim_config_path}\"", "-d", f"runid={runid}", script_path], stdout=fd)
	return(0)


def all_slim_simulation_by_config(all_config):
	### A function that run the SLiM script generated by create_slimscript().
	### It creates subfolders in the working directory and run them (in parallel ideally).
	### And run post data processing for each folder.
	### No return value
	slim_pars, dataprocess_pars = create_slimconfig(all_config)
	create_slimscript(slim_pars)
	wk_dir = slim_pars["cwdir"]
	run_all_slim_simulation(slim_config_path = os.path.join(wk_dir, "slim.params"), slim_pars = slim_pars, dataprocess_pars=dataprocess_pars)
	

def run_all_slim_simulation(slim_config_path="", slim_pars={}, dataprocess_pars={}):
	## Not parallel for now (sequentially)
	if slim_config_path=="":
		slim_config_path = os.path.join(slim_pars["cwdir"], "slim.params")

	run_check = True



	if run_check:
		print("********************************************************************")
		print("                     RUNNING THE SIMULATION")
		print("********************************************************************")
		run_success = []
		for runid in range(1,slim_pars["n_replicates"] + 1):
			print(f"Running simulation for replication {runid}......")
			run_per_slim_simulation(slim_config_path, slim_pars["cwdir"], runid)
			print(f"Replication {runid} simulation finished.")
			if os.path.exists(os.path.join(slim_pars["cwdir"], str(runid), "sampled_genomes.trees")):
				if len(dataprocess_pars) > 0:
					each_wkdir = os.path.join(slim_pars["cwdir"], str(runid))
					print(f"Processing replication {runid} treesequence file...")
					run_per_data_processing(slim_pars["cwdir"], slim_pars["use_genetic_model"], runid, dataprocess_pars["n_trait"], slim_pars["seed_host_matching_path"], dataprocess_pars["tree_plotting"]["branch_color_trait"])
					if slim_pars["use_reference"]:
						seed_phylo = ""
					else:
						seed_phylo = os.path.join(slim_pars["cwdir"], "seeds.nwk")
					print(f"Plotting transmission tree for replication {runid}...")
					plot_per_transmission_tree(each_wkdir, slim_pars["seed_size"], slim_config_path, dataprocess_pars["n_trait"], seed_phylo)
					print(f"Plotting strain distribution trajectory for replication {runid}...")
					plot_strain_distribution_trajectory(each_wkdir, slim_pars["seed_size"], slim_pars["n_generation"])
					print(f"Plotting SEIR trajectory for replication {runid}...")
					if os.path.exists(os.path.join(each_wkdir, "SEIR_trajectory.csv.gz")):
						plot_SEIR_trajectory(each_wkdir, slim_pars["seed_size"], slim_pars["host_size"], slim_pars["n_generation"])
						run_success.append(runid)
			else:
				print(f"There's no sampled genome in replicate {runid}. Either the simulation failed or the sampling rate is too low. Please check your config file if this is undesired.")
		print(f"Plotting the aggregated SEIR trajectory...")
		plot_all_SEIR_trajectory(slim_pars["cwdir"], slim_pars["seed_size"], slim_pars["host_size"], slim_pars["n_generation"], run_success)
		print(f"Plotting the aggregated strain distribution trajectory...")
		plot_all_strain_trajectory(slim_pars["cwdir"], slim_pars["seed_size"], slim_pars["host_size"], slim_pars["n_generation"], run_success)

		print("********************************************************************")
		print("                    FINISHED. THANKS FOR USING.")
		print("********************************************************************")
	return(0)











