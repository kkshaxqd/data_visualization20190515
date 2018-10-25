# !/usr/bin/env python
# -*- coding: utf8 -*-

import os,re,sys

filein = 'E:\\haxqd\\201810\\drugname.txt'

fileout = 'E:\\haxqd\\201810\\drugname.txt_add_fda_approve_disease.txt'

import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By




def get_fdacncer_by_drug(drug):
    disease= ""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options) #
    driver.implicitly_wait(5) #隐式等待10秒
    driver.get('https://www.drugs.com/')
    driver.find_element_by_xpath('//*[@id="livesearch-main"]').send_keys(drug)
    driver.find_element_by_xpath('/html/body/div[1]/div/header/div/div/div/form/div[1]/span[2]/button').click()
    driver.find_element_by_partial_link_text('Drug Interactions').click()
    #havemoredis = re.search(r'\+.*more',pageSource)
    #if havemoredis:
        #driver.find_element_by_partial_link_text(' more').click()
    pageSource = driver.page_source
    #print(pageSource)
    content01 = re.findall(r'data-condition_id=\"\d+\">(\D+)</a></li>',pageSource)
    contentfix = re.findall(r'data-condition_id=\'\d+\'&gt;(\D+)?&lt;\\/a&gt;&lt;\\/li&gt;',pageSource)
    content01.extend(contentfix)
    result = ';'.join(content01)
    driver.close()
    print(result)
    return result

    #print(pageSource)

#get_fdacncer_by_drug('Everolimus')

def get_study_drug_by_NCT(nctid):
    outdisease = ""
    outphase = ""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options) #
    driver.implicitly_wait(5) #隐式等待10秒
    #wait = WebDriverWait(driver, 40)
    #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#footer-menu > ul')))
    driver.get("https://ClinicalTrials.gov/show/"+nctid)
    driver.implicitly_wait(5)
    diseases = driver.find_elements_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td[1]/span')
    for disease in diseases:
        diseaseinfo = disease.text
        outdisease = outdisease+";"+diseaseinfo
    outdisease = re.sub(r"^;",'',outdisease)
    phases = driver.find_elements_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td[3]/span')
    for phase in phases:
        phaseinfo = phase.text
        outphase = outphase+"|"+phaseinfo
    outphase = re.sub(r'^\|','',outphase)
    driver.close()
    outall = nctid+":"+outphase+":"+outdisease
    print(outall)
    return outall


#get_study_drug_by_NCT('NCT02465060')
def getnctcancer(nctid):
    with open('nct_study_cancer_temp_file.txt', 'r', encoding='utf-8') as f:
        studycncer = 'none'
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            linelist = line.split('\t')
            if nctid == linelist[0]:
                studycncer =  linelist[1]
    return studycncer


def getdrugnamenotrunmany(drugname):
    with open('drug_fda_cancer_temp_file.txt', 'r', encoding='utf-8') as f:
        fdacncer = 'none'
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            linelist = line.split('\t')
            if drugname == linelist[0]:
                fdacncer =  linelist[1]
    return fdacncer

def main():
    with open(filein,'r',encoding='utf-8')as f:
        lines = f.readlines()
        #创建临时文件
        if os.path.exists('drug_fda_cancer_temp_file.txt'):
            pass
        else:
            with open('drug_fda_cancer_temp_file.txt', 'w', encoding='utf-8')as gg:
                outss = "Drug" + "\t" + "FDACANCER" + "\n"
                gg.write(str(outss))
        # 创建临时文件
        if os.path.exists('nct_study_cancer_temp_file.txt'):
            pass
        else:
            with open('nct_study_cancer_temp_file.txt', 'w', encoding='utf-8')as gg:
                outss = "NCTID" + "\t" + "nctstudycancer" + "\n"
                gg.write(str(outss))
        hang = lines[0].strip('\n')
        outlang = hang +"\t"+r"FDA批准"+"\t"+r"NCT在研"+"\n"
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(outlang))

        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            drugname = linelist[0]
            fdacncer = getdrugnamenotrunmany(drugname)
            if fdacncer == "none":
                try:
                    fdacncer = get_fdacncer_by_drug(drugname)
                except:
                    fdacncer = '.'

                with open('drug_fda_cancer_temp_file.txt', 'a', encoding='utf-8') as wg:
                    outs = drugname + "\t" + fdacncer + "\n"
                    wg.write(str(outs))
            nctsets = re.findall(r'(NCT\d+)', line)
            print(nctsets)
            if len(nctsets) == 0:
                outnct = '.'
            elif len(nctsets) == 1:
                nctsets = nctsets[0]
                #print(nctsets)  长度是1但里面是个元祖
                outnct = getnctcancer(nctsets)
                if outnct == "none":
                    try:
                        outnct = get_study_drug_by_NCT(nctsets)
                    except:
                        outnct = get_study_drug_by_NCT(nctsets)
                    with open('nct_study_cancer_temp_file.txt', 'a', encoding='utf-8') as ng:
                        outs = nctsets + '\t' + outnct + "\n"
                        ng.write(str(outs))
            elif len(nctsets)>1:
                outnct = ''
                for nctset in nctsets:
                    nctcancer = getnctcancer(nctset)
                    if nctcancer == "none":
                        try:
                            nctcancer = get_study_drug_by_NCT(nctset)
                        except:
                            nctcancer = get_study_drug_by_NCT(nctset)
                        with open('nct_study_cancer_temp_file.txt', 'a', encoding='utf-8') as ng:
                            outs = nctset + '\t' + nctcancer + "\n"
                            ng.write(str(outs))
                    outnct = outnct + " || " + nctcancer
                outnct = re.sub(r'^ \|\| ', '', outnct)

            out = line + "\t" + fdacncer + "\t" + outnct + "\n"
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(out))


if __name__ == "__main__":
    main()
    #get_study_drug_by_NCT('NCT02465060')