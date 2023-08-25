import argparse


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", '--sbn_file', default="G:\github\PMB5.0.0\data\pmb-5.0.0\seq2seq\\zh\\test\standard.sbn", type=str)
    parser.add_argument("-s2", '--write_file', default="G:\github\PMB5.0.0\data\pmb-5.0.0\src\penman\\zh\\standard.out", type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = create_arg_parser()

    sbn_path = args.sbn_file
    write_path = args.write_file

    with open(sbn_path, "r", encoding="utf-8") as f:
        lines = f. readlines()

        with open(write_path, "w", encoding="utf-8") as w:
            for line in lines:
                l = line.split("\t")[1]
                w.write(l)
