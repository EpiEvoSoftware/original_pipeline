### The main script to run the whole pipeline
import argparse
from base_func import *
from seeds_func import *
from genetic_effect_func import *
from seed_host_match_func import *
from simulation_func import *



def main():
	parser = argparse.ArgumentParser(description='Run the whole simulation process by the configuration provided.')
	parser.add_argument('-path_config', action='store',dest='path_config', required=True, help="Path to config file (json)")

	args = parser.parse_args()

	config_path = args.path_config

	## Read the parameters and store them into a dictionary
	param_dict = read_params(config_path)
	config_valid, checked_params_dict = check_config(param_dict)
	if config_valid:
		## Network generation
		network_generation_byconfig(checked_params_dict)

		## Seeds generation
		seeds_generation_byconfig(checked_params_dict)

		## Effect size generation
		effsize_generation_byconfig(checked_params_dict)

		## Seed-host match
		seed_host_match_byconfig(checked_params_dict) ######## UNIFINISHED

		## Simulation
		all_slim_simulation_by_config(checked_params_dict)

	else:
		print("========== Terminated because of incorrect configuration. ==========")


if __name__ == "__main__":
    main()