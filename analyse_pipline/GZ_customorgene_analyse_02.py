# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
#   读入基因型数据，根据数据库中的记录，计算相应的风险
#   首先要把记载的项目和风险型编号入座
#   疾病篇心血管部分的模型
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
fileout = "sampleresult1.txt"
def chuli_databasefile(fileshujuku):
    database_info = {}
    wb = xlrd.open_workbook(fileshujuku)
    sh1 = wb.sheet_by_index(1)
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
        database_info[flag] = info + "@" + hanglist[4] + "@" + hanglist[11] + "@" + refgene+"@"+hanglist[13]  # 增加基因型和位点编号 v20190213;增加参考基因型 v20190222；增加位点说明 ,v20190318
    return database_info
# 所有项目基本数据字典
dmzyyh_info = {} #动脉粥样硬化
dmzyyhresult = {}
dmzyyhrsset = ["rs1801133","rs693","rs1333049","rs699947"]
fangchan_info = {} #房颤
fangchanresult = {}
fangchanrsset = ["rs699","rs5800","rs10465885","rs2200733","rs10033464","rs2106261","rs6499600","rs1799998","rs5063"]
fhxxjb_info = {} #肥厚性心肌病
fhxxjbresult = {}
fhxxjbrsset = ["rs2234962"]
guanxinbing_info = {} #冠心病
guanxinbingresult = {}
guanxinbingrsset = ["rs2230806","rs662","rs2383207","rs3798220","rs1333049","rs662799","rs6903956","rs17465637","rs3782886","rs3900940","rs6511720","rs7439293","rs17165136"]
lncd_info = {} #老年痴呆症
lncdresult = {}
lncdrsset = ["rs429358 ","rs7412","rs1801133","rs1801131","rs11218350","rs1699103","rs1784931","rs1792113","rs726601","rs5882","rs7101429","rs892086","rs908832"]
naogengse_info = {} #脑梗塞
naogengseresult = {}
naogengsersset = ["rs619203","rs2108622","rs10507391","rs1537378","rs2107538","rs9471058","rs2230500"]
naoyixue_info = {} #脑溢血
naoyixueresult = {}
naoyixuersset = ["rs1800790","rs2230500","rs6050"]
sjmxs_info = {} #深静脉血栓
sjmxsresult = {}
sjmxsrsset = ["rs13146272","rs2227589","rs1613662","rs2289252","rs2036914","rs4524"]
xjgs_info = {} #心肌梗塞
xjgsresult = {}
xjgsrsset = ["rs599839","rs17465637","rs501120","rs4977574","rs646776"]
yfxgxy_info = {} #原发性高血压
yfxgxyresult = {}
yfxgxyrsset = ["rs5051","rs5186","rs5443","rs11191548","rs3774372","rs16998073","rs3865418"]
naozhongfeng_info = {} #脑中风
naozhongfengresult = {}
naozhongfengrsset = ["rs10507391","rs2230500","rs3783799","rs3184504","rs966221"]
xyxcs_info = {} #心源性猝死
xyxcsresult = {}
xyxcsrsset = ["rs174230","rs4665058","rs16847548"]
mxzsxfjb_info = {} #慢性阻塞性肺疾病
mxzsxfjbresult = {}
mxzsxfjbrsset = ["rs17576","rs1800469","rs7671167","rs8034191"]
qxxncz_info = {} #缺血性脑卒中
qxxnczresult = {}
qxxnczrsset = ["rs11738269","rs2230500","rs266729"]
iitangniaobing_info = {} #II型糖尿病
iitangniaobingresult = {}
iitangniaobingrsset = ["rs1800795","rs2228570","rs2237892","rs7903146","rs4506565","rs12255372","rs4402960","rs1470579"]
dcxfp_info = {} #单纯性肥胖
dcxfpresult = {}
dcxfprsset = ["rs320","rs660339","rs693","rs662799","rs6971091"]
dfxyh_info = {} #多发性硬化
dfxyhresult = {}
dfxyhrsset = ["rs1800629","rs3135388","rs6897932"]
gtxbgasxz_info = {} #高同型半胱氨酸血症
gtxbgasxzresult = {}
gtxbgasxzrsset = ["rs1801133","rs1801131"]
gzxz_info = {} #高脂血症
gzxzresult = {}
gzxzrsset = ["rs1801133","rs320","rs1260326","rs964184"]
gzss_info = {} #骨质疏松
gzssresult = {}
gzssrsset = ["rs429358","rs1800629","rs1544410","rs11898505","rs1286083","rs2273061","rs2306033","rs3736228","rs4988321","rs3770748","rs6993813","rs7935346"]
lfsxgjy_info = {} #类风湿性关节炎
lfsxgjyresult = {}
lfsxgjyrsset = ["rs231775","rs13031237","rs1953126","rs2269475","rs2476601","rs3761847","rs6682654","rs7574865","rs3890745"]
pingxue_info = {} #贫血
pingxueresult = {}
pingxuersset = ["rs104886456","rs104886457"]
qzxjzy_info = {} #强直性脊柱炎
qzxjzyresult = {}
qzxjzyrsset = ["rs30187","rs10050860","rs2303138","rs13202464"]
xtxhblc_info = {} #系统性红斑狼疮
xtxhblcresult = {}
xtxhblcrsset = ["rs2304256","rs2004640","rs1143679","rs2280714","rs10488631","rs7582694","rs7574865","rs10181656"]
zqgxc_info = {} #支气管哮喘
zqgxcresult = {}
zqgxcrsset = ["rs1695","rs569108","rs1800629","rs7216389","rs4950928","rs1063355","rs13153971"]
zhifanggan_info = {} #脂肪肝
zhifangganresult = {}
zhifangganrsset = ["rs738409","rs13412852"]
tongfeng_info = {} #痛风
tongfengresult = {}
tongfengrsset = ["rs11726117","rs231253","rs2231142","rs505802","rs1165205","rs12498742","rs16890979","rs6855911"]
gmxby_info = {} #过敏性鼻炎
gmxbyresult = {}
gmxbyrsset = ["rs7775228","rs1059513","rs17294280"]

