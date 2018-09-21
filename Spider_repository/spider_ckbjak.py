# !/usr/bin/env python
# -*- coding: utf8 -*-
# need ChromeDriver v2.37 for Chrome 64
import os , re
import time,random
from bs4 import BeautifulSoup  # 引入beautifulsoup 解析html事半功倍
from urllib import request
import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
# 防止被断掉连接
import socket
timeout = 20
socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置

#https://ckb.jax.org/

# 该网站有的全部基因列表  https://ckb.jax.org/gene/grid
def get_gene_list():
    #driver = webdriver.Chrome()
    #driver.get('https://ckb.jax.org/gene/grid')
    url = 'https://ckb.jax.org/gene/grid'
    page = request.Request(url)
    page_info = request.urlopen(page).read().decode('utf-8', 'ignore')
    time.sleep(2)
    soup = BeautifulSoup(page_info, 'lxml')
    #dataresuoure = soup.prettify()
    #获取基因
    genes = soup.find_all(attrs={"class":"btn btn-default btn-gene btn-block"})
    #print(genes)
    #获取geneId
    #entrid = genes.select('href')
    conout = "GENE\tENTRID"
    for gene in genes:
        #  这段代码最重要的是理解bs中gene["href"] 和find_all，select的作用
        #  find_all后获得的hxml，class或href属性本身指的内容，可以通过调用属性字典来获取
        entrid = gene["href"].replace("/gene/show?geneId=","").strip()
        gene = gene.get_text().strip()
        print(gene,":",entrid)
        conout = conout+"\n"+gene+"\t"+entrid
    return conout


def get_gene_text():
    content = get_gene_list()
    with open("ckb_jak_gene.txt", 'w', encoding='utf-8')as ww:
        out = content
        ww.write(str(out))

def zhunbei_file():
    with open("CKB_JAK_GENE_VARIANT_INFO.txt", 'w', encoding='utf-8')as ww:
        out1 = "GENE"+"\t"+"Synonyms"+"\t"+"EntrezId"+"\t"+"MapLocation"+"\t"+"NMID"
        out2 = "Variant"+"\t"+"Impact"+"\t"+"ProteinEffect"+"\t"+"VariantDescription"
        out = out1+"\t"+out2+"\n"
        ww.write(str(out))
    with open("CKB_JAK_VARIANT_CLINCLIN_INFO.txt", 'w', encoding='utf-8')as ff:
        out1 = "GENE"+"\t"+"Synonyms"+"\t"+"EntrezId"+"\t"+"MapLocation"+"\t"+"NMID"
        out2 = "Variant" + "\t" + "TumorType" + "\t" + "ResponseType" + "\t" + "TherapyName"
        out3 = "ApprovalStatus" + "\t" + "EvidenceType" + "\t" + "EfficacyEvidence"+ "\t" + "References"
        out = out1 + "\t" + out2 + "\t"+out3+"\n"
        ff.write(str(out))

def write_gene_vairant_txt(content):
    with open("CKB_JAK_GENE_VARIANT_INFO.txt", 'a', encoding='utf-8')as ww:
        out = content
        ww.write(str(out))

def write_variant_clin_txt(content):
    with open("CKB_JAK_VARIANT_CLINCLIN_INFO.txt", 'a', encoding='utf-8')as ff:
        out = content
        ff.write(str(out))

def get_gene_base(soup):
    ##获得gene base信息
    genebase_list = []  # 结构: [dict1, dict2, ...]
    geneinfo = soup.find_all(attrs={"class":"table table-striped table-hover"})
    #print(type(geneinfo))
    for idx, info in enumerate(geneinfo[0].find_all('tr')):
        # print(idx,":",info)
        cont = info.find_all('td')
        try:
            title = cont[0].getText().strip()
            coninfo = cont[1].getText().strip()
        except IndexError:
            continue
        else:
            # print(title,":",coninfo)
            if title == "Gene Symbol":
                genebase_list.append({title: coninfo})
            elif title == "Synonyms":
                genebase_list.append({title: coninfo})
            elif title == "Map Location":
                genebase_list.append({title: coninfo})
            elif title == "Canonical Transcript":
                genebase_list.append({title: coninfo})
    print(r"获得的基因基本信息是：",genebase_list)
    return genebase_list

