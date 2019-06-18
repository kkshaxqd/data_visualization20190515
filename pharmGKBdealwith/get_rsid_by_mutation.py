# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
from pyquery import PyQuery as pq
filein = 'E:\\haxqd\\201810\\vatition_name.txt'
fileinnew = "E:\\haxqd\\201810\\variant_name_new.txt"
fileoutnew = "E:\\haxqd\\201810\\variant_name_new_add_rsinfo.txt"
fileout = 'E:\\haxqd\\201810\\vatition_name_add_rsinfo.txt'

#https://www.ncbi.nlm.nih.gov/guide/howto/view-all-snps/

#1. find #p.
#2. ;划分
#3. 再确定#p.分割，没有的不管
#NCBI 爬虫涉及了很多坑，网站具有反爬措施，速度太慢
##由于速度太慢，不得不构建多进程爬虫,多进程的输出可能会乱序，所以其实最好的是用多进程把rs与variant成库，最后单独读入写出~
import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

##NCBI 有个比较麻烦的防爬选项，要关掉这个每次
def fangpaclose(driver):
    try:
        fangpa = driver.find_element_by_css_selector('#ui-ncbiexternallink-35 > div.smcx-widget.smcx-modal.smcx-modal-invitation.smcx-show.smcx-widget-dark.smcx-hide-branding.smcx-opaque > div.smcx-modal-content > div.smcx-modal-close')
        fangpa.click()
    except:
        pass

def getrs(driver):
    fangpaclose(driver)
    rsid = driver.find_element_by_partial_link_text('rs').text
    return rsid

def wheatherrs(rsid,driver):
    if re.search('rs', rsid):
        return rsid
    else:
        fangpaclose(driver)
        rsid = driver.find_element_by_css_selector(
            '#main_box > div:nth-child(7) > div > dl > dd:nth-child(14) > ul > li:nth-child(3) > span > a').text
        return rsid


def getrs_by_variant(variant):
    rsid = "."
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options) #
    driver.implicitly_wait(5) #隐式等待10秒
    driver.get('https://www.ncbi.nlm.nih.gov/clinvar/variation/12624/')
    fangpaclose(driver)
    driver.find_element_by_xpath('//*[@id="term"]').send_keys(variant)
    driver.find_element_by_xpath('//*[@id="search"]').click()
    driver.implicitly_wait(5)
    try:
        fangpaclose(driver)
        itemnum = driver.find_element_by_css_selector('#padded_content > div:nth-child(4) > div > h3').text
        number = re.search('Items: (\d+)',itemnum).group(1)
        for i in range(int(number)):
            ii = i+1
            ele = '#tabdocsumtable > tbody > tr:nth-child('+str(ii)+') > td.docsum_table_td > div > a > span'
            fangpaclose(driver)
            ##解析网页前要先看有没有防爬
            newclick = driver.find_element_by_css_selector(ele)
            newclick.click()
            driver.implicitly_wait(5)
            ##点击网页后，新网页中要先检查有没有反爬
            fangpaclose(driver)
            nmgenecdna = driver.find_element_by_css_selector('#main_box > div.clearfix > h2').text
            #print(nmgenecdna)
            gene = variant.split(' ')
            html = driver.page_source
            varshow = re.sub(r'p\.','',gene[1])
            if gene[0] in nmgenecdna and varshow in html:
                rsid = getrs(driver)
                print(rsid)
                break
            driver.back()
    except:
        fangpaclose(driver)
        nmgenecdna = driver.find_element_by_css_selector('#main_box > div.clearfix > h2').text
        gene = variant.split(' ')
        html = driver.page_source
        varshow = re.sub(r'p\.', '', gene[1])
        if gene[0] in nmgenecdna and varshow in html:
            rsid = getrs(driver)
            print(rsid)
    driver.quit()
    return rsid
    #print(rsid)


def getrsid(variant):
    with open('rsid_by_variant_temp_file.txt', 'r', encoding='utf-8') as f:
        rsid = 'none'
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if variant == linelist[0]:
                rsid = linelist[1]
    return rsid

