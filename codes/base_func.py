import json, os, argparse
from error_handling import CustomizedError

def read_params(path_config, default_config):
    """
    Reads configuration parameters from JSON files and merges with default parameters defined in he template dictionary.

    Parameters:
        path_config (str): Full path to configuration file.
        default_config (str): Relative path to the template (e.g., "base_params.json", "slim_only_template.json")
    """
    # Read default template
    default_config = open(os.path.join(os.path.dirname(__file__), default_config), "r")
    default_param_dict = json.loads(default_config.read())
    # Read the user defined parameters
    config = open(path_config, "r")
    usr_param_dict = json.loads(config.read())
    # Update the template with user information
    default_param_dict.update(usr_param_dict)

    return default_param_dict

def read_params_simonly(path_config):
    # Remeber to get rid of
    default_config = open(os.path.join(os.path.dirname(__file__), "slim_only_template.json"), "r")
    pass


def str2bool(v):
    """
    Returns boolean value represented by the given str / bool.

    Parameters:
        v (str / bool): A string representing the boolean value.
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    raise argparse.ArgumentTypeError('Boolean value expected.')

def dump_json(json2dump):
    """
    Writes a JSON object to the SLiM config file.

    Parameters:
        json2dump: A dictionary rerpesenting the JSON object to be dumped.
    """
    out_config_path = os.path.join(json2dump["BasicRunConfiguration"]["cwdir"], "params.json")
    with open(out_config_path, 'w') as out_config:
        json.dump(json2dump, out_config, indent = 4)

def check_config(config_dict):
    pass

# def check_config(config_dict):
#     """
#     """
#     out_dict = {"BasicRunConfiguration":{}, "EvolutionModel":{}, "SeedsConfiguration":{}, "GenomeElement":{}, 
#                 "NetworkModelParameters":{}, "SeedHostMatching":{}, "EpidemiologyModel":{}, "Postprocessing_options":{}}

#     ## Check basic run configuration
#     def _check_basic_run_config(config_dict, out_dict):
#         base_config = config_dict["BasicRunConfiguration"]
#         if base_config["cwdir"] == "":
#             raise CustomizedError("Please provide a working directory (\"cwdir\") in the config file")
#         elif not os.path.exists(base_config["cwdir"]):
#             raise CustomizedError("Path to the provided working directory (\"cwdir\") doesn't exists, please check your config file")
#         out_dict["BasicRunConfiguration"] = base_config
#         return out_dict
    
#     out_dict = _check_basic_run_config(config_dict, out_dict)

#     ## Check EvolutionModel:
#     def _check_evo_model(config_dict, out_dict):
#         evo_config = config_dict["EvolutionModel"]
#         if evo_config["n_generation"] == 0:
#             raise CustomizedError("Please specify a positive number for the number of generation from the seeding event to end of simulation")
#         if evo_config["mut_rate"] == 0:
#             print("WARNING: Mutation rate is set to 0 during the outbreak simulation, please make sure this is what you want.")
#         if evo_config["within_host_reproduction"]:
#             if evo_config["within_host_reproduction_rate"] == 0:
#                 print("WARNING: You've chosen within-host evolution mode, but with a reproduction rate of 0. This setup is not recommended because it essentially deactivates within-host reproduction.")
#             if evo_config["cap_withinhost"] == 1:
#                 print("You've chosen within-host evolution mode, but set the cap of genomes within one host to 1. This setup is not recommended as it essentially deactivates within-host reproduction.")
#         out_dict["EvolutionModel"] = evo_config
#         return out_dict
    
#     out_dict = _check_evo_model(config_dict, out_dict)

#     ## Check NetworkModelParameters:
#     def _check_network_model(config_dict, out_dict):
#         ntwk_config = config_dict["NetworkModelParameters"]
#         if not ntwk_config["use_network_model"]:
#             raise CustomizedError("Please specify to use the network model in the current version. We are working to relax the network requirement in future :)")
#         if ntwk_config["host_size"] <= 0:
#             raise CustomizedError("Please specify a positive number for host population size")

