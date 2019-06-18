# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
from pyquery import PyQuery as pq

filein = 'E:\\haxqd\\201811\\dengtask\\gene.txt'
fileout = 'E:\\haxqd\\201811\\dengtask\\gene_add_nct_content.txt'

import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def write_to_temp(nct,content):
    with open('nct_content_temp.txt', 'a', encoding='utf-8') as wg:
        outs = str(nct) + "\t" + str(content) + "\n"
        wg.write(str(outs))

def gettempcontent(nct):
    with open('nct_content_temp.txt', 'r', encoding='utf-8') as f:
        content = 'none'
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if str(nct) == str(linelist[0]):
                content = linelist[1]
    return content

def opendrugnct(drug):
    nctset = []
    filename = "E:\\haxqd\\201811\\dengtask\\"+drug+".txt"
    with open(filename,'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            nctset.append(line)
    return nctset


def main():
    with open(filein,'r', encoding='utf-8') as f:
        lines = f.readlines()
        # 创建临时文件
        if os.path.exists('nct_content_temp.txt'):
            pass
        else:
            with open('nct_content_temp.txt', 'w', encoding='utf-8')as gg:
                outss = "ncturl" + "\t" + "content" + "\n"
                gg.write(str(outss))
        hang = lines[0].strip('\n')+"\tOTHER_INFO\t"+"NCT:PHASE:STARTTIME:CONTION:PMtitle"+"\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(hang))
        for line in lines[1:]:
            line = line.strip('\n')
            nctset = opendrugnct(line)
            outinfo = ""
            for nct in nctset:
                if outinfo:
                    outcontmain = gettempcontent(nct)
                    if outcontmain == "none":
                        outcontmain = getcontent_in_nct(nct)
                        write_to_temp(nct,outcontmain)
                    outinfo = outinfo+"\t"+outcontmain
                else:
                    outcontmain = gettempcontent(nct)
                    if outcontmain == "none":
                        outcontmain = getcontent_in_nct(nct)
                        write_to_temp(nct,outcontmain)
                    outinfo = outcontmain
            outlang = line + "\t.\t" + outinfo + "\n"
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(outlang))

def getcontent_in_nct(nct):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(10) #隐式等待10秒
    driver.get(nct)
    driver.implicitly_wait(5) #隐式等待10秒
    contitiaons = driver.find_elements_by_css_selector('#tab-body > div > div:nth-child(1) > div:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(1)')
    cont = []
    for contitiaon in contitiaons:
        conti = contitiaon.text
        cont.append(conti)
    conout = ','.join(cont)
    conout = re.sub(r'\n',',',conout)

    phases = driver.find_elements_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td[3]')
    pcont = []
    for phase in phases:
        phase = phase.text
        pcont.append(phase)
    phaseout = ','.join(pcont)
    phaseout = re.sub(r'\n',',',phaseout)
    starttime = driver.find_element_by_css_selector('#tab-body > div > div:nth-child(1) > table > tbody > tr:nth-child(7) > td:nth-child(2)').text
    try:
        pmidcontent = driver.find_element_by_css_selector('#tab-body > div > div:nth-child(12) > div.indent2 > div:nth-child(9) > div > a').text
    except:
        pmidcontent = "No"
    nctid = re.sub('https://ClinicalTrials.gov/show/', "", nct)
    outcontmain = nctid + ":" + phaseout + ":" + starttime + ":" + conout + ":" + pmidcontent
    print(nct,":",outcontmain)
    return (outcontmain)



main()