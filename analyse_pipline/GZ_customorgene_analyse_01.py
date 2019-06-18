# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
#   读入基因型数据，根据数据库中的记录，计算相应的风险
#   首先要把记载的项目和风险型编号入座
#   疾病篇癌症部分的模型

# 定义基因型变形组字典
bianxingzu = {
    "AA":"TT",
    "TT":"AA",
    "CC":"GG",
    "GG":"CC",
    "AT":"TA",
    "AC":"CA",
    "AG":"GA",
    "TA":"AT",
    "TC":"CT",
    "TG":"GT",
    "CA":"AC",
    "CT":"TC",
    "CG":"GC",
    "GA":"AG",
    "GT":"TG",
    "GC":"CG"
}
import xlrd
fileshujuku = "xiaofeizhe_risk_project_data.xlsx"
# 读取样本基因型
filein = "23芯片检测结果输入文件.txt"
samplename = "23芯片检测结果输入文件"
sex = "woman"
fileout = "sampleresult1.txt"
def chuli_databasefile(fileshujuku):
    database_info = {}
    wb = xlrd.open_workbook(fileshujuku)
    sh1 = wb.sheet_by_index(0)
    # 递归显示每行数据
    for rownum in range(sh1.nrows):
        #print(sh1.row_values(rownum))  # 每一行的数据以数组形式存储
        hanglist = sh1.row_values(rownum)
        flag = hanglist[2]+"@"+hanglist[3]
        info = "@".join(hanglist[5:9])
        if "Synonyms" in hanglist[12]:
            refgh = re.findall(r"Synonyms:(\w)\/\w",hanglist[12])
            refgene =  refgh[0]+refgh[0]
        elif "rs" in hanglist[12]:
            refgh = re.findall(r'\d+:\d+:rs\d+:(\w)',hanglist[12])  #13:24205195:rs9510787:A:G
            refgene = refgh[0] + refgh[0]
        else:
            refgene = "VCFinfo"
        database_info[flag] = info+"@"+hanglist[4]+"@"+hanglist[11]+"@"+refgene+"@"+hanglist[13]  #增加基因型和位点编号 v20190213;增加参考基因型 v20190222；增加位点说明 ,v20190318
    return database_info
# 所有项目基本数据字典
biyanaibase_info = {} #鼻咽癌
biyanairesult = {}
biyanairsset = ["rs9510787","rs29232","rs2736098","rs402710","rs2279744","rs6774494","rs2228000","rs1412829"]
dachangai_info = {} #大肠癌
dachangairesult = {}
dachangairsset = ["rs1801131","rs1665650","rs6983267","rs704017","rs10774214","rs647161","rs266729","rs4143094","rs12953717","rs4464148","rs4939827","rs719725","rs4779584","rs10411210","rs2306536","rs3735684"]
jiezhichangai_info = {} #结直肠癌
jiezhichangresult = {}
jiezhichangrsset = ["rs1042522","rs78378222","rs10849432","rs6687758","rs6983267"]
feiai_info = {} #肺癌
feiairesult = {}
feiairsset = ["rs1799793","rs2352028","rs2464196","rs1169300","rs2293347","rs763317","rs11614913","rs17576","rs12050604","rs2228001","rs3117582","rs663048","rs748404","rs1051730","rs8034191","rs16969968","rs1042522","rs2078486"]
jiazhuangxian_info = {} #甲状腺癌
jiazhuangxianresult = {}
jiazhuangxianrsset = ["rs2439302","rs966423","rs965513","rs944289","rs1867277"]
pangguangai_info = {} #膀胱癌
pangguangairesult = {}
pangguangairsset = ["rs1136410","rs11892031","rs7238033","rs401681","rs9642880","rs5275","rs760805","rs798766"]
shenai_info = {} #肾癌
shenairesult = {}
shenairsset = ["rs7105934","rs699947","rs3025039","rs2279744","rs1049380"]
shiguanai_info = {} #食管癌
shiguanairesult = {}
shiguanairsset = ["rs1695","rs1041981","rs2274223","rs2074356","rs1050631","rs204900","rs130079","rs1789924","rs78378222"]
ganai_info = {} #肝癌
ganairesult = {}
ganairsset = ["rs9288516","rs689466","rs1051740","rs1042522","rs1800566"]
weiai_info = {} #胃癌
weiairesult = {}
weiairsset = ["rs1801394","rs17109928","rs2294008","rs2976392","rs13361707","rs9841504","rs4072037"]
yixianai_info = {} #胰腺癌
yixianairesult = {}
yixianairsset = ["rs2736098","rs17688601","rs6971499","rs1561927","rs9581943","rs7190458","rs7214041","rs16986825","rs505922","rs9543325","rs3790844","rs1042522"]
ruxianai_info = {} #散发性乳腺癌
ruxianairesult = {}
ruxianairsset = ["rs1801131","rs1801133","rs2066853","rs1042522","rs1045485","rs10754339","rs3738414","rs11200014","rs3750817","rs1126497","rs12248560","rs1434536","rs1800058","rs4986761"]
neimoai_info = {} #子宫内膜癌
neimoairesult = {}
neimoairsset = ["rs1042522","rs3184504","rs4633","rs9340799","rs34330","rs4680"]
luanchaoai_info = {} #卵巢癌
luanchaoairesult = {}
luanchaoairsset = ["rs2072590","rs2665390","rs10088218","rs9303542","rs2295190","rs2854344","rs1042838","rs608995","rs523349","rs3218536","rs3814113","rs10069690","rs2736100","rs7726159","rs3814113","rs1801131"]
gongjingai_info = {} #宫颈癌
gongjingairesult = {}
gongjingairsset = ["rs1799929","rs9230","rs750749","rs9370729","rs13117307","rs8067378","rs4282438"]
qianliexianai_info = {} #前列腺癌
qianliexianairesult = {}
qianliexianairsset = ["rs1695","rs16260","rs351855","rs78378222","rs2011077","rs339331","rs731236","rs1056836","rs1544410","rs1983891","rs721048","rs4430796","rs10993994"]

