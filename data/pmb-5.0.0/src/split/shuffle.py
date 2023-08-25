'''
Script that selects train, dev and test sets for sbn
'''

import argparse
import random

def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", '--input_file', type=str, help="Input file which needs shuffle")
    parser.add_argument("-o", '--output_file', type=str, help="output file stores the shuffled result")
    parser.add_argument("-rs", '--random_seed', default=32, type=int, help="Random seed for shuffling of the data -- use our default 32 to get our version")
    args = parser.parse_args()
    return args


def shuffle(data_path, output_path, seed):
    random_list = []
    with open(data_path, "r", encoding="utf-8") as f:
        data = f.readlines()

    tmp_list = []
    for line in data:
        if line != "\n":
            tmp_list.append(line)
        else:
            random_list.append(tmp_list)
            tmp_list = []
    
    random.seed(seed)
    random.shuffle(random_list)

    with open(output_path, "w", encoding="utf-8") as w:
        for i in range(len(random_list)):
            tmp_list = random_list[i]
            for j in range(len(tmp_list)):
                w.write(tmp_list[j])
            w.write("\n")


if __name__ == "__main__":
    args = create_arg_parser()
    random_seed = args.random_seed

    shuffle(args.input_file, args.output_file, seed=random_seed)

