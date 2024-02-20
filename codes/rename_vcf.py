import argparse


## A function tp read the samples'log file <final_n_samples> and store all the information
def sample_txt_read(wkdir_):
    # <samples> is a dictionary that the key is sampled generation, and value is a list that includes all names of samples sampled at that generation
    samples = {}
    with open(wkdir_ + "final_n_samples.txt", "r") as txt:
        for line in txt:
            ll = line.rstrip("\n")
            l = ll.split(" ")
            #real_id = l[1].split("_")
            if int(l[0]) in samples:
                samples[int(l[0])].append(l[1])
            else:
                samples[int(l[0])] = [l[1]]
    return(samples)

 
def get_new_vcf(wkdir_, samples):
    for i in samples:
        with open(wkdir_ + "sample_vcfs/" + str(i) + ".sampled.vcf", "r") as vcf_in:
            with open(wkdir_ + "sample_vcfs/" + str(i) + ".sampled.named.vcf", "w") as vcf_out:
                for line in vcf_in:
                    if line.startswith("##"):
                        vcf_out.write(line)
                    elif line.startswith("#"):
                        ll = line.rstrip("\n")
                        l = ll.split("\t")
                        write_line = "\t".join(l[:9]) + "\t" + "\t".join(samples[i]) + "\n"
                        vcf_out.write(write_line)
                    else:
                        vcf_out.write(line)
    return(0)
 


def main():
    parser = argparse.ArgumentParser(description='Rename the vcfs.')
    parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)

    args = parser.parse_args()
    wk_dir_ = args.wk_dir

    
    get_new_vcf(wk_dir_, sample_txt_read(wk_dir_))

	
    

if __name__ == "__main__":
	main()
            

