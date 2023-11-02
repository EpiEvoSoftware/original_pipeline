def modify_vcf(mss):
	### When using SLiM burn-in, don't need to run this.
	### When user provided seeds' vcf, using this function to modify
	return(0)



def main():
	parser = argparse.ArgumentParser(description='Generate the selection coefficient modifying part of the slim script.')
	parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)

	args = parser.parse_args()
	mss = args.wk_dir

	modify_vcf(mss) 

    

if __name__ == "__main__":
	main()