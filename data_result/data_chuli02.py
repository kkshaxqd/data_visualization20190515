# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
filename = 'E:\\data\\前列腺癌PRADDATA\\geneid.txt'
outname = 'E:\\data\\前列腺癌PRADDATA\\geneid_reuslt.txt'
with open(filename,'r',encoding='utf-8')as f:
    lines = f.readlines()
    #print(lines[0])
    for line in lines:
        line = line.strip('\n')
        if re.findall('Tags',line):
            hangshou = line + '\n'
            with open(outname,'w')as ww:
                ww.write(str(hangshou))
        elif re.findall('CTBP1',line):
            ctbp1 = line + '\n'
            with open(outname,'a')as ww:
                ww.write(str(ctbp1))
        elif re.findall('^AR\t',line):
            ar = line + '\n'
            with open(outname,'a')as ww:
                ww.write(str(ar))
        elif re.findall('^CTNNB1\t',line):
            ar = line + '\n'
            with open(outname,'a')as ww:
                ww.write(str(ar))



