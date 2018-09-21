# !/usr/bin/env python
# -*- coding: utf8 -*-
# need ChromeDriver v2.37 for Chrome 64
import os , re
import time,random
from bs4 import BeautifulSoup  # 引入beautifulsoup 解析html事半功倍
from urllib import request
import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

def dingwei_cosmic_find_GENE(index="BRAF p.D594G"):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10) #隐式等待10秒
    driver.get('https://cancer.sanger.ac.uk/cosmic/')
    time.sleep(5)
    # 元素定位的方法
    # 找到“search”
    driver.find_element_by_id("q").send_keys(index)
    # 点击百度一下
    driver.find_element_by_id("nav-search-button").click()
    time.sleep(5)
    #driver.find_element_by_id("mutations").click()
    #/html/body/div[1]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[2] 开发者工具插件真好用，返回单个webelement 得用browser.find_element_by_xpath
    link = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/a")
    link.click()
    time.sleep(10)
    ## 不可见元素点击直接click不可用，会报错，使用ActionChains来
    GenomeVersion = driver.find_element_by_xpath("/html/body/div[1]/nav/ul/li[7]/a")
    ActionChains(driver).click(GenomeVersion).perform()
    GRh37link = driver.find_element_by_xpath("/html/body/div[1]/nav/ul/li[7]/ul/li[1]/a")
    ActionChains(driver).move_to_element(GRh37link).double_click(GRh37link).perform()  # 移动到GRh37link
    #print(GRh37link.text)
    driver.implicitly_wait(10)
    #/html/body/div[1]/div/div[2]/section[1]/div/dl/dd[6]/a[1]
    chrcordition = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/section[1]/div/dl/dd[6]/a[1]").text
    driver.quit()
    return chrcordition
    #print(chrcordition)



def main():
    index_list={}
    with open("variant_for_cosmic_find.txt",'r', encoding='utf-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            info = line.split('\t')
            index = info[-2]+" "+info[-1]
            if info[0] == "Drugname":
                with open("variant_for_cosmic_find_info.txt","w",encoding='utf-8') as ww:
                    out = line+"\t"+r"染色体位置(GRCh37)"+"\n"
                    ww.write(str(out))
            elif index in index_list:
                ## 判断键在字典中否,判断这个基因变异是否已经爬过了
                chrweizhi = index_list[index]
                with open("variant_for_cosmic_find_info.txt","a",encoding='utf-8') as ww:
                    out = line+"\t"+chrweizhi+"\n"
                    ww.write(str(out))
            else:
                try:
                    chrweizhi = dingwei_cosmic_find_GENE(index)
                    print(r"有结果",index,":",chrweizhi)
                except:
                    chrweizhi = "."
                    print(r"没有结果", index, ":", chrweizhi)
                index_list[index] = chrweizhi
                with open("variant_for_cosmic_find_info.txt","a",encoding='utf-8') as ww:
                    out = line+"\t"+chrweizhi+"\n"
                    ww.write(str(out))

import requests
def testproxies():
    proxies = {
        "http":"http://127.0.0.1:9743",
        "https":"https://127.0.0.1:9743",
    }
    response = requests.get("https://www.baidu.com",proxies=proxies)
    print(response.status_code)


import builtwith
def testweb():
    print(builtwith.parse("https://cancer.sanger.ac.uk/cosmic/"))

if __name__ == "__main__":
    # dingwei_cosmic_find_GENE()
    #main()
    #testproxies()
    testweb()
