import argparse
import os


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--index', default="./standard.idx", help="index file")
    parser.add_argument("-r", '--root', default="/net/gsb/pmb/out", help="root of ccg files")
    parser.add_argument("-s", '--save_path', default="./standard", help="Path to save ccg files")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = create_arg_parser()

    index_path = args.index
    root_path = args.root
    save_path = args.save_path

    with open(index_path, "r", encoding="utf-8") as f:
        index = f.readlines()

    for ind in index:
        ind = ind.strip()
        print(f"extracting {ind}")
        with open(os.path.join(root_path, f"{ind}/en.parse.tags"), "r", encoding="utf-8") as f:
            ccg = f.read()

        ind = ind.replace("/", "_")
        with open(os.path.join(save_path, f"{ind}.ccg"), "w", encoding="utf-8") as w:
            w.write(ccg)