def xinxueguan_type(type,hang,value,dict):
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
        dict[hang] = valuesplit[0] + "@" + valuesplit[1] + "@" + valuesplit[3] + "@" + \
                     valuesplit[2] +"@"+valuesplit[-4]+"@"+valuesplit[-3]+"@"+valuesplit[-2]+"@"+valuesplit[-1]  #增加基因型和位点编号 v20190213;增加参考基因型 v20190222；增加位点说明，用原来的or吧还是 v20190318

def getxiangmuresult(linelist,resultdict,rsset):
    for i in range(len(rsset)):
        if linelist[0] == rsset[i]:
            resultdict[rsset[i]] = linelist[3]

def readbiyanai(filein):
    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if "#" in line:
                pass
            else:
                line = line.strip('\n')
                linelist = line.split('\t')
                getxiangmuresult(linelist,dmzyyhresult,dmzyyhrsset) # 动脉粥样硬化
                getxiangmuresult(linelist, fangchanresult, fangchanrsset)  # 房颤
                getxiangmuresult(linelist, fhxxjbresult, fhxxjbrsset)  # 肥厚性心肌病
                getxiangmuresult(linelist, guanxinbingresult, guanxinbingrsset)  # 冠心病
                getxiangmuresult(linelist, lncdresult, lncdrsset)  # 老年痴呆症
                getxiangmuresult(linelist, naogengseresult, naogengsersset)  # 脑梗塞
                getxiangmuresult(linelist, naoyixueresult, naoyixuersset)  # 脑溢血
                getxiangmuresult(linelist, sjmxsresult, sjmxsrsset)  # 深静脉血栓
                getxiangmuresult(linelist, xjgsresult, xjgsrsset)  # 心肌梗塞
                getxiangmuresult(linelist, yfxgxyresult, yfxgxyrsset)  # 原发性高血压
                getxiangmuresult(linelist, naozhongfengresult, naozhongfengrsset)  # 脑中风
                getxiangmuresult(linelist, xyxcsresult, xyxcsrsset)  # 心源性猝死
                getxiangmuresult(linelist, mxzsxfjbresult, mxzsxfjbrsset)  # 慢性阻塞性肺疾病
                getxiangmuresult(linelist, qxxnczresult, qxxnczrsset)  # 缺血性脑卒中
                getxiangmuresult(linelist, iitangniaobingresult, iitangniaobingrsset)  # II型糖尿病
                getxiangmuresult(linelist, dcxfpresult, dcxfprsset)  # 单纯性肥胖
                getxiangmuresult(linelist, dfxyhresult, dfxyhrsset)  # 多发性硬化
                getxiangmuresult(linelist, gtxbgasxzresult, gtxbgasxzrsset)  # 高同型半胱氨酸血症
                getxiangmuresult(linelist, gzxzresult, gzxzrsset)  # 高脂血症
                getxiangmuresult(linelist, gzssresult, gzssrsset)  # 骨质疏松
                getxiangmuresult(linelist, lfsxgjyresult, lfsxgjyrsset)  # 类风湿性关节炎
                getxiangmuresult(linelist, pingxueresult, pingxuersset)  # 贫血
                getxiangmuresult(linelist, qzxjzyresult, qzxjzyrsset)  # 强直性脊柱炎
                getxiangmuresult(linelist, xtxhblcresult, xtxhblcrsset)  # 系统性红斑狼疮
                getxiangmuresult(linelist, zqgxcresult, zqgxcrsset)  # 支气管哮喘
                getxiangmuresult(linelist, zhifangganresult, zhifangganrsset)  # 脂肪肝
                getxiangmuresult(linelist, tongfengresult, tongfengrsset)  # 痛风
                getxiangmuresult(linelist, gmxbyresult, gmxbyrsset)  # 过敏性鼻炎

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
    print(rsid,result_dict[rsid],rsid_freq[needi],rsid_or[needi],risk,sitecontent)
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
    out = outc3 +"\t"+ ".\t" + ".\t"+ ".\t" + ".\t" + ".\t" + str(riskfactor) + "\t" + riskrsult + "\t."+"\n"
    with open(fileout, 'a', encoding='utf-8')as ww:
        ww.write(str(out))

