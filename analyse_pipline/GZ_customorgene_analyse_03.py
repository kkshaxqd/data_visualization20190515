# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
#   读入基因型数据，根据数据库中的记录，计算相应的风险
#   首先要把记载的项目和风险型编号入座
#   能力篇项目，能力篇项目与之前稍有不同，得单独进行，要给出相应结论，模型需要更复杂一些
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
fileout = "sampleresult2.txt"
def chuli_databasefile(fileshujuku):
    database_info = {}
    wb = xlrd.open_workbook(fileshujuku)
    sh1 = wb.sheet_by_index(2)
    # 递归显示每行数据
    for rownum in range(sh1.nrows):
        #print(sh1.row_values(rownum))  # 每一行的数据以数组形式存储
        hanglist = sh1.row_values(rownum)
        for i in range(len(hanglist)):
            hanglist[i]=str(hanglist[i])
        flag = hanglist[2]+"@"+hanglist[3]
        info = "@".join(hanglist[5:9])
        if "Synonyms" in hanglist[12]:
            refgh = re.findall(r"Synonyms:(\w)\/\w", hanglist[12])
            refgene = refgh[0] + refgh[0]
        elif "rs" in hanglist[12]:
            refgh = re.findall(r'\d+:\d+:rs\d+:(\w)', hanglist[12])  # 13:24205195:rs9510787:A:G
            refgene = refgh[0] + refgh[0]
        else:
            refgene = "VCFinfo"
        database_info[flag] = info + "@" + hanglist[4] + "@" + hanglist[
            11] + "@" + refgene  # 增加基因型和位点编号 v20190213;增加参考基因型 v20190222
    return database_info
# 所有项目基本数据字典
zwxshkh_info = {} #紫外线伤害抗衡能力
zwxshkhresult = {}
zwxshkhrsset = ["rs1799793","rs13181","rs322458","rs2228479","rs885479","rs12203592","rs6059655","rs10733310"]
dcfsshkh_info = {} #电磁辐射伤害抗衡能力
dcfsshkhresult = {}
dcfsshkhrsset = ["rs1799782","rs25487"]
whjshkh_info = {} #烷化剂伤害抗衡能力
whjshkhresult = {}
whjshkhrsset = ["rs1799782","rs25487","rs1136410"]
myxtbh_info = {} #免疫系统保护能力
myxtbhresult = {}
myxtbhrsset = ["rs16944","rs231775","rs1800629"]
xbzqhdwtk_info = {} #细胞周期和凋亡调控能力
xbzqhdwtkresult = {}
xbzqhdwtkrsset = ["rs9344","rs2273535"]
tbxbyzyqy_info = {} #突变细胞抑制与迁徙能力
tbxbyzyqyresult = {}
tbxbyzyqyrsset = ["rs3025039","rs2602141","rs1042522"]
dgcdx_info = {} #胆固醇代谢能力
dgcdxresult = {}
dgcdxrsset = ["rs320","rs285","rs2230806"]
qczzxglj_info = {} #清除脂质血管垃圾能力
qczzxgljresult = {}
qczzxgljrsset = ["rs662","rs7412","rs693"]
xytk_info = {} #血压调控能力
xytkresult = {}
xytkrsset = ["rs5051","rs5186","rs1799983","rs5443"]
kyh_info = {} #抗氧化能力
kyhresult = {}
kyhrsset = ["rs1799983","rs662","rs1799895","rs4673","rs4880"]
wczctdx_info = {} #维护正常糖代谢能力
wczctdxresult = {}
wczctdxrsset = ["rs1544410","rs2228570","rs731236","rs1800629","rs1800795","rs2241766"]
kgtxbgas_info = {} #抗高同型半胱氨酸能力
kgtxbgasresult = {}
kgtxbgasrsset = ["rs1801133","rs1801131"]
kfydx_info = {} #咖啡因代谢能力
kfydxresult = {}
kfydxrsset = ["rs762551"]
nldx_info = {} #能量代谢能力
nldxresult = {}
nldxrsset = ["rs1801282","rs660339","rs5443","rs5082","rs662799"]
kyz_info = {} #抗炎症能力
kyzresult = {}
kyzrsset = ["rs1800795","rs1800629","rs569108","rs1800872"]
wssdly_info = {} #维生素D利用能力
wssdlyresult = {}
wssdlyrsset = ["rs1544410","rs2228570","rs731236","rs2282679","rs7041","rs12512631","rs2060793","rs1562902"]
qczjsq_info = {} #清除重金属铅的能力
qczjsqresult = {}
qczjsqrsset = ["rs1544410","rs731236","rs1049296","rs1799945"]
gldxtj_info = {} #钙磷代谢调节能力
gldxtjresult = {}
gldxtjrsset = ["rs1544410","rs2228570","rs731236","rs17251221","rs1697421"]
kjl_info = {} #抗焦虑能力
kjlresult = {}
kjlrsset = ["rs7973260"]
ky_info = {} #抗压能力
kyresult = {}
kyrsset = ["rs4680"]

