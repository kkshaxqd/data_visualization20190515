# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

filein = "E:\\data\\TCGA-BRCA\\HTSeq - FPKM.merge.txt"
fileout = "E:\\data\\TCGA-BRCA\\0need-ctbp1.info.txt"
with open(filein, 'r', encoding='utf-8') as f:
    lines = f.readlines()

    hang = lines[0]

    with open(fileout, 'w', encoding='utf-8')as ww:
        ww.write(str(hang))

    for line in lines[1:]:
        if "ENSG00000159692" in line:
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(line))
        elif "ENSG00000051180" in line:
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(line))
