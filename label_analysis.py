#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
from map_domain_to_id import domain_id_map


def read_label_from(f):
    label_map = dict()
    brand_map = collections.defaultdict(list)
    ff = open(f ,"r")
    for line in ff.readlines():
        line = line.strip()
        if len(line) == 0 or line.startswith('#'):
            continue
        domain = line.split(',')[0]
        l = line.split(',')[-1]
        brand = line.split(',')[1]
        label_map[domain] = l
        brand_map[brand].append([domain,l])
    return label_map,brand_map


def get_false_positive_by_brand(d, brand):
    print (len(d))
    t = sum(1 for o,j in d if j == '1')
    print ("1",t)
    #size = size_map[domain_id_map[int(brand)]]
    #print ("SIZE", size)
    #print ((t+0.0)/size)


if __name__ == "__main__":
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

    visited = pop_brand + other_brand
    visited = list(set(visited))

    f_mb = "/home/ketian/Desktop/phishingdetect/label_tool/SNAP1.MB.label"
    f_web = "/home/ketian/Desktop/phishingdetect/label_tool/SNAP1.WEB.label"
    _, mb_brand = read_label_from(f_mb)
    _, web_brand = read_label_from(f_web)

    for i in busi+com+shopping:
        if i in visited:
            continue
        print (i, domain_id_map[int(i)])
        get_false_positive_by_brand(web_brand[i], i)
        print ("-------------")
        get_false_positive_by_brand(mb_brand[i], i)

        raw_input()