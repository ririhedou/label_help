#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import os
import sys
import map_domain_to_id


parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)


def load_label(filename='LABEL.label'):
    labels = dict()
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) < 1 or line.startswith("#"):
                continue
            x_label = line.split(",")[0]
            y_label = line.split(",")[-1]
            if len(y_label) < 1:
                print (x_label)
                raw_input()
            labels[x_label] = y_label
    X = []
    Y = []
    for ele in labels:
        X.append(ele)
        Y.append(labels[ele])

    print ("LOAD total {} labels".format(len(labels)))
    print ("LOAD total y {} labels".format(sum(1 for i in labels if labels[i] == 'y')))
    print ("LOAD total n {} labels".format(sum(1 for i in labels if labels[i] == 'n')))
    return labels


def label_image(img_path, brand):
    #p = subprocess.Popen(["open", "-W", img_path]) #open for mac
    p = subprocess.Popen(["display", img_path])  # display for linux

    label = raw_input("Give a label for image: ")
    p.kill()
    print ("We label {} as {}".format(img_path, label))
    idx = img_path.split('/')[-1].split('..')[0]
    write_label_into_file(idx,label, brand)


def write_label_into_file(idx, label, brand):
    global LABEL_FILE
    s = str(idx) + "," + str(brand) + "," + str(label) + "\n"
    with open(LABEL_FILE, 'a+') as f:
        f.write(s)
    pass


def label_from_prediction(brand_idx):

    path = "./data_need_label/snap1_mb_retrain.txt"

    global IMG_DIR
    global LABEL_FILE

    def read_brand_predicts(brand):
        fileList = set()
        f = open(path, "r")
        t = []
        for line in f.readlines():
            line = line.strip()
            _brand = line.split("/")[-2][:-7]
            domain_name = line.split("/")[-1].split("..")[0]
            if _brand == brand:
                #print (brand, domain_name)
                fileList.add(domain_name)
        print ("BRAND IDX {} total {} needs label".format(brand, len(fileList)))
        return [IMG_DIR + i+"..screen.png" for i in fileList]

    def read_labeled_brand(filename='LABEL.label'):
        brands = set()
        if not os.path.exists(filename):
            return []
        with open(filename) as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0 or line.startswith("#"):
                    continue
                brand = line.split(',')[1]
                brands.add(brand)
        return list(brands)

    read_ares = read_brand_predicts(brand_idx)
    if brand_idx in read_labeled_brand(LABEL_FILE):
        print ("ALready labeled")
        return

    d_map = map_domain_to_id.domain_id_map
    print ("read {} for domain: {}".format(brand_idx, d_map[int(brand_idx)]))

    for img_path in read_ares:
        label_image(img_path, brand_idx)

    print ("DONE\n\n")


IMG_DIR = "/home/ketian/tmp/SNAP1_MB/"
LABEL_FILE = "MAY14.SNAP1.MOBILE.label"


if __name__ == "__main__":

    pop_brand = ["509", "243", "436", "567", "293", "219", "19", "209"] # Done

    other_brand = ["677", "676", "94", "111", "151", "20"]

    # BUSINESS
    busi = map_domain_to_id.business_v
    # Shopping
    shopping = map_domain_to_id.shopping_v
    # Computer
    com = map_domain_to_id.computer_v

    news = map_domain_to_id.news_v

    banks = map_domain_to_id.banks_brand
    
    for i in range(767):
        label_from_prediction(str(i))

