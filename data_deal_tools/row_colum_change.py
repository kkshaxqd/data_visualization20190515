# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
import pandas as pd
import math

"""实现行列互换,OK,就是这样处理太花时间了"""

filename = 'E:\\data\\前列腺癌PRADDATA\\data_RNA_Seq_v2_expression_median.txt'
clinname = 'E:\\data\\前列腺癌PRADDATA\\Clinical BCR XML.merge.txt'
b=[]
with open(filename,'r',encoding='utf-8')as f:
    for x in f.readlines():
        s1 = []
        s = x.strip('\n')
        s0=s.split('\t')
        for i in range(len(s0)):
            s1.append(s0[i])
        b.append(s1)

for k in zip(*b):
    for y in k:
        with open('E:\\data\\前列腺癌PRADDATA\\outfilePRAD.txt','a')as ww:
            ww.write(y+'\t')
    with open('E:\\data\\前列腺癌PRADDATA\\outfilePRAD.txt', 'a')as ww:
        ww.write('\n')

#print(list(map(list, zip(*a))))  #是否这样输出会让速度变快  newa = list(map(list, zip(*a)))


