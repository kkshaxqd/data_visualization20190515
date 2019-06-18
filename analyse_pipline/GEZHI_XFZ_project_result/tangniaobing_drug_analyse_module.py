# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
import xlrd
import xlwt
"""
time:20190507
分析糖尿病用药结果，根据基因型位点给出最后用药建议
CYP2C9	rs1057910	AA	磺酰脲类药物的肾脏清除率正常,降糖作用正常。
		AC	磺酰脲类药物的肾脏清除率较慢，略微增强降糖作用，低血糖风险略增加，可适当降低用药剂量。
		CC	磺酰脲类药物的肾脏清除率减慢，明显增强降糖作用，低血糖风险增加，可适当降低用药剂量。
位点              基因型     疗效     代谢清除效率  推荐度
rs1057910		AA/AC/CC  1/1.5/2  1/0.8/0.5    
KCNJ11	rs5219	TT	磺酰脲类药物敏感性低，药物失效率高。
		CT	磺酰脲类药物敏感性降低，药物失效率较高。
		CC	磺酰脲类药物敏感性较高，降糖效果属正常水平，继发性失效率低。
rs5219  TT/CT/CC  0.5/0.8/1.2
ABCC8	rs757110	GG	磺酰脲类药物受体敏感性较高，治疗效果好。
		GT	磺酰脲类药物受体敏感性有所降低，疗效下降。
		TT	磺酰脲类药物受体敏感性低，疗效较低。
	rs1799854	CC	磺酰脲类药物受体敏感性较高，治疗效果好。
		CT	磺酰脲类药物受体敏感性有所降低，药物失效率有所升高。
		TT	磺酰脲类药物受体敏感性较低，药物失效率升高。

rs757110 GG/GT/TT 1.5/1.2/0.8
rs1799854 CC/CT/TT 1.5/1.2/0.8

TCF7L2	rs12255372	GG	磺酰脲类药物敏感性属正常水平，疗效正常。
		GT	磺酰脲类药物敏感性属略低水平，药物失效率有所升高。
		TT	磺酰脲类药物敏感性属较低水平，药物失效率较高。
	rs7903146	CC	磺酰脲类药物敏感性属正常水平，疗效正常。
		CT	磺酰脲类药物敏感性属略低水平，降糖作用有所下降。
		TT	磺酰脲类药物敏感性属较低水平，降糖作用较低。

rs12255372  GG/GT/TT 1/0.8/0.5
rs7903146  CC/CT/TT 1/0.8/0.5

"""
fileshujuku='糖尿病用药位点组合.xlsx'
fileout = '糖尿病用药结果.txt'

drugddict = {
    #"rs1057910":"AA/AC/CC:1/1.5/2:1:LV3",
    "rs5219":"TT/CT/CC:0.5/0.8/1.5:1:LV3",
    "rs757110": "GG/GT/TT:1.5/0.9/0.5:1:LV3",
    "rs1799854": "CC/CT/TT:1.5/0.9/0.5:0.8:LV4",
    "rs12255372": "GG/GT/TT:1/0.7/0.4:1:LV3",
    "rs7903146": "CC/CT/TT:1/0.7/0.4:1.2:LV2B"
}

detectdict={}

def huangxianleivalueofalldict():
    #rs1057910list = drugddict['rs1057910'].split(':')
    rs5219list =  drugddict['rs5219'].split(':')
    rs757110list =  drugddict['rs757110'].split(':')
    rs1799854list =  drugddict['rs1799854'].split(':')
    rs12255372list =  drugddict['rs12255372'].split(':')
    rs7903146list =  drugddict['rs7903146'].split(':')

    #weidian1=rs1057910list[0].split('/')
    #weidian1value=rs1057910list[1].split('/')
    #weidian1value=list(map(float,weidian1value))
    #wegiht1=float(rs1057910list[2])

    weidian2=rs5219list[0].split('/')
    weidian2value=rs5219list[1].split('/')
    weidian2value = list(map(float, weidian2value))
    wegiht2=float(rs5219list[2])

    weidian3=rs757110list[0].split('/')
    weidian3value=rs757110list[1].split('/')
    weidian3value = list(map(float, weidian3value))
    wegiht3=float(rs757110list[2])

    weidian4=rs1799854list[0].split('/')
    weidian4value=rs1799854list[1].split('/')
    weidian4value = list(map(float, weidian4value))
    wegiht4=float(rs1799854list[2])

    weidian5=rs12255372list[0].split('/')
    weidian5value=rs12255372list[1].split('/')
    weidian5value = list(map(float, weidian5value))
    wegiht5=float(rs12255372list[2])

    weidian6=rs7903146list[0].split('/')
    weidian6value=rs7903146list[1].split('/')
    weidian6value = list(map(float, weidian6value))
    wegiht6=float(rs7903146list[2])

    #for i in range(0, 3)
    for j in range(0,3):
        for h in range(0,3):
            for n in range(0,3):
                for m in range(0,3):
                    for b in range(0,3):
                        #gtzuhe=weidian1[i]+":"+weidian2[j]+":"+weidian3[h]+":"+weidian4[n]+":"+weidian5[m]+":"+weidian6[b]
                        #gtvaluezuhe=weidian1value[i]*weidian2value[j]*weidian3value[h]*weidian4value[n]*weidian5value[m]*weidian6value[b]
                        #getweight=wegiht1*wegiht2*wegiht3*wegiht4*wegiht5*wegiht6
                        gtzuhe =  weidian2[j] + ":" + weidian3[h] + ":" + weidian4[n] + ":" + \
                                 weidian5[m] + ":" + weidian6[b]
                        gtvaluezuhe = weidian2value[j] * weidian3value[h] * weidian4value[n] * \
                                      weidian5value[m] * weidian6value[b]
                        getweight =  wegiht2 * wegiht3 * wegiht4 * wegiht5 * wegiht6
                        gtvresult=gtvaluezuhe*getweight
                        detectdict[gtzuhe]=gtvresult
                        print('基因型为%s,磺酰脲类药物的疗效评价为%.2f '%(gtzuhe,gtvresult))

