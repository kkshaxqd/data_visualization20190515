# !/usr/bin/env python
# -*- coding: utf8 -*-

import os,re,sys

import pandas as pd

fileadd = 'E:\\haxqd\\myscript\\GEZHI_Script\\pharmGKB20180926\\annotations\\var_pheno_ann.tsv'
filein = 'E:\\haxqd\\myscript\\GEZHI_Script\\pharmGKB20180926\\annotations\\needannodrug.txt'
fileout = 'E:\\haxqd\\myscript\\GEZHI_Script\\pharmGKB20180926\\annotations\\needannodrug_annoresult.txt'
filemeta = 'E:\\haxqd\\myscript\\GEZHI_Script\\pharmGKB20180926\\annotations\\clinical_ann_metadata.tsv'
##根据注释ID找到证据等级信息（在metadata），根据文献id找到PMID信息，根据rs号获得变异位点相应信息
def getadd(fileadd):
    needline = []
    with open(fileadd,'r',encoding='utf-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            needline.append(line)
        return needline


def findevidencebyID(annotiaonID,metainfo):
    evdencilevel = '.'
    for meta in metainfo:
        if annotiaonID in meta:
            metalist = meta.split('\t')
            evdencilevel = metalist[3]
    return  evdencilevel

### 根据文献id 爬取获得PMID
import time,random
from bs4 import BeautifulSoup  # 引入beautifulsoup 解析html事半功倍
from urllib import request
import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from selenium.webdriver.common.action_chains import ActionChains

def get_pmid_by_lid(lid):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(10) #隐式等待10秒
    driver.get('https://www.pharmgkb.org/literature/'+lid)
    #driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div/span/div/div/input').send_keys(lid)
    #driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/button').click()
    #进入新的一页，点击查找到的文献
    #driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div/div/div[2]/div/a').click()
    time.sleep(5)
    references = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div/div/div[1]/div/div[2]/small[1]/a').text
    references = re.sub('\(opens in new window\)','',references)
    print(references)
    driver.quit()
    return references.strip('\r\n')

def getpmidnotrunmany(inlineid):
    with open('temp_file.txt', 'r', encoding='utf-8') as f:
        pmid = 'none'
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            linelist = line.split('\t')
            if inlineid == linelist[1]:
                pmid =  linelist[0]
    return pmid


with open(filein,'r',encoding='utf-8')as f:
    lines = f.readlines()
    infoset = getadd(fileadd)
    metainfo = getadd(filemeta)
    if os.path.exists('temp_file.txt'):
        pass
    else:
        with open('temp_file.txt', 'w', encoding='utf-8')as gg:
            outss = "PMID" + "\t" + "LetrID" + "\n"
            gg.write(str(outss))
    out = lines[0].strip('\n')+"\tAlleles"+"\tPhenotype Category"+"\tSignificance"+"\tSentence"+"\tNotes"+"\tLiterature ID"+"\tEvidence level"+"\n"
    with open(fileout,'w',encoding='utf-8')as ww:
        ww.write(str(out))
    for line in lines[1:]:
        line = line.strip('\n')
        linelist = line.split('\t')
        flag = 0
        zhanweifu = "."
        for info in infoset:
            if linelist[1] in info and linelist[2] in info and linelist[3] in info:
                infolist = info.split('\t')
                evdencilevel = findevidencebyID(infolist[0].strip() ,metainfo)
                pmid = getpmidnotrunmany(infolist[4].strip())
                if pmid == "none":
                    pmid = get_pmid_by_lid(infolist[4].strip())
                    with open('temp_file.txt', 'a', encoding='utf-8') as wg:
                        outs = pmid+"\t"+infolist[4].strip()+"\n"
                        wg.write(str(outs))

                out = line+"\t"+infolist[10]+"\t"+infolist[5]+"\t"+infolist[6]+"\t"+infolist[8]+"\t"+infolist[7]+"\t"+pmid+"\t"+evdencilevel+"\n"
                flag += 1
                with open(fileout,'a',encoding='utf-8')as ww:
                    ww.write(str(out))
        if flag == 0 :
            out = line + "\t"+zhanweifu+"\t"+zhanweifu+"\t"+zhanweifu+"\t"+zhanweifu+"\t"+zhanweifu+"\t"+zhanweifu+"\t"+zhanweifu+"\n"
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(out))