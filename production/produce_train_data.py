# -*- coding: UTF-8 -*-
import csv
import os
import sys


def produce_train_data(in_file, out_file):
    """

    :param in_file: user behavior file
    :param out_file: output file
    :return:
    """
    if not os.path.exists(in_file):
        return
    record = {}
    score_thr = 4.0
    with open(in_file, "r") as f:
        data = csv.reader(f)
        header = next(data)
        for item in data:
            if len(item) < 4:
                continue
            userId, movieId, rating = item[0], item[1], float(item[2])
            if rating < score_thr:
                continue
            if userId not in record:
                record[userId] = []
            record[userId].append(movieId)
    with open(out_file, "w") as f:
        for user in record:
            f.write(" ".join(record[user]) + "\n")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: python xx.py in_file out_file")
        sys.exit()
    else:
        in_file = sys.argv[1]
        out_fie = sys.argv[2]
        produce_train_data(in_file, out_fie)
    # produce_train_data("../data/ratings.csv", "../data/train_data.txt")
