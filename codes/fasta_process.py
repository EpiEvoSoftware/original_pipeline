## This script includes all function to modify fasta files


def time_fasta(_wkdir, start_y, start_m, fa_):
    sample_time = {}
    with open(_wkdir + "epidemiology_log/final_n_samples.txt", "r") as txt:
        for line in txt:
            ll = line.rstrip("\n")
            l = ll.split(" ")
            time_from_start = int(l[0])
            mon_add = start_m + time_from_start % 12
            yr_add = start_y + time_from_start // 12
            if mon_add > 12:
                yr_add = yr_add + 1
                mon_add = mon_add - 12
            if mon_add<10:
                sample_time["p" + l[1]] = "-".join([str(yr_add), "0" + str(mon_add), "01"])
            else:
                sample_time["p" + l[1]] = "-".join([str(yr_add), str(mon_add), "01"])
            
    with open(_wkdir + fa_, "r") as fa_in:
        with open(_wkdir + fa_[:-5] + "timed.fasta", "w") as fa_out:
            for line in fa_in:
                if line.startswith(">"):
                    ll = line.rstrip("\n")
                    l = ll.lstrip(">")
                    fa_out.write(ll + "|" + sample_time[l] + "\n")
                else:
                    fa_out.write(line)