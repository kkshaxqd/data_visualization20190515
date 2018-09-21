# !/usr/bin/env python
# -*- coding: utf8 -*-
# need ChromeDriver v2.37 for Chrome 64

from selenium import webdriver
import time
import chromedriver_binary
def test_01():
    browser = webdriver.Chrome()
    browser.get('https://www.taobao.com')
    input = browser.find_element_by_id('q')
    input.send_keys('iPhone')
    time.sleep(1)
    input.clear()
    input.send_keys('iPad')
    button = browser.find_element_by_class_name('btn-search')
    button.click()


groups = ([x * 20 for x in range(1, 21)])
print(groups)