# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys


filein= 'rs匹配.txt'
fileadd = 'rsnewor.txt'
fileout = 'rs匹配结果.txt'


ordict = {}
with open(fileadd,'r',encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines[1:]:
        line = line.strip('\n')
        linelist = line.split('\t')
        flag = linelist[0] + ":"+linelist[1]
        ordict[flag]=linelist[2]

with open(filein,'r',encoding='utf-8') as f:
    lines = f.readlines()
    hang = lines[0].strip('\n')+"\t"+"新OR\n"
    with open(fileout,'w',encoding='utf-8') as ww:
        ww.write(str(hang))
    for line in lines[1:]:
        line = line.strip('\n')
        linelist = line.split('\t')
        flag = linelist[0] + ":"+linelist[1]
        out = line + "\t"+ordict[flag]+"\n"
        with open(fileout,'a',encoding='utf-8') as ww:
            ww.write(str(out))