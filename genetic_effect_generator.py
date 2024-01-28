from base_func import *
from genetic_effect_func import *
import argparse


def main():
	parser = argparse.ArgumentParser(description='Generate or modify seeds.')
	parser.add_argument('-method', action='store',dest='method', type=str, required=True, help="Method of the genetic element file generation")
	parser.add_argument('-wk_dir', action='store',dest='wk_dir', type=str, required=True, help="Working directory")
	parser.add_argument('-effsize_path', action='store',dest='effsize_path', type=str, required=False, help="Path to the user-provided effect size genetic element csv file", default="")
	parser.add_argument('-trait_n', action='store', nargs='+', dest='trait_n', type=int, required=False, help="Number of traits that user want to generate a genetic architecture for, 1st number for transmissibility, 2nd number for drug resistance", default=0)
	parser.add_argument('-causal_size_each','--causal_size_each', nargs='+', help='Size of causal genes for each trait', required=False, type=int, default=[])
	parser.add_argument('-es_low','--es_low', nargs='+', help='Lower bounds of effect size for each trait', required=False, type=float, default=[])
	parser.add_argument('-es_high','--es_high', nargs='+', help='Higher bounds of effect size for each trait', required=False, type=float, default=[])
	parser.add_argument('-gff', action='store',dest='gff', type=str, required=False, help='Path to the gff file', default="")
	parser.add_argument('-normalize','--normalize', default=False, required=False, type=str2bool, help='Whether to normalize the effect size based on sim_generations and mut_rate')
	parser.add_argument('-sim_generation', action='store',dest='sim_generation', required=False, type=float, default=0)
	parser.add_argument('-mut_rate', action='store',dest='mut_rate', required=False, type=float, default=0)



	args = parser.parse_args()
	method = args.method
	effsize_path = args.effsize_path
	gff_in = args.gff
	trait_n = args.trait_n
	causal_sizes = args.causal_size_each
	es_lows = args.es_low
	es_highs = args.es_high
	wk_dir = args.wk_dir
	n_gen = args.sim_generation
	mut_rate = args.mut_rate
	norm_or_not = args.normalize

	run_effsize_generation(method=method, wk_dir=wk_dir, effsize_path=effsize_path, gff_in=gff_in, trait_n=trait_n, causal_sizes=causal_sizes, es_lows=es_lows, es_highs=es_highs, norm_or_not=norm_or_not, n_gen=n_gen, mut_rate=mut_rate)


if __name__ == "__main__":
    main()