##构建多进程爬虫,多进程的输出可能会乱序，所以其实最好的是用多进程把rs与variant成库，最后单独读入写出~
def get_num_for_cyc(filein):
    with open(filein, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        # 创建临时文件
        if os.path.exists('rsid_by_variant_temp_file.txt'):
            pass
        else:
            with open('rsid_by_variant_temp_file.txt', 'w', encoding='utf-8')as gg:
                outss = "variant" + "\t" + "rsid" + "\n"
                gg.write(str(outss))

        hang = lines[0].strip('\n')
        outlang = hang + "\t" + r"突变位点rs号" + "\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(outlang))
        num = len(lines)
        lineinfo = lines
        return num,lineinfo
def main(line):
    line = line.strip('\n')
    linelist = line.split('\t')
    if ";" in linelist[1]:
        info = linelist[1].split(';')
        for variantinfo in info:
            if "#p." in variantinfo:
                varant = re.search(r'(\w+)\#p\.(\w\d+\w+)', variantinfo)
                variant = varant.group(1) + " " + varant.group(2)
                rsid = getrsid(variant)
                if rsid == "none":
                    try:
                        rsid = getrs_by_variant(variant)
                    except:
                        rsid = "."
                    print(variant, rsid)
                    with open('rsid_by_variant_temp_file.txt', 'a', encoding='utf-8') as wg:
                        outs = variant + "\t" + rsid + "\n"
                        wg.write(str(outs))
    elif "#p." in linelist[1]:
        try:
            varant = re.search(r'(\w+)\#p\.(\w\d+\w+)', linelist[1])
            variant = varant.group(1) + " " + varant.group(2)
        except:
            variant = linelist[1]
        rsid = getrsid(variant)
        if rsid == "none":
            try:
                rsid = getrs_by_variant(variant)
            except:
                rsid = "."
            with open('rsid_by_variant_temp_file.txt', 'a', encoding='utf-8') as wg:
                outs = variant + "\t" + rsid + "\n"
                wg.write(str(outs))
        print(variant, rsid)
def write_rs_to_file(line):
    line = line.strip('\n')
    linelist = line.split('\t')
    if "#p." not in linelist[1]:
        rsid = "."
        outlang = line + "\t" + rsid + "\n"
        with open(fileout, 'a', encoding='utf-8')as ww:
            ww.write(str(outlang))
    elif ";" in linelist[1]:
        info = linelist[1].split(';')
        rsidset = []
        for variantinfo in info:
            rsid = "."
            if "#p." in variantinfo:
                varant = re.search(r'(\w+)\#p\.(\w\d+\w+)', variantinfo)
                variant = varant.group(1) + " " + varant.group(2)
                rsid = getrsid(variant)
            rsidset.append(rsid)
        rsout = ";".join(rsidset)
        outlang = line + "\t" + rsout + "\n"
        with open(fileout, 'a', encoding='utf-8')as ww:
            ww.write(str(outlang))
    elif "#p." in linelist[1]:
        try:
            varant = re.search(r'(\w+)\#p\.(\w\d+\w+)', linelist[1])
            variant = varant.group(1) + " " + varant.group(2)
        except:
            variant = linelist[1]
        rsid = getrsid(variant)
        if rsid == "none":
            rsid = "."
        outlang = line + "\t" + rsid + "\n"
        with open(fileout, 'a', encoding='utf-8')as ww:
            ww.write(str(outlang))

def get_num_for_cyc1(fileinnew):
    with open(fileinnew, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        # 创建临时文件
        if os.path.exists('rsid_by_variant_temp_file.txt'):
            pass
        else:
            with open('rsid_by_variant_temp_file.txt', 'w', encoding='utf-8')as gg:
                outss = "variant" + "\t" + "rsid" + "\n"
                gg.write(str(outss))

        hang = lines[0].strip('\n')
        outlang = hang + "\t" + r"突变位点rs号" + "\n"
        with open(fileoutnew, 'w', encoding='utf-8')as ww:
            ww.write(str(outlang))
        num = len(lines)
        lineinfo = lines
        return num,lineinfo
def main1(line):
    line = line.strip('\n')
    linelist = line.split('\t')
    if "p." in linelist[2]:
        linelist[2] = re.sub(r'p.','',linelist[2])
        variant = linelist[1] + " " + linelist[2]
        rsid = getrsid(variant)
        if rsid == "none":
            try:
                rsid = getrs_by_variant(variant)
            except:
                rsid = "."
            with open('rsid_by_variant_temp_file.txt', 'a', encoding='utf-8') as wg:
                outs = variant + "\t" + rsid + "\n"
                wg.write(str(outs))
        print(variant, rsid)
def write_rs_to_file1(line):
    line = line.strip('\n')
    linelist = line.split('\t')
    if "p." not in linelist[2]:
        rsid = "."
        outlang = line + "\t" + rsid + "\n"
        with open(fileoutnew, 'a', encoding='utf-8')as ww:
            ww.write(str(outlang))
    elif "p." in linelist[2]:
        linelist[2] = re.sub(r'p.', '', linelist[2])
        variant = linelist[1] + " " + linelist[2]
        rsid = getrsid(variant)
        if rsid == "none":
            rsid = "."
        outlang = line + "\t" + rsid + "\n"
        with open(fileoutnew, 'a', encoding='utf-8')as ww:
            ww.write(str(outlang))

from multiprocessing import Pool

if __name__ == "__main__":
    num,lineinfo = get_num_for_cyc1(fileinnew)
    pool = Pool()
    pool.map(main1, (lineinfo[i] for i in range(1,num)))
    pool.close()
    pool.join()

    for i in range(1,num):
        write_rs_to_file1(lineinfo[i])
    #getrs_by_variant('ABL1 T315I')
    #getrs_by_variant('ABL1 p.D400Y')
    #getrs_by_variant('ABL1 p.F317C')
