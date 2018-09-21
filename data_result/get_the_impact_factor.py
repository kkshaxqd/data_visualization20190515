# !/usr/bin/env python
# -*- coding: utf8 -*-
import pandas as pd
import sys,re
addinfo = 'E:\\haxqd\\201807\\JCR_IFINFO.txt'
jourifinfo = {}
with open(addinfo,'r',encoding='utf-8')as f:
    lines = f.readlines()
    #print(lines[0])
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        journame = info[1].lower()
        jourifinfo[journame] = info[3]
