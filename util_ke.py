#!/usr/bin/env python
# -*- coding: utf-8 -*-


def read_results(file):
    f = open(file, "r")
    pattern = "----"
    pre_res = {}
    domains = list()
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0 or not pattern in line:
            continue
        res = line.split(pattern)
        domain = res[0]
        pre = float(res[1])
        pre_res[domain] = pre
        domains.append(domain)

    return pre_res, domains


def analyze_web_mobile_from_brand_idx(idx):

    web_res, web_domains = read_results("./out/"+ idx +"_web.result")
    mobile_res, mb_domains = read_results("./out/"+ idx +"_mobile.result")

    web_mal = list()
    mobile_mal = list()

    for i in web_res:
        if web_res[i] == 1.0:
            web_mal.append(i)

    for i in mobile_res:
        if mobile_res[i] == 1.0:
            mobile_mal.append(i)

    print ("WEB", len(set(web_mal)))
    print ("MOBILE", len(set(mobile_mal)))

    intersection =set(web_mal).intersection(set(mobile_mal))
    print ("Intersection", len(intersection))

    c = 0
    for i in mobile_mal:
        if i not in web_mal:
            c += 1
            #print ("only in mobile", i)
    print ("only in mobile total", c)

    c = 0
    for i in web_mal:
        if i not in mobile_mal:
            c += 1
    print ("only in web total", c)

    for i in mobile_mal:
        if i in web_mal:
            print ("BOTH", i)

    return


def write_a_list_into_file(F, ALIST):
    f = open(F, 'a+')
    f.writelines(["%s\n" % item for item in ALIST])
    f.close()


def generate_scp_file_mobile(idx, OUT_PUT = "snap1_mb.txt"):
    """
    xn--fcebook-pwa.com..redirect
    xn--fcebook-pwa.com..screen.png
    xn--fcebook-pwa.com..screen.txt
    xn--fcebook-pwa.com..source.txt
    """
    DIR = "/home/ketian/ChromeHeadless/snapApr01/MOBILE/"
    mobile_res, mb_domains = read_results("./out/" + idx + "_mobile.result")

    print ("LEN OF MOBILE DOMAINS", len(mb_domains))

    file_list = list()
    for i in mb_domains:
        i = DIR + idx + "_mobile/" + i
        img = i + "..screen.png"
        img_text = i + "..screen.txt"
        source = i + "..source.txt"
        redirect = i + "..redirect"
        file_list.extend([img, img_text, source, redirect])

    write_a_list_into_file(OUT_PUT, ALIST=file_list)


def generate_scp_file_web(idx, OUT_PUT = "snap1_all.txt"):
    """
    xn--fcebook-pwa.com..redirect
    xn--fcebook-pwa.com..screen.png
    xn--fcebook-pwa.com..screen.txt
    xn--fcebook-pwa.com..source.txt
    """
    DIR = "/home/ketian/ChromeHeadless/snapApr01/"
    web_res, web_domains = read_results("./out/" + idx + "_web.result")
    print ("LEN OF WEB DOMAINS", len(web_domains))

    file_list = list()
    for i in web_domains:
        i = DIR + idx + "/" + i
        img = i + "..screen.png"
        img_text = i + "..screen.txt"
        source = i + "..source.txt"
        redirect = i + "..redirect"
        file_list.extend([img, img_text, source, redirect])

    write_a_list_into_file(OUT_PUT, ALIST=file_list)


def generate_all_idxs():
    for i in range(766):
        generate_scp_file_web(str(i))
        generate_scp_file_mobile(str(i))

    print ("DONE on generate scp files")