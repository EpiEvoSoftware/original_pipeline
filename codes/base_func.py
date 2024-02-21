import json
import os
import inspect
import argparse

def read_params(path_config):
    default_config = open(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "base_params.json"), "r")
    default_param_dict = json.loads(default_config.read())
    config = open(path_config, "r")
    usr_param_dict = json.loads(config.read())

    default_param_dict.update(usr_param_dict)

    return(default_param_dict)

def read_params_simonly(path_config):
    default_config = open(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "slim_only_template.json"), "r")
    default_param_dict = json.loads(default_config.read())
    config = open(path_config, "r")
    usr_param_dict = json.loads(config.read())

    default_param_dict.update(usr_param_dict)

    return(default_param_dict)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def check_config(config_dict):
    out_dict = {"BasicRunConfiguration":{}, "EvolutionModel":{}, "SeedsConfiguration":{}, "GenomeElement":{}, "NetworkModelParameters":{}, "SeedHostMatching":{}, "EpidemiologyModel":{}, "Postprocessing_options":{}}

    base_config_check = True
    ## Check basic run configuration
    base_config = config_dict["BasicRunConfiguration"]
    if base_config["cwdir"]=="":
        print("Working directory isn't provided in the config file.")
        base_config_check == False
    elif os.path.exists(base_config["cwdir"]) == False:
        print("Path to the provided working directory doesn't exists, please check your config file.")
        base_config_check == False
    if base_config_check:
        out_dict["BasicRunConfiguration"] = base_config
    else:
        print("###### Config file error: Please check the BasicRunConfiguration module of the config file provided.")

    ## Check EvolutionModel:
    evo_config_check = True
    evo_config = config_dict["EvolutionModel"]
    if evo_config["n_generation"] == 0:
        print("Number of generation from the seeding event to end of simulation has to be specified.")
        base_config_check = False
    if evo_config["mut_rate"] == 0:
        print("WARNING: Mutation rate will be zero during the outbreak simulation, please make sure this is what you want.")
    if evo_config["within_host_reproduction"] == True:
        if evo_config["within_host_reproduction_rate"] == 0:
            print("WARNING: You specify to use a within-host evolution mode, but within-host reproduction rate is 0, which is not recommended as this will essentially do the same thing as within-host reproduction is deactivated, except for additional running time.")
        if evo_config["cap_withinhost"] == 1:
            print("WARNING: You specify to use a within-host evolution mode, but the cap of genomes within one host is 1, which is not recommended as this will essentially do the same thing as within-host reproduction is deactivated, except for additional running time.")
    if evo_config_check:
        out_dict["EvolutionModel"] = evo_config
    else:
        print("###### Config file error: Please check the EvolutionModel module of the config file provided.")

    ## Check NetworkModelParameters:
    ntwk_config_check = True
    ntwk_config = config_dict["NetworkModelParameters"]
    if ntwk_config["use_network_model"]==False:
        print("No network model isn't supported in the current version.")
        ntwk_config_check = False
    if ntwk_config["host_size"]<=0:
        print("Need to specify a host population size bigger than 1.")
        ntwk_config_check = False
    if ntwk_config["method"]=="user_input":
        del ntwk_config["randomly_generate"]
        if ntwk_config["user_input"]["path_network"]=="":
            print("Need to specify a path to the user-provided network.")
            ntwk_config_check = False
        elif os.path.exists(ntwk_config["user_input"]["path_network"]) == False:
            print("Path to the provided network file doesn't exists, please check your config file.")
            ntwk_config_check = False
    elif ntwk_config["method"]=="randomly_generate":
        del ntwk_config["user_input"]
        if ntwk_config["randomly_generate"]["network_model"] == "ER":
            del ntwk_config["randomly_generate"]["RP"]
            del ntwk_config["randomly_generate"]["BA"]
            if ntwk_config["randomly_generate"]["ER"]["p_ER"]==0:
                print("Need to specify a p>0 in Erdos-Renyi graph.")
                ntwk_config_check = False
        elif ntwk_config["randomly_generate"]["network_model"] == "RP":
            del ntwk_config["randomly_generate"]["ER"]
            del ntwk_config["randomly_generate"]["BA"]
            if len(ntwk_config["randomly_generate"]["RP"]["rp_size"])!=2:
                print("Need to specify 2 partitions in random partition graph.")
                ntwk_config_check = False
            elif len(ntwk_config["randomly_generate"]["RP"]["p_within"])!=len(ntwk_config["randomly_generate"]["RP"]["p_between"]):
                print("The parameter p within each partition needs to be the number of partitions.")
                ntwk_config_check = False
            elif len(ntwk_config["randomly_generate"]["RP"]["p_between"])!=len(ntwk_config["randomly_generate"]["RP"]["rp_size"]) - 1:
                print("The parameter p between each partition needs to ......")
                ntwk_config_check = False
        elif ntwk_config["randomly_generate"]["network_model"]=="BA":
            del ntwk_config["randomly_generate"]["ER"]
            del ntwk_config["randomly_generate"]["RP"]
            if ntwk_config["randomly_generate"]["BA"]["ba_m"]==0:
                print("Need to specify a m>0 in Barabasi-Albert graph.")
                ntwk_config_check = False
        else:
            ntwk_config_check = False
            print("Illegal network model specified!")
    else:
        ntwk_config_check = False
        print("Please provide a permitted method.")
    if ntwk_config_check:
        out_dict["NetworkModelParameters"] = ntwk_config
    else:
        print("###### Config file error: Please check the NetworkModelParameters module of the config file provided.")


    ## Check SeedsConfiguration:
    seeds_config_check = True
    seeds_config = config_dict["SeedsConfiguration"]
    if seeds_config["method"]=="user_input":
        del seeds_config["SLiM_burnin_WF"]
        del seeds_config["SLiM_burnin_epi"]
        if seeds_config["user_input"]["path_seeds_vcf"] == "":
            print("The seeds' vcf file has to be provided in the user input mode for seeds' generation.")
            seeds_config_check = False
        elif os.path.exists(seeds_config["user_input"]["path_seeds_vcf"]) == False:
            print("Path to the provided seeds' vcf file doesn't exists, please check your config file.")
            seeds_config_check = False
    elif seeds_config["method"]=="SLiM_burnin_WF":
        del seeds_config["user_input"]
        del seeds_config["SLiM_burnin_epi"]
        if seeds_config["SLiM_burnin_WF"]["burn_in_Ne"]==0:
            print("Need to specify an effective population size bigger than 0 in SLiM WF burn-in mode.")
            seeds_config_check = False
        elif seeds_config["SLiM_burnin_WF"]["burn_in_mutrate"]==0:
            print("Need to specify a mutation rate bigger than 0 in SLiM burn-in mode.")
            seeds_config_check = False
        elif seeds_config["SLiM_burnin_WF"]["burn_in_generations"]==0:
            print("Need to specify a burn-in generation bigger than 0 in SLiM burn-in mode.")
            seeds_config_check = False
    elif seeds_config["method"]=="SLiM_burnin_epi":
        del seeds_config["user_input"]
        del seeds_config["SLiM_burnin_WF"]
        if seeds_config["SLiM_burnin_epi"]["burn_in_mutrate"]==0:
            print("Need to specify a mutation rate bigger than 0 in SLiM burn-in mode.")
            seeds_config_check = False
        elif seeds_config["SLiM_burnin_epi"]["burn_in_generations"]==0:
            print("Need to specify a burn-in generation bigger than 0 in SLiM burn-in mode.")
            seeds_config_check = False
        elif len(seeds_config["SLiM_burnin_epi"]["seeded_host_id"])==0:
            print("Need to specify at least one host id to be seeded in SLiM epi model burn-in mode.")
            seeds_config_check = False
        elif config_dict["NetworkModelParameters"]["host_size"] < len(seeds_config["SLiM_burnin_epi"]["seeded_host_id"]):
            print("Need to specify a host population size bigger than the size of the seeded hosts in SLiM epi model burn-in mode.")
            seeds_config_check = False
        elif max(seeds_config["SLiM_burnin_epi"]["seeded_host_id"]) >= config_dict["NetworkModelParameters"]["host_size"]:
            print("All the host ids to be seeded has to be smaller than host population size.")
            seeds_config_check = False
        elif seeds_config["SLiM_burnin_epi"]["S_IE_rate"]==0:
            print("An infection rate (Susceptible to infected/exposed rate) bigger than 0 needs to be provided in SLiM epi model burn-in mode.")
            seeds_config_check = False
        elif seeds_config["SLiM_burnin_epi"]["latency_prob"]>0:
            if seeds_config["SLiM_burnin_epi"]["E_I_rate"]==0 and seeds_config["SLiM_burnin_epi"]["E_R_rate"]==0:
                print("WARNING: You activated an SEIR model, in which exposed compartment exists, but you doesn't specify any transition from exposed compartment, which will lead to exposed hosts being locked (never recovered and cannot infect others). Please make sure this is what you want.")
        elif seeds_config["SLiM_burnin_epi"]["I_R_rate"]==0:
            print("WARNING: You activated a S(E)I model by setting I>R rate = 0, where recovered component doesn't exists, meaning that all infected hosts never recovered. Please make sure this is what you want.")
        elif seeds_config["SLiM_burnin_epi"]["R_S_rate"]==0:
            print("WARNING: You activated a S(E)IR model with Recovered individuals are fully immune, they don't go back to recovered state. This can probably lead to the outbreak ending before the specified burn-in generation and makes the seeds' sampling fail. Please make sure this is what you want.")
    else:
        print("The provided burn-in method isn't permitted.")
        seeds_config_check = False
    if seeds_config_check:
        out_dict["SeedsConfiguration"] = seeds_config
    else:
        print("###### Config file error: Please check the SeedsConfiguration module of the config file provided.")


    ## Check SeedHostMatching:
    match_config_check = True
    match_config = config_dict["SeedHostMatching"]
    if match_config["method"]=="user_input":
        del match_config["randomly_generate"]
        if match_config["user_input"]["path_matching"] == "":
            print("The matching file has to be provided in the user input mode for seeds' generation.")
            match_config_check = False
        elif os.path.exists(match_config["user_input"]["path_matching"]) == False:
            print("Path to the provided matching file doesn't exists, please check your config file.")
            match_config_check = False
    elif match_config["method"]=="randomly_generate":
        del match_config["user_input"]
        if match_config["randomly_generate"]["method"] == "":
            print("Have to provide a matching scheme for the random generation of seed-host matching.")
            match_config_check = False
        else:
            if match_config["randomly_generate"]["method"] == "random":
                del match_config["randomly_generate"]["random"]
                del match_config["randomly_generate"]["ranking"]
                del match_config["randomly_generate"]["quantile"]
            elif match_config["randomly_generate"]["method"] == "ranking":
                del match_config["randomly_generate"]["random"]
                del match_config["randomly_generate"]["quantile"]
                if len(match_config["randomly_generate"]["ranking"])!=config_dict["SeedsConfiguration"]["seed_size"]:
                    print("Have to provide a one rank for each seed, i.e. length of the ranking parameter has to be the same length as seeds' size.")
                    match_config_check = False
                elif max(match_config["randomly_generate"]["ranking"])>=config_dict["NetworkModelParameters"]["host_size"]:
                    print("The ranks can't exceed the host population size.")
                    match_config_check = False
            elif match_config["randomly_generate"]["method"] == "quantile":
                del match_config["randomly_generate"]["random"]
                del match_config["randomly_generate"]["ranking"]
                if len(match_config["randomly_generate"]["quantile"])!=config_dict["SeedsConfiguration"]["seed_size"]:
                    print("Have to provide a quantile range for each seed, i.e. length of the quantile range parameter has to be the same length as seeds' size.")
                    match_config_check = False
                elif any(len(list(i))!=2 for i in match_config["randomly_generate"]["quantile"]):
                    print("Each quantile range has to be a list of the starting and ending quantile, i.e. [10, 25]")
                    match_config_check = False
                elif any(i[0]>i[1] for i in match_config["randomly_generate"]["quantile"]):
                    print("Starting quantile has to be smaller than ending quantile, i.e. [10, 25]")
                    match_config_check = False
                elif any(max(i)>100 or min(i)<0 for i in match_config["randomly_generate"]["quantile"]):
                    print("The quantile range has to be between 0 and 100")
                    match_config_check = False
            else:
                print("Have to provide a VALID matching scheme for the random generation of seed-host matching.")
                match_config_check = False
    if seeds_config_check:
        out_dict["SeedHostMatching"] = match_config
    else:
        print("###### Config file error: Please check the SeedHostMatching module of the config file provided.")


    ## Check GenomeElement:
    genome_config_check = False
    genome_config = config_dict["GenomeElement"]
    if genome_config["ref_path"]=="":
        print("Reference genome needs to be provided.")
        genome_config_check = False
    elif os.path.exists(genome_config["ref_path"])==False:
        print("Path to the provided reference genome doesn't exists.")
        genome_config_check = False
    if genome_config["use_genetic_model"]:
        if len(genome_config["traits_num"])==0:
            print("If you want to use genetic factors in simulation, traits number has to be specified.")
            genome_config_check = False
        elif len(genome_config["traits_num"])>2:
            print("You can only specify at most 2 numbers for traits number, representing transmissibility and drug resistance")
            genome_config_check = False
        if genome_config["effect_size"]["method"]=="user_input":
            del genome_config["effect_size"]["randomly_generate"]
            if genome_config["effect_size"]["user_input"]["path_effsize_table"]=="":
                print("Effect size needs to be provided.")
                genome_config_check = False
            elif os.path.exists(genome_config["effect_size"]["user_input"]["path_effsize_table"])==False:
                print("Path to the provided effect size doesn't exists.")
                genome_config_check = False
        elif genome_config["effect_size"]["method"]=="randomly_generate":
            del genome_config["effect_size"]["user_input"]
            if genome_config["effect_size"]["randomly_generate"]["gff"]=="":
                print("gff file needs to be provided in random generation mode.")
                genome_config_check = False
            elif os.path.exists(genome_config["effect_size"]["randomly_generate"]["gff"])==False:
                print("Path to the provided gff file doesn't exists.")
                genome_config_check = False
            for item in ["genes_num", "effsize_min", "effsize_max"]:
                if len(genome_config["effect_size"]["randomly_generate"][item])!=sum(genome_config["traits_num"]):
                    print(f"The {item} has to be a list that has the length of the number of traits.")
                    genome_config_check = False
    if genome_config_check:
        out_dict["GenomeElement"] = genome_config
    else:
        print("###### Config file error: Please check the GenomeElement module of the config file provided.")


    ## Check EpidemiologyModel:
    epi_config_check = True
    epi_config = config_dict["EpidemiologyModel"]
    if len(epi_config["method"]["epoch_changing_generation"])!=epi_config["method"]["n_epoch"] - 1:
        print("The epoch changing generation has to be a list that has the length of the number of epochs - 1. (default n_epoch=1)")
        epi_config_check = False
    if genome_config["use_genetic_model"]==False:
        if (any(sum(epi_config["genetic_architecture"][item])>0)):
            print("WARNING: The provided genetic architecture parameters won't be used in a non-genetic mode.")
            epi_config["genetic_architecture"] = {"transmissibility": [], "cap_transmissibility": [], "drug_resistance": [], "cap_drugresist": []}
            for i in range(epi_config["method"]["n_epoch"]):
                for j in epi_config["genetic_architecture"]:
                    epi_config["genetic_architecture"][j].append(0)
    else:
        for item in epi_config["genetic_architecture"]:
            if len(epi_config["genetic_architecture"][item])!=epi_config["method"]["n_epoch"]:
                print(f"The {item} has to be a list that has the length of the number of epochs.")
                epi_config_check = False
        if max(epi_config["genetic_architecture"]["transmissibility"])==0 and max(epi_config["genetic_architecture"]["drug_resistance"])==0:
            print("WARNING: Both transmissibility and drug resistance are not using any genetic effect size under a genetic mode. This is not recommended. If you want to run a non-genetic mode, you can just turn off genetic_architecture.")
        elif max(epi_config["genetic_architecture"]["cap_transmissibility"])==0 and max(epi_config["genetic_architecture"]["cap_drugresist"])==0:
            print("WARNING: Both transmissibility and drug resistance are having a cap being 0, so essentially not using any genetic effect size under a genetic mode. This is not recommended. If you want to run a non-genetic mode, you can just turn off genetic_architecture.")
        else:
            if max(epi_config["genetic_architecture"]["transmissibility"]) > genome_config["traits_num"][0]:
                print("The transmissibility effect size set you are using has to be one of the genetic effect size specified. i.e. cannot exceed the number of transmissibility traits.")
            if max(epi_config["genetic_architecture"]["transmissibility"]) > genome_config["traits_num"][0]:
                print("The drug resistance effect size set you are using has to be one of the genetic effect size specified. i.e. cannot exceed the number of drug resistance traits.")
    for rate in ["S_IE_rate", "I_R_rate", "R_S_rate", "sample_rate", "recovery_prob_after_sampling"]:
        if len(epi_config["transiton_rate"][rate]) > 0:
            if len(epi_config["transiton_rate"][rate])!=epi_config["method"]["n_epoch"]:
                print(f"The transition rate {rate} has to be a list that has the length of the number of epochs.")
                epi_config_check = False
        else:
            epi_config["transiton_rate"][rate]= []
            for i in range(epi_config["method"][rate]):
                epi_config["transiton_rate"][rate].append(0)
    if epi_config["method"]=="":
        print("Please specify an epidemiological model (SIR/SEIR)")
        epi_config_check = False
    elif epi_config["epoch_changing"]=="SIR":
        for rate in ["latency_prob", "E_I_rate", "I_E_rate", "E_R_rate"]:
            if len(epi_config["transiton_rate"][rate]) > 0:
                print(f"WARNING: The provided {rate} won't be used in an SIR model.")
            epi_config["transiton_rate"][rate] = []
            for i in range(epi_config["method"]["n_epoch"]):
                epi_config["transiton_rate"][rate].append(0)
    elif epi_config["epoch_changing"]=="SEIR":
        for rate in ["latency_prob", "E_I_rate", "I_E_rate", "E_R_rate"]:
            if len(epi_config["transiton_rate"][rate]) > 0:
                if len(epi_config["transiton_rate"][rate])!=epi_config["method"]["n_epoch"]:
                    print(f"The transition rate {rate} has to be a list that has the length of the number of epochs.")
                    epi_config_check = False
            else:
                epi_config["transiton_rate"][rate]= []
                for i in range(epi_config["method"]["n_epoch"]):
                    epi_config["transiton_rate"][rate].append(0)
    else:
        print("The epidemiological model provided isn't permitted.")
        epi_config_check = False
    if epi_config["massive_sampling"]["event_num"]==0:
        for lst in ["generation", "sampling_prob", "recovery_prob_after_sampling"]:
            if epi_config["massive_sampling"][lst]!=[]:
                print(f"WARNING: The provided {lst} won't be used if the massive sampling event number is 0.")
                epi_config["transiton_rate"][lst] = []
    else:
        for lst in ["generation", "sampling_prob", "recovery_prob_after_sampling"]:
            if len(epi_config["massive_sampling"][lst])!=epi_config["massive_sampling"]["event_num"]:
                print(f"WARNING: The provided {lst} has to be a list that has the length of the number of the massive sampling events.")
                epi_config_check = False

    if epi_config_check:
        out_dict["EpidemiologyModel"] = epi_config
    else:
        print("###### Config file error: Please check the EpidemiologyModel module of the config file provided.")
        
    ## Check Postprocessing_options:
    postprocess_config = config_dict["Postprocessing_options"]
    postprocess_config_check = True
    if genome_config["use_genetic_model"]==False:
        postprocess_config["tree_plotting"]["branch_color_trait"]=0
    else:
        if postprocess_config["tree_plotting"]["branch_color_trait"]>sum(genome_config["traits_num"]):
            print("Have to provide a valid trait number for coloring the tree. (between 0 and the total number of traits.)")
            postprocess_config_check = False
    if postprocess_config_check:
        out_dict["Postprocessing_options"] = postprocess_config_check
    else:
        print("###### Config file error: Please check the Postprocessing_options module of the config file provided.")

    return(all(base_config_check, evo_config_check, ntwk_config_check, seeds_config_check, match_config_check, genome_config_check, epi_config_check, postprocess_config_check), out_dict)


def dump_json(json2dump):
    out_config_path = os.path.join(json2dump["BasicRunConfiguration"]["cwdir"], "params.json")
    with open(out_config_path, 'w') as out_config:
        json.dump(json2dump, out_config, indent=4)







