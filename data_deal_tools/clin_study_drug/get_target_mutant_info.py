# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re

filein = 'E:\\haxqd\\python\\data_visualization\\data_deal_tools\\clin_study_drug\\clin_drug_id_info_out.txt'
fileout = 'E:\\haxqd\\python\\data_visualization\\data_deal_tools\\clin_study_drug\\clin_drug_id_info_targets_and_AA.txt'

targetdict = {}
with open('Targettherapy_AA.txt','r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        if re.findall(u'氨基酸改变', line):
            continue
        try:
            if targetdict[str(info[1])]:
                targetdict[str(info[1])] = targetdict[str(info[1])] +'||'+str(info[0])+str(info[4])
        except KeyError:
                targetdict[str(info[1])] = str(info[0])+str(info[4])

with open(filein,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        if re.findall('Drugname', line):
            with open(fileout, 'w', encoding='utf-8')as ww:
                out = 'Drugname' + '\t' + 'NCIDS:Phase:Status:Literature' + '\t' + 'Targets' + '\n'
                ww.write(str(out))
            continue
        else:
            drugname = info[0].lower()
            for key in sorted(targetdict, key=targetdict.get):
                value = targetdict[key]
                if drugname in key.lower():
                    drugaa = key+':'+value
                    break
                else:
                    drugaa = "No"

            with open(fileout, 'a', encoding='utf-8')as ww:
                outnr = line + '\t' + drugaa + '\n'
                ww.write(str(outnr))





