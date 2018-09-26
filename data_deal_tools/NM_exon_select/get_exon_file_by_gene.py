# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re,io

filein = r'E:\haxqd\201809\epilepsy.txt'
addfile = r"E:\haxqd\myscript\joingenetic\bed\WES.bed"
fileout = r'E:\haxqd\201809\epilepsy.bed'

genedict = {}

with open(filein,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        genedict[line] = 1

def write_file(out):
    with open(fileout,"a",encoding='utf-8')as ww:
        out = out +"\n"
        ww.write(str(out))

def main():
    with open(addfile,'r',encoding='utf-8')as g:
        lines = g.readlines()
        for line in lines:
            line = line.strip('\n')
            info = line.split('\t')
            if genedict.get(info[3]):
                print(info[3])
                write_file(line)



main()