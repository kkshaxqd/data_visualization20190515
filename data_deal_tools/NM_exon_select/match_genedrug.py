# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re,io
import pandas as pd
filein = 'liver_info_drug.txt'
addfile = "liver_gene.txt"
fileout = 'liver_info_drug_addliver_gene.txt'

adddict = {}
geneflag = {}
with open(addfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        #print(line)
        #info = line.split('\t')
        if line:
            adddict[line] = 1
def write_all_info():
    excel_add = u'E:\\haxqd\\myscript\\GEZHI_Script\\靶向药20180510.xlsx'
    ad = pd.read_excel(excel_add,sheet_name="All-info") # 取第二个sheet表，第一行作为标题
    writer = pd.ExcelWriter(r'E:\\haxqd\\myscript\\GEZHI_Script\\all_targetdrug_info.xlsx')
    ad.to_excel(writer,'Sheet1',index_label=None,index = False)
    writer.save()


def all_target_drug(file="all_info.txt",fileout="all_info_high_liver_gene.txt"):
    with open(file,'r',encoding='utf-8')as g:
        lines = g.readlines()
        for line in lines:
            line = line.strip('\n')
            if re.search(r"商用药物机理",line):
                with open(fileout, "w", encoding='utf-8')as ww:
                    out = line + "\n"
                    ww.write(str(out))
            else:
                outstr = []
                for gene in adddict:
                    if re.search(gene,line):
                        #,re.IGNORECASE
                        outstr.append(gene)
                outline = "\t".join(outstr)
                print(outline)
                if outline:
                    with open(fileout, "a", encoding='utf-8')as ww:
                        out = line + "\t"+outline+"\n"
                        ww.write(str(out))

#all_target_drug()

def liver_target_drug():
    with open(filein,'r',encoding='utf-8')as g:
        lines = g.readlines()
        for line in lines:
            line = line.strip('\n')
            if re.search(r"染色体位置",line):
                with open(fileout, "w", encoding='utf-8')as ww:
                    out = line + "\n"
                    ww.write(str(out))
            else:
                outstr = []
                for gene in adddict:
                    if re.search(gene,line):
                        outstr.append(gene)
                outline = "\t".join(outstr)
                print(outline)
                with open(fileout, "a", encoding='utf-8')as ww:
                    out = line + "\t"+outline+"\n"
                    ww.write(str(out))

liver_target_drug()