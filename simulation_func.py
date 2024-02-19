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
	slim_pars = {}
	with open(os.path.join(all_config["BasicRunConfiguration"]["cwdir"], "slim.params"), "w") as out_config:
		slim_pars["cwdir"] = all_config["BasicRunConfiguration"]["cwdir"]
		out_config.write("cwdir:" + slim_pars["cwdir"] + "\n")
		slim_pars["n_replicates"] = all_config["BasicRunConfiguration"]["n_replicates"]
		out_config.write("n_replicates:" + str(slim_pars["n_replicates"]) + "\n")

		slim_pars["n_generation"] = all_config["EvolutionModel"]["n_generation"]
		out_config.write("n_generation:" + str(slim_pars["n_generation"]) + "\n")
		slim_pars["mut_rate"] = all_config["EvolutionModel"]["mut_rate"]
		out_config.write("mut_rate:" + str(slim_pars["mut_rate"]) + "\n")
		slim_pars["trans_type"] = all_config["EvolutionModel"]["trans_type"]
		out_config.write("trans_type:" + slim_pars["trans_type"] + "\n")
		slim_pars["dr_type"] = all_config["EvolutionModel"]["dr_type"]
		out_config.write("dr_type:" + slim_pars["dr_type"] + "\n")
		slim_pars["within_host_reproduction"] = all_config["EvolutionModel"]["within_host_reproduction"]
		out_config.write("within_host_reproduction:" + writebinary(slim_pars["within_host_reproduction"]) + "\n")
		slim_pars["cap_withinhost"] = all_config["EvolutionModel"]["cap_withinhost"]
		out_config.write("cap_withinhost:" + str(slim_pars["cap_withinhost"]) + "\n")

		slim_pars["seed_size"] = all_config["SeedsConfiguration"]["seed_size"]
		out_config.write("seed_size:" + str(slim_pars["seed_size"]) + "\n")
		slim_pars["use_reference"] = all_config["SeedsConfiguration"]["use_reference"]
		out_config.write("use_genetic_model:" + writebinary(slim_pars["use_reference"]) + "\n")

		slim_pars["ref_path"] = all_config["GenomeElement"]["ref_path"]
		out_config.write("ref_path:" + slim_pars["ref_path"] + "\n")
		slim_pars["use_genetic_model"] = all_config["GenomeElement"]["use_genetic_model"]
		out_config.write("use_genetic_model:" + writebinary(slim_pars["use_genetic_model"]) + "\n")
		slim_pars["use_network_model"] = all_config["NetworkModelParameters"]["use_network_model"]
		out_config.write("use_network_model:" + writebinary(slim_pars["use_network_model"]) + "\n")

		slim_pars["epi_model"] = all_config["EpidemiologyModel"]["model"]
		out_config.write("epi_model:" + slim_pars["epi_model"] + "\n")
		slim_pars["n_epoch"] = all_config["EpidemiologyModel"]["epoch_changing"]["n_epoch"]
		out_config.write("n_epoch:" + str(slim_pars["n_epoch"]) + "\n")
		if slim_pars["n_epoch"]>1:
			slim_pars["epoch_changing_generation"] = all_config["EpidemiologyModel"]["epoch_changing"]["epoch_changing_generation"]
			out_config.write("epoch_changing_generation:" + ",".join([str(x) for x in slim_pars["epoch_changing_generation"]]) + "\n")
		slim_pars["transmissibility_effsize"] = all_config["EpidemiologyModel"]["genetic_architecture"]["transmissibility"]
		out_config.write("transmissibility_effsize:" + ",".join([str(x) for x in slim_pars["transmissibility_effsize"]]) + "\n")
		slim_pars["cap_transmissibility"] = all_config["EpidemiologyModel"]["genetic_architecture"]["cap_transmissibility"]
		out_config.write("cap_transmissibility:" + ",".join([str(x) for x in slim_pars["cap_transmissibility"]]) + "\n")
		slim_pars["drugresistance_effsize"] = all_config["EpidemiologyModel"]["genetic_architecture"]["drug_resistance"]
		out_config.write("drugresistance_effsize:" + ",".join([str(x) for x in slim_pars["drugresistance_effsize"]]) + "\n")
		slim_pars["cap_drugresist"] = all_config["EpidemiologyModel"]["genetic_architecture"]["cap_drugresist"]
		out_config.write("cap_drugresist:" + ",".join([str(x) for x in slim_pars["cap_drugresist"]]) + "\n")
		slim_pars["S_IE_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["S_IE_rate"]
		out_config.write("S_IE_rate:" + ",".join([str(x) for x in slim_pars["S_IE_rate"]]) + "\n")
		slim_pars["I_R_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["I_R_rate"]
		out_config.write("I_R_rate:" + ",".join([str(x) for x in slim_pars["I_R_rate"]]) + "\n")
		slim_pars["R_S_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["R_S_rate"]
		out_config.write("R_S_rate:" + ",".join([str(x) for x in slim_pars["R_S_rate"]]) + "\n")
		slim_pars["latency_prob"] = all_config["EpidemiologyModel"]["transiton_rate"]["latency_prob"]
		out_config.write("latency_prob:" + ",".join([str(x) for x in slim_pars["latency_prob"]]) + "\n")
		slim_pars["E_I_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["E_I_rate"]
		out_config.write("E_I_rate:" + ",".join([str(x) for x in slim_pars["E_I_rate"]]) + "\n")
		slim_pars["I_E_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["I_E_rate"]
		out_config.write("I_E_rate:" + ",".join([str(x) for x in slim_pars["I_E_rate"]]) + "\n")
		slim_pars["E_R_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["E_R_rate"]
		out_config.write("E_R_rate:" + ",".join([str(x) for x in slim_pars["E_R_rate"]]) + "\n")
		slim_pars["sample_rate"] = all_config["EpidemiologyModel"]["transiton_rate"]["sample_rate"]
		out_config.write("sample_rate:" + ",".join([str(x) for x in slim_pars["sample_rate"]]) + "\n")
		slim_pars["recovery_prob_after_sampling"] = all_config["EpidemiologyModel"]["transiton_rate"]["recovery_prob_after_sampling"]
		out_config.write("recovery_prob_after_sampling:" + ",".join([str(x) for x in slim_pars["recovery_prob_after_sampling"]]) + "\n")

		slim_pars["n_massive_sample"] = all_config["EpidemiologyModel"]["massive_sampling"]["event_num"]
		out_config.write("n_massive_sample:" + str(slim_pars["n_massive_sample"]) + "\n")
		if slim_pars["n_massive_sample"]>0:
			slim_pars["massive_sample_generation"] = all_config["EpidemiologyModel"]["massive_sampling"]["generation"]
			out_config.write("massive_sample_generation:" + ",".join([str(x) for x in slim_pars["massive_sample_generation"]]) + "\n")
			slim_pars["massive_sample_prob"] = all_config["EpidemiologyModel"]["massive_sampling"]["sampling_prob"]
			out_config.write("massive_sample_prob:" + ",".join([str(x) for x in slim_pars["massive_sample_prob"]]) + "\n")
			slim_pars["massive_sample_recover_prob"] = all_config["EpidemiologyModel"]["massive_sampling"]["recovery_prob_after_sampling"]
			out_config.write("massive_sample_recover_prob:" + ",".join([str(x) for x in slim_pars["massive_sample_recover_prob"]]) + "\n")

		slim_pars["super_infection"] = all_config["EpidemiologyModel"]["super_infection"]
		out_config.write("super_infection:" + writebinary(slim_pars["n_massive_sample"]) + "\n")

		slim_pars["cap_withinhost"] = all_config["EvolutionModel"]["cap_withinhost"]
		out_config.write("cap_withinhost:" + str(slim_pars["cap_withinhost"]) + "\n")
		slim_pars["within_host_reproduction"] = all_config["EvolutionModel"]["within_host_reproduction"]
		out_config.write("within_host_reproduction:" + writebinary(slim_pars["within_host_reproduction"]) + "\n")

		if slim_pars["use_genetic_model"]:
			out_config.write("causal_gene_path:" + os.path.join(slim_pars["cwdir"], "causal_gene_info.csv") + "\n")
		else:
			out_config.write("causal_gene_path:" + "\n")
		slim_pars["seed_host_matching_path"] = os.path.join(slim_pars["cwdir"], "seed_host_match.csv")
		out_config.write("seed_host_matching_path:" + slim_pars["seed_host_matching_path"] + "\n")

		if slim_pars["use_network_model"]:
			slim_pars["host_size"] = all_config["NetworkModelParameters"]["host_size"]
			out_config.write("host_size:" + str(slim_pars["host_size"]) + "\n")
			out_config.write("contact_network_path:" + os.path.join(slim_pars["cwdir"], "contact_network.adjlist") + "\n")

		if slim_pars["within_host_reproduction"]:
			slim_pars["within_host_reproduction_rate"] = all_config["EvolutionModel"]["within_host_reproduction_rate"]
			out_config.write("within_host_reproduction_rate:" + str(slim_pars["within_host_reproduction_rate"]) + "\n")
		else:
			out_config.write("host_size:" + str(slim_pars["host_size"]) + "\n")

		if all_config["Postprocessing_options"]["do_postprocess"]:
			post_processing_config = all_config["Postprocessing_options"]
			post_processing_config["n_trait"] = all_config["GenomeElement"]["traits_num"]
		else:
			post_processing_config = {}
		

	return(slim_pars, post_processing_config)


def check_all_params(slim_pars):
	### A function that takes in all parameters needed for the simulation (A dictionary) and check whether it's legit

	## Return T/F
	return(True)


def check_prerequisites(wk_dir, use_genetic_model=True, use_network_model=True):
	### A function that takes in the parameters and check whether the required prerequisites files are already in the working directory
	pres_met = True
	if os.path.exists(os.path.join(wk_dir, "originalvcfs"))==False:
		print("No seed file is provided in the working directory, please run seed_generator module before running the simulation.")
		pres_met = False
	if use_network_model:
		if os.path.exists(os.path.join(wk_dir, "contact_network.adjlist"))==False:
			print("No network file is provided in the working directory under network model, please run network_generator module before running the simulation or use a no-network model.")
			pres_met = False
		if os.path.exists(os.path.join(wk_dir, "seed_host_match.csv"))==False:
			print("No seed-host matching file file is provided in the working directory under network model, please run seed_host_matcher module before running the simulation.")
			pres_met = False
	if use_genetic_model:
		if os.path.exists(os.path.join(wk_dir, "causal_gene_info.csv"))==False:
			print("No causal gene effect size file is provided in the working directory under network model, please run genetic_effect_generator module before running the simulation or use a no-genetic-effect model.")
			pres_met = False
	return(pres_met)



def create_slimscript(slim_pars):
	### A function that create a SLiM script in the working directory according to the config
	### The script should take in SLiM config file and the current output directory (related to n_replicates) as parameters
	### No return value
	
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
	if slim_pars["super_infection"] > 0:
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
	if check_all_params(slim_pars)==False:
		print("Checking slim configuration not passed, please check for the error message to adjust for the parameters.")
		run_check = False
	if check_prerequisites(slim_pars["cwdir"], use_genetic_model=slim_pars["use_genetic_model"], use_network_model=slim_pars["use_network_model"])==False:
		print("Prerequisites for your specified slim configuration isn't met, please see the error message and run the pre-simulation steps as suggested.")
		run_check = False

	#lst = [(slim_config_path, slim_pars["cwdir"], runid) for runid in range(1, slim_pars["n_replicates"] + 1)]

	if run_check:
		run_success = []
		for runid in range(1,slim_pars["n_replicates"] + 1):
			run_per_slim_simulation(slim_config_path, slim_pars["cwdir"], runid)
			if os.path.exists(os.path.join(slim_pars["cwdir"], str(runid), "sampled_genomes.trees")):
				if len(dataprocess_pars) > 0:
					each_wkdir = os.path.join(slim_pars["cwdir"], str(runid))
					run_per_data_processing(slim_pars["cwdir"], slim_pars["use_genetic_model"], runid, dataprocess_pars["n_trait"], slim_pars["seed_host_matching_path"], dataprocess_pars["tree_plotting"]["branch_color_trait"])
					if slim_pars["use_reference"]:
						seed_phylo = ""
					else:
						seed_phylo = os.path.join(slim_pars["cwdir"], "seeds.nwk")
					plot_per_transmission_tree(each_wkdir, slim_pars["seed_size"], slim_config_path, dataprocess_pars["n_trait"], seed_phylo)
					plot_strain_distribution_trajectory(each_wkdir, slim_pars["seed_size"], slim_pars["n_generation"])
					if os.path.exists(os.path.join(each_wkdir, "SEIR_trajectory.csv.gz")):
						plot_SEIR_trajectory(each_wkdir, slim_pars["seed_size"], slim_pars["host_size"], slim_pars["n_generation"])
						run_success.append(runid)
			else:
				print(f"There's no sampled genome in replicate {runid}. Either the simulation failed or the sampling rate is too low. Please check your config file if this is undesired.")
		plot_all_SEIR_trajectory(slim_pars["cwdir"], slim_pars["seed_size"], slim_pars["host_size"], slim_pars["n_generation"], run_success)
		plot_all_strain_trajectory(slim_pars["cwdir"], slim_pars["seed_size"], slim_pars["host_size"], slim_pars["n_generation"], run_success)
	return(0)











