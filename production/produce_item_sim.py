# -*- coding: UTF-8 -*-
import operator
import os
import numpy as np
import sys


def load_item_vec(in_file):
    """

    :param in_file:item vec file
    :return: a dict, key itemId, value np.array([num1,num2,...])
    """
    if not os.path.exists(in_file):
        return {}
    item_vec = {}
    with open(in_file, "r") as f:
        next(f)
        for line in f:
            item = line.strip().split()
            if len(item) < 129:
                continue
            itemId = item[0]
            if itemId == "</s>":
                continue
            item_vec[itemId] = np.array([float(i) for i in item[1:]])
    return item_vec


def cal_item_sim(item_vec, itemid, out_file):
    """

    :param item_vec: item embedding vector
    :param itemid: fixed itemid to cal item sim
    :param out_file: the file to store result
    :return:
    """
    if itemid not in item_vec:
        return
    score = {}
    topK = 10
    fix_item_vec = item_vec[itemid]
    for tmp_itemid in item_vec:
        if tmp_itemid == itemid:
            continue
        tmp_item_vec = item_vec[tmp_itemid]
        fenmu = np.linalg.norm(fix_item_vec) * np.linalg.norm(tmp_item_vec)
        if fenmu == 0:
            score[tmp_itemid] = 0
        else:
            score[tmp_itemid] = round(np.dot(fix_item_vec, tmp_item_vec) / fenmu, 3)
    with open(out_file, "w+") as f:
        out_str = itemid + "\t"
        tmp_list = []
        for sim_item_id, sim_val in sorted(score.items(), key=operator.itemgetter(1), reverse=True)[:topK]:
            tmp_list.append(sim_item_id + "_" + str(sim_val))
        out_str += ";".join(tmp_list)
        f.write(out_str + "\n")


def run_main(in_file, out_file):
    item_vec = load_item_vec(in_file)
    cal_item_sim(item_vec, "27", out_file)


if __name__ == '__main__':
    # item_vec = load_item_vec("../data/item_vec.txt")
    # print(len(item_vec))
    # print(item_vec['318'])
    # run_main("../data/item_vec.txt", "../data/sim_result.txt")
    if len(sys.argv) < 3:
        print("usage: python xx.py in_file out_file")
        sys.exit()
    else:
        in_file = sys.argv[1]
        out_fie = sys.argv[2]
        run_main(in_file, out_fie)
