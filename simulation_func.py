import os


def writebinary(v):
	if v:
		return("T")
	else:
		return("")


def create_slimconfig(all_config, wk_dir):
	### A function to create a SLiM-readable config file that includes the SLiM-needed parameters from the big config file
	## Input: all_config: dictionary of the big config file, read by read_config()
	##        wk_dir: working directory
	## Output: no return value

	with open(os.path.join(wk_dir, "slim.params"), "w") as out_json:
		out_json.write("cwdir:" + all_config["BasicRunConfiguration"]["cwdir"] + "\n")
		out_json.write("n_generation:" + str(all_config["EvolutionModel"]["n_generation"]) + "\n")
		out_json.write("mut_rate:" + str(all_config["EvolutionModel"]["mut_rate"]) + "\n")
		out_json.write("trans_type:" + all_config["EvolutionModel"]["trans_type"] + "\n")
		out_json.write("dr_type:" + all_config["EvolutionModel"]["dr_type"] + "\n")
		out_json.write("within_host_evolution:" + writebinary(all_config["EvolutionModel"]["within_host_evolution"]) + "\n")
		out_json.write("cap_withinhost:" + str(all_config["EvolutionModel"]["cap_withinhost"]) + "\n")

		out_json.write("seed_size:" + str(all_config["SeedsConfiguration"]["seed_size"]) + "\n")
		out_json.write("ref_path:" + all_config["GenomeElement"]["ref_path"] + "\n")
		out_json.write("use_genetic_model:" + writebinary(all_config["GenomeElement"]["use_genetic_model"]) + "\n")
		out_json.write("use_network_model:" + writebinary(all_config["NetworkModelParameters"]["use_network_model"]) + "\n")

		out_json.write("epi_model:" + all_config["EpidemiologyModel"]["model"] + "\n")
		out_json.write("n_epoch:" + str(all_config["EpidemiologyModel"]["epoch_changing"]["epoch_num"]) + "\n")
		out_json.write("epoch_changing_generation:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["epoch_changing"]["epoch_changing_generation"]]) + "\n")
		out_json.write("transmissibility_effsize:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["genetic_architecture"]["transmissibility"]]) + "\n")
		out_json.write("drugresistance_effsize:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["genetic_architecture"]["drug_resistance"]]) + "\n")
		out_json.write("S_IE_rate:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["transiton_rate"]["S_IE_rate"]]) + "\n")
		out_json.write("I_R_rate:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["transiton_rate"]["I_R_rate"]]) + "\n")
		out_json.write("R_I_rate:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["transiton_rate"]["R_I_rate"]]) + "\n")
		out_json.write("latency_prob:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["transiton_rate"]["latency_prob"]]) + "\n")
		out_json.write("E_I_rate:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["transiton_rate"]["E_I_rate"]]) + "\n")
		out_json.write("I_E_rate:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["transiton_rate"]["I_E_rate"]]) + "\n")
		out_json.write("E_R_rate:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["transiton_rate"]["E_R_rate"]]) + "\n")
		out_json.write("sample_rate:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["transiton_rate"]["sample_rate"]]) + "\n")
		out_json.write("recovery_prob_after_sampling:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["transiton_rate"]["recovery_prob_after_sampling"]]) + "\n")

		out_json.write("n_massive_sample:" + str(all_config["EpidemiologyModel"]["massive_sampling"]["event_num"]) + "\n")
		out_json.write("massive_sample_generation:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["massive_sampling"]["generation"]]) + "\n")
		out_json.write("massive_sample_prob:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["massive_sampling"]["sampling_prob"]]) + "\n")
		out_json.write("massive_sample_recover_prob:" + ",".join([str(x) for x in all_config["EpidemiologyModel"]["massive_sampling"]["recovery_prob_after_sampling"]]) + "\n")

		out_json.write("super_infection:" + writebinary(all_config["EpidemiologyModel"]["super_infection"]) + "\n")