def main(fileshujuku):
    database_info = chuli_databasefile(fileshujuku)
    for key,value in database_info.items():
        #得到基础信息字典
        xinxueguan_type("动脉粥样硬化", key, value, dmzyyh_info)
        xinxueguan_type("房颤", key, value, fangchan_info)
        xinxueguan_type("肥厚性心肌病", key, value, fhxxjb_info)
        xinxueguan_type("冠心病", key, value, guanxinbing_info)
        xinxueguan_type("老年痴呆症", key, value, lncd_info)
        xinxueguan_type("脑梗塞", key, value, naogengse_info)
        xinxueguan_type("脑溢血", key, value, naoyixue_info)
        xinxueguan_type("深静脉血栓", key, value, sjmxs_info)
        xinxueguan_type("心肌梗塞", key, value, xjgs_info)
        xinxueguan_type("原发性高血压", key, value, yfxgxy_info)
        xinxueguan_type("脑中风", key, value, naozhongfeng_info)
        xinxueguan_type("心源性猝死", key, value, xyxcs_info)
        xinxueguan_type("慢性阻塞性肺疾病", key, value, mxzsxfjb_info)
        xinxueguan_type("缺血性脑卒中", key, value, qxxncz_info)
        xinxueguan_type("II型糖尿病", key, value, iitangniaobing_info)
        xinxueguan_type("单纯性肥胖", key, value, dcxfp_info)
        xinxueguan_type("多发性硬化", key, value, dfxyh_info)
        xinxueguan_type("高同型半胱氨酸血症", key, value, gtxbgasxz_info)
        xinxueguan_type("高脂血症", key, value, gzxz_info)
        xinxueguan_type("骨质疏松", key, value, gzss_info)
        xinxueguan_type("类风湿性关节炎", key, value, lfsxgjy_info)
        xinxueguan_type("贫血", key, value, pingxue_info)
        xinxueguan_type("强直性脊柱炎", key, value, qzxjzy_info)
        xinxueguan_type("系统性红斑狼疮", key, value, xtxhblc_info)
        xinxueguan_type("支气管哮喘", key, value, zqgxc_info)
        xinxueguan_type("脂肪肝", key, value, zhifanggan_info)
        xinxueguan_type("痛风", key, value, tongfeng_info)
        xinxueguan_type("过敏性鼻炎", key, value, gmxby_info)

    # 得到基因型结果字典
    readbiyanai(filein)
    # 比较呈现癌结果并输出  v20190320 把原本的第一个和第二个文档合并，都算是疾病篇里头的，能力篇才算是单独的，所以fileout输出的在第一个文档之后就可以了
    #out = samplename+"\t" + "疾病篇\t" + "参考基因型\t"+ "基因型\t" + "基因\t" + "位点编号ID\t"+"新风险值\t"+"风险结果\t" + "位点说明"+"\n"
    #with open(fileout, 'w', encoding='utf-8')as ww:
    #    ww.write(str(out))
    chuli_show_xiangmu(dmzyyhresult, dmzyyh_info, "动脉粥样硬化")
    chuli_show_xiangmu(fangchanresult, fangchan_info, "房颤")
    chuli_show_xiangmu(fhxxjbresult, fhxxjb_info, "肥厚性心肌病")
    chuli_show_xiangmu(guanxinbingresult, guanxinbing_info, "冠心病")
    chuli_show_xiangmu(lncdresult, lncd_info, "老年痴呆症")
    chuli_show_xiangmu(naogengseresult, naogengse_info, "脑梗塞")
    chuli_show_xiangmu(naoyixueresult, naoyixue_info, "脑溢血")
    chuli_show_xiangmu(sjmxsresult, sjmxs_info, "深静脉血栓")
    chuli_show_xiangmu(xjgsresult, xjgs_info, "心肌梗塞")
    chuli_show_xiangmu(yfxgxyresult, yfxgxy_info, "原发性高血压")
    chuli_show_xiangmu(naozhongfengresult, naozhongfeng_info, "脑中风")
    chuli_show_xiangmu(xyxcsresult, xyxcs_info, "心源性猝死")
    chuli_show_xiangmu(mxzsxfjbresult, mxzsxfjb_info, "慢性阻塞性肺疾病")
    chuli_show_xiangmu(qxxnczresult, qxxncz_info, "缺血性脑卒中")
    chuli_show_xiangmu(iitangniaobingresult, iitangniaobing_info, "II型糖尿病")
    chuli_show_xiangmu(dcxfpresult, dcxfp_info, "单纯性肥胖")
    chuli_show_xiangmu(dfxyhresult, dfxyh_info, "多发性硬化")
    chuli_show_xiangmu(gtxbgasxzresult, gtxbgasxz_info, "高同型半胱氨酸血症")
    chuli_show_xiangmu(gzxzresult, gzxz_info, "高脂血症")
    chuli_show_xiangmu(gzssresult, gzss_info, "骨质疏松")
    chuli_show_xiangmu(lfsxgjyresult, lfsxgjy_info, "类风湿性关节炎")
    chuli_show_xiangmu(pingxueresult, pingxue_info, "贫血")
    chuli_show_xiangmu(qzxjzyresult, qzxjzy_info, "强直性脊柱炎")
    chuli_show_xiangmu(xtxhblcresult, xtxhblc_info, "系统性红斑狼疮")
    chuli_show_xiangmu(zqgxcresult, zqgxc_info, "支气管哮喘")
    chuli_show_xiangmu(zhifangganresult, zhifanggan_info, "脂肪肝")
    chuli_show_xiangmu(tongfengresult, tongfeng_info, "痛风")
    chuli_show_xiangmu(gmxbyresult, gmxby_info, "过敏性鼻炎")


main(fileshujuku)



