




def main():
	parser = argparse.ArgumentParser(description='Generate the selection coefficient modifying part of the slim script.')
	parser.add_argument('-causal_dr', action='store',dest='causal_dr', required=True)
	parser.add_argument('-causal', action='store',dest='causal', required=True, type=int)
	parser.add_argument('-es_low', action='store',dest='es_low', required=True, type=float)
	parser.add_argument('-es_high', action='store',dest='es_high', required=True, type=float)
	parser.add_argument('-wk_dir', action='store',dest='seeds_dir', required=True)

	args = parser.parse_args()
	gff_in = args.gff
	causal_size = args.causal
	effsize_low = args.es_low
	effsize_high = args.es_high
	mss = args.seeds_dir


	generate_eff(gff_in, causal_size, effsize_low, effsize_high, mss)
    

if __name__ == "__main__":
	main()