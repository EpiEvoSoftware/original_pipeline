import argparse


## A function to find the order of appearance for one transition event or infection event
def find_range_fit(range_list, query):
    if len(range_list)==0:
        return(1)
    elif query <= min(range_list):
        return(1)
    elif query > max(range_list):
        return(len(range_list) + 1)
    else:
        for i in range(len(range_list)-1):
            if query > range_list[i] and query <= range_list[i+1]:
                return(i+2)



def rename_logfiles(wk_dir_, pop_size_):
    recover_matrix = {}

    for i in range(pop_size_):
        recover_matrix[i]=[]

    with open(wk_dir_ + "recovery.txt", "r") as rec_in:
        with open(wk_dir_ + "recovery.renamed.txt", "w") as rec_out:
            for line in rec_in:
                ll = line.rstrip("\n")
                l = ll.split(" ")
                recover_matrix[int(l[1])].append(int(l[0]))
                rec_out.write(l[0] + " " + l[1] + "_" + str(len(recover_matrix[int(l[1])])) + "\n")

    with open(wk_dir_ + "sample.txt", "r") as smp_in:
        with open(wk_dir_ + "final_n_samples.txt", "w") as smp_out:
            for line in smp_in:
                ll = line.rstrip("\n")
                l = ll.split(" ")
                id_smp = find_range_fit(recover_matrix[int(l[1])], int(l[0]))
                smp_out.write(l[0] + " " + l[1] + "_" + str(id_smp) + "\n")


    with open(wk_dir_ + "infection.txt", "r") as inf_in:
        with open(wk_dir_ + "infection.renamed.txt", "w") as inf_out:
            for line in inf_in:
                ll = line.rstrip("\n")
                l = ll.split(" ")
                id_infector = find_range_fit(recover_matrix[int(l[1])], int(l[0]))
                id_infectee = find_range_fit(recover_matrix[int(l[2])], int(l[0]))
                inf_out.write(l[0] + " " + l[1] + "_" + str(id_infector) + " " + l[2] + "_" + str(id_infectee) + "\n")



def main():
    parser = argparse.ArgumentParser(description='Rename the vcfs.')
    parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)
    parser.add_argument('-pop_size', action='store',dest='pop_size', required=True, type=int)

    args = parser.parse_args()
    wk_dir_ = args.wk_dir
    pop_size_ = args.pop_size

    
    rename_logfiles(wk_dir_, pop_size_)

    
    

if __name__ == "__main__":
    main()
            
