# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re,io

addfile = "all_info.txt"
filein = "highfre_gene_needlist.txt"
fileout = "highfre_gene_needlist_add_all_drug_info.txt"
lineli=0
addmingandict = {}
addnaiyaodict = {}
with open(addfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split("\t")
        lineli=lineli+1
        print(lineli,info[9])
        if re.search(r"商用药物机理",line):
            continue
        elif re.search(r"耐药性增加|敏感性降低|毒性增加",info[9]):
            flag = info[7]+":"+info[8]
            content = info[4]+":"+info[10]
            try:
                if addnaiyaodict[flag]:
                    addnaiyaodict[flag]=addnaiyaodict[flag]+";"+content
            except KeyError:
                addnaiyaodict[flag] = content
        elif re.search(r"敏感性增加|\.",info[9]):
            flag = info[7]+":"+info[8]
            content = info[4]+":"+info[10]
            try:
                if addmingandict[flag]:
                    addmingandict[flag]=addmingandict[flag]+";"+content
            except KeyError:
                addmingandict[flag] = content
## 数组去重
def quchong():
    for gene in addmingandict:
        if re.search(";",addmingandict[gene]):
            newcontent = addmingandict[gene].split(";")
            conteng = list(set(newcontent))
            conteng.sort(key=newcontent.index)
            addmingandict[gene] = ";".join(conteng)


with open(filein,"r",encoding='utf-8')as g:
    lines = g.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split("\t")
        if re.search(r"突变类型",line):
            with open(fileout,"w",encoding='utf-8')as ww:
                out = line+"\t"+r"Drug_anno(敏感增加或.)"+"\t"+r"Drug_anno(毒性增加或敏感降低或耐药提高)"+"\n"
                ww.write(str(out))
        else:
            outfl = "None"
            outg1 = "None"
            for key in addmingandict:
                genefl = key.split(":")
                if info[0] in genefl:
                    if outfl == "None":
                        outfl = addmingandict[key]
                    else:
                        outfl = outfl + "||" + addmingandict[key]
            for key in addnaiyaodict:
                genegl = key.split(":")
                if info[0] in genegl:
                    if outg1 == "None":
                        outg1 = addnaiyaodict[key]
                    else:
                        outg1 = outg1 + "||" + addnaiyaodict[key]
            with open(fileout,"a",encoding='utf-8')as ww:
                out = line+"\t"+outfl+"\t"+outg1+"\n"
                ww.write(str(out))



