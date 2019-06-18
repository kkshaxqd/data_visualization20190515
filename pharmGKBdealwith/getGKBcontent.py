# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
from pyquery import PyQuery as pq

filein = 'E:\\haxqd\\201810\\GGG.txt'
fileinin = 'E:\\haxqd\\201810\\ggg_ggg.txt'
fileout = 'E:\\haxqd\\201810\\GGG_add_pmid_content.txt'

#在pharmaGKB里获得想要的pmid 的content

import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def getcontent_in_ncbi(pmid):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(5) #隐式等待10秒
    driver.get('https://www.ncbi.nlm.nih.gov/pubmed/')
    driver.find_element_by_xpath('//*[@id="term"]').send_keys(pmid)
    driver.find_element_by_xpath('//*[@id="search"]').click()
    driver.implicitly_wait(5)
    try:
        content = driver.find_element_by_css_selector('#maincontent > div > div.rprt_all > div > div.abstr').text
        driver.quit()
    except:
        content = "."
    return content




def gettempcontent(pmid):
    with open('pmid_content_temp.txt', 'r', encoding='utf-8') as f:
        content = 'none'
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if str(pmid) == str(linelist[0]):
                content = linelist[1]
    return content

def write_to_temp(pmid,content):
    with open('pmid_content_temp.txt', 'a', encoding='utf-8') as wg:
        outs = str(pmid) + "\t" + str(content) + "\n"
        wg.write(str(outs))

def getcontent_by_pmid(pmid):
    content = gettempcontent(pmid)
    if content == "none":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options) #
        #driver.implicitly_wait(5) #隐式等待10秒
        driver.get('https://www.pharmgkb.org/literature/')
        wait = WebDriverWait(driver, 10)
        try:
            input = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/header/div[1]/div/div[2]/nav/div[1]/div/div/span/div/div/input')))
            submit = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[1]/div/header/div[1]/div/div[2]/nav/div[1]/div/button')))
            input.send_keys(pmid)
            submit.click()
            lecitem = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/span[2]/span/a')))
            lecitem.click()
            contentinfo = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/main/div/div[2]/div/div/div[2]/div/span')))
            print(contentinfo)
            #html = driver.page_source # 这个得不到网页源代码竟然
            #print(html)
            driver.implicitly_wait(10)
            references = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div/div/div[1]/div/div[2]/small[1]/a').text
            references = re.sub('\(opens in new window\)','',references)
            print(references) ##为毛加上这个就能识别出来了
            content = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div/div/div[2]/div/span').text
        except:
            print('PharmGKB no result,go to NCBI for',pmid)
            content = getcontent_in_ncbi(pmid)
            content = re.sub('Abstract',"",content)
            content = content.replace('\n',' ').replace('\r',' ')
            content = content.strip()
        driver.quit()
        write_to_temp(pmid, content)
    print(content)
    return content


def get_num_for_cyc(filein):
    with open(filein, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        # 创建临时文件
        if os.path.exists('pmid_content_temp.txt'):
            pass
        else:
            with open('pmid_content_temp.txt', 'w', encoding='utf-8')as gg:
                outss = "pmid" + "\t" + "content" + "\n"
                gg.write(str(outss))

        hang = lines[0].strip('\n')
        outlang = hang + "\t" + r"GKB描述" + "\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(outlang))
        num = len(lines)
        lineinfo = lines
        return num,lineinfo

def get_cyc_temp_line(fileinin):
    with open(fileinin, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        tempnum = len(lines)
        templineinfo = lines
        return tempnum,templineinfo
def main(line):
    line = line.strip('\n')
    #linelist = line.split('\t')
    if "PMID" in line:
        pmids = re.findall('(\d+)',line)
        for pmid in pmids:
            if len(pmid)>4:
                getcontent_by_pmid(pmid)


def write_rs_to_file(line):
    line = line.strip('\n')
    linelist = line.split('\t')
    if "PMID" in linelist[4]:
        pmids = re.findall('(\d+)',linelist[4])
        contents = []
        for pmid in pmids:
            if len(pmid)>4:
                content = gettempcontent(pmid)
            else:
                content = "."
            contents.append(content)
        out = " // ".join(contents)
        outlang = line + "\t" + out + "\n"
        with open(fileout, 'a', encoding='utf-8')as ww:
            ww.write(str(outlang))
    else:
        out = "."
        outlang = line + "\t" + out + "\n"
        with open(fileout, 'a', encoding='utf-8')as ww:
            ww.write(str(outlang))

def write_pmcontent_to_file(line):
    line = line.strip('\n')
    #linelist = line.split('\t')
    if "PMID" in line:
        pmids = re.findall('(\d+)',line)
        contents = []
        for pmid in pmids:
            if len(pmid)>4:
                content = gettempcontent(pmid)
            else:
                content = "."
            contents.append(content)
        out = " // ".join(contents)
        outlang = line + "\t" + out + "\n"
        with open(fileout, 'a', encoding='utf-8')as ww:
            ww.write(str(outlang))
    else:
        out = "."
        outlang = line + "\t" + out + "\n"
        with open(fileout, 'a', encoding='utf-8')as ww:
            ww.write(str(outlang))

def  buchong_temp_pmid(fileinin):
    with open(fileinin, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            if "PMID" in line:
                pmids = re.findall('(\d+)',line)
                for pmid in pmids:
                    if len(pmid)>4:
                        getcontent_by_pmid(pmid)


from multiprocessing import Pool
if __name__ == "__main__":
    num, lineinfo = get_num_for_cyc(filein)
    tempnum, templineinfo = get_cyc_temp_line(fileinin)
    buchong_temp_pmid(fileinin)
    pool = Pool()
    pool.map(main, (templineinfo[i] for i in range(1, tempnum)))
    pool.close()
    pool.join()
    for i in range(1, tempnum):
        #write_rs_to_file(lineinfo[i])
        write_pmcontent_to_file(templineinfo[i])
#getcontent_by_pmid('20673586')
#getcontent_by_pmid('19307503')