def get_and_out_variant_info(genebase_list,soup):
    ##获得variant 信息
    variantinfo = soup.find_all(attrs={"class":"table table-bordered table-hover table-striped basicDataTable gene_variant_tab_table"})
    # bs4获取表格数据更好用的getText()
    #print(type(variantinfo))
    for idx, info in enumerate(variantinfo[0].find_all('tr')):
        if idx != 0:
            cont = info.find_all('td')
            variant = cont[0].getText().strip()
            vartype = cont[1].getText().strip()
            proteffect = cont[2].getText().strip()
            variantdes = cont[3].getText().strip()
            geneinfo = genebase_list[0]["Gene Symbol"]+"\t"+genebase_list[1]["Synonyms"]+"\t"+genebase_list[2]["Map Location"]+"\t"+genebase_list[3]["Canonical Transcript"]
            content = geneinfo+"\t"+variant+"\t"+vartype+"\t"+proteffect+"\t"+variantdes+"\n"
            write_gene_vairant_txt(content)

def get_and_out_variant_clin_info(genebase_list,soup):
    ##获得clin 临床证据信息
    clininfo = soup.find_all(attrs={
        "class": "table table-bordered table-hover table-striped basicDataTable profile-response-table-without-treatment-approach"})
    # clininfo变量包含一个数组。你需要调用find_all在它的成员上(即使你知道它是一个只有一个成员的数组)，而不是整个事情,所以clininfo[0]就对了，直接clininfo反而不能用find_all。
    #print(clininfo)
    for idx,row in enumerate(clininfo[0].find_all('tr')):
        #print(row)
        if idx != 0:
            cont = row.find_all('td')
            variant = cont[0].getText().strip()
            tumortype = cont[1].getText().strip()
            responsetype = cont[2].getText().strip()
            therapyname = cont[3].getText().strip()
            approvalstatus = cont[4].getText().strip()
            evidencetype = cont[5].getText().strip()
            references = cont[6].getText().strip()
            geneinfo = genebase_list[0]["Gene Symbol"]+"\t"+genebase_list[1]["Synonyms"]+"\t"+genebase_list[2]["Map Location"]+"\t"+genebase_list[3]["Canonical Transcript"]
            content = geneinfo+"\t"+variant+"\t"+tumortype+"\t"+responsetype+"\t"+therapyname+"\t"+approvalstatus+"\t"+evidencetype+"\t"+references+"\n"
            #print(content)
            write_variant_clin_txt(content)

def get_gene_info(geneid=207):
    url = "https://ckb.jax.org/gene/show?geneId="+str(geneid)
    time.sleep(random.randint(5, 10))
    page = request.Request(url)
    page = request.urlopen(page)
    page_info = page.read().decode('utf-8', 'ignore')
    page.close()  # 记得要关闭
    time.sleep(random.randint(5,10))
    soup = BeautifulSoup(page_info, 'html5lib') #html5lib是最标准的HTML分析格式，比lxml完美解决不标准格式问题
    #dataresuoure = soup.prettify()
    genebase_list = get_gene_base(soup) ##获得gene base信息
    get_and_out_variant_info(genebase_list,soup) ##获得并输出variant 信息
    time.sleep(random.randint(5,9))
    get_and_out_variant_clin_info(genebase_list,soup) ##获得并输出clin 信息
    time.sleep(random.randint(3,5))


def spider_by_geneid():
    #读取基因id，以这个作为标签读网页处理
    with open("ckb_jak_gene.txt", 'r', encoding='utf-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            info = line.split('\t')
            try:
                if havegenename[info[0]]:
                    continue
            except KeyError:
                    geneid = info[1]
                    print(r"开始处理基因：", info[0])
                    get_gene_info(geneid)


if __name__ == "__main__":
    # get_gene_info()
    #zhunbei_file()
    havegenename = {}
    with open("CKB_JAK_GENE_VARIANT_INFO.txt", 'r', encoding='utf-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            info = line.split('\t')
            havegenename[info[0]]=1
    spider_by_geneid()
