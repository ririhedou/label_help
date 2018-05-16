#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
from map_domain_to_id import domain_id_map


def read_label_from(f):
    label_map = dict()
    brand_map = collections.defaultdict(list)
    ff = open(f,"r")

    def label_split(l,domain):
        if len(l) == 1:
            return l
        elif len(l) == 2:
            return l[0]
        else:
            print (domain, l)
            #raw_input()
            return '1'

    for line in ff.readlines():
        line = line.strip()
        if len(line) == 0 or line.startswith('#'):
            continue
        domain = line.split(',')[0]
        l = line.split(',')[-1]

        l = label_split(l,domain)

        brand = line.split(',')[1]
        label_map[domain] = l
        brand_map[brand].append([domain,l])
    return label_map, brand_map


def get_false_positive_by_brand(d):
    print (len(d))
    t = sum(1 for j in d if d[j] == '1')
    print ("1", t)

    t = sum(1 for j in d if d[j] == '2')
    print ("2", t)

    t = sum(1 for j in d if d[j] == '0')
    print ("0", t)

    #size = size_map[domain_id_map[int(brand)]]
    #print ("SIZE", size)
    #print ((t+0.0)/size)


def statistcs_on_classification_predictions(prediction_f):
    f = open(prediction_f, "r")
    brand_size_map = collections.defaultdict(list)

    predictions = []
    for line in f.readlines():
        line = line.strip()
        _brand = line.split("/")[-2]
        domain_name = line.split("/")[-1].split("..")[0]
        brand_size_map[_brand].append(domain_name)

    for i in brand_size_map:
        brand_size_map[i] =list(set(brand_size_map[i]))

    f.close()
    keys = brand_size_map.keys()
    keys.sort()
    for i in range(766):
        if not str(i) in keys:
            print (i,  domain_id_map[i], 0)
            predictions.append([domain_id_map[i], 0])
        else:
            print (i, domain_id_map[i], len(brand_size_map[str(i)]))
            predictions.append([domain_id_map[i], len(brand_size_map[str(i)])])

    predictions.sort(key=lambda x: x[1])
    total = sum(i[1] for i in predictions)

    for i in predictions:
        print (i[0], i[1], float(i[1])/total)

    print ("TOTAL", total)
    return

if __name__ == "__main__":

    #f_mb = "MAY14.SNAP1.MB.label"
    f_web = "MAY14.SNAP1.WEB.label"
    #_, mb_brand = read_label_from(f_mb)
    web_label, _ = read_label_from(f_web)
    #get_false_positive_by_brand(web_label)
    statistcs_on_classification_predictions("data_need_label/snap1_retrain.txt")
