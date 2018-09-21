# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re,io
import pandas as pd
import time
from bs4 import BeautifulSoup  # 引入beautifulsoup 解析html事半功倍
from urllib import request
# 参考https://blog.csdn.net/jim7424994/article/details/22675759
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')    #改变标准输出的默认编码,增加程序容错。
#构造头文件，模拟浏览器访问
def get_clinical(NCIDS):
    url="https://ClinicalTrials.gov/show/"+NCIDS
    #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url)
    page_info = request.urlopen(page).read().decode('utf-8','ignore')#打开Url,获取HttpResponse返回对象并读取其ResposneBody
    time.sleep(2)
    #print(page_info)
    # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
    #方法参考https://blog.csdn.net/csdn2497242041/article/details/77170746 ，但是titles无内容，用正则吧还是。
    soup = BeautifulSoup(page_info, 'lxml')
    dataresuoure = soup.prettify()
    #print(dataresuoure)
    if re.search(r'Publications of Results.*?<a href=.*?onclick=.*?return false',dataresuoure,re.S):
        allcontent = re.compile(r'Publications of Results.*?title=\"(.*?)\">', re.S)
        zazhititle = allcontent.search(dataresuoure).group(1).lstrip()
        return zazhititle
    elif re.search(r'Publications of Results',dataresuoure,re.S):
        allcontent = re.compile(r'Publications of Results.*?style=\"margin-top:2ex\">(.*?)</div>', re.S)
        zazhititle = allcontent.search(dataresuoure).group(1).strip()
        return zazhititle
    else:
        return "No publish"
cldict = {}
with open('clin_result.txt','r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        cldict[str(info[0])] = str(info[1])
        """
        try:
            if cldict[info[0]]:
                cldict[info[0]]  = info[1]
        except KeyError:
            cldict[info[0]] = 'no_result'
        """

"""处理下载的临床再研药数据，得到以药物为ID的信息内容"""
filein = 'E:\\haxqd\\python\\data_visualization\\data_deal_tools\\clin_study_drug\\clin_drug_id_info.txt'
fileout = 'E:\\haxqd\\python\\data_visualization\\data_deal_tools\\clin_study_drug\\clin_drug_id_info_out2.txt'
#最好是新靶向药，单抗等，辐射联合，化疗药最好可以过滤
#过滤Radiation
clindruginfo={}
with open(filein,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        if re.findall('Radiation', line):
            continue
        elif re.findall('Interventions',line):
            #hangshou =  'Drugname'+'\t'+'NCIDS:Phase:Status:Literature'+'\n'
            for i in range(len(info)):
                if re.match(r'Interventions',info[i]):
                   itt_index = i
                elif re.match(r'NCT Number',info[i]):
                   id_index = i
                elif re.match(r'Phases',info[i]):
                   ph_index = i
                elif re.match(r'Status',info[i]):
                   st_index = i
            print(itt_index,id_index,ph_index,st_index)
        else:
            NCID = str(info[id_index])
            #print(NCID)
            try:
                if cldict[NCID]:
                    lepublish = cldict[NCID]
            except KeyError:
                lepublish = get_clinical(NCID).replace(u'\xf6|\xe4', u' ')
                #
                time.sleep(3)
                with open('clin_result.txt', 'a',encoding='utf-8')as ww:
                    outt = NCID+'\t'+lepublish+'\n'
                    ww.write(str(outt))
            #print(lepublish)

            if re.findall('|',info[itt_index]):
                drugs = info[itt_index].split('|')
                for drug in drugs:
                    if 'Drug:' in drug:
                        drug = re.sub('Drug: ', ' ', drug).lstrip().lower()
                        #drugcomplie = re.compile(r'(\S+)')
                        #drug = drugcomplie.search(drug).group(1).lower()
                        try:
                            if clindruginfo[drug]:
                                outinfo = NCID+':'+info[ph_index]+':'+info[st_index]+':'+lepublish
                                clindruginfo[drug] = clindruginfo[drug] + ';;' + outinfo
                        except KeyError:
                            outinfo = NCID + ':' + info[ph_index] + ':' + info[st_index] + ':' + lepublish
                            clindruginfo[drug] = outinfo
            else:
                if 'Drug:' in drug:
                    drug = re.sub('Drug: ', ' ', info[itt_index]).lstrip().lower()
                    #drugcomplie = re.compile(r'(\S+)')
                    #drug = drugcomplie.search(drug).group(1).lower()
                    try:
                        if clindruginfo[drug]:
                            outinfo = NCID + ':' + info[ph_index] + ':' + info[st_index] + ':' + lepublish
                            clindruginfo[drug] = clindruginfo[drug] + ';;' + outinfo
                    except KeyError:
                        outinfo = NCID + ':' + info[ph_index] + ':' + info[st_index] + ':' + lepublish
                        clindruginfo[drug] = outinfo
#寻找靶点
def get_drug_target(drugname='sorafenib'):
    #driver = webdriver.Chrome()
    #driver.get('http://xueshu.baidu.com/')
    #time.sleep(2)
    try:
        url = 'http://www.selleckchem.com/products/'+drugname+'.html'
        #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        page = request.Request(url)#,headers=headers)
        page_info = request.urlopen(page).read().decode('utf-8')#打开Url,获取HttpResponse返回对象并读取其ResposneBody
        soup = BeautifulSoup(page_info, 'lxml')
    except:
        return 'html not right'
    #soup = soup.find_all(name='td')
    try :
        if 'Targets' in soup:
            allcontent = re.compile(r'<td>(.*?)<sup><a class=\"sref\"')
            targets = allcontent.findall(str(soup))
            targett = ','.join(targets)
            return targett
        else:
            return 'No target'
    except KeyError:
        return 'Not find'

# 药物靶点有否中间文件
targetdict = {}
with open('drug_targets.txt','r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        targetdict[str(info[0])] = str(info[1])

with open(fileout, 'w',encoding='utf-8')as ww:
    out = 'Drugname'+'\t'+'NCIDS:Phase:Status:Literature'+'\t'+'Targets'+'\n'
    ww.write(str(out))
for key in sorted(clindruginfo,key=clindruginfo.get):
    value = clindruginfo[key]
    try:
        if targetdict[key]:
            outtarget = targetdict[key]
    except KeyError:
        # 中间文件里没有才爬并写入
        outtarget = get_drug_target(key)
        time.sleep(2)
        print(key,' ',outtarget)
        with open('drug_targets.txt', 'a', encoding='utf-8')as ww:
            outt = key + '\t' + outtarget + '\n'
            ww.write(str(outt))

    out = key+'\t'+value+'\t'+outtarget+'\n'
    with open(fileout, 'a',encoding='utf-8')as ww:
        ww.write(str(out))







