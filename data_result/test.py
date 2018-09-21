# !/usr/bin/env python
# -*- coding: utf8 -*-
from serachbybaiduxueshu import get_title_year_yinyong
seq = ['1','2','1','2','3','4','5','6']

tdict = {}
for i in seq:
    try:
        if tdict[i]:
            tdict[i] = tdict[i]+1
    except KeyError:
        tdict[i] = 1

for key,value in tdict.items():
    print(key,':',value)

#(title, year, yinyong) = get_title_year_yinyong(23736036)
#print(title, year, yinyong)


def  duplicate_count(text):
    # Your code goes here
    text = text.lower()
    texts = set(text)
    lists = []
    for i in texts:
        numbers = text.count(i)
        if numbers != 1:
            lists.append(numbers)
    return len(lists)

sss = duplicate_count('abcde')
print(sss)
import pandas as pd
obj = pd.Series(['a','a','b','c']*4)
print(obj)

def div():
    2 / 10

try:
    div()
except ZeroDivisionError as e:
    raise ValueError(e)

import tesseract
from PIL import Image
image = Image.open('E:\\haxqd\\201807\\微信截图_20180730102003.png')
print(tesserocr.image_to_text(image))


import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
def get_drug_target(drugname='sorafenib'):
    #driver = webdriver.Chrome()
    #driver.get('http://xueshu.baidu.com/')
    #time.sleep(2)
    url = 'http://www.selleckchem.com/products/'+drugname+'.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url,headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')#打开Url,获取HttpResponse返回对象并读取其ResposneBody
    soup = BeautifulSoup(page_info, 'lxml')
    soup = soup.find_all(name='td')
    allcontent = re.compile(r'<td>(.*?)<sup>',re.S)