"""
糖尿病用药双胍类	SLC22A1	rs72552763	Wt/Wt	肝细胞的药物摄取能力正常，疗效正常。
PharmGKB summary: very important pharmacogene information
for SLC22A1
			Wt/Del	肝细胞的药物摄取能力有所下降，疗效降低。
			Del/Del	肝细胞的药物摄取能力下降，疗效降低。
	SLC22A2	rs316019	TT	二甲双胍的肾脏清除率降低，长期降糖效果增加，有低血糖风险。
			GT	二甲双胍的肾脏清除率有所降低，长期降糖效果增加，有低血糖风险。
			GG(Wide)	二甲双胍的肾脏清除率正常，长期降糖效果正常。

"""

drugdictshuanggua={
    "rs72552763": "WW/WD/DD:1.2/0.8/0.5:1:LV3",
    "rs316019": "TT/GT/GG:0.8/0.8/1.2:1:LV3"
}
def shuangguanlei():
    rs72552763_list = drugdictshuanggua['rs72552763'].split(':')
    rs316019_list =  drugdictshuanggua['rs316019'].split(':')
    weidian1=rs72552763_list[0].split('/')
    weidian1value=rs72552763_list[1].split('/')
    weidian1value=list(map(float,weidian1value))
    wegiht1=float(rs72552763_list[2])

    weidian2=rs316019_list[0].split('/')
    weidian2value=rs316019_list[1].split('/')
    weidian2value = list(map(float, weidian2value))
    wegiht2=float(rs316019_list[2])
    for i in range(0, 3):
        for j in range(0,3):
            gtzuhe = weidian1[i] + ":" + weidian2[j]
            gtvaluezuhe=weidian1value[i]*weidian2value[j]
            getweight = wegiht1 * wegiht2
            gtvresult = gtvaluezuhe * getweight
            detectdict[gtzuhe] = gtvresult
            print('基因型为%s,二甲双胍的疗效评价为%.2f ' % (gtzuhe, gtvresult))


"""
糖尿病用药噻唑烷二酮类	PPARG	rs1801282	CC	噻唑烷二酮类药物敏感性属正常水平，疗效正常。
			GC 	噻唑烷二酮类药物敏感性属较高水平，降糖效果较好，可能发生药源性水肿。
			GG 	噻唑烷二酮类药物敏感性属高水平，降糖效果好，可能发生药源性水肿。
糖尿病用药格列奈类	SLCO1B1	rs4149056	TT 	格列奈类药物代谢速度正常，血液药物浓度正常,药效较好。
			TC	格列奈类药物代谢速度减慢，血液药物浓度上升，药物半衰期延长，有低血糖风险。
			CC 	格列奈类药物代谢速度减慢，血液药物浓度上升，药物半衰期延长，有低血糖风险。
	CYP2C9	rs1057910	AA	格列奈类药物的肾脏清除率正常，疗效正常。
			AC	格列奈类药物的肾脏清除率较慢，有低血糖风险。
			CC	格列奈类药物的肾脏清除率减慢，增加低血糖风险。

"""
dictsecuowan={
    "rs1801282": "CC/GC/GG:1/0.8/0.8:1:LV3"
}

def secuowan():
    rs1801282_list=dictsecuowan['rs1801282'].split(':')
    weidian1=rs1801282_list[0].split('/')
    weidian1value=rs1801282_list[1].split('/')
    weidian1value=list(map(float,weidian1value))
    wegiht1=float(rs1801282_list[2])
    for i in range(0, 3):
        gtzuhe = weidian1[i]
        gtvaluezuhe = weidian1value[i]
        getweight = wegiht1
        gtvresult = gtvaluezuhe * getweight
        detectdict[gtzuhe] = gtvresult
        print('基因型为%s,噻唑烷二酮类药物的疗效评价为%.2f ' % (gtzuhe, gtvresult))

