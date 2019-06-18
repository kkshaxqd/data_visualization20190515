# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
def last():
    file1 = "E:\\haxqd\\201811\\18R17344_S1_L004.hg19.filterresult_by_gene_by_name.txt"
    file2 = "E:\\haxqd\\201811\\18R17345_S2_L004.hg19.filterresult_by_gene_by_name.txt"

    file_common = "E:\\haxqd\\201811\\18R17344_18R17345_common.tsv"
    file1_different = "E:\\haxqd\\201811\\18R17344_S1_different.tsv"
    file2_different = "E:\\haxqd\\201811\\18R17345_S2_L004_different.tsv"
def last2():
    file1 = "E:\\haxqd\\201811\\18R17344_S1_L004.hg19.filterresult_by_gene.txt"
    file2 = "E:\\haxqd\\201811\\18R17345_S2_L004.hg19.filterresult_by_gene.txt"

    file_common = "E:\\haxqd\\201811\\noselectbyname\\18R17344_18R17345_noselect_common.tsv"
    file1_different = "E:\\haxqd\\201811\\noselectbyname\\18R17344_S1_noselect_different.tsv"
    file2_different = "E:\\haxqd\\201811\\noselectbyname\\18R17345_S2_noselect_different.tsv"

file1 = "E:\\haxqd\\201811\\18R17344_S1_L004.hg19.filterresult_by_gene_select.txt"
file2 = "E:\\haxqd\\201811\\18R17345_S2_L004.hg19.filterresult_by_gene_select.txt"

file_common = "E:\\haxqd\\201811\\noselectbyname\\18R17344_18R17345_select_common.tsv"
file1_different = "E:\\haxqd\\201811\\noselectbyname\\18R17344_S1_select_different.tsv"
file2_different = "E:\\haxqd\\201811\\noselectbyname\\18R17345_S2_select_different.tsv"

def filecontent(file):
    dict = {}
    with open(file,'r', encoding='utf-8')as f:
        lines = f.readlines()
        hang = lines[0].strip('\n')
        for line in lines[1:]:
            line = line.strip('\n')
            linlist = line.split('\t')
            flag = "\t".join(linlist[0:5])
            #print(flag)
            dict[flag] = line
        return dict,hang

dictfile1,hang = filecontent(file1)
dictfile2,hang = filecontent(file2)

commonkey = dictfile1.keys() & dictfile2.keys()
#print(commonkey)
dictfile1_different = dictfile1.keys() - dictfile2.keys()
#print(dictfile1_different)
dictfile2_different = dictfile2.keys() - dictfile1.keys()
#print(dictfile2_different)
def write_dict(keylist, dictfile,hang,fileout):
    with open(fileout, 'w', encoding='utf-8')as ww:
        outlang = hang+"\n"
        ww.write(str(outlang))
    for key in keylist:
        out = dictfile[key]
        with open(fileout, 'a', encoding='utf-8')as ww:
            outlang = out + "\n"
            ww.write(str(outlang))

def main():
    #common
    write_dict(commonkey,dictfile1,hang,file_common)
    #different1
    write_dict(dictfile1_different,dictfile1,hang,file1_different)
    #different2
    write_dict(dictfile2_different,dictfile2,hang,file2_different)

if __name__ == "__main__":
    main()