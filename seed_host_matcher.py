from base_func import *
from seed_host_match_func import *
import argparse


def main():
	parser = argparse.ArgumentParser(description='Match seeds and hosts.')
	parser.add_argument('-method',  action='store',dest='method', type=str, required=True, help="Method of the seed host matching")
	parser.add_argument('-wkdir', action='store',dest='wkdir', type=str, required=True, help="Working directory")
	parser.add_argument('-seed_size', action='store',dest='seed_size', type=int, required=True, help="Number of seeds to be matched.")
	parser.add_argument('-host_size', action='store',dest='host_size', type=int, required=True, help="Number of hosts to be matched.")
	parser.add_argument('-path_matching',  action='store',dest='path_matching', type=str, required=False, help="Path to the user-provided matching file", default="")
	parser.add_argument('-match_scheme',  action='store',dest='match_scheme', type=str, required=False, help="Scheme of matching", default="")
	parser.add_argument('-ranking','--ranking', nargs='+', help='Ranking of the host contact degree for each seed.', required=False, type=int, default=[])
	parser.add_argument('-percentile','--percentile', nargs='+', help='Percentile ranges of the host contact degree for each seed.', required=False, type=int, default=[])


	args = parser.parse_args()

	method = args.method
	wkdir = args.wkdir
	seed_size = args.seed_size
	host_size = args.host_size
	path_matching = args.path_matching
	match_scheme = args.match_scheme
	ranking = args.ranking
	percentile = args.percentile


	run_seed_host_match(method=method, wkdir=wkdir, seed_size=seed_size, host_size=host_size, path_matching=path_matching, match_scheme=match_scheme, ranking=ranking, percentile=percentile)


if __name__ == "__main__":
    main()