dictgelienai={
    "rs4149056": "TT/TC/CC:1.2/0.5/0.5:1:LV3",
    "rs1057910": "AA/AC/CC:1/0.7/0.5:1:LV3"
}

def gelienai():
    rs4149056_list = dictgelienai['rs4149056'].split(':')
    rs1057910_list =  dictgelienai['rs1057910'].split(':')
    weidian1=rs4149056_list[0].split('/')
    weidian1value=rs4149056_list[1].split('/')
    weidian1value=list(map(float,weidian1value))
    wegiht1=float(rs4149056_list[2])

    weidian2=rs1057910_list[0].split('/')
    weidian2value=rs1057910_list[1].split('/')
    weidian2value = list(map(float, weidian2value))
    wegiht2=float(rs1057910_list[2])
    for i in range(0, 3):
        for j in range(0,3):
            gtzuhe = weidian1[i] + ":" + weidian2[j]
            gtvaluezuhe=weidian1value[i]*weidian2value[j]
            getweight = wegiht1 * wegiht2
            gtvresult = gtvaluezuhe * getweight
            detectdict[gtzuhe] = gtvresult
            print('基因型为%s,格列奈类的疗效评价为%.2f ' % (gtzuhe, gtvresult))


def chuli_databasefile(fileshujuku):
    huangxianleivalueofalldict()  # 疗效评价值从6.48-0.02  6-3以上强烈推荐，3-0.9 正常推荐 ，0.9以下，不推荐
    shuangguanlei()  # 1.44-0.4  0.96以上正常推荐 ，以下不推荐
    secuowan()  # 不管多少都正常推荐
    gelienai()  # 1.2-0.4 0.6以上正常推荐，以下不推荐

    wb = xlrd.open_workbook(fileshujuku)
    sh1 = wb.sheet_by_index(0)
    # 递归显示每行数据
    for rownum in range(sh1.nrows):
        #print(sh1.row_values(rownum))  # 每一行的数据以数组形式存储
        hanglist = sh1.row_values(rownum)
        rsweidian=hanglist[2]
        gytbiaoxian=hanglist[4]
        #if rsweidian == 'rs1057910':
        #    w1=gytbiaoxian
        if rsweidian == 'rs5219':
            w2=gytbiaoxian
        if rsweidian == 'rs757110':
            w3=gytbiaoxian
        if rsweidian == 'rs1799854':
            w4=gytbiaoxian
        if rsweidian == 'rs12255372':
            w5=gytbiaoxian
        if rsweidian == 'rs7903146':
            w6=gytbiaoxian

        if rsweidian == 'rs72552763':
            sg1=re.sub('/','',gytbiaoxian)
            if 'Wt' in sg1:
                sg1=re.sub('Wt','W',sg1)
            if 'Del' in sg1:
                sg1=re.sub('Del','D',sg1)
        if rsweidian == 'rs316019':
            sg2=gytbiaoxian

        if rsweidian == 'rs1801282'  :
            ertong = gytbiaoxian

        if rsweidian == 'rs4149056':
            gln1=gytbiaoxian
        if rsweidian == 'rs1057910':
            gln2=gytbiaoxian
    ####result
    #huanganleiressult = w1 + ":" + w2 + ":" + w3 + ":" + w4 + ":" + w5 + ":" + w6
    huanganleiressult =w2 + ":" + w3 + ":" + w4 + ":" + w5 + ":" + w6
    huanganvalue = detectdict[huanganleiressult]
    if float(huanganvalue)>=1:
        print('磺酰脲类药物结果\t%.2f'%huanganvalue,'\t强烈推荐')
    elif  float(huanganvalue) >=0.3 and float(huanganvalue)<1:
        print('磺酰脲类药物结果\t%.2f'%huanganvalue,'\t正常推荐')
    elif float(huanganvalue) <0.3:
        print('磺酰脲类药物结果\t%.2f'%huanganvalue,'\t不推荐')

    erjiashaungguar = sg1+ ":" + sg2
    erjiashuanggv = detectdict[erjiashaungguar]
    if float(erjiashuanggv)>=0.96:
        print('二甲双胍药物结果\t%.2f'%erjiashuanggv,'\t正常推荐')
    elif float(erjiashuanggv)<0.96:
        print('二甲双胍药物结果\t%.2f'%erjiashuanggv,'\t不推荐')

    kuisewanv=detectdict[ertong]
    print('噻唑烷二酮类药物结果\t%.2f'%kuisewanv,'\t正常推荐')

    gelienair = gln1 +':'+gln2
    geilienaiv = detectdict[gelienair]

    if float(geilienaiv)>=0.6:
        print('格列奈类药物结果\t%.2f'%geilienaiv,'\t正常推荐')
    elif float(geilienaiv)<0.6:
        print('格列奈类药物结果\t%.2f'%geilienaiv,'\t不推荐')

chuli_databasefile(fileshujuku)