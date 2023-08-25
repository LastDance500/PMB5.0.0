#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
Script for update the correction of data in ./data folder
'''

import argparse
import os
import re


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", '--split_path', default="../../split", help="Root of split files")
    args = parser.parse_args()
    return args


def sbn_to_one_line(ori_sbn):
    sbn = ori_sbn.split("\n")

    one_line = ""
    for s in sbn:
        if "%%%" not in s:
            new_sbn = s.split("%")[0].strip() + " "
            one_line += new_sbn

    return one_line


def data2dict(data_path):
    with open(data_path, "r", encoding="utf-8") as f1:
        data = f1.readlines()

    data_dict = {}
    for i in range(len(data)):
        d = data[i]
        if re.match('^p\d+/d\d+$', d):
            idx = d.strip()
            flag = True
            raw_sbn = []
        elif flag and d != "\n":
            raw_sbn.append(d)
        else:
            data_dict[idx] = raw_sbn
            flag = False

    return data_dict


def dict2data(data_dict, data_path):
    with open(data_path, "w", encoding="utf-8") as w:
        for key in data_dict.keys():
            try:
                raw = data_dict[key][0].strip()
                sbn = data_dict[key][1].strip()
            except Exception as e:
                print(f"{key} in {data_path} is sbn-empty")
            w.write(key.strip() + "\n")
            w.write(raw + "\n")
            w.write(sbn + "\n")
            w.write("\n")

def read_data(data_path, lang, data_type, idx):
    with open(os.path.join(data_path, f"{lang}/{data_type}/{idx}/{lang}.drs.sbn"), "r", encoding="utf-8") as f:
        sbn = sbn_to_one_line(f.read())

    return sbn


if __name__ == "__main__":
    args = create_arg_parser()

    for root, dirs, files in os.walk(args.split_path):
        for file in files:
            if file.endswith('.sbn'):
                flag = False
                file_path = os.path.join(root, file)
                print(f"checking {file_path}......")
                data_dict = data2dict(file_path)
                dict2data(data_dict, file_path)


