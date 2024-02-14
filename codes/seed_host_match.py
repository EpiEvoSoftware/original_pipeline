import argparse
import random

def random_seedmatch(seed_size, host_size):
    who_2_plant = random.sample(range(host_size), seed_size)
    dict_sh = {who_2_plant[i]:i for i in range(seed_size)}
    return({key: dict_sh[key] for key in sorted(dict_sh)})

def write_match(match, wk_dir):
    with open(wk_dir + "seed_host_match.csv", "w") as match_doc:
        for i in match:
            match_doc.write(str(i) + "," + str(match[i]) + "\n")


def main():
    parser = argparse.ArgumentParser(description='Rename the vcfs.')
    parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True, type=str)
    parser.add_argument('-seed_size', action='store',dest='seed_size', required=True, type=int)
    parser.add_argument('-host_size', action='store',dest='host_size', required=True, type=int)
    parser.add_argument('-match_method', action='store',dest='match_method', required=True, type=str)

    args = parser.parse_args()
    wk_dir_ = args.wk_dir
    host_size_ = args.host_size
    seed_size_ = args.seed_size
    match_m_ = args.match_method

    if match_m_=="random":
    	write_match(random_seedmatch(seed_size_, host_size_), wk_dir_)

    
if __name__ == "__main__":
    main()
