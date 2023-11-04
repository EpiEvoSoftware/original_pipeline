import tskit
import re
import argparse

## This script read the tree file from SLiM burn-in output and find the samples' true genealogy.
## As it's a forward-in-time simulation, the tree doesn't necessarily coalesce.
## If the tree doesn't coalesce, i.e., having multiple roots, 


def tree_process(wk_dir, scale_t_):
    seeds_id = {}
    seeds = []
    ## Read the file that store the correspondance between seed index and index from the burn-in simulation
    ## Store ids of the seeds to the list <seeds>
    ## For every individual, there are two genomes while one of the is null (as we are simulating haploid individual)
    ## We thus only choose the first tree (the tree that has mutation), the second tree is of the same topology but no mutation
    with open(wk_dir + "seeds.tree.id.txt", "r") as ids:
        for line in ids:
            ll = line.rstrip("\n")
            l = ll.split(" ")
            genome_id = 2 * int(l[1])
            seeds_id[l[1]] = l[0]
            seeds.append(genome_id)

    ## Read the tree file, which includes all genomes in the last generation of the SLiM simulation
    ts = tskit.load(wk_dir + "seeds.trees")
    ## Filter the seeds file, simplify to only include the sampled genomes i.e. seeds.
    sampled_tree = ts.simplify(samples = seeds, filter_populations=False, filter_individuals=False, filter_sites=False, filter_nodes=False)
    roots_all = sampled_tree.first().roots
    
    ## Write the simplified tree into <seeds.burn_in_id.nwk>, but the name id of tips take their id from the burn-in simulation.
    with open(wk_dir + "seeds.burn_in_id.nwk", "w") as nwk:
        for i in roots_all:
            nwk.write(sampled_tree.first().as_newick(root=i))


    nwk_ori = open(wk_dir + "seeds.burn_in_id.nwk", "r+")
    nwk_out = open(wk_dir + "seeds.nwk", "a+")

    for tree_l in nwk_ori.readlines():
        new = tree_l
        ## substitute the id from burn-in simulation to the new / true simulation host id in the tree string, and store it to <seeds.nwk>
        for j in seeds_id:
            sub_ = "n" + str(2 * int(j))
            new = re.sub(sub_, seeds_id[j], new)
        
        new_nwk = ""
        number = False
        number_str = ""
        for j in new:
            if number==True:
                if j==")" or j==",":
                    number = False
                    ## Since in the burn-in part, people may want to use a different time scale than the main simulation part
                    ## We provide a way to rescale the branch length by scaling parameter <scale_t_>.
                    new_nwk = new_nwk + str(scale_t_ * int(number_str)) + j
                    number_str = ""
                else:
                    number_str = number_str + j
            else:
                if j==":":
                    number = True
                new_nwk = new_nwk + j

        nwk_out.write(new_nwk)
    nwk_ori.close()
    nwk_out.close()




def main():
    parser = argparse.ArgumentParser(description='Process the .trees output from SLiM, output the whole tree of seed individuals.')
    parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)
    parser.add_argument('-scale_time', action='store',dest='scale_time', required=True, type=float)

    args = parser.parse_args()

    wk_dir = args.wk_dir
    scale_t = args.scale_time

    tree_process(wk_dir, scale_t)
    #print(match(gen1, genf))
    

if __name__ == "__main__":
    main()

