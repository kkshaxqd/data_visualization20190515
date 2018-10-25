# !/usr/bin/env python
# -*- coding: utf8 -*-
# need ChromeDriver v2.37 for Chrome 64
import os , re
import time,random
from bs4 import BeautifulSoup  # 引入beautifulsoup 解析html事半功倍
from urllib import request
import chromedriver_binary  # Adds chromedriver binary to path 这就可以自动打开网页了
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

def get_target_info(driver):
    #获取多个元素
    links = driver.find_elements_by_link_text('Target Info')
    targets = []
    index = len(links)
    for ig in range(index):
        #print(link)
        driver.implicitly_wait(5)
        links = driver.find_elements_by_link_text('Target Info')
        if ig <= index:
            links[ig].click()
            gene = driver.find_element_by_class_name("target__field-gene-name").text
            targets.append(gene)
            driver.implicitly_wait(5)
            driver.back()  # 控制回退
    return targets

## 数组去重
def quchong(shuzu):
    conteng = list(set(shuzu))
    conteng.sort(key=shuzu.index)
    return conteng

def get_target_wenxian(driver):
    references = driver.find_elements_by_class_name('ref-row')  #可以串联的逐层定位，连续两个find
    #print(references)
    refs = []
    index = len(references)
    for ig in range(index):
        if ig <= index:
            refee = references[ig].text
            refee = re.sub("REF\s\d+","",refee).strip()
            refs.append(refee)
    refss = quchong(refs)
    return refss
    #print(references)




def get_drug_info_main(drug="Sorafenib"):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10) #隐式等待10秒
    driver.get('https://db.idrblab.org/ttd/')
    time.sleep(5)
    # 元素定位的方法
    # 找到输入框 #//*[@id="edit-search-api-fulltext"] #edit-search-api-fulltext //*[@id="edit-submit-home-search-api-drug"]
    driver.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/div/div[1]/div/div[1]/div/form[2]/table/tbody/tr[2]/td[1]/div/input').send_keys(drug)
    #"/html/body/div[1]/div/main/div[2]/div/div[1]/div/div[1]/div/form[2]/table/tbody/tr[2]/td[1]/div" 原来是少了个input标签才不行
    # 点击search一下
    driver.find_element_by_xpath('//*[@id="edit-submit-home-search-api-drug"]').click()
    time.sleep(5)
    #进入新的一页，点击Drug info
    #"/html/body/div[1]/div/main/div[2]/div/div/table/tbody/tr[4]/td[2]/span/a"
    driver.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/div/div/table/tbody/tr[4]/td[2]/span/a').click()
    ##获得文献信息
    try:
        references = get_target_wenxian(driver)
    except:
        references = "None"
    print(references)
    ##获得靶点信息
    try:
        targets = get_target_info(driver)
    except:
        targets = "None"
    print(targets)
    driver.quit()
    return targets,references

filin = "E:\\haxqd\\201810\\drugtargetinfo.txt"
fileout = "E:\\haxqd\\201810\\drugtargetinfo_add_target_and_other_info.txt"


def write_result_step(line):
    targets, references = get_drug_info_main(line)
    if targets == "None":
        with open(fileout, "a", encoding='utf-8')as ww:
            out = line + "\t" + targets + "\t" + references + "\n"
            ww.write(str(out))
    else:
        for ig in range(len(targets)):
            with open(fileout, "a", encoding='utf-8')as ww:
                out = line + "\t" + targets[ig] + "\t" + references[ig] + "\n"
                ww.write(str(out))

def main():
    with open(filin,"r",encoding='utf-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            if re.search(r"Drugname",line):
                with open(fileout,"w",encoding='utf-8')as ww:
                    out = line+"\t"+r"TARGET_GENE"+"\t"+r"支持文献"+"\n"
                    ww.write(str(out))
            else:
                try:
                    write_result_step(line)
                except:
                    references = "None drug records"
                    targets = "None drug records"
                    with open(fileout, "a", encoding='utf-8')as ww:
                        out = line + "\t" + targets + "\t" + references + "\n"
                        ww.write(str(out))






if __name__ == "__main__":
    main()




def not_use(driver):
    js = 'window.open(link);'
    print(js)
    driver.execute_script(js)  # 在新标签页中打开
    chandel = driver.current_window_handle
    print(chandel)  # 输出当前窗口句柄（百度）
    handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
    print(handles)  # 输出句柄集合
    driver.switch_to.window(handles[1])  # 切换句柄切换到新打开的窗口
    """处理..."""
    driver.switch_to.window(handles[0])