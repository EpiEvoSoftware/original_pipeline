import argparse

def modify_vcf(_wkdir):
    with open(_wkdir + "samples.merged.vcf", "r") as vcf_in:
        with open(_wkdir + "samples.merged.modified.vcf", "w") as vcf_out:
            for line in vcf_in:
                if line.startswith("##"):
                    continue
                elif line.startswith("#"):
                    vcf_out.write(line)
                else:
                    ll = line.rstrip("\n")
                    l = ll.split("\t")
                    if len(l[4])==1:
                        alt = [l[4]]
                    else:
                        alt = l[4].split(",")
                    newline = "\t".join(l[:9])
                    #newline = "\t".join(l[:4])
                    for i in l[9:]:
                        if i=="0" or i==".":
                            newline = newline + "\t0"
                        else:
                            newline = newline + "\t" + i
                        
                    newline = newline + "\n"
                    vcf_out.write(newline)



def main():
    parser = argparse.ArgumentParser(description='Rename the vcfs.')
    parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)

    args = parser.parse_args()
    wk_dir_ = args.wk_dir

    modify_vcf(wk_dir_)


if __name__ == "__main__":
	main()
