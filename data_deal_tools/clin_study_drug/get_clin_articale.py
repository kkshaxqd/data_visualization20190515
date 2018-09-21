# !/usr/bin/env python
# -*- coding: utf8 -*-

import os , re
import time
from bs4 import BeautifulSoup  # 引入beautifulsoup 解析html事半功倍
from urllib import request

#构造头文件，模拟浏览器访问
def get_clinical(NCIDS='NCT00077142'):
    url="https://ClinicalTrials.gov/show/"+NCIDS
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url,headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')#打开Url,获取HttpResponse返回对象并读取其ResposneBody
    time.sleep(2)
    #print(page_info)
    # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
    #方法参考https://blog.csdn.net/csdn2497242041/article/details/77170746 ，但是titles无内容，用正则吧还是。
    soup = BeautifulSoup(page_info, 'html.parser')
    dataresuoure = soup.prettify()
    if re.findall('Publications of Results',dataresuoure):
        allcontent = re.compile(r'Publications of Results.*?title=\"(.*?)\">',re.S)
        zazhititle = allcontent.search(dataresuoure).group(1).lstrip()
        return zazhititle
    else:
        return "No publish"

#oout = get_clinical("NCT01877187")
#print(oout)


def get_drug_target(drugname='sorafenib'):
    #driver = webdriver.Chrome()
    #driver.get('http://xueshu.baidu.com/')
    #time.sleep(2)
    url = 'http://www.selleckchem.com/products/'+drugname+'.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url,headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')#打开Url,获取HttpResponse返回对象并读取其ResposneBody
    soup = BeautifulSoup(page_info, 'lxml')
    if 'Targets' in soup:
        #soup = soup.find_all(name='td')
        allcontent = re.compile(r'<td>(.*?)<sup><a class=\"sref\"')
        targets = allcontent.findall(str(soup))
        return targets


#get_drug_target()
import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
def geet_targt_by_open_html(drugname='sorafenib'):
    driver = webdriver.Chrome()
    driver.get('http://www.selleckchem.com/')
    time.sleep(2)
   # 元素定位的方法
    # 找到“search”
    driver.find_element_by_id("searchParam").send_keys(drugname)
    # 点击百度一下
    time.sleep(2)

    driver.find_element_by_class_name("search").submit() # 强制关闭会
    time.sleep(2)
    datasourse = driver.page_source
    print(datasourse)


geet_targt_by_open_html()