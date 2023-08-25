#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
Script that selects train, dev and test sets for sbn
'''

import argparse
import os
import re
import random
import Levenshtein
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", '--release_root', type=str, help="Root of release files")
    parser.add_argument("-o", '--output_folder', type=str, help="Folder to write output DRSs to (file-names are standardized)")
    parser.add_argument("-sk", '--skip_file', type=str, help="skip index file")
    parser.add_argument("-s", '--skip', default=False, type=bool, help="skip or not")
    parser.add_argument("-l", '--language', default="en", choices=['en', 'de', 'nl', 'it', "ja"], type=str, help="Languages we select")
    parser.add_argument("-p", '--plot', default=True, type=bool, help="plot the figure or not")
    parser.add_argument("-d", '--data_type', default="gold", choices=['gold', 'silver', 'bronze'], help="Whether we extract gold/silver/bronze data")
    parser.add_argument("-rs", '--random_seed', default=32, type=int, help="Random seed for shuffling of the data -- use our default 32 to get our version")
    args = parser.parse_args()
    return args


def skip(raw_dict, lst):
    if lst != []:
        new_dict = {}
        for key in raw_dict.keys():
            if key in lst:
                print(f"skip {key}")
            else:
                new_dict[key] = raw_dict.get(key)

        return new_dict
    else:
        return raw_dict


def detect_remove_duplicate(raw_dict):
    """
    remove duplicates
    """
    value_count = {}

    # count the keys
    for key, value in raw_dict.items():
        if not value_count.get(value):
            value_count[value] = [key]
        else:
            value_count[value].append(key)

    # detect
    new_dict = {}
    duplicates = []
    for value, keys in value_count.items():
        new_dict[keys[0]] = raw_dict[keys[0]]
        if len(keys) > 1:
            duplicates.append(keys)

    print(f"{len(duplicates)} duplicates cluster have been found:")
    for i in range(len(duplicates)):
        print(duplicates[i])

    return new_dict


def length_distribution(path, string_list):
    """
    plot the distribution of string list
    """
    print("Generate distribution...")
    char_lengths = [len(s) for s in string_list]
    word_lengths = [len(s.split()) for s in string_list]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))

    ax1.hist(char_lengths, bins=range(min(char_lengths), max(char_lengths) + 2), align='left', alpha=0.75)
    ax1.set_xlabel('Character Length')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Distribution of Character Length')
    ax1.grid(True)

    ax2.hist(word_lengths, bins=range(min(word_lengths), max(word_lengths) + 2), align='left', alpha=0.75)
    ax2.set_xlabel('Word Length')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Word Length')
    ax2.grid(True)

    fig.tight_layout()

    plt.savefig(path, dpi=300)


def extract_values(raw_dict, keys):
    values = []
    for k in keys:
        values.append(raw_dict[k])
    return values


def read_files_in_folder(folder_path, lang, data_type, skip_lst):
    p = os.listdir(os.path.join(folder_path, f"{lang}/{data_type}"))

    raw_dict = {}
    for sub_p in p:
        d = os.listdir(os.path.join(folder_path, f"{lang}/{data_type}/{sub_p}"))

        for sub_d in d:
            try:
                with open(os.path.join(folder_path, f"{lang}/{data_type}/{sub_p}/{sub_d}/{lang}.raw"), "r", encoding="utf-8") as f:
                    raw = f.readlines()
                    raw = "".join(raw)
            except Exception as e:
                print(e)
            if not raw_dict.get(f"{sub_p}/{sub_d}"):
                raw_dict[f"{sub_p}/{sub_d}"] = raw.replace("\n", "")
            else:
                print(f"duplicate {sub_p}/{sub_d}")

    # sort the dict
    raw_dict = detect_remove_duplicate(raw_dict)
    raw_dict = skip(raw_dict, skip_lst)
    sorted_dict = dict(sorted(raw_dict.items(), key=lambda item: len(item[1].replace("\n", ""))))

    return sorted_dict


def get_train_dev_test_parts(sorted_dict, seed, lang):
    """
    :param sorted_dict: dict sorted by the character length.
    :return: Three lists: train, dev, test
    """
    random.seed(seed)

    group_size = 10

    items = list(sorted_dict.items())
    groups = [items[i:i + group_size] for i in range(0, len(items), group_size)]

    new_train = set()
    new_dev = set()
    new_test = set()

    for group in groups:
        group_len = len(group)

        distances = [
            sum(Levenshtein.distance(group[i][1], group[j][1])
                for j in range(group_len) if i != j)
            for i in range(group_len)
        ]

        sorted_items = [x for _, x in sorted(zip(distances, group))]

        dice_roll = random.randint(1, 6)
        chosen_option = [8, 9] if dice_roll <= 5 else [9, 8]

        if lang == "en":
            if group_len >= 8:
                new_train.update(item[0] for item in sorted_items[:8])
                new_dev.add(sorted_items[chosen_option[0]][0])

            if group_len >= 10:
                new_test.add(sorted_items[chosen_option[1]][0])
        else:
            if group_len >= 10:
                new_train.update(item[0] for item in sorted_items[:4])

                remaining_items = sorted_items[4:10]
                random.shuffle(remaining_items)

                new_dev.update(item[0] for item in remaining_items[:3])
                new_test.update(item[0] for item in remaining_items[3:])
            else:
                new_train.update(item[0] for item in sorted_items)

    new_train = [k for k in sorted_dict.keys() if k in new_train]
    new_dev = [k for k in sorted_dict.keys() if k in new_dev]
    new_test = [k for k in sorted_dict.keys() if k in new_test]

    return new_train, new_dev, new_test


def sbn_to_one_line(ori_sbn):
    sbn = ori_sbn.split("\n")

    one_line = ""
    for s in sbn:
        if "%%%" not in s:
            new_sbn = s.split("%")[0].strip() + " "
            one_line += new_sbn

    return one_line


def write_file(folder_path, output_folder, lang, data_type, id_list, id_name):

    # print information
    print(f"language: {lang}    data_type: {data_type}    {id_name} length: {len(id_list)} \n")

    with open(os.path.join(output_folder, f"{lang}/{id_name}/{data_type}.txt.sbn"), "w", encoding="utf-8") as w_sbn:
            for idx in id_list:
                try:
                    with open(os.path.join(folder_path, f"{lang}/{data_type}/{idx}/{lang}.raw"), "r", encoding="utf-8") as f:
                        raw = f.read().replace("\n", "")

                    with open(os.path.join(folder_path, f"{lang}/{data_type}/{idx}/{lang}.drs.sbn"), "r", encoding="utf-8") as f:
                        sbn = f.read()

                    # remove unknown ref
                    if "(unknown_ref)" in sbn:
                        with open(os.path.join(folder_path, f"{lang}/{data_type}/{idx}/{lang}.drs.sbn"), "w",
                                  encoding="utf-8") as w:
                            sbn = sbn.replace("(unknown_ref)", "")
                            w.write(sbn)

                    sbn = sbn_to_one_line(sbn)
                    sbn = re.sub(r'\s+', ' ', sbn)

                    w_sbn.write(idx + "\n")
                    w_sbn.write(raw + "\n")
                    w_sbn.write(sbn.rstrip() + "\n\n")
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    args = create_arg_parser()

    languages = [args.language] if isinstance(args.language, str) else args.language
    data_type = [args.data_type] if isinstance(args.data_type, str) else args.data_type
    random_seed = args.random_seed

    skip_file = args.skip_file

    if args.skip:
        with open(skip_file, "r", encoding="utf-8") as f:
            skip_lst = f.readlines()
            skip_lst = [string.strip() for string in skip_lst]
    else:
        skip_lst = []

    for l in languages:
        for d in data_type:
            if d == "gold":
                print(f"{l} {d} running...")
                lang = l
                data_type = d

                sorted_dict = read_files_in_folder(args.release_root, lang=lang, data_type=data_type, skip_lst=skip_lst)

                train, dev, test = get_train_dev_test_parts(sorted_dict, random_seed, lang=lang)

                output_folder = args.output_folder

                print(f"{l} {d} total number of instances: {len(sorted_dict)}")
                print(f"{l} {d} number of train, dev, test: {len(train)} {len(dev)} {len(test)}")

                for experiment in ["train", "dev", "test"]:
                    if not os.path.exists(f"{output_folder}/{lang}/{experiment}"):
                        os.makedirs(f"{output_folder}/{lang}/{experiment}")

                write_file(args.release_root, output_folder, lang, data_type, train, id_name="train")
                write_file(args.release_root, output_folder, lang, data_type, dev, id_name="dev")
                write_file(args.release_root, output_folder, lang, data_type, test, id_name="test")


                length_distribution(os.path.join(output_folder, f"{lang}/train/.{data_type}_distribution.png"),
                                    extract_values(sorted_dict, train))

                length_distribution(os.path.join(output_folder, f"{lang}/dev/.{data_type}_distribution.png"),
                                    extract_values(sorted_dict, dev))

                length_distribution(os.path.join(output_folder, f"{lang}/test/.{data_type}_distribution.png"),
                                    extract_values(sorted_dict, test))

            else:
                print(f"{l} {d} running...")
                lang = l
                data_type = d

                sorted_dict = read_files_in_folder(args.release_root, lang=lang, data_type=data_type, skip_lst=skip_lst)

                train = list(sorted_dict.keys())

                output_folder = args.output_folder

                print(f"{l} {d} total number of instances: {len(sorted_dict)}")

                for experiment in ["train"]:
                    if not os.path.exists(f"{output_folder}/{lang}/{experiment}"):
                        os.makedirs(f"{output_folder}/{lang}/{experiment}")

                write_file(args.release_root, output_folder, lang, data_type, train, id_name="train")

                length_distribution(os.path.join(output_folder, f"{lang}/train/.{data_type}_distribution.png"),
                                list(sorted_dict.values()))

