# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

"""
分析manta 与lumpy 结果,找到统计共同sv
"""
pathlumpy = "E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\TXT" #文件夹目录
fileslumpy = os.listdir(pathlumpy)  # 得到文件夹下的所有文件名称

pathmanta = 'E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\ANNOTXT'
filemanta =  os.listdir(pathmanta)  # 得到文件夹下的所有文件名称

def getlumpyfilesv(lines):
    thesv=[]
    for line in lines[1:]:
        line = line.strip('\n')
        if 'GL000' in line:
            continue
        linelist = line.split('\t')
        if "Y:" not in linelist[7] and "chrY" not in linelist[0]:
            chrnum=re.sub('chr','',linelist[0])
            svpart1 = chrnum+":"+ linelist[2]
            if "[" in linelist[7]:
                svpart2 = re.search("\[(.*)\[", linelist[7]).group(1)
            elif ']' in linelist[7]:
                svpart2 = re.search("\](.*)\]", linelist[7]).group(1)
        breakpoint=svpart1.split(':')
        breakpointanti=svpart2.split(':')
        ##sv断点按照染色体顺序排序，小的在前，大的在后，X最后
        if 'X' == breakpoint[0] and 'X'==breakpointanti[0]:
            if int(breakpointanti[1])>int(breakpoint[1]):
                strduandian = str(':'.join(breakpoint) + "_" + ':'.join(breakpointanti))
            else:
                strduandian = str(':'.join(breakpointanti) + "_" + ':'.join(breakpoint))
        elif breakpoint[0]==breakpointanti[0]:
            if breakpointanti[1]>breakpoint[1]:
                strduandian = str(':'.join(breakpoint) + "_" + ':'.join(breakpointanti))
            else:
                strduandian = str(':'.join(breakpointanti) + "_" + ':'.join(breakpoint))
        elif 'X' == breakpoint[0]  :
            strduandian = str(':'.join(breakpointanti) + "_" + ':'.join(breakpoint))
        elif 'X'==breakpointanti[0] :
            strduandian =  str(':'.join(breakpoint) + "_" + ':'.join(breakpointanti))
        elif int(breakpoint[0])>int(breakpointanti[0]):
            strduandian = str(':'.join(breakpointanti) + "_" + ':'.join(breakpoint))
        elif int(breakpointanti[0])>int(breakpoint[0]):
            strduandian =  str(':'.join(breakpoint) + "_" + ':'.join(breakpointanti))

        if strduandian in thesv:
            pass #这个sv已经有了。
        else:
            thesv.append(strduandian)
    return thesv

def getmantafilesv(gines):
    svlist1=[]
    for line in gines:
        if '#' not in line and "GL000" not in line and 'MantaBND' in line:
            line = line.strip('\n')
            linelist = line.split('\t')
            if 'Y' in linelist[0] or 'Y' in linelist[4]:
                continue
            else:
                svpart1=linelist[0]+":"+linelist[1]
                if '[' in linelist[4]:
                    svpart2=re.search("\[(.*)\[",linelist[4]).group(1)
                elif ']' in linelist[4]:
                    svpart2=re.search("\](.*)\]",linelist[4]).group(1)
                sv = svpart1 +"_"+ svpart2
                #print(sv)
                svpipei = svpart2 +"_"+ svpart1
                if svpipei in svlist1:
                    #说明已经有这个记录，是同样匹配的sv
                    pass
                else:
                    svlist1.append(sv)
    return svlist1

def compareandstat():
    resultstat="E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\manta_lumpy_statsv.txt"
    with open(resultstat, 'w', encoding='utf-8') as ww:
        strout="样本名\t"+"共同匹配的断点\t"+'数目\n'
        ww.write(str(strout))
    for file in fileslumpy:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            fileout = re.sub('.bam.txt', '', file)
            #print('分析样本',fileout)
            f1 = open(pathlumpy + "\\" + file, 'r', encoding='UTF-8');  # 打开文件
            lines = f1.readlines()
            lumpysvlist = getlumpyfilesv(lines)
            mantafile=fileout+'.bam.vcf'
            f2=  open(pathmanta + "\\" + mantafile, 'r', encoding='UTF-8');  # 打开文件
            gines = f2.readlines()
            mantasvlist = getmantafilesv(gines)
            flag=0
            outlist=[]
            for lumpysv in lumpysvlist:
                if lumpysv in mantasvlist:
                    print(fileout,'有共同sv',lumpysv)
                    flag=1
                    outlist.append(lumpysv)
            #print(outlist)
            if flag==0:
                print(fileout,'没有共同sv')
                with open(resultstat, 'a', encoding='utf-8') as ww:
                    strout = fileout +'\t'+'.'+'\t'+"0"+'\n'
                    ww.write(str(strout))
            else:
                with open(resultstat, 'a', encoding='utf-8') as ww:
                    svout = ','.join(outlist)
                    svnum = len(outlist)
                    strout = fileout +'\t'+str(svout)+'\t'+str(svnum)+'\n'
                    ww.write(str(strout))


