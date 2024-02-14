import argparse


## Split the vcfs to make them separate vcf files for each seed to facilitate SLiM to read
def modify_vcf(wkdir, seed_size):
    with open(wkdir + "seeds.vcf", "r") as vcf:
        for line in vcf:
            if line.startswith("##"):
                for i in range(seed_size):
                    with open(wkdir + "seed." + str(i) + ".vcf", "a") as newvcf:
                        newvcf.write(line)
            elif line.startswith("#"):
                ll = line.rstrip("\n")
                l = ll.split("\t")
                for i in range(seed_size):
                    with open(wkdir + "seed." + str(i) + ".vcf", "a") as newvcf:
                        newvcf.write("\t".join(l[:10]) + "\n")
            else:
                ll = line.rstrip("\n")
                l = ll.split("\t")
                for i in range(seed_size):
                    if (l[9+i]=="0|0"):
                        continue
                    else:
                        ref = l[3]
                        geno = l[9+i].split("|")[0]
                        if len(l[4]) > 1:
                            alt = l[4].split(",")
                            with open(wkdir + "seed." + str(i) + ".vcf", "a") as newvcf:
                                newvcf.write("\t".join(l[:4]) + "\t" + alt[int(geno)-1] + "\t1000\tPASS\tS=0;DOM=1;TO=1;MT=0;AC=1;DP=1000;AA=" + ref + "\tGT\t1\n")
                        else:
                            alt = l[4]
                            with open(wkdir + "seed." + str(i) + ".vcf", "a") as newvcf:
                                newvcf.write("\t".join(l[:7]) + "\tS=0;DOM=1;TO=1;MT=0;AC=1;DP=1000;AA=" + ref + "\tGT\t" + geno + "\n")



def main():
    parser = argparse.ArgumentParser(description='Split and modify the vcfs.')
    parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)
    parser.add_argument('-seed_size', action='store',dest='seed_size', type=int, required=True)

    args = parser.parse_args()
    wk_dir_ = args.wk_dir
    seed_size_ = args.seed_size
    modify_vcf(wk_dir_, seed_size_)

if __name__ == "__main__":
    main()