#         if ntwk_config["method"] == "user_input":
#             del ntwk_config["randomly_generate"]
#             if ntwk_config["user_input"]["path_network"] == "":
#                 raise CustomizedError("Please specify a path to the user-provided network")
#             if not os.path.exists(ntwk_config["user_input"]["path_network"]):
#                 raise CustomizedError("Path to the provided network file doesn't exists, please check your config file")
#         elif ntwk_config["method"] == "randomly_generate":
#             del ntwk_config["user_input"]
#             if ntwk_config["randomly_generate"]["network_model"] == "ER":
#                 del ntwk_config["randomly_generate"]["RP"]
#                 del ntwk_config["randomly_generate"]["BA"]
#                 if ntwk_config["randomly_generate"]["ER"]["p_ER"] == 0:
#                     raise CustomizedError("Please specify a p > 0 in Erdos-Renyi graph")
#             elif ntwk_config["randomly_generate"]["network_model"] == "RP":
#                 del ntwk_config["randomly_generate"]["ER"]
#                 del ntwk_config["randomly_generate"]["BA"]
#                 num_part = len(ntwk_config["randomly_generate"]["RP"]["rp_size"])
#                 if num_part != 2:
#                     raise CustomizedError("Please specify 2 partitions in random partition graph.")
#                 if len(ntwk_config["randomly_generate"]["RP"]["p_within"]) != num_part:
#                     raise CustomizedError("The length of parameter p within each partition needs to be the number of partitions.")
#                 elif len(ntwk_config["randomly_generate"]["RP"]["p_between"])!= 1:
#                     raise CustomizedError("The length of parameter p between each partition needs to be 1")
#             elif ntwk_config["randomly_generate"]["network_model"] == "BA":
#                 del ntwk_config["randomly_generate"]["ER"]
#                 del ntwk_config["randomly_generate"]["RP"]
#                 if ntwk_config["randomly_generate"]["BA"]["ba_m"] == 0:
#                     raise CustomizedError("Please specify a m > 0 in Barabasi-Albert graph.")
#             else:
#                 raise CustomizedError("Please specify a legit random graph model (-model) in random \
#                                         generate mode. (Supported model: ER/RP/BA)")
#         else:
#             raise CustomizedError("Please provide a permitted method (user_input/randomly_generate)")

#         out_dict["NetworkModelParameters"] = ntwk_config
#         return out_dict
    
#     out_dict = _check_network_model(config_dict, out_dict)