#compareandstat()

def analysehighfresv():
    #找高频的sv,各样本中
    file = "E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\manta_lumpy_statsv.txt"
    fileout = "E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\manta_lumpy_highsv.txt"
    svfiledict={}
    with open(fileout, 'w', encoding='utf-8') as ww:
        strout = "SV断点\t"+"样本名\t"+'数目\n'
        ww.write(str(strout))
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if '.' in linelist[1]:
                continue
            if ',' in linelist[1]:
                svlist = linelist[1].split(',')
                for sv in svlist:
                    if svfiledict.get(sv):
                        svfiledict[sv]=svfiledict[sv] + "," + linelist[0]
                    else:
                        svfiledict[sv] =linelist[0]
            else:
                if svfiledict.get(linelist[1]):
                    svfiledict[linelist[1]] = svfiledict[linelist[1]] + "," + linelist[0]
                else:
                    svfiledict[linelist[1]] = linelist[0]

    for k,v in svfiledict.items():
        with open(fileout,'a', encoding='utf-8') as ww:
            if ',' in v:
                vlist=v.split(',')
                filenum = len(vlist)
            else:
                filenum = 1
            strout = k + '\t' + v +'\t'+ str(filenum) +'\n'
            ww.write(str(strout))

#analysehighfresv()

def analysewheatherinneiyizheng():
    pathneiyizheng = 'E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\neiyizhengTXT'
    fileneiyizhengdir = os.listdir(pathneiyizheng)
    neiyizhengsvlist = []
    for fileneiyizheng in fileneiyizhengdir:
        if not os.path.isdir(fileneiyizheng):  # 判断是否是文件夹，不是文件夹才打开
            f3 = open(pathneiyizheng + "\\" + fileneiyizheng, 'r', encoding='UTF-8') # 打开文件
            lines = f3.readlines()
            svlist = getlumpyfilesv(lines)
            for sv in svlist:
                if sv not in neiyizhengsvlist:
                    neiyizhengsvlist.append(sv)
        file = "E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\manta_lumpy_highsv.txt"
        fileout = "E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\manta_lumpy_highsv_filter_neiyizheng.txt"
        with open(fileout, 'w', encoding='utf-8') as ww:
            strout="样本名\t"+"共同匹配的断点\t"+'数目\t'+'该sv是在内异症中情况\n'
            ww.write(str(strout))
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip('\n')
                linelist = line.split('\t')
                if linelist[0] in neiyizhengsvlist:
                    pass
                    #with open(fileout,'a', encoding='utf-8') as ww:
                        #strout=line+'\t有\n'
                        #ww.write(str(strout))
                else:
                    with open(fileout,'a', encoding='utf-8') as ww:
                       strout=line+'\t无\n'
                       ww.write(str(strout))

#analysewheatherinneiyizheng()

def analyse_sv_fugai_sample(n):
    file = "E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\manta_lumpy_highsv_filter_neiyizheng.txt"
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        samplestat=[]
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if int(linelist[2])>=n:
                samplelist = linelist[1].split(',')
                for sample in samplelist:
                    if sample not in samplestat:
                        samplestat.append(sample)
        numb=len(samplestat)
        freque=float((numb/119)*100)
        print('在%s个样本以上出现的sv，可以覆盖%.2f %%样本'%(n,freque))


analyse_sv_fugai_sample(2)

def getnotfugai_sample():
    file = "E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\manta_lumpy_highsv_filter_neiyizheng.txt"
    fileout="E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\manta_lumpy_highsv_fugai_sampleresult.txt"
    allsamplelist=[]
    with open(fileout, 'w', encoding='utf-8') as ww:
        out = "sample"+"\t"+"覆盖情况\n"
        ww.write(str(out))
    for lfile in fileslumpy:  # 遍历文件夹
        if not os.path.isdir(lfile):
            samplename=re.sub('.bam.txt', '', lfile)
            allsamplelist.append(samplename)

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        samplestat=[]
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if int(linelist[2])>=12:
                samplelist = linelist[1].split(',')
                for sample in samplelist:
                    if sample not in samplestat:
                        samplestat.append(sample)
        for sample in allsamplelist:
            if sample in samplestat:
                out=sample+'\t'+'覆盖\n'
            else:
                out = sample + '\t' + '不覆盖\n'
            with open(fileout, 'a', encoding='utf-8') as ww:
                ww.write(str(out))
#getnotfugai_sample()