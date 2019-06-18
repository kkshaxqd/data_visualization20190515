# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
def heisesucancer():
    filein = 'E:\\data\\黑色素瘤临床\\ClinicalFull_matrix.txt'
    fileout = 'E:\\data\\黑色素瘤临床\\Clinical_add_ctbp1_fxbw7_FPKM_content_AIPANG.txt'
    fileadd = "E:\\data\\TCGA-FPKM-CANCERTISSUE\\CTBP1-FXBW7.txt"

    tcgadict = {}

    with open(fileadd, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        hanglist = lines[0].strip('\n').split('\t')

        ctbp1list = lines[1].strip('\n').split('\t')

        fxbw7list = lines[2].strip('\n').split('\t')

        for i in range(1,len(hanglist)):
            key = hanglist[i].rsplit('-',1)[0]
            #print(key.rsplit('-',1)[0])
            tcgadict[key]=ctbp1list[i]+"\t"+fxbw7list[i]

    #for key in tcgadict:
    #    print(key,tcgadict[key])

    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        hang = lines[0].strip('\n')
        out = hang + "\t"+ "CTBP1"+"\t"+"FXBW7"+"\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(out))
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split("\t")
            #print(linelist[1])
            #这个文件里linelist[1]是tcga编号
            if tcgadict.get(linelist[1]):
                #print(linelist[1])
                out = line +"\t"+tcgadict[linelist[1]]+"\n"
            else:
                out = line + "\t" +"."+"\t"+"."+"\n"
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(out))


def breastcancer():
    filein = 'E:\\data\\TCGA-BRCA-CLIN\\Clinical BCR XML.merge.txt'
    fileout = 'E:\\data\\TCGA-BRCA-CLIN\\Clinical_add_ctbp1_rad51_FPKM_content_AIPANG.txt'
    fileadd = "E:\\data\\TCGA-BRCA\\0need-ctbp1.info.txt"

    tcgadict = {}

    with open(fileadd, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        hanglist = lines[0].strip('\n').split('\t')

        ctbp1list = lines[2].strip('\n').split('\t')

        rad51list = lines[1].strip('\n').split('\t')

        for i in range(1, len(hanglist)):
            key = hanglist[i].rsplit('-', 1)[0]
            # print(key.rsplit('-',1)[0])
            tcgadict[key] = ctbp1list[i] + "\t" + rad51list[i]

    # for key in tcgadict:
    #    print(key,tcgadict[key])

    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        hang = lines[0].strip('\n')
        out = hang + "\t" + "CTBP1" + "\t" + "RAD51" + "\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(out))
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split("\t")
            # print(linelist[1])
            # 这个文件里linelist[1]是tcga编号
            if tcgadict.get(linelist[0]):
                # print(linelist[1])
                out = line + "\t" + tcgadict[linelist[0]] + "\n"
            else:
                out = line + "\t" + "." + "\t" + "." + "\n"
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(out))

breastcancer()