#     ## Check SeedsConfiguration:
#     def _check_seed_config(config_dict, out_dict):
#         seeds_config = config_dict["SeedsConfiguration"]
#         if seeds_config["method"] == "user_input":
#             del seeds_config["SLiM_burnin_WF"]
#             del seeds_config["SLiM_burnin_epi"]
#             if seeds_config["user_input"]["path_seeds_vcf"] == "":
#                 raise CustomizedError("Please provide the directory to seeds' vcf file in the user input mode for seeds' generation.")
#             if not os.path.exists(seeds_config["user_input"]["path_seeds_vcf"]):
#                 print("Path to the provided seeds' vcf file does NOT exist, please check your config file.")
#         elif seeds_config["method"] == "SLiM_burnin_WF":
#             del seeds_config["user_input"]
#             del seeds_config["SLiM_burnin_epi"]
#             if seeds_config["SLiM_burnin_WF"]["burn_in_Ne"] == 0:
#                 raise CustomizedError("Please specify a positive number for effective population size in SLiM WF burn-in mode.")
#             if seeds_config["SLiM_burnin_WF"]["burn_in_mutrate"] == 0:
#                 raise CustomizedError("Please specify a positive mutation rate in SLiM burn-in mode.")
#             if seeds_config["SLiM_burnin_WF"]["burn_in_generations"] ==  0:
#                 raise CustomizedError("Please specify a positive number for the number of burn-in generations in SLiM burn-in mode.")
#         elif seeds_config["method"] == "SLiM_burnin_epi":
#             del seeds_config["user_input"]
#             del seeds_config["SLiM_burnin_WF"]
#             if seeds_config["SLiM_burnin_epi"]["burn_in_mutrate"] == 0:
#                 raise CustomizedError("Please specify a positive mutation rate in SLiM burn-in mode.")
#             if seeds_config["SLiM_burnin_epi"]["burn_in_generations"] == 0:
#                 raise CustomizedError("Please specify a positive number for the number of burn-in generations in SLiM burn-in mode.")
#             if len(seeds_config["SLiM_burnin_epi"]["seeded_host_id"]) == 0:
#                 raise CustomizedError("Please specify at least one host id to be seeded in SLiM epi model burn-in mode.")
#             if config_dict["NetworkModelParameters"]["host_size"] < len(seeds_config["SLiM_burnin_epi"]["seeded_host_id"]):
#                 raise CustomizedError("Please specify a host population size bigger than the size of the seeded hosts in SLiM epi model burn-in mode.")
#             if max(seeds_config["SLiM_burnin_epi"]["seeded_host_id"]) >= config_dict["NetworkModelParameters"]["host_size"]:
#                 raise CustomizedError("All the host ids to be seeded has to be smaller than host population size.")
#             if seeds_config["SLiM_burnin_epi"]["S_IE_rate"] == 0:
#                 raise CustomizedError("A positive infection rate (Susceptible to infected/exposed rate) needs to be provided in SLiM epi model burn-in mode.")
#             if seeds_config["SLiM_burnin_epi"]["latency_prob"] > 0 and seeds_config["SLiM_burnin_epi"]["E_I_rate"] == 0 and seeds_config["SLiM_burnin_epi"]["E_R_rate"] == 0:
#                 print("WARNING: You activated an SEIR model, in which exposed compartment exists, but you doesn't specify any transition from exposed compartment, which will lead to exposed hosts being locked (never recovered and cannot infect others). Please make sure this is what you want.")
#             elif seeds_config["SLiM_burnin_epi"]["I_R_rate"] == 0:
#                 print("WARNING: You activated a S(E)I model by setting I -> R rate = 0, where recovered component doesn't exists, meaning that all infected hosts never recovered. Please make sure this is what you want.")
#             elif seeds_config["SLiM_burnin_epi"]["R_S_rate"] == 0:
#                 print("WARNING: You activated a S(E)IR model with Recovered individuals are fully immune, they don't go back to recovered state. This can probably lead to the outbreak ending before the specified burn-in generation and makes the seeds' sampling fail. Please make sure this is what you want.")
#         else:
#             raise CustomizedError("The provided burn-in method isn't permitted.")
#         out_dict["SeedsConfiguration"] = seeds_config
#         return out_dict

#     out_dict = _check_seed_config(config_dict, out_dict)

#     ## Check SeedHostMatching:
#     def _check_matching_config(config_dict, out_dict):
#         match_config = config_dict["SeedHostMatching"]
#         if match_config["method"] == "user_input":
#             del match_config["randomly_generate"]
#             if match_config["user_input"]["path_matching"] == "":
#                 raise CustomizedError("The path to the matching file has to be provided in the user input mode for seeds' generation")
#             if not os.path.exists(match_config["user_input"]["path_matching"]):
#                 raise CustomizedError("Path to the provided matching file doesn't exists, please check your config file")
#         elif match_config["method"] == "randomly_generate":
#             del match_config["user_input"]
#             if match_config["randomly_generate"]["method"] == "":
#                 raise CustomizedError("Please provide a matching scheme for the random generation of seed-host matching")
#         out_dict["SeedHostMatching"] = match_config
#         return out_dict
    
#     out_dict = _check_matching_config(config_dict, out_dict)


