### The main script to run the whole pipeline
import argparse
from base_func import *
from seeds_func import *
from genetic_effect_func import *



def main():
	parser = argparse.ArgumentParser(description='Process the .trees output from SLiM, output the whole tree of seed individuals.')
	parser.add_argument('-path_config', action='store',dest='path_config', required=True, help="Path to config file (json)")

	args = parser.parse_args()

	config_path = args.path_config

	## Read the parameters and store them into a dictionary
	param_dict = read_params(config_path)

	## Seeds generation
	seeds_generation_byconfig(param_dict)

	## Effect size generation
	effsize_generation_byconfig(param_dict)


if __name__ == "__main__":
    main()