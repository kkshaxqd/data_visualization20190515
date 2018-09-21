# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
ctbp_dic = {}
def only_ctbp1():
    #addinfo = 'E:\\data\\前列腺癌PRADDATA\\ctbp1.txt'
    addinfo = 'E:\\haxqd\\python\\data_visualization\\data_result\\tcga-prad-ctbp1-ar-exp.txt'
    with open(addinfo,'r',encoding='utf-8')as p:
        langs = p.readlines()
        for lang in langs:
            lang = lang.strip('\n')
            if re.findall('SAMPLE_ID',lang):
                continue
            elif re.findall('TCGA',lang):
                lang_list = lang.split('\t')
                gebename = re.split("-",lang_list[0])
                flag = gebename[1]+'-'+gebename[2]
                flag =str(flag.lower())
                ctbp_dic[flag] = lang_list[1]
    return ctbp_dic
#only_ctbp1()

addfile = 'E:\\data\\前列腺癌PRADDATA\\outfilePRAD.txt'
hang_dict = {}
with open(addfile,'r',encoding='utf-8')as p:
    langs = p.readlines()
    for lang in langs:
        lang = lang.strip('\n')
        if re.findall('Entrez_Gene_Id', lang):
            continue
        elif re.findall("Hugo_Symbol",lang):
            hang_dict["Hugo_Symbol"]=lang
        elif re.findall("TCGA",lang):
            lang_list = lang.split('\t')
            gebename = re.split("-", lang_list[0])
            flag = gebename[1] + '-' + gebename[2]
            flag = str(flag.lower())
            hang_dict[flag] = lang

inputfile = 'E:\\data\\前列腺癌PRADDATA\\Clinical_BCR_XML.merge.txt'
with open(inputfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    num=0
    for line in lines:
        line = line.strip('\n')
        if re.findall('A0_Samples',line):
            hangshou = line+'\t'+hang_dict["Hugo_Symbol"]+'\n'  #这样是OK的
            with open('E:\\data\\前列腺癌PRADDATA\\outclin_geneexp_info.txt','w')as ww:
                ww.write(str(hangshou))
            continue              #print(sample[2])   如果数据里头有空或不对的，那么会报一个超出索引的错误
        else:
            line_list = line.split('\t')
            sample= re.split("-",line_list[0])
            flagc = str(sample[1]+'-'+sample[2])
            flagc = flagc.lower()
            if flagc in hang_dict.keys():
                outinfo = line+'\t'+str(hang_dict[flagc])+'\n'
                with open('E:\\data\\前列腺癌PRADDATA\\outclin_geneexp_info.txt','a')as ww: #这才是追加 w+不是，也是替换
                    ww.write(str(outinfo))
            else:
                continue