def cancer_type(type,hang,value,dict):
    if type in hang:
        print("开始处理",hang)
        ddelcont = type+"@"
        hang = re.sub(ddelcont,"",hang)
        valuesplit = value.split('@')
        genetypesplit = valuesplit[0].split('/')
        valuesplit[1] = re.sub("\(\d+\)","",valuesplit[1])
        genefreqsplit = valuesplit[1].split('/')
        generisksplit = valuesplit[2].split('/')
        geneorsplit = valuesplit[3].split('/')
        # 计算MOR 修正OR值，MOR = ORref*refFRQ% + ORhet*hetFRQ% + ORhom*homFRQ%   OR* = OR/MOR
        MOR = float(geneorsplit[0])*float(genefreqsplit[0]) + \
              float(geneorsplit[1])*float(genefreqsplit[1]) + \
              float(geneorsplit[2])*float(genefreqsplit[2])
        gene_ornew = [0]*3
        gene_ornew[0] = str(round(float(geneorsplit[0])/MOR,3))
        gene_ornew[1] = str(round(float(geneorsplit[1])/MOR,3))
        gene_ornew[2] = str(round(float(geneorsplit[2])/MOR,3))

        ornewvalue = "/".join(gene_ornew)  #数字不能直接这样转化为字符串
        print(hang,valuesplit[0],valuesplit[1],"新OR",ornewvalue,valuesplit[2])
        if "all" in valuesplit[0]:
            valuesplit[0] = re.sub("all/","",valuesplit[0])
        dict[hang] = valuesplit[0] + "@" + valuesplit[1] + "@" + valuesplit[3] + "@" + \
                     valuesplit[2] +"@"+valuesplit[-4]+"@"+valuesplit[-3]+"@"+valuesplit[-2]+"@"+valuesplit[-1]  #增加基因型和位点编号 v20190213;增加参考基因型 v20190222；增加位点说明，用原来的or吧还是 v20190318

def getxiangmuresult(linelist,resultdict,rsset):
    for i in range(len(rsset)):
        if linelist[0] == rsset[i]:
            resultdict[rsset[i]] = linelist[3]

