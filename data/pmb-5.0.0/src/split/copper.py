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
    parser.add_argument("-l", '--language', default="en", choices=['en', 'de', 'nl', 'it', 'zh', 'ja'], type=str, help="Languages we select")
    parser.add_argument("-p", '--plot', default=True, type=bool, help="plot the figure or not")
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

    return raw_dict


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


def sbn_to_one_line(ori_sbn):
    sbn = ori_sbn.split("\n")

    one_line = ""
    for s in sbn:
        if "%%%" not in s:
            new_sbn = s.split("%")[0].strip() + " "
            one_line += new_sbn

    return one_line


def read_files_in_folder(folder_path, lang, data_type, skip_lst):
    p = os.listdir(os.path.join(folder_path, f"{lang}/{data_type}"))

    raw_dict = {}
    for sub_p in p:
        d = os.listdir(os.path.join(folder_path, f"{lang}/{data_type}/{sub_p}"))

        for sub_d in d:
            try:
                with open(os.path.join(folder_path, f"{lang}/{data_type}/{sub_p}/{sub_d}/{lang}.met"), "r", encoding="utf-8") as f1:
                    subcorpus = f1.readlines()[0].strip()

                    if subcorpus[0:2] == "ID":
                        corpus = "incident"
                    else:
                        corpus = "others"

                with open(os.path.join(folder_path, f"{lang}/{data_type}/{sub_p}/{sub_d}/{lang}.raw"), "r", encoding="utf-8") as f:
                    raw = f.read()

                with open(os.path.join(folder_path, f"{lang}/{data_type}/{sub_p}/{sub_d}/{lang}.drs.sbn"), "r", encoding="utf-8") as f:
                    s = f.read()
                    one_line_s = sbn_to_one_line(s)

            except Exception as e:
                print(e)

            if not raw_dict.get(f"{sub_p}/{sub_d}"):
                raw_dict[f"{sub_p}/{sub_d}"] = (raw.replace("\n", ""), one_line_s.strip(), corpus)
            else:
                print(f"duplicate {sub_p}/{sub_d}")

    # sort the dict
    raw_dict = detect_remove_duplicate(raw_dict)
    raw_dict = skip(raw_dict, skip_lst)

    return raw_dict


def get_train_dev_test_parts(sorted_dict, seed):
    """
    :param sorted_dict: dict sorted by the character length.
    :return: Three lists: train, dev, test
    """
    group_size = 10
    groups = []
    items = list(sorted_dict.items())

    for i in range(0, len(items), group_size):
        group = items[i:i + group_size]
        groups.append(group)

    train = []
    dev = []
    test = []

    for group in groups:
        group_len = len(group)

        distances = []
        for i in range(group_len):
            total_distance = 0
            for j in range(group_len):
                if i != j:
                    distance = Levenshtein.distance(group[i][1], group[j][1])
                    total_distance += distance
            distances.append(total_distance)

        sorted_items = [x for _, x in sorted(zip(distances, group), reverse=False)]

        # throw a dice to decide which one is in dev and which one should be in test
        random.seed(seed)
        dice_roll = random.randint(1, 6)

        if dice_roll <= 5:
            chosen_option = [8, 9]
        else:
            chosen_option = [9, 8]

        if len(sorted_items) >= 8:
            train.extend([item[0] for item in sorted_items[:8]])
            dev.append(sorted_items[chosen_option[0]][0])
        else:
            train.extend([item[0] for item in sorted_items])

        if len(sorted_items) >= 10:
            test.append(sorted_items[chosen_option[1]][0])

    new_train = []
    new_test = []
    new_dev = []
    for k in sorted_dict.keys():
        if k in train:
            new_train.append(k)
        elif k in dev:
            new_dev.append(k)
        elif k in test:
            new_test.append(k)

    return new_train, new_dev, new_test


def write_file(output_folder, lang, en_dict, l_dict):
    new_dict = {}
    for k in l_dict.keys():
        raw = l_dict.get(k)[0]
        corpus = l_dict.get(k)[2]
        if en_dict.get(k) and corpus != "incident":
            sbn = en_dict.get(k)[1]
        else:
            sbn = l_dict.get(k)[1]

        if raw and sbn:
            sbn = sbn_to_one_line(sbn)
            sbn = re.sub(r'\s+', ' ', sbn)
            new_dict[k] = [raw, sbn]

    new_dict = dict(sorted(new_dict.items(), key=lambda item: len(item[1][0].replace("\n", ""))))

    with open(os.path.join(output_folder, f"{lang}/train/copper.sbn"), "w", encoding="utf-8") as w_sbn:
        for k in new_dict.keys():
            raw = new_dict[k][0]
            sbn = new_dict[k][1]

            w_sbn.write(k+"\n")
            w_sbn.write(raw+"\n")
            w_sbn.write(sbn+"\n\n")


if __name__ == "__main__":
    args = create_arg_parser()

    output_folder = args.output_folder

    lang = args.language
    random_seed = args.random_seed

    bronze_en_dict = read_files_in_folder(args.release_root, lang="en", data_type="bronze", skip_lst=[])
    gold_en_dict = read_files_in_folder(args.release_root, lang="en", data_type="gold", skip_lst=[])
    silver_en_dict = read_files_in_folder(args.release_root, lang="en", data_type="silver", skip_lst=[])

    en_dict = {**bronze_en_dict, **gold_en_dict, **silver_en_dict}

    l_dict = read_files_in_folder(args.release_root, lang=lang, data_type="bronze", skip_lst=[])

    write_file(output_folder, lang, en_dict, l_dict)

