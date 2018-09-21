# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re,io

filein = 'drugfile.txt'
addfile = "regionfile_bygene.txt"
fileout = 'drugfile_regionfile_bygene.txt'

adddict = {}
wenxiandict = {}
with open(addfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        gene_region = info[1]+"("+info[2]+")"
        gene_wenxian = info[1]+"("+info[3]+")"
        try:
            if adddict[info[0]]:
                adddict[info[0]] = adddict[info[0]]+";"+gene_region
        except KeyError:
            adddict[info[0]] = gene_region

        try:
            if wenxiandict[info[0]]:
                wenxiandict[info[0]] = wenxiandict[info[0]]+";"+gene_wenxian
        except KeyError:
            wenxiandict[info[0]] = gene_wenxian

def main():
    with open(filein,'r',encoding='utf-8')as g:
        lines = g.readlines()
        for line in lines:
            line = line.strip('\n')
            if re.search("Drugname",line):
                with open(fileout,'w',encoding='utf-8')as ww:
                    out = line+"\t"+r"靶点基因区域"+"\t"+r"靶点基因支持文献"+"\n"
                    ww.write(str(out))
            else:
                try:
                    if adddict[line]:
                        with open(fileout, 'a', encoding='utf-8')as ww:
                            out = line + "\t" + adddict[line] + "\t" + wenxiandict[line] + "\n"
                            ww.write(str(out))
                except:
                    print(line)
                    with open(fileout, 'a', encoding='utf-8')as ww:
                        out = line + "\t" + "." + "\t" + "." + "\n"
                        ww.write(str(out))

if __name__ == "__main__":
    main()

