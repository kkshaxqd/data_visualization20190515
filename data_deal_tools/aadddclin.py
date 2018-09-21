# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re

addfile = 'E:\\data\\前列腺癌PRADDATA\\Clinical_BCR_XML.merge.txt'
hang_dict={}
with open(addfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        if re.findall('A0_Samples',line):
            hang_dict['A0_Samples'] = line
            continue
        elif re.findall("TCGA",line):
            lang_list = line.split('\t')
            gebename = re.split("-", lang_list[0])
            flag = gebename[1] + '-' + gebename[2]
            flag = str(flag.lower())
            hang_dict[flag] = line

inputfile = 'E:\\haxqd\\201806\\70ctbpvalue.txt'
with open(inputfile,'r',encoding='utf-8')as p:
    langs = p.readlines()
    for lang in langs:
        lang = lang.strip('\n')
        if re.findall('patient',lang):
            hangshou = lang+'\t'+hang_dict["A0_Samples"]+'\n'  #这样是OK的
            with open('E:\\haxqd\\201806\\70ctbpvalue_info.txt','w')as ww:
                ww.write(str(hangshou))
            continue
        else:
            line_list = lang.split('\t')
            sample = re.split("-", line_list[0])
            flagc = str(sample[1] + '-' + sample[2])
            flagc = flagc.lower()
            if flagc in hang_dict.keys():
                outinfo = lang + '\t' + str(hang_dict[flagc]) + '\n'
                with open('E:\\haxqd\\201806\\70ctbpvalue_info.txt', 'a')as ww:  # 这才是追加 w+不是，也是替换
                    ww.write(str(outinfo))