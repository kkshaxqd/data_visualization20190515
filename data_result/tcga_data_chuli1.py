# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
addinfo = 'tcga-prad-ctbp1-ar-exp.txt'
hang_dic = {}
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
            value = lang_list[1]+'\t'+lang_list[2]
            flag =str(flag.lower()) #大小写转换
            #print(type(flag))
            #print(flag)
            if flag in hang_dic.keys():  #python 中判断key是否存在与Perl不一样
                hang_dic[flag] = hang_dic[flag]+'\t'+'value'
            else:
                hang_dic[flag] = value


filename = '70bingren.txt'
with open(filename,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        if re.findall('patient',line):
            #print("test")
            hangshou = line+'\tCTBP1'+'\tAR'+'\n'  #这样是OK的
            with open('70bingrenaddresult.txt','w')as ww:
                ww.write(str(hangshou))
            continue              #print(sample[2])   如果数据里头有空或不对的，那么会报一个超出索引的错误
        else:
            line_list = line.split('\t')
            sample= re.split("-",line_list[0])
            flagc = str(sample[1]+'-'+sample[2])

            if flagc in hang_dic.keys():
                outinfo = line+'\t'+str(hang_dic[flagc])+'\n'
                with open('70bingrenaddresult.txt','a')as ww: #这才是追加 w+不是，也是替换
                    ww.write(str(outinfo))
            else:
                outinfo = line+'\t\n'
                with open('70bingrenaddresult.txt', 'a')as ww:
                    ww.write(str(outinfo))
