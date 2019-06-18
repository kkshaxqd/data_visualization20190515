# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

#   读入基因型数据，根据数据库中的记录，计算相应的风险
#   首先要把记载的项目和风险型编号入座

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


import xlrd
fileshujuku = "xiaofeizhe_risk_project_data.xlsx"

def chuli_databasefile(fileshujuku):
    database_info = {}
    wb = xlrd.open_workbook(fileshujuku)
    sh1 = wb.sheet_by_index(0)
    # 递归显示每行数据
    for rownum in range(sh1.nrows):
        #print(sh1.row_values(rownum))  # 每一行的数据以数组形式存储
        hanglist = sh1.row_values(rownum)
        flag = hanglist[2]+":"+hanglist[3]
        info = ":".join(hanglist[5:9])
        database_info[flag] = info
    return database_info
# 所有项目基本数据字典
biyanaibase_info = {} #鼻咽癌

# 测试肿瘤篇
# 鼻咽癌
def  biyancancer(hang,value):
    if "鼻咽癌" in hang:
        #print("这是疾病篇鼻咽癌结果处理部分：")
        print("开始处理",hang)
        hang = re.sub("鼻咽癌:","",hang)
        valuesplit = value.split(':')
        genetypesplit = valuesplit[0].split('/')
        valuesplit[1] = re.sub("\(\d+\)","",valuesplit[1])
        genefreqsplit = valuesplit[1].split('/')
        generisksplit = valuesplit[2].split('/')
        geneorsplit = valuesplit[3].split('/')
        # 计算MOR 修正OR值，MOR = ORref*refFRQ% + ORhet*hetFRQ% + ORhom*homFRQ%   OR* = OR/MOR
        MOR = float(geneorsplit[0])*float(genefreqsplit[0]) + \
              float(geneorsplit[1])*float(genefreqsplit[1]) + \
              float(geneorsplit[2])*float(genefreqsplit[2])
        gene_ornew = [0]*3
        gene_ornew[0] = str(round(float(geneorsplit[0])/MOR,3))
        gene_ornew[1] = str(round(float(geneorsplit[1])/MOR,3))
        gene_ornew[2] = str(round(float(geneorsplit[2])/MOR,3))
        ornewvalue = "/".join(gene_ornew)  #数字不能直接这样转化为字符串
        print(valuesplit[0],valuesplit[1],"新OR",ornewvalue,valuesplit[2])
        biyanaibase_info[hang] = valuesplit[0]+":"+valuesplit[1]+":"+ornewvalue+":"+valuesplit[2] #例如CC/CT/TT:0.429/0.467/0.105:0.936/1.029/1.123

# 读取样本基因型
filein = "women23chip.txt"

def readbiyanai(filein):
    biyanairesult = {}
    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if "#" in line:
                pass
            else:
                line = line.strip('\n')
                linelist = line.split('\t')
                if linelist[0] == "rs9510787":
                    biyanairesult["rs9510787"] = linelist[3]
                elif linelist[0] == "rs29232":
                    biyanairesult["rs29232"] = linelist[3]
                elif linelist[0] == "rs2736098":
                    biyanairesult["rs2736098"] = linelist[3]
                elif linelist[0] == "rs402710":
                    biyanairesult["rs402710"] = linelist[3]
                elif linelist[0] == "rs2279744":
                    biyanairesult["rs2279744"] = linelist[3]
                elif linelist[0] == "rs6774494":
                    biyanairesult["rs6774494"] = linelist[3]
                elif linelist[0] == "rs2228000":
                    biyanairesult["rs2228000"] = linelist[3]
                elif linelist[0] == "rs1412829":
                    biyanairesult["rs1412829"] = linelist[3]
    return biyanairesult

def comparegenetype(biyanairesult,biyanaibase_info,rsid):
    rsid_split = biyanaibase_info[rsid].split(':')
    rsid_gene = rsid_split[0].split('/')
    #print(biyanairesult[rsid])
    #print(rsid_gene)
    for i in range(len(rsid_gene)):
        if biyanairesult[rsid] == rsid_gene[i]:
            needi = i
            break
        elif bianxingzu[biyanairesult[rsid]]== rsid_gene[i]:
            needi = i
    rsid_freq = rsid_split[1].split('/')
    rsid_or = rsid_split[2].split('/')
    risk_value = float(rsid_or[needi])
    if  risk_value < 0.9:
        risk = "该位点降低风险"
    elif risk_value>=0.9 and risk_value<=1.1:
        risk = "该位点正常风险"
    elif risk_value >1.1:
        risk = "该位点提高风险"

    print(rsid,biyanairesult[rsid],rsid_freq[needi],rsid_or[needi],risk)
    return rsid_freq[needi],rsid_or[needi]
# main

def main(fileshujuku):
    database_info = chuli_databasefile(fileshujuku)
    for key,value in database_info.items():
        biyancancer(key,value)    #  生成新的MOR修正后的OR值得，biyanaibase_info字典数据
    biyanairesult = readbiyanai(filein)  # 获得检测结果里相应rsid的基因型
    riskfactor = 1
    orresult = []
    print("rs位点","检测基因型结果","该基因型频率","该基因型风险值","风险结果")
    for key in biyanairesult.keys():
        key_freq,key_or = comparegenetype(biyanairesult, biyanaibase_info, key)
        orresult.append(float(key_or))
        riskfactor = riskfactor*float(key_or)
    risk_num = 0
    for j in orresult:
        if j>1.1:
            risk_num +=1

    if  riskfactor < 0.9 and risk_num == 0:
        riskrsult = "低风险"
    elif riskfactor>=0.9 and riskfactor<=1.1:
        riskrsult = "正常风险"
    elif riskfactor >1.1 and risk_num !=0:
        riskrsult = "高风险"
    else:
        riskrsult = "正常风险"
    print("食管癌项目总体风险值：",riskfactor)
    print("您的食管癌风险结果为：",riskrsult)









main(fileshujuku)