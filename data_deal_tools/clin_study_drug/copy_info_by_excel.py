# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re

import pandas as pd
excel_path = 'E:\\haxqd\\myscript\\GEZHI_Script\\clin_drug_id_info_targets_and_AA_output.xlsx'
d = pd.read_excel(excel_path,header=0)

excel_add = u'E:\\haxqd\\myscript\\GEZHI_Script\\靶向药20180510.xlsx'

ad = pd.read_excel(excel_add,sheet_name="All-info") # 取第二个sheet表，第一行作为标题

#want_info = {}
gene_name = {}
aa_mutation = {}
cln_result = {}
are_in = {}
are_fda = {}
drug_stats = {}
for i in range(len(ad["line number"])):
    drugname = ad.ix[i,"Drug Name"]
    try:
        if gene_name[drugname]:
            gene_name[drugname] = gene_name[drugname] + "//" + ad.ix[i,"Gene Name"]
    except KeyError:
        gene_name[drugname] = ad.ix[i,"Gene Name"]
    try:
        if aa_mutation[drugname]:
            aa_mutation[drugname] = aa_mutation[drugname] + "//" + ad.ix[i,"AA Mutation"]
    except KeyError:
        aa_mutation[drugname] = ad.ix[i,"AA Mutation"]
    try:
        if cln_result[drugname]:
            cln_result[drugname] = cln_result[drugname] + "//" + str(ad.ix[i,u"临床疗效"])
    except KeyError:
        cln_result[drugname] = str(ad.ix[i,u"临床疗效"])
    try:
        if are_in[drugname]:
            are_in[drugname] = are_in[drugname] + "//" + ad.ix[i,u"中国是否上市"]
    except KeyError:
        are_in[drugname] = ad.ix[i,u"中国是否上市"]
    try:
        if are_fda[drugname]:
            are_fda[drugname] = are_fda[drugname] + "//" + ad.ix[i,u"FDA批准适应症"]
    except KeyError:
        are_fda[drugname] = ad.ix[i,u"FDA批准适应症"]
    try:
        if drug_stats[drugname]:
            drug_stats[drugname] = drug_stats[drugname] + "//" + str(ad.ix[i,"Drug status"])
    except KeyError:
        drug_stats[drugname] = str(ad.ix[i,"Drug status"])

#    print(ad.ix[i,["Drug Name","Gene Name","AA Mutation",u"临床疗效",u"中国是否上市",u"FDA批准适应症","Drug status"]])

for j in range(len(d['Drugname'])):
    drugname = d.ix[j,'Drugname']
    try:
        if gene_name[drugname]:
            d.ix[j,"Drug Name"] = drugname
            d.ix[j, "Gene Name"] = gene_name[drugname]
            d.ix[j, "AA Mutation"] = aa_mutation[drugname]
            d.ix[j, u"临床疗效"] = cln_result[drugname]
            d.ix[j, u"中国是否上市"] = are_in[drugname]
            d.ix[j, u"FDA批准适应症"] = are_fda[drugname]
            d.ix[j, "Drug status"] = drug_stats[drugname]
    except KeyError:
        pass

#print(ad.head())

writer = pd.ExcelWriter('E:\\haxqd\\myscript\\GEZHI_Script\\clin_drug_id_info_targets_and_AA_addinfo_all_info.xlsx')
d.to_excel(writer,'Sheet1',index_label=None,index = False)
writer.save()
#print(d.head())