def readbiyanai(filein,sex):
    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if "#" in line:
                pass
            else:
                line = line.strip('\n')
                linelist = line.split('\t')
                getxiangmuresult(linelist,biyanairesult,biyanairsset) # 鼻咽癌
                getxiangmuresult(linelist, dachangairesult, dachangairsset) # 大肠癌
                getxiangmuresult(linelist, jiezhichangresult, jiezhichangrsset) # 结直肠癌
                getxiangmuresult(linelist, feiairesult, feiairsset)  # 肺癌
                getxiangmuresult(linelist, jiazhuangxianresult, jiazhuangxianrsset)  # 甲状腺癌
                getxiangmuresult(linelist, pangguangairesult, pangguangairsset)  # 膀胱癌
                getxiangmuresult(linelist, shenairesult, shenairsset) #肾癌
                getxiangmuresult(linelist, shiguanairesult, shiguanairsset)  # 食管癌
                getxiangmuresult(linelist, ganairesult, ganairsset)  # 肝癌
                getxiangmuresult(linelist, weiairesult, weiairsset)  # 胃癌
                getxiangmuresult(linelist, yixianairesult, yixianairsset)  # 胰腺癌
                if sex == "woman":
                    getxiangmuresult(linelist, ruxianairesult, ruxianairsset) # 散发性乳腺癌
                    getxiangmuresult(linelist, neimoairesult, neimoairsset)  # 子宫内膜癌
                    getxiangmuresult(linelist, luanchaoairesult, luanchaoairsset)  # 卵巢癌
                    getxiangmuresult(linelist, gongjingairesult, gongjingairsset)  # 宫颈癌
                elif sex == "man":
                    getxiangmuresult(linelist, qianliexianairesult, qianliexianairsset)  # 前列腺癌

def comparegenetype(result_dict,baseinfo_dict,rsid,type):
    rsid_split = baseinfo_dict[rsid].split('@')
    rsid_gene = rsid_split[0].split('/')
    for i in range(len(rsid_gene)):
        if result_dict[rsid] == rsid_gene[i]:
            needi = i
            break
        elif bianxingzu[result_dict[rsid]]== rsid_gene[i]:
            needi = i
    rsid_freq = rsid_split[1].split('/')
    rsid_or = rsid_split[2].split('/')
    risk_value = float(rsid_or[needi])
    if  risk_value < 0.9:
        risk = "该位点降低风险"
    elif risk_value>=0.9 and risk_value<=1.1:
        risk = "该位点正常风险"
    elif risk_value >1.1:
        risk = "该位点提高风险"
    #print(rsid_split[-1])
    if "基因型为" in rsid_split[-1] :
        xxtype = re.search('基因型为(\w\w)', rsid_split[-1]).group(1)
        if xxtype == result_dict[rsid]:
            sitecontent = rsid_split[-1]
        else:
            sitecontent = "该基因型下位点作用正常"
    elif "基因型有" in rsid_split[-1]:
        xtype = re.search('基因型有(\w)', rsid_split[-1]).group(1)
        if xtype in result_dict[rsid]:
            sitecontent = rsid_split[-1]
        else:
            sitecontent = "该基因型下位点作用正常"
    else:
        sitecontent = "位点说明"
    ##写下新or
    '''
    with open('rsnewor.txt','a', encoding='utf-8')as hh:
        outhh = type + "\t" + rsid +  "\t" +rsid_split[2]+ "\n"
        hh.write(str(outhh))
    '''
    print(rsid,result_dict[rsid],rsid_split[-4],rsid_freq[needi],rsid_or[needi],risk,sitecontent)
    out = type + "\t" + rsid + "\t" + rsid_split[-2] + "\t" + result_dict[rsid] + "\t" + rsid_split[-4] + "\t" \
          + rsid_split[-3] + "\t" + rsid_or[needi] + "\t" + risk + "\t" + sitecontent + "\n"
    with open(fileout, 'a', encoding='utf-8')as ww:
        ww.write(str(out))
    return rsid_freq[needi],rsid_or[needi]

