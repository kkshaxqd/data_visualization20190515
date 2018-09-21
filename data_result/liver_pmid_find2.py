# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
import pandas as pd
from serachbybaiduxueshu import get_title_year_yinyong
addinfo = 'E:\\haxqd\\201807\\JCR_IFINFO.txt'
jourifinfo = {}
with open(addinfo,'r',encoding='utf-8')as f:
    lines = f.readlines()
    #print(lines[0])
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        journame = info[1].lower()
        jourifinfo[journame] = info[3]

addrsinfo = 'E:\\haxqd\\myscript\\GEZHI_Script\\PharmGKB\\annotations_v20180705\\rsid_for_coord_anno1.txt'
rsdict = {}
with open(addrsinfo,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        if re.findall('refsnp_id',line):
            continue
        info = line.split(':')
        rsid = info[0]
        s1 = ':'
        otherinfo = s1.join(info[1:])
        try:
            if rsdict[rsid]:
                rsdict[rsid] = rsdict[rsid] + '|' + otherinfo
        except KeyError:
            rsdict[rsid] = line





filename = 'E:\\haxqd\\myscript\\GEZHI_Script\\PharmGKB\\annotations_v20180705\\fanshengzi_rs_pmid.txt'
outresult = 'E:\\haxqd\\myscript\\GEZHI_Script\\PharmGKB\\annotations_v20180705\\fanshengzi_rs_pmid_anno.tsv'
with open(filename,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        if re.findall('Location',line):
            hangshou =  line+'\t'+'PMIDS:TITLE:IF:YEAR:CITED'+'\t'+'RSID_info'+'\n'
            for i in range(len(info)):
                if re.match('PMIDs',info[i]):
                    pmid_index = i
            with open(outresult,'w')as ww:
                ww.write(str(hangshou))
        elif info[0] == '':
            outkong = line +'\t'+'\t'+'\n'
            with open(outresult,'a')as ww:
                ww.write(str(outkong))
        else:
            PMID = re.sub('PMID:',' ',info[pmid_index])
            PMIDS = PMID.lstrip().split(',')
            outpmidinfo = ""
            for pmid in PMIDS:
                try:
                    (title, year, yinyong) = get_title_year_yinyong(pmid)
                    tit_index = str(title).lower()
                    if jourifinfo[tit_index]:
                        impact_factor = jourifinfo[tit_index]
                    else:
                        impact_factor = "NA"
                except KeyError:
                    impact_factor = "NA"

                if year == "None" or int(year)<2005:
                    continue
                outinfo = pmid.lstrip()+':'+title+':'+impact_factor+':'+year+':'+yinyong
                print(outinfo)
                if outpmidinfo:
                    outpmidinfo = outpmidinfo+"|"+outinfo
                else:
                    outpmidinfo = outinfo
            rsadd = info[4].split('#')
            try:
                if rsdict[rsadd[0]]:
                    rsaddinfo = rsdict[rsadd[0]]
            except KeyError:
                rsaddinfo = 'Not find'
            out = line +'\t'+outpmidinfo+'\t'+rsaddinfo+'\n'
            with open(outresult, 'a')as ww:
                ww.write(str(out))
