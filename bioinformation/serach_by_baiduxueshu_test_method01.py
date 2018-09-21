# !/usr/bin/env python
# -*- coding: utf8 -*-
# need ChromeDriver v2.37 for Chrome 64
import os , re
import time
import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
driver = webdriver.Chrome()

driver.get('http://xueshu.baidu.com/')

time.sleep(3)
# 元素定位的方法
# 找到“百度一下”
driver.find_element_by_id("kw").send_keys(u"Age- and genotype-dependent variability in the protein abundance and activity of six major uridine")
# 点击百度一下
driver.find_element_by_id("su").click()

# 进行页面截屏
#driver.save_screenshot("./baidu.png")
# driver 获取html字符串
#print(driver.page_source) # 内容
print(driver.current_url) # 网址
# 打开第一个链接
datasourse = driver.page_source.split(u'<!--  -->')  # 按这个标志分组
compile_rule = re.compile(r'被引量:\xa0\n.*(\d+).*</span>\n',re.S)
yinyong = compile_rule.search(datasourse[1]).group(1)  # python中括号捕获，group(1) 相当于Perl中$1
"""这样可以获得引用量，比较难匹配的是被引量:\xa0\n，用findall先全查看了，才知道后面的:&nbsp; 识别为\xa0 """
print(yinyong)
#link.click()


# 退出浏览器
time.sleep(3)
driver.quit()