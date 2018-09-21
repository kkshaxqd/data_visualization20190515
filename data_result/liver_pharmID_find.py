# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
import pandas as pd
from serachbybaiduxueshu import get_title_year_yinyong
#filename = 'E:\\haxqd\\myscript\\GEZHI_Script\\PharmGKB\\annotations_v20180705\\clinical_ann_metadata.tsv'
#outname = 'E:\\haxqd\\myscript\\GEZHI_Script\\PharmGKB\\annotations_v20180705\\liver_pharm_ann_info.tsv'
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


filename = 'E:\\haxqd\\myscript\\GEZHI_Script\\PharmGKB\\annotations_v20180705\\liver_pharm_ann_info.tsv'
outresult = 'E:\\haxqd\\myscript\\GEZHI_Script\\PharmGKB\\annotations_v20180705\\liver_wenxian_anno.tsv'
with open(filename,'r',encoding='utf-8')as f:
    lines = f.readlines()
    #print(lines[0])
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        if re.findall('PMIDs',line):
            hangshou =  'Location\tGene\tLevel of Evidence\tClinical Annotation Types\tPMIDs\tRelated Diseases\n'
            with open(outresult,'w')as ww:
                ww.write(str(hangshou))
        else:
            PMIDS = info[9].split(',')
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
                except IndexError:
                    impact_factor = "None"
                    title = "None"
                    year = "None"
                    yinyong = "None"
                if year == "None" or int(year)<2005:
                    continue
                outinfo = pmid+':'+title+':'+impact_factor+':'+year+':'+yinyong
                print(outinfo)
                if outpmidinfo:
                    outpmidinfo = outpmidinfo+"|"+outinfo
                else:
                    outpmidinfo = outinfo
            out = info[1]+"\t"+info[2]+"\t"+info[3]+"\t"+info[4]+"\t"+outpmidinfo+"\t"+info[12]+'\n'
            with open(outresult, 'a')as ww:
                ww.write(str(out))

