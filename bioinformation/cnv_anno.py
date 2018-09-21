# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re

addfile = "E:\\haxqd\\myscript\\GEZHI_Script\\CNV_ANNO_find_liver_cancer_type\\gene_coord.txt"
inputfile ="E:\\haxqd\\cnvdata.txt"
add_dict = {}
with open(addfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        line_list = line.split('\t')
        flag = line_list[0]+'-'+line_list[1]+'-'+line_list[2]
        add_dict[flag] = line_list[3]

with open(inputfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        line_list = line.split('\t')
        if re.findall('SAMPLE_NAME',line):
            hangshou = line + 'GENE' + '\n'
            with open('E:\\haxqd\\cnvdata.anno.txt','w')as ww:
                ww.write(str(hangshou))
        else:
             chrpo = 'chr'+line_list[1]
             out = None
             for key,value in add_dict.items():
                 #print(key) ok
                 add_gene = key.split('-')
                 if add_gene[0] == chrpo:
                     #print('get') ok
                     if line_list[2] < add_gene[2] and line_list[3] > add_gene[1]:
                        if out:
                             out = out + '|' + value
                        else:
                            out = value

             outlang = line+'\t'+str(out)+'\n'
             with open('E:\\haxqd\\cnvdata.anno.txt', 'a')as ww:
                 ww.write(str(outlang))





