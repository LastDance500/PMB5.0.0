#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
Script that dectect duplicates in two files
'''

import argparse


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", '--file_one', type=str, help="first_file to check duplicates")
    parser.add_argument("-f2", '--file_two', type=str, help="second_file to check duplicats "
                                                            "(duplicates will be removed from this file)")
    parser.add_argument("-o", '--output_file', type=str, help="output file path")
    args = parser.parse_args()
    return args


def read_files(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.readlines()

    triple_list = []
    sbn_dict = {}
    for i in range(len(data)):
        text = data[i]
        if text != "\n":
            triple_list.append(text)
        else:
            triple_list = []

        if len(triple_list) == 3:
            sbn_dict[triple_list[0]] = [triple_list[1], triple_list[2]]

    return sbn_dict


def detect_duplicates(sbn_dict1, sbn_dict2):
    text1_list = [value[0] for value in sbn_dict1.values()]

    keys_to_delete = []
    for key, value in sbn_dict2.items():
        if value[0] in text1_list:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del sbn_dict2[key]
        print(key)

    return sbn_dict2


def rewrite_files(file_path, sbn_dict):
    with open(file_path, "w", encoding="utf-8") as w:
        for key in sbn_dict.keys():
            lst = sbn_dict[key]
            raw = lst[0]
            sbn = lst[1]

            w.write(key)
            w.write(raw)
            w.write(sbn)
            w.write("\n")


if __name__ == "__main__":
    args = create_arg_parser()
    file1 = args.file_one
    file2 = args.file_two
    output = args.output_file

    sbn_dict1 = read_files(file1)
    sbn_dict2 = read_files(file2)

    sbn_dict2 = detect_duplicates(sbn_dict1, sbn_dict2)

    rewrite_files(output, sbn_dict2)

