# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re,io
addfile = "liver_info_drug.txt"
filein = "highfre_gene_needlist.txt"
fileout = "highfre_gene_needlist_add_liver_info_drug.txt"



with open(filein,"r",encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split("\t")
        if re.search(r"突变类型",line):
            with open(fileout,"w",encoding='utf-8')as ww:
                outline = line+"\t"+r"liver_drug"+"\n"
                ww.write(str(outline))
        else:
            out = "None"
            with open(addfile,"r",encoding='utf-8')as g:
                glines = g.readlines()
                for gline in glines:
                    gline = gline.strip("\n")
                    ginfo = gline.split("\t")
                    if re.search(r"FDA批准上市|\.",ginfo[4]):
                        continue
                    if info[0] in gline:
                        print(info[0],ginfo[0])
                        if out == "None":
                            out = ginfo[0]
                        else:
                            out = out+";"+ginfo[0]
            if re.search(";",out):
                newcontent = out.split(";")
                conteng = list(set(newcontent))
                conteng.sort(key=newcontent.index)
                out = ";".join(conteng)
            with open(fileout,"a",encoding='utf-8')as ww:
                outline = line+"\t"+out+"\n"
                ww.write(str(outline))