#     ## Check GenomeElement:
#     def _check_genome_ele(config_dict, out_dict):
#         genome_config = config_dict["GenomeElement"]
#         if genome_config["ref_path"] == "":
#             raise CustomizedError("Please specify the path to the reference genome")
#         if not os.path.exists(genome_config["ref_path"]):
#             raise CustomizedError("Path to the provided reference genome doesn't exists.")
#         if genome_config["use_genetic_model"]:
#             if len(genome_config["traits_num"]) == 0:
#                 raise CustomizedError("If you want to use genetic factors in simulation, please specify a positive number for number of traits.")
#             if len(genome_config["traits_num"]) > 2:
#                 raise CustomizedError("You can only specify at most 2 numbers for traits number, representing transmissibility and drug resistance")
#             if genome_config["effect_size"]["method"] == "user_input":
#                 del genome_config["effect_size"]["randomly_generate"]
#                 if genome_config["effect_size"]["user_input"]["path_effsize_table"] == "":
#                     raise CustomizedError("Please specify path to the effect size file.")
#                 if not os.path.exists(genome_config["effect_size"]["user_input"]["path_effsize_table"]):
#                     raise CustomizedError("Path to the provided effect size doesn't exists.")
#             elif genome_config["effect_size"]["method"] == "randomly_generate":
#                 del genome_config["effect_size"]["user_input"]
#                 if genome_config["effect_size"]["randomly_generate"]["gff"] == "":
#                     raise CustomizedError("gff file needs to be provided in random generation mode.")
#                 if not os.path.exists(genome_config["effect_size"]["randomly_generate"]["gff"]):
#                     raise CustomizedError("Path to the provided gff file doesn't exists.")
#                 for item in ["genes_num", "effsize_min", "effsize_max"]:
#                     if len(genome_config["effect_size"]["randomly_generate"][item]) != sum(genome_config["traits_num"]):
#                         raise CustomizedError(f"The {item} has to be a list that has the length of the number of traits.")
#         out_dict["GenomeElement"] = genome_config
#         return out_dict
    
#     out_dict = _check_genome_ele(config_dict, out_dict)


