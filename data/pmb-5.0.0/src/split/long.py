#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
Script that selects train, dev and test sets for sbn
'''
import re
import argparse
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", '--release_root', type=str, help="Root of release files")
    parser.add_argument("-o", '--output_folder', type=str, help="Folder to write output DRSs to (file-names are standardized)")
    parser.add_argument("-li", '--long_ind', type=str, help="long text document index")
    parser.add_argument("-l", '--language', default="en", choices=['en', 'de', 'nl', 'it'], type=str, help="Languages we select")
    parser.add_argument("-d", '--data_type', default="silver", choices=['gold', 'silver', 'bronze'], help="Whether we extract gold/silver/bronze data")
    parser.add_argument("-rs", '--random_seed', default=32, type=int, help="Random seed for shuffling of the data -- use our default 32 to get our version")
    args = parser.parse_args()
    return args


def extract_by_ind(raw_dict, lst):
    new_dict = {}
    if lst != []:
        for key in raw_dict.keys():
            if key in lst:
                new_dict[key] = raw_dict.get(key)
                print(f"chosen {key}")
    return new_dict


def length_distribution(path, string_list):
    """
    plot the distribution of string list
    """
    print("Generate distribution...")
    char_lengths = [len(s) for s in string_list]
    word_lengths = [len(s.split()) for s in string_list]

    # 创建包含两个子图的画布
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))

    # 绘制字符长度分布
    ax1.hist(char_lengths, bins=range(min(char_lengths), max(char_lengths) + 2), align='left', alpha=0.75)
    ax1.set_xlabel('Character Length')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Distribution of Character Length')
    ax1.grid(True)

    # 绘制单词长度分布
    ax2.hist(word_lengths, bins=range(min(word_lengths), max(word_lengths) + 2), align='left', alpha=0.75)
    ax2.set_xlabel('Word Length')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Word Length')
    ax2.grid(True)

    # 调整子图之间的间距
    fig.tight_layout()

    # Save the figure
    plt.savefig(path, dpi=300)


def extract_values(raw_dict, keys):
    values = []
    for k in keys:
        values.append(raw_dict[k])
    return values


def read_files_in_folder(folder_path, lang, data_type, chosen_lst):
    p = os.listdir(os.path.join(folder_path, f"{lang}/{data_type}"))

    raw_dict = {}
    for sub_p in p:
        d = os.listdir(os.path.join(folder_path, f"{lang}/{data_type}/{sub_p}"))

        for sub_d in d:
            try:
                with open(os.path.join(folder_path, f"{lang}/{data_type}/{sub_p}/{sub_d}/{lang}.raw"), "r", encoding="utf-8") as f:
                    raw = f.read()
            except Exception as e:
                print(e)
            raw_dict[f"{sub_p}/{sub_d}"] = raw.strip()

    # sort the dict
    raw_dict = dict(sorted(raw_dict.items(), key=lambda item: len(item[1])))
    raw_dict = extract_by_ind(raw_dict, chosen_lst)

    return raw_dict


def sbn_to_one_line(ori_sbn):
    sbn = ori_sbn.split("\n")

    one_line = ""
    for s in sbn:
        if "%%%" not in s:
            new_sbn = s.split("%")[0].strip() + " "
            one_line += new_sbn

    return one_line


def write_file(folder_path, output_folder, lang, id_list, id_name="long"):
    # print information
    print(f"language: {lang}    {id_name} length: {len(id_list)} \n")

    with open(os.path.join(output_folder, f"{lang}/test/long.txt.sbn"), "w+", encoding="utf-8") as w_sbn:
        for idx in id_list:
            try:
                with open(os.path.join(folder_path, f"{lang}/gold/{idx}/{lang}.raw"), "r", encoding="utf-8") as f:
                    raw = f.read().replace("\n", "")

                with open(os.path.join(folder_path, f"{lang}/gold/{idx}/{lang}.drs.sbn"), "r",
                          encoding="utf-8") as f:
                    sbn = f.read()

                # remove unknown ref
                if "(unknown_ref)" in sbn:
                    with open(os.path.join(folder_path, f"{lang}/gold/{idx}/{lang}.drs.sbn"), "w",
                              encoding="utf-8") as w:
                        sbn = sbn.replace("(unknown_ref)", "")
                        w.write(sbn)

                sbn = sbn_to_one_line(sbn)
                sbn = re.sub(r'\s+', ' ', sbn)

                w_sbn.write(idx + "\n")
                w_sbn.write(raw + "\n")
                w_sbn.write(sbn.rstrip() + "\n\n")
            except Exception as e:
                pass

            try:
                with open(os.path.join(folder_path, f"{lang}/silver/{idx}/{lang}.raw"), "r", encoding="utf-8") as f:
                    raw = f.read().replace("\n", "")

                with open(os.path.join(folder_path, f"{lang}/silver/{idx}/{lang}.drs.sbn"), "r",
                          encoding="utf-8") as f:
                    sbn = f.read()

                # remove unknown ref
                if "(unknown_ref)" in sbn:
                    with open(os.path.join(folder_path, f"{lang}/silver/{idx}/{lang}.drs.sbn"), "w",
                              encoding="utf-8") as w:
                        sbn = sbn.replace("(unknown_ref)", "")
                        w.write(sbn)

                sbn = sbn_to_one_line(sbn)
                sbn = re.sub(r'\s+', ' ', sbn)

                w_sbn.write(idx + "\n")
                w_sbn.write(raw + "\n")
                w_sbn.write(sbn.rstrip() + "\n\n")
            except Exception as e:
                pass


if __name__ == "__main__":
    args = create_arg_parser()
    output_folder = args.output_folder
    lang = args.language

    with open(args.long_ind, "r", encoding="utf-8") as f:
        chosen_lst = f.readlines()
        chosen_lst = [string.strip() for string in chosen_lst]

    raw_dict1 = read_files_in_folder(args.release_root, lang=lang, data_type="gold", chosen_lst=chosen_lst)
    raw_dict2 = read_files_in_folder(args.release_root, lang=lang, data_type="silver", chosen_lst=chosen_lst)

    raw_dict = {**raw_dict1, **raw_dict2}

    write_file(args.release_root, output_folder, lang, chosen_lst, id_name="long")

    length_distribution(os.path.join(output_folder, f"{lang}/test/long_distribution.png"),
                        extract_values(raw_dict, list(raw_dict.keys())))


