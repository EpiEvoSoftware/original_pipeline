### The main script to run the whole pipeline
import argparse
from base_func import *
from network_generator import network_generation_byconfig
from seed_generator import seeds_generation_byconfig
from genetic_effect_generator import effsize_generation_byconfig
from seed_host_matcher import read_config_and_match
from outbreak_simulator import all_slim_simulation_by_config



def main():
	parser = argparse.ArgumentParser(description='Run the whole simulation process by the configuration provided.')
	parser.add_argument('-path_config', action='store',dest='path_config', required=True, help="Path to config file (json)")

	args = parser.parse_args()

	config_path = args.path_config

	## Read the parameters and store them into a dictionary
	param_dict = read_params(config_path, "base_params.json")

	# try:
	# Network generation
	network_generation_byconfig(param_dict)

	## Seeds generation
	seeds_generation_byconfig(param_dict)

	## Effect size generation
	effsize_generation_byconfig(param_dict)

	## Seed-host match
	read_config_and_match(param_dict) ######## UNIFINISHED

	## Simulation
	all_slim_simulation_by_config(param_dict)

	# except Exception as e:
	# 	print(e)


if __name__ == "__main__":
	main()