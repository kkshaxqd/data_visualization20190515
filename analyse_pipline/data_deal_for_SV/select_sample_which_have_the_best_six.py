# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re,sys
"""
分析excel中样本，sv数据，统计样本在六个sv中分部情况
"""

"""
chr12:104359630_chr12:125801148，
chr11:99690483_chr11:99691307，
chr6:43655533_chr9:33130549，
chr11:108585748_chr13:21750661，
chr5:141456960_chr13:82367698，
chr7:26241365_chr15:40854180
"""
import xlrd
fileshujuku = "newstat_sv_for_manta_lumpy.xlsx"
fileout = "select_sv_sample_result_jieguo.txt"
with open(fileout, 'w', encoding='utf-8')as hh:
    outhh = "样本名称"+"\t"+"样本ID"+"\t"+"chr12:104359630_chr12:12580114"+"\t"+"chr11:99690483_chr11:99691307"+"\t"+"chr6:43655533_chr9:33130549"+"\t"+"chr11:108585748_chr13:21750661"+"\t"+"chr5:141456960_chr13:82367698"+"\t"+"chr7:26241365_chr15:40854180"+"\n"
    hh.write(str(outhh))

def chuli_databasefile(fileshujuku):
    sampleid = 1
    wb = xlrd.open_workbook(fileshujuku)
    sh1 = wb.sheet_by_index(0)
    # 递归显示每行数据
    for rownum in range(sh1.nrows)[1:]:
        #print(sh1.row_values(rownum))  # 每一行的数据以数组形式存储
        hanglist = sh1.row_values(rownum)
        svset = hanglist[1].split(',')
        flag1=0;flag2=0;flag3=0;flag4=0;flag5=0;flag6=0
        for sv in svset:
            if sv == "12:104359630_12:125801148" :flag1 = 1
            if sv == "11:99690483_11:99691307" :flag2 = 1
            if sv == "6:43655533_9:33130549" :flag3 = 1
            if sv == "11:108585748_13:21750661" :flag4 = 1
            if sv == "5:141456960_13:82367698" :flag5 = 1
            if sv == "7:26241365_15:40854180" :flag6 = 1
        with open(fileout, 'a', encoding='utf-8')as hh:
            outhh = hanglist[0]+"\t"+str(sampleid)+"\t"+str(flag1)+"\t"+str(flag2)+"\t"+str(flag3)+"\t"+str(flag4)+"\t"+str(flag5)+"\t"+str(flag6)+"\n"
            hh.write(str(outhh))
        sampleid += 1


chuli_databasefile(fileshujuku)
