# !/usr/bin/env python
# -*- coding: utf8 -*-

import os,re,sys

filein = 'E:\\haxqd\\myscript\\GEZHI_Script\\pharmGKB20180926\\annotations\\needannodrug_annoresult.txt'

fileout = 'E:\\haxqd\\myscript\\GEZHI_Script\\pharmGKB20180926\\annotations\\needannodrug_annoresult_addcdna.txt'


import time,random
import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver

def get_cdna_by_rs(rsnp):
    hgvsset= ""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options) #
    driver.implicitly_wait(10) #隐式等待10秒
    driver.get('https://www.ncbi.nlm.nih.gov/projects/SNP/')
    driver.find_element_by_xpath('//*[@id="entrez_term"]').send_keys(rsnp)
    driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[3]/td/table/tbody/tr/td/input[2]').click()
    pageSource = driver.page_source
    panduanset = set(re.findall(r'(rs\d+)',pageSource))
    #print(panduanset)
    if len(panduanset)>1:
        hgvsinfos = driver.find_elements_by_xpath(
            '/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[5]/div[1]/div[2]/div[1]/dl/dd[8]/span/a')
        if hgvsinfos:
            pass
        else:
            hgvsinfos = driver.find_elements_by_xpath(
                '/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[5]/div/div[2]/div[1]/dl/dd[6]/span/a')

    else:
        hgvsinfos = driver.find_elements_by_xpath('/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[5]/div/div[2]/div[1]/dl/dd[6]/span/a')
        if hgvsinfos:
            pass
        else:
            hgvsinfos = driver.find_elements_by_xpath(
                '/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[5]/div[1]/div[2]/div[1]/dl/dd[8]/span/a')
    for hgvs in hgvsinfos:
        hgvsinfo = hgvs.text
        hgvslist = hgvsinfo.split(':')
        if "NM" in hgvsinfo and hgvslist[0] not in hgvsset:
            hgvsset = hgvsset+";"+hgvsinfo
        hgvsset = re.sub(r"^;",'',hgvsset)
    print(hgvsset)
    return hgvsset

def getrscdnanotrunmany(rs):
    with open('rs_cdna_temp_file.txt', 'r', encoding='utf-8') as f:
        cdna = 'none'
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            linelist = line.split('\t')
            if rs == linelist[0]:
                cdna =  linelist[1]
    return cdna


with open(filein,'r',encoding='utf-8')as f:
    lines = f.readlines()
    if os.path.exists('rs_cdna_temp_file.txt'):
        pass
    else:
        with open('rs_cdna_temp_file.txt', 'w', encoding='utf-8')as gg:
            outss = "rsID" + "\t" + "cDNA" + "\n"
            gg.write(str(outss))
    out = lines[0].strip('\n') +"\tNM:cDNA:variant"+"\n"
    with open(fileout,'w',encoding='utf-8')as ww:
        ww.write(str(out))
    for line in lines[1:]:
        line = line.strip('\n')
        linelist = line.split('\t')
        cdna = getrscdnanotrunmany(linelist[3])
        if cdna == "none":
            cdna = get_cdna_by_rs(linelist[3])
            if cdna == "":
                cdna = "."
            with open('rs_cdna_temp_file.txt', 'a', encoding='utf-8') as wg:
                outs = linelist[3] + "\t" + cdna + "\n"
                wg.write(str(outs))
        out = line+"\t"+cdna+"\n"
        with open(fileout, 'a', encoding='utf-8')as ww:
            ww.write(str(out))





