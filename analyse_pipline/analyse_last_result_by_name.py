# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys


filein = "E:\\haxqd\\201811\\18R17344_S1_L004.hg19.filterresult_by_gene.txt"
fileout = "E:\\haxqd\\201811\\18R17344_S1_L004.hg19.filterresult_by_gene_by_name.txt"
NAME = "ataxia"
#NAME1 = "incoordination"
#NAME2 = "dystaxia"
#NAME3 = "asynergy"

def get_result_by_name(filein,fileout,NAME):
    with open(filein,'r', encoding='utf-8')as f:
        lines = f.readlines()
        hang = lines[0]
        outlang = hang
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(outlang))
        for line in lines[1:]:
            if NAME in line:
                out = line
                with open(fileout, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))

filein1 = "E:\\haxqd\\201811\\18R17345_S2_L004.hg19.filterresult_by_gene.txt"
fileout1 = "E:\\haxqd\\201811\\18R17345_S2_L004.hg19.filterresult_by_gene_by_name.txt"

get_result_by_name(filein,fileout,NAME)
get_result_by_name(filein1,fileout1,NAME)