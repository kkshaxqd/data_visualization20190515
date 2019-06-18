# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys


filein = 'testrssite.txt'
fileout = 'rsdescribtion_file.txt'

import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver


def getmfid(rsid):
    mfid = rsid+"\tnone"
    with open('rsid_and_describetion_temp_file.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if rsid == linelist[0]:
                describtion = linelist[1]
                mfid =rsid+"\t"+ describtion
    return mfid


def getchrconditioninsnp(rsid):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome() #chrome_options=chrome_options
    driver.get('http://grch37.ensembl.org/Homo_sapiens/Variation/Explore?db=core;r=3:169082133-169083133;v=rs6774494;vdb=variation;vf=323317620')
    driver.implicitly_wait(10) #隐式等待10秒
    driver.find_element_by_css_selector('#se_q').send_keys(rsid)
    driver.find_element_by_css_selector('#searchPanel > form > div.search.print_hide > div:nth-child(3) > img').click()
    driver.implicitly_wait(8)
    try:
        show = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div/div[12]/div[2]/p[1]/a[2]').text
    except:
        show = "none"

    if show != "none":
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div/div[12]/div[2]/p[1]/a[2]').click()
            driver.implicitly_wait(8)
            describ = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div/div[12]/div[2]/p').text
        except:
            describ = "none"
    else:
        describ = "none"
    driver.quit()
    print(describ)
    return describ

getchrconditioninsnp('rs2228000')