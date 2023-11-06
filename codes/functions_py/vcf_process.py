"""
Functions for modifying vcf files (intermediate files or input files)

Author: Perry Xu
Date: November 6, 2023
"""

def convert_external_vcf(vcf, wkdir):
    """
    Create a SLiM-readable vcf format based on customized vcf input as opposed to SLiM generated vcf.

    :param vcf: The vcf file path
    :type vcf: str
    :param wkdir: The path to store generated vcf
    :type wkdir: str
    """
    with open(vcf, "r") as vcf_external:
        with open(wkdir + "seeds.vcf", "a") as newvcf:
            newvcf.write("##fileformat=VCFv4.2\n##INFO=<ID=S,Number=.,Type=Float,Description=\"Selection Coefficient\">\n##INFO=<ID=DOM,Number=.,Type=Float,Description=\"Dominance\">\n##INFO=<ID=PO,Number=.,Type=Integer,Description=\"Population of Origin\">\n##INFO=<ID=TO,Number=.,Type=Integer,Description=\"Tick of Origin\">\n##INFO=<ID=MT,Number=.,Type=Integer,Description=\"Mutation Type\">\n##INFO=<ID=AC,Number=.,Type=Integer,Description=\"Allele Count\">\n##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total Depth\">\n##INFO=<ID=AA,Number=1,Type=String,Description=\"Ancestral Allele\">\n##INFO=<ID=NONNUC,Number=0,Type=Flag,Description=\"Non-nucleotide-based\">\n##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n##source=GenomicsDBImport\n##source=SelectVariants\n##source=VariantFiltration\n")
            for line in vcf_external:
                if line.startswith("##"):
                    continue
                elif line.startswith("#"):
                    newvcf.write(line)
                else:
                    ll = line.rstrip("\n")
                    l = ll.split("\t")
                    num_seeds = len(l) - 9
                    ref = l[3]
                    geno = l[9+i].split("|")[0]
                    if len(l[4]) > 1:
                        alt = l[4].split(",")
                    new_line = "\t".join(l[:5]) + "\t1000\tPASS\tS=0;DOM=1;TO=1;MT=0;AC=1;DP=1000;AA=" + ref + "\tGT"
                    for i in range(num_seeds):
                        if (l[9+i]=="0|0" or l[9+i]=="0/0"):
                            new_line = new_line + "\t0" 
                        else:
                            for j in range(1, len(alt)):
                                if str(j) in l[9+i]:
                                    new_line = new_line + "\t" + str(j)
                                    break        
                    newvcf.write(new_line + "\n")


## This function should probably be put in <log_process.py> since it's reading from log files, but the returned value <samples> will be used
## in converting vcf files (in function <get_new_vcf>)
def sample_txt_read(wkdir_):
    """
    Returns a dictionary documenting generation (keys) and host_ids sampled in that generation (values).

    :param wkdir_: The data directory of sampled individuals's information.
    :type wkdir_: str
    :return: A dictionary with generation (keys) and host_ids sampled in that generation (values).
    :rtype: dict[int, list[?]]
    """
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
    """
    Creates vcfs with renamed columns. It replaces i0, i1, ..., in the columns of SLiM outputed vcf with host IDs.

    :param wkdir_: The data directory of SLiM vcf outputs about sampled individuals.
    :type wkdir_: str
    :param samples: The dictionary with generation (keys) and host_ids sampled in that generation (values).
    :type samples: dict[int, list[?]]
    """
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


def modify_vcf(_wkdir):
    """
    ???
    """
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

def split_vcf(wkdir):
    """
    ???
    """
    with open(wkdir + "seeds.vcf", "r") as vcf:
        for line in vcf:
            if line.startswith("##"):
                for i in range(10):
                    with open(wkdir + "seed." + str(i) + ".vcf", "a") as newvcf:
                        newvcf.write(line)
            elif line.startswith("#"):
                ll = line.rstrip("\n")
                l = ll.split("\t")
                for i in range(10):
                    with open(wkdir + "seed." + str(i) + ".vcf", "a") as newvcf:
                        newvcf.write("\t".join(l[:10]) + "\n")
            else:
                ll = line.rstrip("\n")
                l = ll.split("\t")
                for i in range(10):
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




