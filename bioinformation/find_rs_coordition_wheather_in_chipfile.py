# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys,xlrd


filein = 'rsid.txt'
fileout = 'rsid_in_not_in_result_CBC.txt'

filechip0 = "E:\\weixin_file\\WeChat Files\\kkshaxqd\\FileStorage\\File\\2019-03\\ASA-24v1-0_A1.txt"
filechip1 = "E:\\weixin_file\\WeChat Files\\kkshaxqd\\FileStorage\\File\\2019-03\\ASA-24v1-0_A1.csv\\ASA-24v1-0_A1.csv"#这种地址就有问题
filechip2 = "E:\\weixin_file\\WeChat Files\\kkshaxqd\\FileStorage\\File\\2019-03\\CBC-PMRA位点信息.xlsx"
database_info = []
def chuli_databasefile(filechip2):
    #csv不是纯正的xls数据
    wb = xlrd.open_workbook(filechip2)
    sh1 = wb.sheet_by_index(0)
    # 递归显示每行数据
    for rownum in range(sh1.nrows):
        #print(sh1.row_values(rownum))  # 每一行的数据以数组形式存储
        hanglist = sh1.row_values(rownum)
        if "#" in hanglist:
            continue
        elif hanglist[0]:
            if "rs" in hanglist[3]:
                hanglist[3] = str(hanglist[3])
                print(hanglist[3])
                content = re.sub('\.0', '', str(hanglist[1])) + ":" + re.sub('\.0', '', str(hanglist[2]))
                database_info.append(content)
                database_info.append(hanglist[3])
            else:
                content = re.sub('\.0','',str(hanglist[1]))+":"+re.sub('\.0','',str(hanglist[2]))
                #print(content)
                database_info.append(content)


def getdatabaseinfo(filechip):
    with open(filechip, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[8:]:
            line = line.strip('\r\n')
            linelist = line.split(',')
            #print(linelist[1])
            linelist[1] = str(linelist[1])
            database_info.append(linelist[1])

#getdatabaseinfo(filechip)

import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
def paqucoordition_by_rs(rsid):
    content = "none"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome() #chrome_options=chrome_options
    driver.get('https://www.ncbi.nlm.nih.gov/snp/rs6774494')
    driver.implicitly_wait(10) #隐式等待10秒
    driver.find_element_by_css_selector('#search-field').send_keys(rsid)
    driver.find_element_by_css_selector('#main_content > div > div > div:nth-child(2) > form > div > button > span').click()
    driver.implicitly_wait(8)
    try:
        content1 = driver.find_element_by_css_selector('#ui-ncbigrid-1 > tbody > tr:nth-child(1) > td:nth-child(1)').text
        content2 = driver.find_element_by_css_selector('#ui-ncbigrid-1 > tbody > tr:nth-child(1) > td:nth-child(2)').text
        content1 = re.sub('GRCh37.p13\schr\s','',content1)
        content2 = re.sub(r'.*g\.(\d+)\w>\w',r'\1',content2)#NC_000003.11:g.169082633G>A
        content = content1+":"+content2
    except:
        content = "none"
    #print(content)
    driver.quit()
    with open('rs_coordition_temp.txt','a', encoding='utf-8')as dd:
        outss = rsid + "\t" + content + "\n"
        dd.write(str(outss))
    return str(content)

#paqucoordition_by_rs('rs29232')
def getmfid(rsid):
    content = "none"
    with open('rs_coordition_temp.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if rsid == linelist[0]:
                content = linelist[1]
    return content


def main():
    #getdatabaseinfo(filechip)
    chuli_databasefile(filechip2)
    if os.path.exists('rs_coordition_temp.txt'):
        pass
    else:
        with open('rs_coordition_temp.txt', 'w', encoding='utf-8')as gg:
            outss = "rsid" + "\t" + "coordition" +"\n"
            gg.write(str(outss))

    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        hang = lines[0].strip('\n')+"\t"+r"是否在新芯片文件中"+"\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(hang))
        for line in lines[1:]:
            line = line.strip('\r\n')
            if line in database_info:
                result = "在"
            else:
                content = getmfid(line)
                if content == "none":
                    content = paqucoordition_by_rs(line)
                    if content in database_info:
                        result = "在"
                    else:
                        result = "不在"
                else:
                    if content in database_info:
                        result = "在"
                    else:
                        result = "不在"
            out = line + "\t"+ result+"\n"
            print(out)
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(out))
main()