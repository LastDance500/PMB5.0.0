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
    parser.add_argument("-l", "--lang", required=False, type=str,default="en",
                        help="language in [en, nl, de ,it]")
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
    parser.add_argument("-tti2", "--test2", required=False, type=str,
                        default=os.path.join(path, "data/pmb-5.0.0/seq2seq/en/test/long.sbn"),
                        help="test text input file")
    args = parser.parse_args()

    return args


def main():
    args = create_arg_parser()

    # train process
    lang = args.lang
    train_dataloader1 = get_dataloader(args.pretrain)

    train_dataloader2 = get_dataloader(args.train)

    test_dataloader = get_dataloader(args.test)
    test_dataloader2 = get_dataloader(args.test2)

    bart_classifier = Generator(lang)
    bart_classifier.train(train_dataloader1, test_dataloader, lr=0.0001, epoch_number=5)
    bart_classifier.train(train_dataloader2, test_dataloader, lr=0.0001, epoch_number=5)
    bart_classifier.evaluate(test_dataloader, os.path.join(path, "src/model/mBART/result/mBart_en_standard.txt"))
    bart_classifier.evaluate(test_dataloader2, os.path.join(path, "src/model/mBART/result/mBart_en_long.txt"))

    bart_classifier.model.save_pretrained(os.path.join(path, "models/Bart_seq2seq/en"))


if __name__ == '__main__':
    main()
