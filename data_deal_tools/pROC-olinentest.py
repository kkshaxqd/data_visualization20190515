# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
import pandas as pd
from sklearn.metrics import roc_curve, auc

io = "E:\\haxqd\\201806\\0622cscore\\data-zhenghe.xlsx"
d=pd.read_excel(io,sheet_name=0,header=0) # 返回的是一个表格，sheet_name为none的话返回的是一个字典表格

#还是R的方便好用些



