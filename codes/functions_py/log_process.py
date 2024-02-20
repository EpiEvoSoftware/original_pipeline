"""
Functions for processing the log files generated during simulated transmission.

Author: Perry Xu
Date: November 6, 2023
"""

def find_range_fit(range_list, query):
    """
    Return how many times an individual has been infected from the start to the current generation (inclusive).

    :param range_list: The list of generations during which recoveries happened for an individual.
    :type range_list: list[int]
    :param query: The current generation.
    :type query: int
    :return: The number of times an individual has been infected.
    :rtype: int
    """
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
    """
    Create a new log file with renamed infection information to incorporate the repetitive infections of an individual. More specifically, host_id is replaced by host_id_x, x being the times host_id has been infected. For example, host_id is originally 2023. It will be renamed to 2023_3 if the piece of log information is relevant to 2023's third infection.

    :param wk_dir_: The data directory for log files.
    :type wk_dir_: str
    :param pop_size_: The population size of host individuals.
    :type pop_size_: int
    """
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