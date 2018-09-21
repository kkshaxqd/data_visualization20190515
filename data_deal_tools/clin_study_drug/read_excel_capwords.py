# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
import string

import pandas as pd
excel_path = 'clin_drug_id_info_targets_and_AA.xls'
d = pd.read_excel(excel_path,header=0)
def stringdeal(x):
    x = x.lower()
    x = x.capwords()
    return x

d["Drugname"]=d["Drugname"].str.lower()
d["Drugname"]=d["Drugname"].str.capitalize()  #  列小写，首字母大写
#print(d)

writer = pd.ExcelWriter('clin_drug_id_info_targets_and_AA_output.xlsx')
d.to_excel(writer,'Sheet1',index_label=None,index = False)
writer.save()
