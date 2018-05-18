#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
from map_domain_to_id import domain_id_map
import map_domain_to_id
import sys



def get_verfied_percent(f):
    label_map, brand_map =read_label_from(f)
    brand_positive = collections.defaultdict(int)
    for i in label_map:
        b = i.split(' ')[-1]
        if label_map[i] == '1':
            brand_positive[b] += 1

    for i in brand_positive:
        print (i, domain_id_map[int(i)], brand_positive[i])


def read_label_from(f):
    label_map = dict()
    brand_map = collections.defaultdict(list)
    ff = open(f,"r")

    def label_split(l,domain):
        if len(l) == 1:
            return l
        elif len(l) == 2:
            #if l[0] == '1':
            #print (domain, l)
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
        brand = line.split(',')[1]

        l = line.split(',')[-1]
        l = label_split(l,domain)
        label_map[domain+ ' ' +brand] = l
        #if l == '1':
        brand_map[brand].append(domain)

    #for i in brand_map:
    #    print (domain_id_map[int(i)],i, len(brand_map[i]))
    print ("TOTAL POSITIVE", sum(len(brand_map[i]) for i in brand_map))
    return label_map, brand_map


def get_false_positive_by_brand(d):

    print (len(d))
    t1 = sum(1 for j in d if d[j] == '1')
    print ("1", t1)

    t2 = sum(1 for j in d if d[j] == '2')
    print ("2", t2)

    t3 = sum(1 for j in d if d[j] == '0')
    print ("0", t3)

    #size = size_map[domain_id_map[int(brand)]]
    #print ("SIZE", size)
    #print ((t+0.0)/size)
    print ("ONLY 1", (t1+0.0)/len(d))
    print ("1 AND 2",(t1+t2+0.0)/len(d))


def statistcs_on_classification_predictions(prediction_f, web=True):
    f = open(prediction_f, "r")
    brand_map = collections.defaultdict(list)

    predictions = []
    for line in f.readlines():
        line = line.strip()
        if web:
            _brand = line.split("/")[-2]
        else:
            _brand = line.split("/")[-2][:-7]
        domain_name = line.split("/")[-1].split("..")[0]
        brand_map[_brand].append(domain_name)

    for i in brand_map:
        brand_map[i] =list(set(brand_map[i]))

    f.close()
    keys = brand_map.keys()
    keys.sort()
    for i in range(766):
        if not str(i) in keys:
            #print (i,  domain_id_map[i], 0)
            predictions.append([domain_id_map[i], 0])
        else:
            #print (i, domain_id_map[i], len(brand_map[str(i)]))
            predictions.append([domain_id_map[i], len(brand_map[str(i)])])

    predictions.sort(key=lambda x: x[1], reverse=True)
    total = sum(i[1] for i in predictions)

    zero = 0
    #for i in predictions[:10]:
        #print (i[0], i[1], float(i[1])/total)
        #if i[1] == 0:
        #print (i[0])
        #zero += 1

    print ("TOTAL", total)
    print ("TOTAL", sum(len(brand_map[i]) for i in brand_map))
    print ("ZERO", zero)
    return brand_map


def label_stat():

    f_mb = "MAY14.SNAP1.MOBILE.label"
    f_web = "MAY14.SNAP1.WEB.label"
    mb_label, mb_brand_map = read_label_from(f_mb)
    web_label, web_brand_map = read_label_from(f_web)
    get_false_positive_by_brand(web_label)

    #for i in web_brand_map:
    #    print (i, len(web_brand_map[i]))

    pop_dict = dict()
    non_pop_dict = dict()
    popular_brands = map_domain_to_id.pop_brand

    for i in mb_label:
        if i.split(' ')[-1] in popular_brands:
            pop_dict[i] = mb_label[i]
        else:
            non_pop_dict[i] = mb_label[i]

    get_false_positive_by_brand(pop_dict)
    get_false_positive_by_brand(non_pop_dict)


    web_brand_snap1_map = statistcs_on_classification_predictions("data_need_label/snap1_retrain.txt")
    mb_brand_snap1_map = statistcs_on_classification_predictions("data_need_label/snap1_mb_retrain.txt", web=False)

    #compute overlapping
    overlapping = 0
    for i in web_brand_snap1_map:
        web_domains = web_brand_snap1_map[i]
        mb_domains = mb_brand_snap1_map[i]
        overlapping += len(set(mb_domains).intersection(set(web_domains)))

    print (overlapping)
    for i in mb_brand_snap1_map:
        if len(mb_brand_snap1_map[i]) != len(mb_brand_map[i]):
            print ("FUCK", i, len(web_brand_snap1_map[i]))


def compare_web_mobile():
    f_mb = "MAY14.SNAP1.MOBILE.label"
    f_web = "MAY14.SNAP1.WEB.label"
    mb_label_, mb_brand = read_label_from(f_mb)
    web_label, web_brand = read_label_from(f_web)

    brands = map_domain_to_id.pop_brand
    for i in brands:
        web_mal = web_brand[i]
        mobile_mal = mb_brand[i]
        intersection = set(web_mal).intersection(set(mobile_mal))
        print ("Intersection", len(intersection))

        c = 0
        for i in mobile_mal:
            if i not in web_mal:
                c += 1
                print ("only in mobile", i)

        print ("only in mobile total", c)

        c = 0
        for i in web_mal:
            if i not in mobile_mal:
                c += 1
                print ("only in web", i)
        print ("only in web total", c)

        for i in mobile_mal:
            if i in web_mal:
                print ("both", i)


#WEB
#web_stat()
##2331
#Counter({'combo': 1737, 'typo': 296, 'bits': 116, 'wrongTLD': 99, 'homo': 83})
#read_label_from("MAY14.SNAP1.WEB.label")
#get_verfied_percent("MAY14.SNAP1.MOBILE.label")
#compare_web_mobile()
label_stat()