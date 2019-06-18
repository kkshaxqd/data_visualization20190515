# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
filein = 'fanzhaun_use.txt'
fileout = 'fanzhaun_use_result.txt'

with open(filein, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    hang = lines[0].strip('\n')
    out = hang + "\n"
    with open(fileout, 'w', encoding='utf-8')as ww:
        ww.write(str(out))
    for line in lines[1:]:
        line = line.strip('\n')
        #line = line.strip()
        linelist = line.split('\t')
        print(linelist[0],"=",linelist[2])
        if linelist[0] == linelist[2]:
            out = line + "\n"
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(out))
        else:
            out = line + "\tbuyiyang"+"\n"
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(out))

