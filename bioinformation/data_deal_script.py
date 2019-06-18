# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

filein = "E:\\haxqd\\00杨明燕任务\\SNP-TP53_20190606-1 SNP HF Result.txt"
fileout = "E:\\haxqd\\00杨明燕任务\\SNP-TP53_20190606-1.10SITE.txt"



with open(filein, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    hang = lines[0]
    with open(fileout, 'w', encoding='utf-8')as ww:
        ww.write(str(hang))
    for line in lines[1:]:
        if "Well" in line:
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(line))
        else:
            line = line.strip("\n")
            linelsit = line.split("\t")
            linelsit[5]=linelsit[5].replace(" ", "")
            #print(linelsit[5])
            print(len(linelsit[5]))
            if len(linelsit[5])==10:
                out = line+"\n"
                with open(fileout, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))
