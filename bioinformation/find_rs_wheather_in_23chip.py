# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

filein = 'testrssite.txt'
fileout = 'testrssite_results.txt'
fileadd = "women23chip.txt"

rssitedict = {}
def getrssitedict(fileadd):
    with open(fileadd, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if "#" in line:
                pass
            else:
                hanglist = line.strip('\n').split('\t')
                rssitedict[hanglist[0]]=hanglist[1]+":"+hanglist[2]

getrssitedict(fileadd)

import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
def getmfid(rsid):
    mfid = "none"
    with open('mfid_2_rsid_temp_file.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if rsid == linelist[0]:
                mfid = linelist[1]
    return mfid

def getchrconditioninsnp(rsid):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options) #
    driver.implicitly_wait(10) #隐式等待10秒
    driver.get('https://www.ncbi.nlm.nih.gov/snp/rs1048943/')
    driver.find_element_by_xpath('//*[@id="search-field"]').send_keys(rsid)
    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/form/div/button').click()
    driver.implicitly_wait(8)
    wantchr = driver.find_element_by_css_selector('#ui-ncbigrid-1 > tbody > tr:nth-child(1) > td:nth-child(1)').text
    wantcoordition = driver.find_element_by_css_selector('#ui-ncbigrid-1 > tbody > tr:nth-child(1) > td:nth-child(2)').text
    chr = re.sub("GRCh37.p13 chr ","",wantchr)
    coordition = re.search(":g.(\d+)\w",wantcoordition).group(1)
    fanhui = str(chr)+":"+str(coordition)
    driver.quit()
    return fanhui

#result = getchrconditioninsnp('rs4646903')
#print(result)

def readandwriters(filein,fileout):
    if os.path.exists('mfid_2_rsid_temp_file.txt'):
        pass
    else:
        with open('mfid_2_rsid_temp_file.txt', 'w', encoding='utf-8')as gg:
            outss = "rsid" + "\t" + "mfid" + "\t"+"coordition"+ "\n"
            gg.write(str(outss))
    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        hang = lines[0].strip('\n')
        out = hang + "\t"+ "是否在23芯片中"+"\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(out))
        for line in lines[1:]:
            line = line.strip('\n')
            line = line.strip()
            if "." in line:
                out = line+ "\t"+ "."+"\n"
                with open(fileout, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))
            elif line.lower() in rssitedict:
                out = line+ "\t"+ "在"+"\n"
                with open(fileout, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))
            else:
                line = line.lower()
                mfid = getmfid(line)
                if mfid == "none":
                    fanhuicoordition = getchrconditioninsnp(line)
                    for i in rssitedict.keys():
                        if fanhuicoordition == rssitedict[i]:
                            mfid = i
                            break
                        else:
                            mfid = "不在"
                    with open('mfid_2_rsid_temp_file.txt', 'a', encoding='utf-8') as wg:
                        outs = line + "\t" + mfid + "\t" + fanhuicoordition + "\n"
                        wg.write(str(outs))
                        print(line, fanhuicoordition, mfid)


                out = line+ "\t"+ mfid+"\n"
                with open(fileout, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))
readandwriters(filein,fileout)