cjsdx_info = {} #雌激素代谢能力(仅女性)
cjsdxresult ={}
cjsdxrsset = ["rs1256054","rs6259"]
#酒精代谢能力
jjdx_info = {}
jjdxresult = {}
jjdxrsset = ["rs671","rs1229984","rs2066702"]

#叶酸代谢能力
ysdx_info = {}
ysdxresult = {}
ysdxrsset = ["rs1801131","rs1801133","rs1801394"]

def xiangmu_type(type,hang,value,dict):
    if type in hang:
        print("开始处理",hang)
        ddelcont = type+"@"
        hang = re.sub(ddelcont,"",hang)
        valuesplit = value.split('@')
        #genetypesplit = valuesplit[0].split('/')
        valuesplit[1] = re.sub("\(\d+\)","",valuesplit[1])
        genefreqsplit = valuesplit[1].split('/')
        #generisksplit = valuesplit[2].split('/')
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
        dict[hang] = valuesplit[0] + "@" + valuesplit[1] + "@" + ornewvalue + "@" + \
                     valuesplit[2] +"@"+valuesplit[-3]+"@"+valuesplit[-2]+"@"+valuesplit[-1]  #增加基因型和位点编号 v20190213;增加参考基因型 v20190222

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
                getxiangmuresult(linelist, zwxshkhresult, zwxshkhrsset) #紫外线伤害抗衡能力
                getxiangmuresult(linelist, dcfsshkhresult, dcfsshkhrsset)  #电磁辐射伤害抗衡能力
                getxiangmuresult(linelist, whjshkhresult, whjshkhrsset) #烷化剂伤害抗衡能力
                getxiangmuresult(linelist, myxtbhresult, myxtbhrsset)  #免疫系统保护能力
                getxiangmuresult(linelist, xbzqhdwtkresult, xbzqhdwtkrsset)  #细胞周期和凋亡调控能力
                getxiangmuresult(linelist, tbxbyzyqyresult, tbxbyzyqyrsset)  #突变细胞抑制与迁徙能力
                getxiangmuresult(linelist, dgcdxresult, dgcdxrsset)  #胆固醇代谢能力
                getxiangmuresult(linelist, qczzxgljresult, qczzxgljrsset)  # 清除脂质血管垃圾能力
                getxiangmuresult(linelist, xytkresult, xytkrsset)  # 血压调控能力
                getxiangmuresult(linelist, kyhresult, kyhrsset)  # 抗氧化能力
                getxiangmuresult(linelist, wczctdxresult, wczctdxrsset)  # 维护正常糖代谢能力
                getxiangmuresult(linelist, kgtxbgasresult, kgtxbgasrsset)  # 抗高同型半胱氨酸能力
                getxiangmuresult(linelist, kfydxresult, kfydxrsset)  # 咖啡因代谢能力
                getxiangmuresult(linelist, nldxresult, nldxrsset)  # 能量代谢能力
                getxiangmuresult(linelist, kyzresult, kyzrsset)  # 抗炎症能力
                getxiangmuresult(linelist, wssdlyresult, wssdlyrsset)  # 维生素D利用能力
                getxiangmuresult(linelist, qczjsqresult, qczjsqrsset)  # 清除重金属铅的能力
                getxiangmuresult(linelist, gldxtjresult, gldxtjrsset)  # 钙磷代谢调节能力
                getxiangmuresult(linelist, kjlresult, kjlrsset)  # 抗焦虑能力
                getxiangmuresult(linelist, kyresult, kyrsset)  # 抗压能力
                if sex == "woman":
                    getxiangmuresult(linelist, cjsdxresult, cjsdxrsset)  # 雌激素代谢能力
                else:
                    pass
                getxiangmuresult(linelist, jjdxresult, jjdxrsset)  # 酒精代谢能力
                getxiangmuresult(linelist, ysdxresult, ysdxrsset)  # 叶酸代谢能力

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
    if  risk_value <= 0.9:
        risk = "该位点能力增强"
    elif risk_value>0.9 and risk_value<1.1:
        risk = "该位点能力正常"
    elif risk_value >=1.1:
        risk = "该位点能力降低"
    print(rsid,result_dict[rsid],rsid_freq[needi],rsid_or[needi],risk)
    if type == "酒精代谢能力" and rsid == "rs671" and risk == "该位点能力增强":
        risk = "该位点能力较强,ALDH乙醛脱氢酶活性强,乙醛代谢成无毒的乙酸快，降低喝酒对身体的损害"
    elif type == "酒精代谢能力" and rsid == "rs671" and risk == "该位点能力正常":
        risk = "该位点能力正常"
    elif type == "酒精代谢能力" and rsid == "rs671" and risk == "该位点能力降低":
        risk = "该位点能力较弱，ALDH乙醛脱氢酶活性降低，乙醛代谢成无毒的乙酸慢，喝酒容易脸红"

    out = type + "\t" + rsid + "\t" + rsid_split[-1] + "\t" + result_dict[rsid] + "\t" + rsid_split[-3] + "\t" \
          + rsid_split[-2] + "\t" + rsid_or[needi] + "\t" + risk + "\n"
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
    if type == "叶酸代谢能力":
        if resultdict["rs1801131"] == "TG" and resultdict["rs1801133"]=="AG":
            risk_num = 2

    for j in orresult:
        if j>=1.1:
            risk_num +=1
        if j<=0.9:
            risk_good +=1
    if  riskfactor <= 0.9 and risk_good > risk_num :
        riskrsult = "能力较强"
    elif riskfactor>0.9 and riskfactor<1.1:
        riskrsult = "能力正常"
    elif riskfactor >=1.1 and risk_num >= risk_good+1:
        riskrsult = "能力较弱"
    else:
        riskrsult = "能力正常"

    if type == "叶酸代谢能力" and riskfactor >0.6 and riskfactor <=0.9 and risk_num >= risk_good+1 :
        riskrsult = "能力正常"
    if type == "叶酸代谢能力" and riskrsult == "能力较弱":
        riskrsult = "能力较弱,需要补充叶酸"


    if type == "酒精代谢能力" and riskfactor<0.5:
        riskrsult = "很强，酒神"
    elif type == "酒精代谢能力" and riskfactor>0.5 and riskfactor< 0.8:
        riskrsult = "较强，酒仙"
    elif type == "酒精代谢能力" and riskfactor>0.8 and riskfactor<= 1:
        riskrsult = "一般，酒徒"
    elif  type == "酒精代谢能力" and riskfactor>1 and riskfactor< 2:
        riskrsult = "较弱，酒弱"
    elif  type == "酒精代谢能力" and riskfactor>2:
        riskrsult = "很弱，酒渣"



    outc1 = type+"项目总体风险值："
    outc2 = "您的"+type+"结果为："
    outc3 = "您的" + type + "结果"
    print(outc1,riskfactor)
    print(outc2,riskrsult)
    out = outc3 +"\t"+ ".\t" + ".\t"+ ".\t" + ".\t" + ".\t" + str(riskfactor) + "\t" + riskrsult + "\n"
    with open(fileout, 'a', encoding='utf-8')as ww:
        ww.write(str(out))

