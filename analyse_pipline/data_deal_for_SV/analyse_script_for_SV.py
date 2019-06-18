# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

"""
分析脚本对SV结果，提取TXT进行分析
"""
path = "E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\neiyizhengTXT" #文件夹目录
def main1():
    files= os.listdir(path) #得到文件夹下的所有文件名称
    resultstat="E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\neiyizheng\\statsv.txt"
    with open(resultstat, 'w', encoding='utf-8') as ww:
        strout="断点\t"+"样本名\t"+"数目\n"
        ww.write(str(strout))
    duandiandict = {}
    for file in files: #遍历文件夹
         if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
              f = open(path+"\\"+file,'r', encoding='UTF-8'); #打开文件
              lines = f.readlines()
              for i in range(1,len(lines),2):
                  line = lines[i].strip('\n')
                  if "Y:" in line or "chrY" in line:
                      continue
                  linelist = line.split('\t')
                  if "X" not in linelist[7]:
                    breakpoint=re.findall('\d+',linelist[7])
                  else:
                    breakpoint=["X"]
                    breakpoint.append(re.findall('\d+',linelist[7])[0])
                  j=i+1
                  linenext = lines[j].strip('\n')
                  linenextlist = linenext.split('\t')
                  if "X" not in linenextlist[7]:
                      breakpointanti=re.findall('\d+',linenextlist[7])
                  else:
                      breakpointanti=["X"]
                      breakpointanti.append(re.findall('\d+',linenextlist[7])[0])
                  print(breakpoint,breakpointanti)
                  strduandian = str(':'.join(breakpointanti)+"_"+':'.join(breakpoint))
                  print(file)
                  print(linenextlist[2])
                  if str(linenextlist[2])==str(breakpoint[1]):
                      print("这是一个sv",'断点是',strduandian)
                      fileout=re.sub('.bam.txt','',file)
                      if duandiandict.get(strduandian):
                          duandiandict[strduandian]=duandiandict[strduandian]+","+fileout
                      else:
                          duandiandict[strduandian]=fileout

    for k,v in sorted(duandiandict.items(),key=lambda item:item[1]):
        with open(resultstat, 'a', encoding='utf-8') as ww:
            numlist=duandiandict[k].split(',')
            num=len(numlist)
            strout=k+"\t"+duandiandict[k]+"\t"+str(num)+'\n'
            ww.write(str(strout))
#统计出现数目，高频的sv
main1()


def main2():
    sampledict={}
    fileshujuku="E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\neiyizheng\\calfile.txt"
    fileshujukuout='E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\neiyizheng\\statsvoutdata.txt'
    with open(fileshujukuout, 'w', encoding='utf-8') as ww:
        out = '断点' + "\t" + '样本名' + '\n'
        ww.write(str(out))

    with open(fileshujuku, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(3,9):
            samplelist = []
            for line in lines[1:i]:
                line = line.strip('\n')
                linelist = line.split('\t')
                sampleset=linelist[1].split(',')
                for sample in sampleset:
                    sampledict[sample]=sampledict.get(sample,0)+1
                    with open(fileshujukuout, 'a', encoding='utf-8') as ww:
                        out = linelist[0]+"\t"+sample+'\n'
                        ww.write(str(out))
                    if sample not in samplelist:
                        samplelist.append(sample)
            svnum=i-1
            covtate=(len(samplelist)/119)*100
            print("sv个数%d，覆盖样本个数%d，覆盖率是%.2f %%"%(svnum,len(samplelist),covtate))
            if i==8:
                print(samplelist)

    import matplotlib.pyplot as plt
    xlist=[]
    ylist=[]
    for k,v in sampledict.items():
        xlist.append(k)
        ylist.append(v)
    plt.bar(xlist,ylist,)
    plt.xticks(rotation=90)
    plt.savefig('E:\\haxqd\\python\\data_visualization\\analyse_pipline\\data_deal_for_SV\\neiyizheng\\result.png')
    plt.show()

    files = os.listdir(path)
    for file in files:
        file=re.sub('.bam.txt','',file)
        if file not in samplelist:
            print(file)


#main2()

def main3():
    #找到覆盖100%样本的sv组合
    sampledict={}
    fileshujuku="statsv.txt"
    fileshujukuout='statsvoutdata.txt'

