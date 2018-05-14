#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import os
import sys
import csv


DEFAULT_FILE = "SNAP1.MB.label"  #"crawl.LABEL.label" #"phishingTank.LABEL.label" #"LABEL.label"
DATABASE_DIR = "/mnt/sdb1/browser_phishingTank/database/"  # we set global output dir


parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

import util_ke

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
    p = subprocess.Popen(["display", img_path])
    label = raw_input("Give a label for image: ")
    p.kill()
    print ("We label {} as {}".format(img_path, label))
    idx = img_path.split('/')[-1].split('..')[0]
    write_label_into_file(idx,label, brand)


def write_label_into_file(idx, label, brand):

    s = str(idx) + "," + str(brand) + "," + str(label) + "\n"
    with open(DEFAULT_FILE, 'a') as f:
        f.write(s)
    pass


# we store a csv file as the database
def search_database_for_url(_id):
    database = DATABASE_DIR + str(_id) + '.csv'
    exist_indexes = dict()
    if os.path.exists(database):
        with open(database, 'r') as userFile:
            userFileReader = csv.reader(userFile)
            for row in userFileReader:
                exist_indexes[row[0]] = row[1]


def get_prediction_1_from_crawl(brand):
    path = "/home/ketian/Desktop/phishingdetect/measurement/snap1.txt"
    DIR = "/home/ketian/tmp/SNAP1/"

    def read_brand_predicts(brand):
        fileList = set()
        f = open(path, "r")
        for line in f.readlines():
            line = line.strip()
            _brand = line.split("/")[-2]
            domain_name = line.split("/")[-1].split("..")[0]
            if _brand == brand:
                #print (brand, domain_name)
                fileList.add(domain_name)
        return [DIR + i+"..screen.png" for i in fileList]

    print ("\n\n\n {}".format(brand))
    read_ares = read_brand_predicts(brand)

    c = 0
    for img_path in read_ares:
        label_image(img_path, brand)


def get_prediction_1_from_crawl_mb(brand):
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
        return [DIR + i+"..screen.png" for i in fileList]


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


EXCEPTION_LIST = ["502", "708", "377", "565", "587", "617", "327", "43", "193", "56", "325", "143", "441", "637", "396", "308", "657", "7", "338"
                  , "493", "118", "135", "471"]

"""
502: oup.com.out 135
708: vr.de.out 143
377: key.com.out 145
565: salon.com.out 146
587: sky.com.out 152
617: state.gov.out 156
327: hp.com.out 163
43: apa.org.out 168
193: db.com.out 175
56: att.com.out 181
325: hotels.com.out 191
143: china.com.cn.out 213
441: mit.edu.out 217
637: ted.com.out 241
396: live.com.out 259
308: health.com.out 267
657: time.com.out 267
7: aa.com.out 269
338: ign.com.out 293
493: office.com.out 311
118: business.gov.au.out 319
135: cc.com.out 328
471: news.com.au.out 359
"""

if __name__ == "__main__":

    #twitter 676
    #uber 677
    #bitcoin 94
    #booking 111
    #citi 151
    #20 adp
    #509 - paypal 243-facebook 436 msft 567 santa, 293-google , 219-ebay
    # 19-adobe 209-dropbox
    # generate_scp_file("243")

    # sys.exit(0)

    other_brand = ["677", "676", "94", "111", "151" ,"20"]

    pop_brand = ["509", "243", "436", "567", "293", "219", "19", "209"]

    # BUSINESS
    busi = ['493', '509', '231', '140', '345', '28', '574', '68', '268', '721', '762', '582', '119', '589', '632',
            '566', '36', '307', '127', '609', '102', '248', '80', '731', '334', '742', '357', '550', '56', '700', '239',
            '20', '716', '490', '433', '636', '253', '356', '206', '149', '651', '352', '545', '760', '360']

    shopping = ['467', '711', '235', '340', '83', '632', '331', '324', '731', '124', '321', '482', '296', '470', '486',
                '412', '656', '88', '107', '177', '282', '408', '381', '714', '759', '578', '690', '502', '339', '587',
                '546', '281', '270', '293', '5', '503', '710', '59', '366', '616', '755', '72', '64', '581', '389',
                '337']
    #computer
    com = ['293', '758', '243', '753', '676', '393', '92', '343', '737', '447', '493', '436', '671', '45', '613',
             '727', '285', '509', '520', '19', '209', '445', '50', '600', '564', '101', '703', '593', '424', '158',
             '290', '728', '574', '665', '451', '428', '329', '604', '398', '293', '97', '42']

    visited = pop_brand + other_brand + busi +shopping
    brand = com

    for i in brand:
        if i in visited or i in EXCEPTION_LIST:
            print ("SKIP I", i)
            continue
        get_prediction_1_from_crawl_mb(i)