def main(fileshujuku,sex):
    database_info = chuli_databasefile(fileshujuku)
    for key,value in database_info.items():
        #得到基础信息字典
        xiangmu_type("紫外线伤害抗衡能力", key, value, zwxshkh_info)
        xiangmu_type("电磁辐射伤害抗衡能力", key, value, dcfsshkh_info)
        xiangmu_type("烷化剂伤害抗衡能力", key, value, whjshkh_info)
        xiangmu_type("免疫系统保护能力", key, value, myxtbh_info)
        xiangmu_type("细胞周期和凋亡调控能力", key, value, xbzqhdwtk_info)
        xiangmu_type("突变细胞抑制与迁徙能力", key, value, tbxbyzyqy_info)
        xiangmu_type("胆固醇代谢能力", key, value, dgcdx_info)
        xiangmu_type("清除脂质血管垃圾能力", key, value, qczzxglj_info)
        xiangmu_type("血压调控能力", key, value, xytk_info)
        xiangmu_type("抗氧化能力", key, value, kyh_info)
        xiangmu_type("维护正常糖代谢能力", key, value, wczctdx_info)
        xiangmu_type("抗高同型半胱氨酸能力", key, value, kgtxbgas_info)
        xiangmu_type("咖啡因代谢能力", key, value, kfydx_info)
        xiangmu_type("能量代谢能力", key, value, nldx_info)
        xiangmu_type("抗炎症能力", key, value, kyz_info)
        xiangmu_type("维生素D利用能力", key, value, wssdly_info)
        xiangmu_type("清除重金属铅的能力", key, value, qczjsq_info)
        xiangmu_type("钙磷代谢调节能力", key, value, gldxtj_info)
        xiangmu_type("抗焦虑能力", key, value, kjl_info)
        xiangmu_type("抗压能力", key, value, ky_info)
        if sex == "woman":
            xiangmu_type("雌激素代谢能力", key, value, cjsdx_info)
        else:
            pass
        xiangmu_type("酒精代谢能力", key, value, jjdx_info)
        xiangmu_type("叶酸代谢能力", key, value, ysdx_info)

    # 得到基因型结果字典
    readbiyanai(filein,sex)
    # 比较呈现癌结果并输出
    out = samplename+"\t" + "能力篇\t" + "参考基因型\t"+ "基因型\t" + "基因\t" + "位点编号ID\t" + "新风险值\t" + "能力结果" + "\n"
    with open(fileout, 'w', encoding='utf-8')as ww:
        ww.write(str(out))
    chuli_show_xiangmu(zwxshkhresult, zwxshkh_info, "紫外线伤害抗衡能力")
    chuli_show_xiangmu(dcfsshkhresult, dcfsshkh_info, "电磁辐射伤害抗衡能力")
    chuli_show_xiangmu(whjshkhresult, whjshkh_info, "烷化剂伤害抗衡能力")
    chuli_show_xiangmu(myxtbhresult, myxtbh_info, "免疫系统保护能力")
    chuli_show_xiangmu(xbzqhdwtkresult, xbzqhdwtk_info, "细胞周期和凋亡调控能力")
    chuli_show_xiangmu(tbxbyzyqyresult, tbxbyzyqy_info, "突变细胞抑制与迁徙能力")
    chuli_show_xiangmu(dgcdxresult, dgcdx_info, "胆固醇代谢能力")
    chuli_show_xiangmu(qczzxgljresult, qczzxglj_info, "清除脂质血管垃圾能力")
    chuli_show_xiangmu(xytkresult, xytk_info, "血压调控能力")
    chuli_show_xiangmu(kyhresult, kyh_info, "抗氧化能力")
    chuli_show_xiangmu(wczctdxresult, wczctdx_info, "维护正常糖代谢能力")
    chuli_show_xiangmu(kgtxbgasresult, kgtxbgas_info, "抗高同型半胱氨酸能力")
    chuli_show_xiangmu(kfydxresult, kfydx_info, "咖啡因代谢能力")
    chuli_show_xiangmu(nldxresult, nldx_info, "能量代谢能力")
    chuli_show_xiangmu(kyzresult, kyz_info, "抗炎症能力")
    chuli_show_xiangmu(wssdlyresult, wssdly_info, "维生素D利用能力")
    chuli_show_xiangmu(qczjsqresult, qczjsq_info, "清除重金属铅的能力")
    chuli_show_xiangmu(gldxtjresult, gldxtj_info, "钙磷代谢调节能力")
    chuli_show_xiangmu(kjlresult, kjl_info, "抗焦虑能力")
    chuli_show_xiangmu(kyresult, ky_info, "抗压能力")
    if sex == "woman":
        chuli_show_xiangmu(cjsdxresult, cjsdx_info, "雌激素代谢能力")

    chuli_show_xiangmu(jjdxresult, jjdx_info, "酒精代谢能力")
    chuli_show_xiangmu(ysdxresult, ysdx_info, "叶酸代谢能力")


