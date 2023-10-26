import argparse


def rename_by_host(wkdir):
	all_names = {}
	with open(wkdir + "seeds.name", "r") as names:
		for line in names:
			ll = line.rstrip("\n")
			l = ll.split(",p")
			all_names[l[0]] = l[1]
	nwk_ori = open(wkdir + "seeds.nwk", "r+")
	nwk_out = open(wkdir + "seeds.renamed.nwk", "a+")
	for tree_l in nwk_ori.readlines():
		take = 0
		index_now = ""
		new_line = ""
		for i in tree_l:
			if take==0:
				if i=="(" or i==",":
					take = 1
				new_line = new_line + i
			elif take==1:
				if i=="(":
					index_now = ""
					new_line = new_line + i
				elif i==":":
					take = 0
					new_line = new_line + all_names[index_now] + "_1:"
					index_now = ""
				else:
					index_now = index_now + i
	nwk_out.write(new_line)




def main():
    parser = argparse.ArgumentParser(description='Process the .trees output from SLiM, output the whole tree of seed individuals.')
    parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)

    args = parser.parse_args()

    wk_dir = args.wk_dir

    rename_by_host(wk_dir)
    

if __name__ == "__main__":
    main()