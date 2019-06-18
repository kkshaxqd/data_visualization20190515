# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
import scipy.stats as stats
import numpy as np

filein1 = "E:\\data\\TCGA-BRCA\\HTSeq-FPKM-gene.merge.txt"
filein2 = "E:\\data\\TCGA-PRAD\\HTSeq-FPKM-gene.merge.txt"
filein3 = "E:\\data\\TCGA-SKCM-FPKM\\HTSeq-FPKM-gene.merge.txt"

fileout = "ctbp1-other-gene-corr.info.txt"

filein4 = "E:\\data\\TCGA-STAD\\HTSeq-FPKM-gene.merge.txt"
filein5 = "E:\\data\\TCGA-LUAD\\HTSeq-FPKM-gene.merge.txt"
filein6 = "E:\\data\\TCGA-BLCA\\HTSeq-FPKM-gene.merge.txt"


def dealfile(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        out = "TAGS" + "\t" + "CTBP1" + "\t" + r"相关性" +"\t"+r"P值"+"\n"
        outfile = file+".ctbp1_corr_result.txt"
        with open(outfile, 'w', encoding='utf-8')as ww:
            ww.write(str(out))
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split("\t")
            if linelist[0]=="CTBP1":
                ctbp1 = [float(x) for x in linelist[1:] if x != "."]
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split("\t")
            if linelist[0]!="CTBP1":
                othergene = [float(x) for x in linelist[1:] if x != "."]
                #print(ctbp1,othergene)
                corvalue,pvalue = stats.pearsonr(ctbp1, othergene) #np.float64
                corvalue = corvalue.item()
                pvalue = pvalue.item()
                print(corvalue, pvalue)
                corvalue = '%.4f' %corvalue
                if float(corvalue)<-0.5:
                    print(corvalue)
                pvalue = '%.6f' %pvalue
                if abs(float(corvalue))>=0.5:
                    #print(linelist[0],corvalue, pvalue)
                    out = linelist[0]+"\tCTBP1"+"\t"+corvalue+"\t"+pvalue+"\n"
                    with open(outfile, 'a', encoding='utf-8')as ww:
                        ww.write(str(out))
    return outfile

def ctbp1main():
    brca_file = dealfile(filein1)
    prad_file = dealfile(filein2)
    skcm_file = dealfile(filein3)


    stad_file = dealfile(filein4)
    luad_file = dealfile(filein5)
    blca_file = dealfile(filein6)


def dealmaea(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        out = "TAGS" + "\t" + "MAEA" + "\t" + r"相关性" +"\t"+r"P值"+"\n"
        outfile = file+".maea_corr_result.txt"
        with open(outfile, 'w', encoding='utf-8')as ww:
            ww.write(str(out))
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split("\t")
            if linelist[0]=="MAEA":
                maea = [float(x) for x in linelist[1:] if x != "."]
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split("\t")
            if linelist[0]!="MAEA":
                othergene = [float(x) for x in linelist[1:] if x != "."]
                #print(maea,othergene)
                corvalue,pvalue = stats.pearsonr(maea, othergene) #np.float64
                corvalue = corvalue.item()
                pvalue = pvalue.item()
                #print(corvalue, pvalue)
                corvalue = '%.4f' %corvalue
                if float(corvalue)<-0.5:
                    #print(corvalue)
                    pass
                pvalue = '%.6f' %pvalue
                if abs(float(corvalue))>=0.5:
                    print(linelist[0],corvalue, pvalue)
                    out = linelist[0]+"\tMAEA"+"\t"+corvalue+"\t"+pvalue+"\n"
                    with open(outfile, 'a', encoding='utf-8')as ww:
                        ww.write(str(out))
    return outfile

def MAEAmain():
    print("BRCA")
    brca_file = dealmaea(filein1)
    print("PRAD")
    prad_file = dealmaea(filein2)
    print("SKCM")
    skcm_file = dealmaea(filein3)

    print("STAD")
    stad_file = dealmaea(filein4)
    print("LUAD")
    luad_file = dealmaea(filein5)
    print("BLCA")
    blca_file = dealmaea(filein6)

MAEAmain()