main(fileshujuku,sex)
filetest = "testread_jiujing_yesuan.txt"
def readtestjiujingyesuan(filein):
    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if "#" in line:
                pass
            else:
                line = line.strip('\n')
                linelist = line.split('\t')
                getxiangmuresult(linelist, jjdxresult, jjdxrsset)  # 酒精代谢能力
                getxiangmuresult(linelist, ysdxresult, ysdxrsset)  # 叶酸代谢能力

def testjjys(fileshujuku):
    database_info = chuli_databasefile(fileshujuku)
    for key,value in database_info.items():
        #得到基础信息字典
        xiangmu_type("酒精代谢能力", key, value, jjdx_info)
        xiangmu_type("叶酸代谢能力", key, value, ysdx_info)
    # 得到基因型结果字典
    readtestjiujingyesuan(filetest)
    # 比较呈现癌结果并输出
    out = samplename+"\t" + "能力篇\t" + "参考基因型\t"+ "基因型\t" + "基因\t" + "位点编号ID\t" + "新风险值\t" + "能力结果" + "\n"
    with open(fileout, 'w', encoding='utf-8')as ww:
        ww.write(str(out))
    chuli_show_xiangmu(jjdxresult, jjdx_info, "酒精代谢能力")
    chuli_show_xiangmu(ysdxresult, ysdx_info, "叶酸代谢能力")

#testjjys(fileshujuku)