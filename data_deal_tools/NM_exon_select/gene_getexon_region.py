# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re,io

filein = 'target_genefile.txt'
addfile = "04_WES.uniq.bed"
fileout = 'target_genefile.txt_addgene_exon.txt'

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

def get_exon_by_gene(gene="KIT"):
    region = adddict[gene]
    return region

def main():
    with open(filein,'r',encoding='utf-8')as g:
        lines = g.readlines()
        for line in lines:
            line = line.strip('\n')
            if re.search("TARGET_GENE",line):
                print(r"行首")
                with open(fileout,"w",encoding='utf-8')as ww:
                    out = line+"\t"+"REGION"+"\n"
                    ww.write(str(out))
            elif re.match("\.",line):
                with open(fileout,"a",encoding='utf-8')as ww:
                    out = line+"\t"+"."+"\n"
                    ww.write(str(out))
            else:
                try:
                    region = get_exon_by_gene(line)
                except:
                    region = "."
                with open(fileout, "a", encoding='utf-8')as ww:
                    out = line + "\t" + region + "\n"
                    ww.write(str(out))

if __name__ == "__main__":
    main()