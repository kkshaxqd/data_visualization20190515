# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re,io

filein = 'jjjkkglg.txt'
addfile = "04_WES.uniq.bed"
fileout = 'jjjkkglg_addgene_exon.txt'

adddict = {}
geneflag = {}
with open(addfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        #print(info[3])
        try:
            if adddict[info[3]] and geneflag[info[3]]:
                geneflag[info[3]] = geneflag[info[3]]+1
                adddict[info[3]] = adddict[info[3]]+","+info[1]+".."+info[2]+"..exon"+str(geneflag[info[3]])
        except KeyError:
            geneflag[info[3]]=1
            adddict[info[3]] = info[0]+":"+info[1]+".."+info[2]+"..exon"+str(geneflag[info[3]])
def main():
    with open(filein,'r',encoding='utf-8')as g:
        lines = g.readlines()
        for line in lines:
            line = line.strip('\n')
            info = line.split('\t')
            if re.search(r"基因",info[1]):
                print(r"行首")
                with open(fileout,"w",encoding='utf-8')as ww:
                    out = line+"\n"
                    ww.write(str(out))
            elif re.search("p\.",info[2]):
                with open(fileout,"a",encoding='utf-8')as ww:
                    out = line+"\n"
                    ww.write(str(out))
            else:
                try:
                    if adddict[info[1]]:
                        with open(fileout,"a",encoding='utf-8')as ww:
                            out = info[0]+"\t"+info[1]+"\t"+info[2]+"\t"+adddict[info[1]]+"\n"
                            ww.write(str(out))
                except:
                    with open(fileout, "a", encoding='utf-8')as ww:
                        out = line + "\n"
                        ww.write(str(out))


def find_gene_exon(gene):
    print(adddict[gene])


find_gene_exon("BCR")
