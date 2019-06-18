# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

# 定义基因型变形组字典
bianxingzu = {
    "AA":"TT",
    "TT":"AA",
    "CC":"GG",
    "GG":"CC",
    "AT":"TA",
    "AC":"CA",
    "AG":"GA",
    "TA":"AT",
    "TC":"CT",
    "TG":"GT",
    "CA":"AC",
    "CT":"TC",
    "CG":"GC",
    "GA":"AG",
    "GT":"TG",
    "GC":"CG"
}
#rs78378222	17:7571752:rs78378222:T:G	all/TT/GG/GT	0.995(2492)/0.000399361022364217(1)/0.004(11)
#rs12951053	17:7577407:rs12951053:A:C	AA/AC/CC	0.476(50)/0.448(47)/0.076(8)
#rs1042522	17:7579472:rs1042522:G:C,T	GG/CC/CG	0.152(16)/0.352(37)/0.495(52)
#rs2078486	17:7583083:rs2078486:G:A,C	GG/AA/AG	0.505(53)/0.057(6)/0.438(46)
#rs78378222 A/C
#rs12951053 A/C
#rs1042522 C/G
#rs2078486 A/G

tp53gf = {
    'rs78378222_AA':'0.995',
    'rs78378222_AC':'0.004',
    'rs78378222_CC':'0.0004',
    'rs12951053_AA':'0.476',
    'rs12951053_AC':'0.448',
    'rs12951053_CC':'0.076',
    'rs1042522_GG':'0.352',
    'rs1042522_CC':'0.152',
    'rs1042522_CG':'0.495',
    'rs2078486_GG':'0.505',
    'rs2078486_AA': '0.057',
    'rs2078486_AG': '0.438',
}
filein = 'testrsor.txt'
fileout = 'testrsor_xiuzheng_or.txt'

with open('testrsor.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    hangshou = lines[0]
    with open('testrsor_xiuzheng_or.txt', 'w', encoding='utf-8')as gg:
        outss = hangshou
        gg.write(str(outss))
    for line in lines[1:]:
        line = line.strip('\n')
        linelist = line.split('\t')
        rsidgt1 = linelist[0]+"_"+linelist[1]
        rsidgt2 = linelist[0] + "_" + linelist[3]
        rsidgt3 = linelist[0] + "_" + linelist[5]
        or1 = float(linelist[2])
        or2 = float(linelist[4])
        or3 = float(linelist[6])
        print(tp53gf[rsidgt1],or1)
        MOR = (float(tp53gf[rsidgt1])*or1) + (float(tp53gf[rsidgt2])*or2) + (float(tp53gf[rsidgt3])*or3)
        print(MOR)
        linelist[2] = str(round(or1/MOR,3))
        linelist[4] = str(round(or2/MOR,3))
        linelist[6] = str(round(or3/MOR,3))
        outnew = '\t'.join(linelist)
        with open('testrsor_xiuzheng_or.txt', 'a', encoding='utf-8')as gg:
            outss = outnew + "\n"
            gg.write(str(outss))

