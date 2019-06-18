# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

filein = "E:\\haxqd\\201811\\18R17344_S1_L004_last_cnv.txt"
fileout = "E:\\haxqd\\201811\\18R17344_S1_L004_last_cnv_select_by_ataxiagene.txt"
filegene = "E:\\haxqd\\201811\\ataxia.txt"


filein1 = "E:\\haxqd\\201811\\18R17345_S2_L004_last_cnv.txt"
fileout1 = "E:\\haxqd\\201811\\18R17345_S2_L004_last_cnv_select_by_ataxiagene.txt"

def ataxiagene(filegene):
    genedict = []
    with open(filegene,'r', encoding='utf-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            #print(line)
            genedict.append(line)
    return genedict

def main(filein,fileout):
    with open(filein,'r', encoding='utf-8')as f:
        lines = f.readlines()
        hang = lines[0].strip('\n')
        outlang = hang+"\t"+r"符合的ataxia基因"+"\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(outlang))
        genedict = ataxiagene(filegene)
        print(genedict)
        for line in lines[1:]:
            line = line.strip('\n')
            fuhegene = []
            for gene in genedict:
                if re.search(gene,line):
                    print(re.search(gene,line).group())
                    fuhegene.append(gene)
            print(len(fuhegene))
            if len(fuhegene)>0:
                fuheout = ";".join(fuhegene)
                out = line + "\t" +fuheout + "\n"
                with open(fileout, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))

main(filein,fileout)



