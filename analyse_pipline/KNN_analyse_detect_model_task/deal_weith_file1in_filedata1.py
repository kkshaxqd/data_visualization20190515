# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
fileshujuku = "filedata1.txt"
# 读取样本基因型
filein = "file1in.txt"

fileout="fileout.txt"

sampledict={}

with open(fileshujuku, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines[1:]:
        line = line.strip('\n')
        linelist = line.split('\t')
        linetag=linelist[1].split(' ')
        sampledict[linetag[0]]=linelist[0]+"_"+linetag[1]

with open(filein, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    with open(fileout, 'w', encoding='utf-8') as ww:
        out=lines[0].strip('\n')+"\tTAGRESULT"+"\n"
        ww.write(str(out))
    for line in lines[1:]:
        line = line.strip('\n')
        if sampledict.get(line):
            out=line+"\t"+sampledict[line]+"\n"
        else:
            out=line+"\t"+"."+"\n"
        with open(fileout, 'a', encoding='utf-8') as ww:
            ww.write(str(out))


