from base_func import *
from seed_host_match_func import *
import argparse


def main():
	parser = argparse.ArgumentParser(description='Generate or modify seeds.')
	parser.add_argument('-config', action='store',dest='config', type=str, required=True, help="Path to the config file")

	args = parser.parse_args()

	config_path = args.config

	all_slim_simulation_by_config(read_params(config_path))


if __name__ == "__main__":
    main()