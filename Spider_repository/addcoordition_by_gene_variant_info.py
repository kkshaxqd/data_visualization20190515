# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re,io


filein = 'needaddcoordition.txt'
addfile = "xxxxcoordition.txt"
fileout = 'needaddcoordition_xxxxcoordition.txt'

adddict = {}
with open(addfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        if re.findall('input', line):
            continue
        elif re.findall('ins',line):
            allcontent = re.compile("/.*")
            coordition = allcontent.sub("",info[1])
            adddict[info[0]] = coordition
            #print(coordition)
        else:
            allcontent = re.compile(r"(chr\d+:g\.\d+)([ATCG]\>[ATCG]/\S+)")
            coordition = allcontent.sub(r"\1", info[1])  ##需要r 才能捕获变量
            adddict[info[0]] = coordition
            #print(coordition)

with open(filein,'r',encoding='utf-8')as d:
    lines = d.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        if re.findall(r'基因', line):
            with open(fileout, 'w', encoding='utf-8')as ww:
                out = line +"\n"
                ww.write(str(out))
        elif re.match("^.$",info[2]) and re.findall("\w+",info[0]):
            index = info[0]+":"+info[1]
            try:
                if adddict[index]:
                    info[2] = adddict[index]
                    line = info[0]+"\t"+info[1]+"\t"+info[2]
            except:
                print(r"出错",line)
            with open(fileout, 'a', encoding='utf-8')as ww:
                out = line +"\n"
                ww.write(str(out))
        else:
            with open(fileout, 'a', encoding='utf-8')as ww:
                out = line +"\n"
                ww.write(str(out))
