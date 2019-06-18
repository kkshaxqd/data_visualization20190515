# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

"""
分析脚本,对SV统计结果，提取内异症与卵巢癌SV判断是否有重叠的
"""


file2="E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\statsv.txt"
file1="E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\neiyizheng\\statsv.txt"
ovsvdict={}
def creatdict():
    with open(file2, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip('\n')
                linelist = line.split('\t')
                ovsvdict[linelist[0]]=linelist[2]+" "+linelist[1]

def pointqianhou(point,detectpoint,region=50):
    pointqian=int(point)-int(region)
    pointhou=int(point)+int(region)
    #print('比较大小',pointqian,pointhou)
    flag = 0
    for number in range(pointqian,pointhou):
        if int(detectpoint) == number:
            #print("maybe fusion")
            flag= 1
            break

    return flag

def panduanwheatherxiangjiao(yuansvsplitpoint,yuansample):
    #print('处理',svsplitpoint)
    svsplitpoint = yuansvsplitpoint.split('_')
    for svbufen in svsplitpoint:
        svbufenlist = svbufen.split(':')
        for k in ovsvdict.keys():
            klist = k.split('_')
            for klistlist in klist:
                klistlistfen = klistlist.split(':')
                if svbufenlist[0] == klistlistfen[0]:
                    resultflag = pointqianhou(svbufenlist[1], klistlistfen[1])
                    if resultflag == 1:
                        print(yuansvsplitpoint, yuansample, k, ovsvdict[k],"可能交叉")
                        break


def readdictandcompare():
    creatdict()
    with open(file1, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            panduanwheatherxiangjiao(linelist[0],linelist[1])


readdictandcompare()