#     ## Check EpidemiologyModel:
#     epi_config_check = True
#     epi_config = config_dict["EpidemiologyModel"]
#     if len(epi_config["method"]["epoch_changing_generation"])!=epi_config["method"]["n_epoch"] - 1:
#         print("The epoch changing generation has to be a list that has the length of the number of epochs - 1. (default n_epoch=1)")
#         epi_config_check = False
#     if genome_config["use_genetic_model"]==False:
#         if (any(sum(epi_config["genetic_architecture"][item])>0)):
#             print("WARNING: The provided genetic architecture parameters won't be used in a non-genetic mode.")
#             epi_config["genetic_architecture"] = {"transmissibility": [], "cap_transmissibility": [], "drug_resistance": [], "cap_drugresist": []}
#             for i in range(epi_config["method"]["n_epoch"]):
#                 for j in epi_config["genetic_architecture"]:
#                     epi_config["genetic_architecture"][j].append(0)
#     else:
#         for item in epi_config["genetic_architecture"]:
#             if len(epi_config["genetic_architecture"][item])!=epi_config["method"]["n_epoch"]:
#                 print(f"The {item} has to be a list that has the length of the number of epochs.")
#                 epi_config_check = False
#         if max(epi_config["genetic_architecture"]["transmissibility"])==0 and max(epi_config["genetic_architecture"]["drug_resistance"])==0:
#             print("WARNING: Both transmissibility and drug resistance are not using any genetic effect size under a genetic mode. This is not recommended. If you want to run a non-genetic mode, you can just turn off genetic_architecture.")
#         elif max(epi_config["genetic_architecture"]["cap_transmissibility"])==0 and max(epi_config["genetic_architecture"]["cap_drugresist"])==0:
#             print("WARNING: Both transmissibility and drug resistance are having a cap being 0, so essentially not using any genetic effect size under a genetic mode. This is not recommended. If you want to run a non-genetic mode, you can just turn off genetic_architecture.")
#         else:
#             if max(epi_config["genetic_architecture"]["transmissibility"]) > genome_config["traits_num"][0]:
#                 print("The transmissibility effect size set you are using has to be one of the genetic effect size specified. i.e. cannot exceed the number of transmissibility traits.")
#             if max(epi_config["genetic_architecture"]["transmissibility"]) > genome_config["traits_num"][0]:
#                 print("The drug resistance effect size set you are using has to be one of the genetic effect size specified. i.e. cannot exceed the number of drug resistance traits.")
#     for rate in ["S_IE_rate", "I_R_rate", "R_S_rate", "sample_rate", "recovery_prob_after_sampling"]:
#         if len(epi_config["transiton_rate"][rate]) > 0:
#             if len(epi_config["transiton_rate"][rate])!=epi_config["method"]["n_epoch"]:
#                 print(f"The transition rate {rate} has to be a list that has the length of the number of epochs.")
#                 epi_config_check = False
#         else:
#             epi_config["transiton_rate"][rate]= []
#             for i in range(epi_config["method"][rate]):
#                 epi_config["transiton_rate"][rate].append(0)
#     if epi_config["method"]=="":
#         print("Please specify an epidemiological model (SIR/SEIR)")
#         epi_config_check = False
#     elif epi_config["epoch_changing"]=="SIR":
#         for rate in ["latency_prob", "E_I_rate", "I_E_rate", "E_R_rate"]:
#             if len(epi_config["transiton_rate"][rate]) > 0:
#                 print(f"WARNING: The provided {rate} won't be used in an SIR model.")
#             epi_config["transiton_rate"][rate] = []
#             for i in range(epi_config["method"]["n_epoch"]):
#                 epi_config["transiton_rate"][rate].append(0)
#     elif epi_config["epoch_changing"]=="SEIR":
#         for rate in ["latency_prob", "E_I_rate", "I_E_rate", "E_R_rate"]:
#             if len(epi_config["transiton_rate"][rate]) > 0:
#                 if len(epi_config["transiton_rate"][rate])!=epi_config["method"]["n_epoch"]:
#                     print(f"The transition rate {rate} has to be a list that has the length of the number of epochs.")
#                     epi_config_check = False
#             else:
#                 epi_config["transiton_rate"][rate]= []
#                 for i in range(epi_config["method"]["n_epoch"]):
#                     epi_config["transiton_rate"][rate].append(0)
#     else:
#         print("The epidemiological model provided isn't permitted.")
#         epi_config_check = False
#     if epi_config["massive_sampling"]["event_num"]==0:
#         for lst in ["generation", "sampling_prob", "recovery_prob_after_sampling"]:
#             if epi_config["massive_sampling"][lst]!=[]:
#                 print(f"WARNING: The provided {lst} won't be used if the massive sampling event number is 0.")
#                 epi_config["transiton_rate"][lst] = []
#     else:
#         for lst in ["generation", "sampling_prob", "recovery_prob_after_sampling"]:
#             if len(epi_config["massive_sampling"][lst])!=epi_config["massive_sampling"]["event_num"]:
#                 print(f"WARNING: The provided {lst} has to be a list that has the length of the number of the massive sampling events.")
#                 epi_config_check = False

#     if epi_config_check:
#         out_dict["EpidemiologyModel"] = epi_config
#     else:
#         print("###### Config file error: Please check the EpidemiologyModel module of the config file provided.")
        
#     ## Check Postprocessing_options:
#     postprocess_config = config_dict["Postprocessing_options"]
#     postprocess_config_check = True
#     if genome_config["use_genetic_model"]==False:
#         postprocess_config["tree_plotting"]["branch_color_trait"]=0
#     else:
#         if postprocess_config["tree_plotting"]["branch_color_trait"]>sum(genome_config["traits_num"]):
#             print("Have to provide a valid trait number for coloring the tree. (between 0 and the total number of traits.)")
#             postprocess_config_check = False
#     if postprocess_config_check:
#         out_dict["Postprocessing_options"] = postprocess_config_check
#     else:
#         print("###### Config file error: Please check the Postprocessing_options module of the config file provided.")

#     return(all(base_config_check, evo_config_check, ntwk_config_check, seeds_config_check, match_config_check, genome_config_check, epi_config_check, postprocess_config_check), out_dict)


# def dump_json(json2dump):
#     """
#     Writes a JSON object to the SLiM config file.

#     Parameters:
#         json2dump: A dictionary rerpesenting the JSON object to be dumped.
#     """
#     out_config_path = os.path.join(json2dump["BasicRunConfiguration"]["cwdir"], "params.json")
#     with open(out_config_path, 'w') as out_config:
#         json.dump(json2dump, out_config, indent = 4)







