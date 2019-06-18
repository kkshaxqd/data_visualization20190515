# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys


filein = 'testrssite.txt'
fileout = 'testrssite_genometype_freq.txt'

import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def getmfid(rsid):
    mfid = "none\tnone\tnone"
    with open('rsid_and_genome_type_temp_file.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            if rsid == linelist[0]:
                vcfinfo = linelist[1]
                genome_type = linelist[2]
                freq = linelist[3]
                mfid =vcfinfo+"\t"+ genome_type +"\t"+freq
    return mfid

def getchrconditioninsnp(rsid):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome() #chrome_options=chrome_options
    driver.get('http://grch37.ensembl.org/Homo_sapiens/Variation/Explore?db=core;r=19:45866759-45867759;v=rs1799793;vdb=variation;vf=1245174')
    driver.implicitly_wait(10) #隐式等待10秒
    driver.find_element_by_css_selector('#se_q').send_keys(rsid)
    driver.find_element_by_css_selector('#searchPanel > form > div.search.print_hide > div:nth-child(3) > img').click()
    driver.implicitly_wait(8)
    try:
        vcfinfo = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div/div[3]/div[2]/p/span[4]').text
    except:
        vcfinfo = "none"
    #print(vcfinfo)
    ##点击基因型信息表
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[4]/a/img').click()
        driver.implicitly_wait(10)
        chsbeixuan1 = driver.find_element_by_xpath(
            '//*[@id="1000genomesprojectphase3_table"]/tbody/tr[17]/td[1]/span[1]/b').text
        chs = driver.find_element_by_xpath(
            '//*[@id="1000genomesprojectphase3_table"]/tbody/tr[18]/td[1]/span[1]/b').text
        chsbeixuan2 = driver.find_element_by_xpath(
            '//*[@id="1000genomesprojectphase3_table"]/tbody/tr[18]/td[1]/span[1]/b').text
        if chs == "CHS":
            genomes = driver.find_element_by_xpath('//*[@id="1000genomesprojectphase3_table"]/tbody/tr[18]/td[4]').text
            genomeset = genomes.split('\n')
            if len(genomeset) < 3:
                genomes = driver.find_element_by_xpath('//*[@id="1000genomesprojectphase3_table"]/tbody/tr[1]/td[4]/div').text
                genomes = "all/"+genomes
        elif chsbeixuan1 == "CHS" :
            genomes = driver.find_element_by_css_selector('//*[@id="1000genomesprojectphase3_table"]/tbody/tr[17]/td[4]').text
            genomeset = genomes.split('\n')
            if len(genomeset) < 3:
                genomes = driver.find_element_by_xpath('//*[@id="1000genomesprojectphase3_table"]/tbody/tr[1]/td[4]/div').text
                genomes = "all/" + genomes
        elif chsbeixuan2 == "CHS":
            genomes = driver.find_element_by_css_selector('//*[@id="1000genomesprojectphase3_table"]/tbody/tr[19]/td[4]').text
            genomeset = genomes.split('\n')
            if len(genomeset) < 3:
                genomes = driver.find_element_by_xpath('//*[@id="1000genomesprojectphase3_table"]/tbody/tr[1]/td[4]/div').text
                genomes = "all/" + genomes
    except:
        genomes = "none"


    driver.quit()
    return vcfinfo,genomes


#vcfinfo,genomes = getchrconditioninsnp('rs10033464')
#print(vcfinfo,genomes)

def readandwriters(filein,fileout):
    if os.path.exists('rsid_and_genome_type_temp_file.txt'):
        pass
    else:
        with open('rsid_and_genome_type_temp_file.txt', 'w', encoding='utf-8')as gg:
            outss = "rsid" + "\t" + "VCFinfo" + "\t"+"genometype"+"\t"+"freqence"+"\n"
            gg.write(str(outss))
    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        hang = lines[0].strip('\n')
        out = hang + "\t"+ "VCFinfo"+"\t"+"基因型"+"\t"+"频率"+"\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(out))
        for line in lines[1:]:
            line = line.strip('\n')
            line = line.strip()
            if "rs" in line:
                line = line.lower()
                mfid = getmfid(line)
                if mfid == "none\tnone\tnone":
                    vcfinfo,genomesinfo = getchrconditioninsnp(line)
                    vcfinfo = re.sub("  ",':',vcfinfo)
                    if genomesinfo != "none":
                        #print(genomesinfo)
                        genomeset = genomesinfo.split('\n')
                        #print(genomeset)
                        genonewset = []
                        freqset = []
                        for genome in genomeset:
                            splitinfo = genome.split(':')
                            splitinfo[0] = re.sub('\|','',splitinfo[0])
                            #print(splitinfo[0])
                            genonewset.append(splitinfo[0])
                            #print(splitinfo[1])
                            splitinfo[1] = re.sub('\s','',splitinfo[1])
                            #print(splitinfo[1])
                            freqset.append(splitinfo[1])
                        genomeout = "/".join(genonewset)
                        freqout = "/".join(freqset)
                    else:
                        genomeout = "none"
                        freqout = "none"
                    out = line + "\t" + vcfinfo + "\t" + genomeout + "\t" + freqout + "\n"
                    with open('rsid_and_genome_type_temp_file.txt', 'a', encoding='utf-8') as wg:
                        wg.write(str(out))
                        print(line, "\n", vcfinfo, "\n", genomeout, "\n", freqout)
                else:
                    vcfinfo,genomeout,freqout=mfid.split('\t')

                out = line + "\t" + vcfinfo + "\t" + genomeout + "\t" + freqout + "\n"
                with open(fileout, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))
            else:
                out = line+ "\t"+ "."+"\t"+ "."+"\t"+ "."+"\n"
                with open(fileout, 'a', encoding='utf-8')as ww:
                    ww.write(str(out))


readandwriters(filein,fileout)