def chuli_show_xiangmu(resultdict,base_infodict,type):
    riskfactor = 1
    orresult = []
    for key in resultdict.keys():
        key_freq,key_or = comparegenetype(resultdict, base_infodict,key,type)
        orresult.append(float(key_or))
        riskfactor = round(riskfactor*float(key_or),3)
    risk_num = 0
    risk_good = 0
    for j in orresult:
        if j>1.1:
            risk_num +=1
        if j<0.9:
            risk_good +=1
    if  riskfactor < 0.9 and risk_good > risk_num :
        riskrsult = "低风险"
    elif riskfactor>=0.9 and riskfactor<=1.1:
        riskrsult = "正常风险"
    elif riskfactor >1.1 and risk_num >= risk_good+1:
        riskrsult = "高风险"
    else:
        riskrsult = "正常风险"
    outc1 = type+"项目总体风险值："
    outc2 = "您的"+type+"风险结果为："
    outc3 = "您的" + type + "风险结果"
    print(outc1,riskfactor)
    print(outc2,riskrsult)
    out = outc3 +"\t"+ ".\t" + ".\t"+ ".\t" + ".\t" + ".\t" +str(riskfactor) + "\t" + riskrsult + ".\t" +"\n"
    with open(fileout, 'a', encoding='utf-8')as ww:
        ww.write(str(out))


def main(fileshujuku,sex):
    database_info = chuli_databasefile(fileshujuku)
    for key,value in database_info.items():
        #得到基础信息字典
        cancer_type("鼻咽癌",key,value,biyanaibase_info)
        cancer_type("大肠癌",key,value,dachangai_info)
        cancer_type("结直肠癌",key,value,jiezhichangai_info)
        cancer_type("肺癌", key, value, feiai_info)
        cancer_type("甲状腺癌", key, value, jiazhuangxian_info)
        cancer_type("膀胱癌", key, value, pangguangai_info)
        cancer_type("肾癌", key, value, shenai_info)
        cancer_type("食管癌", key, value, shiguanai_info)
        cancer_type("肝癌", key, value, ganai_info)
        cancer_type("胃癌", key, value, weiai_info)
        cancer_type("胰腺癌", key, value, yixianai_info)
        if sex == "woman":
            cancer_type("散发性乳腺癌", key, value, ruxianai_info)
            cancer_type("子宫内膜癌", key, value, neimoai_info)
            cancer_type("卵巢癌", key, value, luanchaoai_info)
            cancer_type("宫颈癌", key, value, gongjingai_info)
        elif sex == "man":
            cancer_type("前列腺癌", key, value, qianliexianai_info)
    #得到基因型结果字典
    readbiyanai(filein,sex)
    #比较呈现癌结果并输出
    out = samplename+"\t" + "疾病篇\t" + "参考基因型\t"+ "基因型\t" + "基因\t" + "位点编号ID\t"+"新风险值\t"+"风险结果\t" + "位点说明"+"\n"
    with open(fileout, 'w', encoding='utf-8')as ww:
        ww.write(str(out))
    #写下新or
    '''
    outhh =  "检测项目\t" + "位点\t" +  "新or\n"
    with open('rsnewor.txt', 'w', encoding='utf-8')as hh:
        hh.write(str(outhh))
    '''
    chuli_show_xiangmu(biyanairesult,biyanaibase_info,"鼻咽癌")
    chuli_show_xiangmu(dachangairesult, dachangai_info, "大肠癌")
    chuli_show_xiangmu(jiezhichangresult, jiezhichangai_info, "结直肠癌")
    chuli_show_xiangmu(feiairesult, feiai_info, "肺癌")
    chuli_show_xiangmu(jiazhuangxianresult, jiazhuangxian_info, "甲状腺癌")
    chuli_show_xiangmu(pangguangairesult, pangguangai_info, "膀胱癌")
    chuli_show_xiangmu(shenairesult, shenai_info, "肾癌")
    chuli_show_xiangmu(shiguanairesult, shiguanai_info, "食管癌")
    chuli_show_xiangmu(ganairesult, ganai_info, "肝癌")
    chuli_show_xiangmu(weiairesult, weiai_info, "胃癌")
    chuli_show_xiangmu(yixianairesult, yixianai_info, "胰腺癌")
    if sex == "woman":
        chuli_show_xiangmu(ruxianairesult, ruxianai_info, "散发性乳腺癌")
        chuli_show_xiangmu(neimoairesult, neimoai_info, "子宫内膜癌")
        chuli_show_xiangmu(luanchaoairesult, luanchaoai_info, "卵巢癌")
        chuli_show_xiangmu(gongjingairesult, gongjingai_info, "宫颈癌")
    elif sex == "man":
        chuli_show_xiangmu(qianliexianairesult, qianliexianai_info, "前列腺癌")


main(fileshujuku,sex)