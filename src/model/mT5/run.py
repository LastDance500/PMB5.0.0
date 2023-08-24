#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：DRG_parsing 
@File ：run.py
@Author ：xiao zhang
@Date ：2022/11/14 12:27
'''

import argparse
import os
import sys
sys.path.append(".")

from model import get_dataloader, Generator

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pt", "--pretrain", required=False, type=str,
                        default=os.path.join(path, "data/pmb-5.0.0/seq2seq/en/train/gold_silver.sbn"),
                        help="text input file")
    parser.add_argument("-t", "--train", required=False, type=str,
                        default=os.path.join(path, "data/pmb-5.0.0/seq2seq/en/train/gold.sbn"),
                        help="text input file")
    parser.add_argument("-dti", "--dev", required=False, type=str,
                        default=os.path.join(path, "data/pmb-5.0.0/seq2seq/en/dev/standard.sbn"),
                        help="dev text input file")
    parser.add_argument("-tti", "--test", required=False, type=str,
                        default=os.path.join(path, "data/pmb-5.0.0/seq2seq/en/test/standard.sbn"),
                        help="test text input file")
    args = parser.parse_args()

    return args


def main():
    args = create_arg_parser()

    # train process
    train_dataloader1 = get_dataloader(args.pretrain)

    train_dataloader2 = get_dataloader(args.train)

    test_dataloader = get_dataloader(args.test)

    T5_classifier = Generator()
    T5_classifier.train(train_dataloader1, test_dataloader, lr=0.0001, epoch_number=5)
    T5_classifier.train(train_dataloader2, test_dataloader, lr=0.0001, epoch_number=10)
    T5_classifier.evaluate(test_dataloader, os.path.join(path, "src/model/mT5/result/mT5_en_small.txt"))

    T5_classifier.model.save_pretrained(os.path.join(path, "models/T5_seq2seq/it/"))


if __name__ == '__main__':
    main()
