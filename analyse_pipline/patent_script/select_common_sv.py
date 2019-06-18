# !/usr/bin/env python
# -*- coding: utf8 -*-
## __author__: 'zhangqiaoshi'
## mail: zhangqiaoshi@gezhigene.com
import os,re,sys
"""
选取两个软件共同call出的sv结果，根据参数的不同
"""
import argparse
parser = argparse.ArgumentParser(description='manual to this script, use like python select_common_sv.py -lumpy 目录 -manta 目录 -o 结果文件 or python select_common_sv.py -lumpyfile 单独文件 -mantafile 单独文件 -o 结果文件 ')
parser.add_argument('--verbose', '-v', action='store_true', help='verbose mode 20190515')
parser.add_argument('-lumpy', type=str, default = None,help='必须是目录')
parser.add_argument('-lumpyfile', type=str, default = None,help='单独文件分析，与-mantafile配对，不能与-lumpy共同出现')
parser.add_argument('-manta', type=str, default = None,help='必须是目录')
parser.add_argument('-mantafile', type=str, default = None,help='单独文件分析，与-lumpyfile配对，不能与-manta共同出现')
parser.add_argument('--out','-o', type=str, default = None,help='结果文件，建议为txt, 例如： -o XXX.txt')
parser.add_argument('-health', type=str, default = None,help='必须是目录,健康人sv结果目录，分析排除健康人中的sv')
parser.add_argument('-analyse',type=str,default = None,help='如果想要需要分析结果数据，在得到输出文件后启用这个来进行分析即可')
args = parser.parse_args()
#print(args.lumpy)
#print(args.lumpyfile)
#print(args.manta)
#print(args.mantafile)

pathlumpy = args.lumpy #文件夹目录
fileslumpy = os.listdir(pathlumpy)  # 得到文件夹下的所有文件名称

pathmanta = args.manta
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
    resultstat=args.out
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

def compareandstatsinglestat():
    resultstat = args.out
    with open(resultstat, 'w', encoding='utf-8') as ww:
        strout = "样本名\t" + "共同匹配的断点\t" + '数目\n'
        ww.write(str(strout))
    fileout = re.sub('.txt', '', args.lumpyfile)
    f1 = open(args.lumpyfile, 'r', encoding='UTF-8')  # 打开文件
    lines = f1.readlines()
    lumpysvlist = getlumpyfilesv(lines)
    f2 = open(args.mantafile, 'r', encoding='UTF-8')  # 打开文件
    gines = f2.readlines()
    mantasvlist = getmantafilesv(gines)
    flag = 0
    outlist = []
    for lumpysv in lumpysvlist:
        if lumpysv in mantasvlist:
            print(fileout, '有共同sv', lumpysv)
            flag = 1
            outlist.append(lumpysv)
    # print(outlist)
    if flag == 0:
        print(fileout, '没有共同sv')
        with open(resultstat, 'a', encoding='utf-8') as ww:
            strout = fileout + '\t' + '.' + '\t' + "0" + '\n'
            ww.write(str(strout))
    else:
        with open(resultstat, 'a', encoding='utf-8') as ww:
            svout = ','.join(outlist)
            svnum = len(outlist)
            strout = fileout + '\t' + str(svout) + '\t' + str(svnum) + '\n'
            ww.write(str(strout))



def analysehighfresv():
    #找高频的sv,各样本中
    file = args.out
    fileout = file+"_manta_lumpy_highsv.txt"
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
    pathneiyizheng = args.health
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
        file = args.out
        fileout =file+"manta_lumpy_highsv_filter_neiyizheng.txt"
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
    file = args.out+"manta_lumpy_highsv_filter_neiyizheng.txt"
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


#analyse_sv_fugai_sample(2)

def getnotfugai_sample():
    file = args.out+"manta_lumpy_highsv_filter_neiyizheng.txt"
    fileout=args.out+"manta_lumpy_highsv_fugai_sampleresult.txt"
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



def main():
    if args.lumpy and args.manta :
        compareandstat()
    elif args.lumpyfile and args.mantafile:
        compareandstatsinglestat()
    if args.analyse:
        analysehighfresv()
        analysewheatherinneiyizheng()
        analyse_sv_fugai_sample(2)
        getnotfugai_sample()

if __name__ == "__main__" :
    main()


