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
    p = subprocess.Popen(["open", "-W", img_path]) #open for mac
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

    path = "./data_need_label/snap1_retrain.txt"

    global IMG_WEB_DIR
    global LABEL_FILE

    def read_brand_predicts(brand):
        fileList = set()
        f = open(path, "r")
        t = []
        for line in f.readlines():
            line = line.strip()
            _brand = line.split("/")[-2]
            domain_name = line.split("/")[-1].split("..")[0]
            if _brand == brand:
                #print (brand, domain_name)
                fileList.add(domain_name)
        print ("total {} needs label".format(len(fileList)))
        return [IMG_WEB_DIR + i+"..screen.png" for i in fileList]

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
    print ("\n\n\nread {} for domain: {}".format(brand_idx, d_map[int(brand_idx)]))

    for img_path in read_ares:
        label_image(img_path, brand_idx)


def label_for_prediction_mobile(brand):
    path = "/home/ketian/Desktop/phishingdetect/measurement/snap1_mb.txt"
    web_path = "/home/ketian/Desktop/phishingdetect/measurement/snap1.txt"

    DIR = "/home/ketian/tmp/SNAP1_MB/"

    def read_label_from_web(f="/home/ketian/Desktop/phishingdetect/label_tool/SNAP1.WEB.label"):
        label_map = dict()
        ff = open(f,"r")
        for line in ff.readlines():
            line = line.strip()
            if len(line) == 0 or line.startswith('#'):
                continue
            domain = line.split(',')[0]
            l = line.split(',')[-1]
            label_map[domain] = l
        return label_map

    def read_brand_predicts_mb(brand, path):
        fileList = set()
        f = open(path, "r")
        for line in f.readlines():
            line = line.strip()
            _brand = line.split("/")[-2][:-7]
            #print (_brand)
            domain_name = line.split("/")[-1].split("..")[0]
            if _brand == brand:
                #print (brand, domain_name)
                fileList.add(domain_name)
        return [DIR + i+"..screen.png" for i in fileList]

    def read_brand_predicts(brand,path):
        fileList = set()
        f = open(path, "r")
        for line in f.readlines():
            line = line.strip()
            _brand = line.split("/")[-2]
            domain_name = line.split("/")[-1].split("..")[0]
            if _brand == brand:
                #print (brand, domain_name)
                fileList.add(domain_name)
        return [DIR + i+ "..screen.png" for i in fileList]

    print ("\n\n\n {}".format(brand))

    read_ares = read_brand_predicts_mb(brand,path)
    read_web = read_brand_predicts(brand, web_path)
    label_map = read_label_from_web()
    c = 0
    for img_path in read_ares:
        if img_path in read_web:
            idx = img_path.split('/')[-1].split('..')[0]
            print ("alreay labeled", img_path, label_map[idx] )
            write_label_into_file(idx,label_map[idx],brand)
        else:
            print ("NOT", img_path)
            label_image(img_path, brand)


IMG_WEB_DIR = "/Users/stevejan/Desktop/SNAP1/"
LABEL_FILE = "MAY14.SNAP1.WEB.label"


if __name__ == "__main__":

    other_brand = ["677", "676", "94", "111", "151" ,"20"] #Done

    pop_brand = ["509", "243", "436", "567", "293", "219", "19", "209"] #Done

    # BUSINESS
    busi = map_domain_to_id.business_v #Done

    shopping = map_domain_to_id.shopping_v #Done

    #computer
    com = map_domain_to_id.computer_v #done

    news = map_domain_to_id.news_v  #Done

    banks = map_domain_to_id.banks_brand
    
    for i in banks :
        label_from_prediction(i)

