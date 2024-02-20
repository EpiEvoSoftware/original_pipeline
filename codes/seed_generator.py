from base_func import *
from seeds_func import *
import argparse


def main():
	parser = argparse.ArgumentParser(description='Generate or modify seeds.')
	parser.add_argument('-method', action='store',dest='method', type=str, required=True, help="Method of the seed generation")
	parser.add_argument('-wkdir', action='store',dest='wkdir', type=str, required=True, help="Working directory")
	parser.add_argument('-seed_size', action='store',dest='seed_size', type=int, required=True, help="How many seeds is required")
	parser.add_argument('-seed_vcf', action='store',dest='seed_vcf', type=str, required=False, help="Path to the user-provided seeds' vcf", default="")
	parser.add_argument('-Ne', action='store',dest='Ne', type=int, required=False, help="Ne for a WF model, required in WF burn-in mode", default=0)
	parser.add_argument('-ref_path', action='store',dest='ref_path', type=str, required=False, help="Reference genome path, required in SLiM burn-in", default="")
	parser.add_argument('-mu', action='store',dest='mu', type=float, required=False, help="Mutation rate, required in SLiM burn-in", default=0)
	parser.add_argument('-n_gen', action='store',dest='n_gen', type=int, required=False, help="Number of generations of the burn-in process, required in SLiM burn-in", default=0)
	parser.add_argument('-path_seeds_phylogeny', action='store',dest='path_seeds_phylogeny', type=str, required=False, help="Phylogeny of the provided seeds", default="")
	parser.add_argument('-host_size', action='store',dest='host_size', type=int, required=False, help="Size of the host population", default=0)
	parser.add_argument('-seeded_host_id','--seeded_host_id', nargs='+', help='IDs of the host(s) that are seeded', required=False, type=int, default=[])
	parser.add_argument('-S_IE_rate', action='store',dest='S_IE_rate', type=float, required=False, help="Probability of transmission for each contact pair per generation", default=0)
	parser.add_argument('-E_I_rate', action='store',dest='E_I_rate', type=float, required=False, help="Probability of activation (E>I) for each infected host per generation", default=0)
	parser.add_argument('-E_R_rate', action='store',dest='E_R_rate', type=float, required=False, help="Probability of recovery (E>R) for each exposed host per generation", default=0)
	parser.add_argument('-latency_prob', action='store',dest='latency_prob', type=float, required=False, help="Probability of being a latent infection per infection event", default=0)
	parser.add_argument('-I_R_rate', action='store',dest='I_R_rate', type=float, required=False, help="Probability of recovery (I>R) for each infected host per generation", default=0)
	parser.add_argument('-I_E_rate', action='store',dest='I_E_rate', type=float, required=False, help="Probability of deactivation (I>E) for each infected host per generation", default=0)
	parser.add_argument('-R_S_rate', action='store',dest='R_S_rate', type=float, required=False, help="Probability of immunity loss (R>S) for each recovered host per generation", default=0)



	args = parser.parse_args()

	method = args.method
	wk_dir = args.wkdir
	seed_size = args.seed_size
	seed_vcf = args.seed_vcf
	Ne = args.Ne
	ref_path = args.ref_path
	mu = args.mu
	n_gen = args.n_gen
	path_seeds_phylogeny = args.path_seeds_phylogeny
	host_size = args.host_size
	seeded_host_id = args.seeded_host_id
	S_IE_rate = args.S_IE_rate
	E_I_rate = args.E_I_rate
	E_R_rate = args.E_R_rate
	latency_prob = args.latency_prob
	I_R_rate = args.I_R_rate
	I_E_rate = args.I_E_rate
	R_S_rate = args.R_S_rate

	run_seed_generation(method=method, wk_dir=wk_dir, seed_size=seed_size, seed_vcf=seed_vcf, Ne=Ne, ref_path=ref_path, mu=mu, n_gen=n_gen, path_seeds_phylogeny=path_seeds_phylogeny, host_size=host_size, seeded_host_id=seeded_host_id, S_IE_rate=S_IE_rate, E_I_rate=E_I_rate, E_R_rate=E_R_rate, latency_prob=latency_prob, I_R_rate=I_R_rate, I_E_rate=I_E_rate, R_S_rate=R_S_rate)


if __name__ == "__main__":
    main()


