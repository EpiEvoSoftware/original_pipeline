from base_func import *
from seeds_func import *
import argparse


def main():
	parser = argparse.ArgumentParser(description='Generate or modify seeds.')
	parser.add_argument('-method', action='store',dest='method', type=str, required=True, help="Method of the seed generation")
	parser.add_argument('-wk_dir', action='store',dest='wk_dir', type=str, required=True, help="Working directory")
	parser.add_argument('-seed_size', action='store',dest='seed_size', type=int, required=True, help="How many seeds is required")
	parser.add_argument('-seed_vcf', action='store',dest='seed_vcf', type=str, required=False, help="Path to the user-provided seeds' vcf", default="")
	parser.add_argument('-Ne', action='store',dest='Ne', type=int, required=False, help="Ne for a WF model, required in WF burn-in mode", default=0)
	parser.add_argument('-ref_path', action='store',dest='ref_path', type=str, required=False, help="Reference genome path, required in SLiM burn-in", default="")
	parser.add_argument('-mu', action='store',dest='mu', type=float, required=False, help="Mutation rate, required in SLiM burn-in", default=0)
	parser.add_argument('-n_gen', action='store',dest='n_gen', type=int, required=False, help="Number of generations of the burn-in process, required in SLiM burn-in", default=0)



	args = parser.parse_args()

	method = args.method
	wk_dir = args.wk_dir
	seed_size = args.seed_size
	seed_vcf = args.seed_vcf
	Ne = args.Ne
	ref_path = args.ref_path
	mu = args.mu
	n_gen = args.n_gen

	run_seed_generation(method=method, wk_dir=wk_dir, seed_size=seed_size, seed_vcf=seed_vcf, Ne=Ne, ref_path=ref_path, mu=mu, n_gen=n_gen)


if __name__ == "__main__":
    main()


