import os,re,sys

import pandas as pd

filemeta = 'E:\\haxqd\\myscript\\GEZHI_Script\\pharmGKB20180926\\annotations\\clinical_ann_metadata.tsv'
filein = "E:\\haxqd\\201810\\sss.txt"
fileout = 'E:\\haxqd\\201810\\sss_add_pharmgkb.txt'

filenew = "E:\\haxqd\\201810\\kkk.txt"
fileoutnew = "E:\\haxqd\\201810\\kkk_add_zhichi.txt"
fileaddnew = "E:\\haxqd\\201810\\kkk_alltarget.txt"

def gettargetinfo(fileaddnew):
    targetinfo = {}
    with open(fileaddnew, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            genevar = linelist[0]+linelist[1]
            content = linelist[2]+"\t"+linelist[3]
            targetinfo[genevar] = content

    return targetinfo

def main2():
    targetinfo = gettargetinfo(fileaddnew)
    with open(filenew,'r',encoding='utf-8')as f:
        lines = f.readlines()
        out = lines[0].strip('\n') + r"\t临床疗效" + "\tReference" +"\n"
        with open(fileoutnew, 'w', encoding='utf-8')as ww:
            ww.write(str(out))
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            genevar = linelist[0]+linelist[1]
            if targetinfo.get(genevar):
                out = line + '\t' + targetinfo[genevar] + "\n"
                with open(fileoutnew, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))
            else:
                out = line + "\t." + "\t." + "\n"
                with open(fileoutnew, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))












def getpharmgbinfo(filemeta):
    pharmgkbinfo = {}
    with open(filemeta, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            rsid = linelist[1]
            content = linelist[4]+"\t"+linelist[6]+"\t"+linelist[8]+"\t"+linelist[3]
            if pharmgkbinfo.get(rsid):
                temp = pharmgkbinfo[rsid].split("\t")
                temp2 = content.split("\t")
                temp3 = ["." for i in range(len(temp))]
                for i in range(len(temp)):
                    temp3[i] = temp[i]+" // "+temp2[i]
                newcontent = "\t".join(temp3)
                pharmgkbinfo[rsid] = newcontent
            else:
                pharmgkbinfo[rsid] = content

    return pharmgkbinfo

def main():
    pharmgkbinfo = getpharmgbinfo(filemeta)
    with open(filein,'r',encoding='utf-8')as f:
        lines = f.readlines()
        out = lines[0].strip('\n') + "\tClinical Annotation Types" + "\tAnnotation Text" + "\tVariant Annotations" + "\tLevel of Evidence"  + "\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(out))
        for line in lines[1:]:
            line = line.strip('\n')
            if pharmgkbinfo.get(line):
                out = line+"\t"+pharmgkbinfo[line]+"\n"
                with open(fileout,'a',encoding='utf-8')as ww:
                    ww.write(str(out))
            else:
                out = line+"\t."+"\t."+"\t."+"\t."+"\n"
                with open(fileout,'a',encoding='utf-8')as ww:
                    ww.write(str(out))

main()
main2()

