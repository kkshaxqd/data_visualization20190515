# !/usr/bin/env python
# -*- coding: utf8 -*-

import os,re,sys

filein = 'E:\\haxqd\\201810\\drugtargetinfo.txt'

fileout = 'E:\\haxqd\\201810\\drugtargetinfo_add_target_and_other_info.txt'

fileoutout2 = 'E:\\haxqd\\201810\\drugtargetinfo_add_target_and_other_info_add_region.txt'

import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def quchong(shuzu):
    conteng = list(set(shuzu))
    conteng.sort(key=shuzu.index)
    return conteng

def get_target_info(driver):
    #获取多个元素
    wait = WebDriverWait(driver, 10)
    #element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'Target Info')))
    links = driver.find_elements_by_link_text('Target Info')
    print(links)
    if links:
        targets = []
        index = len(links)
        for ig in range(index):
            #print(links)
            links = driver.find_elements_by_link_text('Target Info')
            if ig <= index:
                links[ig].click()
                try:
                    gene = driver.find_element_by_class_name("target__field-gene-name").text
                except:
                    gene = driver.find_element_by_class_name('target__name').text
                targets.append(gene)
                #driver.implicitly_wait(5)
                driver.back()  # 控制回退
    else:
        targets = "."
    return targets


def get_target_wenxian(driver):
    wait = WebDriverWait(driver, 10)
    #element = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'ref-row ref-row-processed')))
    references = driver.find_elements_by_class_name('ref-row')  #可以串联的逐层定位，连续两个find
    print(references)
    if references:
        refs = []
        index = len(references)
        for ig in range(index):
            if ig <= index:
                refee = references[ig].text
                refee = re.sub("REF\s\d+","",refee).strip()
                refs.append(refee)
        refss = quchong(refs)
    else:
        refss = '.'
    return refss

def get_target_from_ttd(drug):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options) #
    driver.implicitly_wait(5) #隐式等待10秒
    driver.get('https://db.idrblab.org/ttd/')
    driver.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/div/div[1]/div/div[1]/div/form[2]/table/tbody/tr[2]/td[1]/div/input').send_keys(drug)
    #"/html/body/div[1]/div/main/div[2]/div/div[1]/div/div[1]/div/form[2]/table/tbody/tr[2]/td[1]/div" 原来是少了个input标签才不行
    # 点击search一下
    driver.find_element_by_xpath('//*[@id="edit-submit-home-search-api-drug"]').click()
    driver.implicitly_wait(5) #隐式等待10秒
    #进入新的一页，点击Drug info
    #"/html/body/div[1]/div/main/div[2]/div/div/table/tbody/tr[4]/td[2]/span/a"
    try:
        driver.find_element_by_link_text('Drug Info').click()
        driver.implicitly_wait(5)
        targets = get_target_info(driver)
        references = get_target_wenxian(driver)
    except:
        references = '.'
        targets = '.'
    print(targets,references)
    driver.quit()
    return targets,references

def getfromtemp(drugname):
    with open('drug_target_temp_file.txt', 'r', encoding='utf-8') as f:
        target = 'none'
        references = 'none'
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            linelist = line.split('\t')
            if drugname == linelist[0]:
                target =  linelist[1]
                references = linelist[2]
    return target,references


def main():
    with open(filein,'r',encoding='utf-8')as f:
        lines = f.readlines()
        #创建临时文件
        if os.path.exists('drug_target_temp_file.txt'):
            pass
        else:
            with open('drug_target_temp_file.txt', 'w', encoding='utf-8')as gg:
                outss = "Drug" + "\t" + "targets" + "\n"
                gg.write(str(outss))

        hang = lines[0]
        with open(fileout, 'w', encoding='utf-8')as ww:
            ww.write(str(hang))

        for line in lines[1:]:
            line = line.strip('\n')
            linelist = line.split('\t')
            drugname = linelist[0].strip()
            target = linelist[3]
            #if target == "." or not target :
            targetout, referencesout = getfromtemp(drugname)
            if targetout == "none":
                targets, references = get_target_from_ttd(drugname)

                targetout = ';'.join(targets)
                referencesout = ';'.join(references)

                with open('drug_target_temp_file.txt', 'a', encoding='utf-8') as wg:
                    outs = drugname + "\t" + targetout + "\t" + referencesout + "\n"
                    wg.write(str(outs))
            #else:
                #targetout = linelist[3]
                #referencesout = linelist[5]
            out = '\t'.join(linelist[0:3])+"\t"+targetout+"\t"+linelist[4]+"\t"+referencesout+"\n"
            print(out)
            with open(fileout, 'a', encoding='utf-8')as ww:
                ww.write(str(out))

addfile = r"E:\\haxqd\\myscript\\mydatabase\\04_WES.uniq.bed"
adddict = {}
geneflag = {}
with open(addfile,'r',encoding='utf-8')as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        info = line.split('\t')
        #print(info[3])
        try:
            if adddict[info[3]] and geneflag[info[3]]:
                geneflag[info[3]] = geneflag[info[3]]+1
                adddict[info[3]] = adddict[info[3]]+","+info[1]+".."+info[2]+"..exon"+str(geneflag[info[3]])
        except KeyError:
            geneflag[info[3]]=1
            adddict[info[3]] = info[0]+":"+info[1]+".."+info[2]+"..exon"+str(geneflag[info[3]])
def get_exon_by_gene(gene="KIT"):
    region = gene+"("+adddict[gene]+")"
    return region


def main2():
    #给上一步main的结果增加region的注释
    with open(fileout,'r',encoding='utf-8')as g:
        lines = g.readlines()
        hang = lines[0]
        with open(fileoutout2, 'w', encoding='utf-8')as ww:
            ww.write(str(hang))

        for line in lines[1:]:
            line = line.strip('\n')
            info = line.split('\t')

            if info[3] and info[3] != ".":
                if ";" in info[3]:
                    genesplit = info[3].split(';')
                    out = ""
                    for gene in genesplit:
                        try:
                            region = get_exon_by_gene(gene.strip())
                        except:
                            region = gene.strip()+"(.)"
                        out = out+" ; "+region
                    out = re.sub(r'^ ; ','',out)
                    with open(fileoutout2, 'a', encoding='utf-8')as ww:
                        outline = '\t'.join(info[0:4])+"\t"+out+"\t"+info[5]+"\n"
                        ww.write(str(outline))
                else:
                    try:
                        region = get_exon_by_gene(info[3].strip())
                    except:
                        region = info[3].strip() + "(.)"
                    out = region
                    with open(fileoutout2, 'a', encoding='utf-8')as ww:
                        outline = '\t'.join(info[0:4])+"\t"+out+"\t"+info[5]+"\n"
                        ww.write(str(outline))
            else:
                with open(fileoutout2, 'a', encoding='utf-8')as ww:
                    outline = '\t'.join(info[0:6]) + "\t"+ "." +"\n"
                    ww.write(str(outline))







if __name__ == "__main__":
    #main()
    main2()
    #get_target_from_ttd("ABT-751")





