# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys

#给出不同基因型的癌症风险结果
#rsid	VCFinfo	基因型	频率
#rs78378222	17:7571752:rs78378222:T:G	all/TT/GG/GT	0.995(2492)/0.000399361022364217(1)/0.004(11)
#rs12951053	17:7577407:rs12951053:A:C	AA/AC/CC	0.476(50)/0.448(47)/0.076(8)
#rs1042522	17:7579472:rs1042522:G:C,T	GG/CC/CG	0.152(16)/0.352(37)/0.495(52)
#rs2078486	17:7583083:rs2078486:G:A,C	GG/AA/AG	0.505(53)/0.057(6)/0.438(46)
filein = "test3.txt"
sex = "woman"
riskrsdict = {
    "rs78378222_TT":"0.995",
    "rs78378222_GG":"0.0004",
    "rs78378222_GT":"0.004",
    "rs12951053_CC":"0.076",
    "rs12951053_AA":"0.476",
    "rs12951053_AC":"0.448",
    "rs1042522_GG":"0.152",
    "rs1042522_CC":"0.352",
    "rs1042522_CG":"0.495",
    "rs2078486_GG":"0.505",
    "rs2078486_AA":"0.057",
    "rs2078486_AG":"0.438",
}
resultdict = {}
def getresultgenetype(filein):
    with open(filein, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line =  line.strip('\n')
            linelist = line.split('\t')
            if "rs78378222" in line:
                resultdict["rs78378222"] = linelist[1]
                print("rs78378222 %s get"%linelist[1])
            elif "rs12951053" in line:
                resultdict["rs12951053"] = linelist[1]
                print("rs12951053 %s get"%linelist[1])
            elif "rs1042522" in line:
                resultdict["rs1042522"] = linelist[1]
                print("rs1042522 %s get"%linelist[1])
            elif "rs2078486" in line:
                resultdict["rs2078486"] = linelist[1]
                print("rs2078486 %s get"%linelist[1])

def liverrisk():
    genetype = resultdict["rs1042522"]
    id = "rs1042522_"+genetype
    getfre = '%.2f%%'% (float(riskrsdict[id])*100)
    print("您肝癌风险所属的人群占比约为：",getfre)
def stomachrisk():
    genetype = resultdict["rs1042522"]
    id = "rs1042522_"+genetype
    getfre = '%.2f%%'% (float(riskrsdict[id])*100)
    print("您胃癌风险所属的人群占比约为：",getfre)
def yixianairisk():
    genetype = resultdict["rs1042522"]
    id = "rs1042522_"+genetype
    getfre = '%.2f%%'% (float(riskrsdict[id])*100)
    print("您胰腺癌风险所属的人群占比约为：",getfre)
def zigongneimoairisk():
    genetype = resultdict["rs1042522"]
    id = "rs1042522_"+genetype
    getfre = '%.2f%%'% (float(riskrsdict[id])*100)
    print("您子宫内膜癌风险所属的人群占比约为：",getfre)
def toujingairisk():
    genetype = resultdict["rs78378222"]
    id = "rs78378222_"+genetype
    getfre = '%.2f%%'% (float(riskrsdict[id])*100)
    print("您头颈癌风险所属的人群占比约为：",getfre)
def shiguanairisk():
    genetype = resultdict["rs78378222"]
    id = "rs78378222_"+genetype
    getfre = '%.2f%%'% (float(riskrsdict[id])*100)
    print("您食管癌风险所属的人群占比约为：",getfre)
def qianliexianairisk():
    genetype = resultdict["rs78378222"]
    id = "rs78378222_"+genetype
    getfre = '%.2f%%'% (float(riskrsdict[id])*100)
    print("您前列腺癌风险所属的人群占比约为：",getfre)
def shenjingjiaozhiairisk():
    genetype = resultdict["rs78378222"]
    id = "rs78378222_"+genetype
    getfre = '%.2f%%'% (float(riskrsdict[id])*100)
    print("您神经胶质瘤风险所属的人群占比约为：",getfre)

#双位点的
def gurouliurisk():
    genetype1 = resultdict["rs12951053"]
    id1 = "rs12951053_"+genetype1
    genetype2 = resultdict["rs1042522"]
    id2 = "rs1042522_"+genetype2
    getfre = '%.2f%%'% ( (float(riskrsdict[id1])+float(riskrsdict[id2]))*50)
    print("您骨肉瘤风险所属的人群占比约为：",getfre)

def pifuairisk():
    genetype1 = resultdict["rs12951053"]
    id1 = "rs12951053_"+genetype1
    genetype2 = resultdict["rs78378222"]
    id2 = "rs78378222_"+genetype2
    getfre = '%.2f%%'% ( (float(riskrsdict[id1])+float(riskrsdict[id2]))*50)
    print("您皮肤癌风险所属的人群占比约为：",getfre)

def jiezhichangairisk():
    genetype1 = resultdict["rs1042522"]
    id1 = "rs1042522_"+genetype1
    genetype2 = resultdict["rs78378222"]
    id2 = "rs78378222_"+genetype2
    getfre = '%.2f%%'% ( (float(riskrsdict[id1])+float(riskrsdict[id2]))*50)
    print("您结直肠癌风险所属的人群占比约为：",getfre)

def luanchaoairisk():
    genetype1 = resultdict["rs12951053"]
    id1 = "rs12951053_"+genetype1
    genetype2 = resultdict["rs2078486"]
    id2 = "rs2078486_"+genetype2
    getfre = '%.2f%%'% ( (float(riskrsdict[id1])+float(riskrsdict[id2]))*50)
    print("您卵巢癌风险所属的人群占比约为：",getfre)

def ruxianairisk():
    genetype1 = resultdict["rs12951053"]
    id1 = "rs12951053_"+genetype1
    genetype2 = resultdict["rs1042522"]
    id2 = "rs1042522_"+genetype2
    getfre = '%.2f%%'% ( (float(riskrsdict[id1])+float(riskrsdict[id2]))*50)
    print("您乳腺癌风险所属的人群占比约为：",getfre)

def lungrisk():
    genetype1 = resultdict["rs12951053"]
    id1 = "rs12951053_"+genetype1
    genetype2 = resultdict["rs1042522"]
    id2 = "rs1042522_"+genetype2
    genetype3 = resultdict["rs2078486"]
    id3 = "rs2078486_"+genetype3
    getfre = '%.2f%%' % (((float(riskrsdict[id1]) + float(riskrsdict[id2])+ float(riskrsdict[id3])) /3)* 100)
    print("您肺癌风险所属的人群占比约为：", getfre)


getresultgenetype(filein)
liverrisk()
stomachrisk()
yixianairisk()
if sex == "woman":
    zigongneimoairisk()
    luanchaoairisk()
    ruxianairisk()
elif sex == "man":
    qianliexianairisk()
toujingairisk()
shiguanairisk()
shenjingjiaozhiairisk()
gurouliurisk()
pifuairisk()
jiezhichangairisk()
lungrisk()

