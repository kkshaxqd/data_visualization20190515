# !/usr/bin/env python
# -*- coding: utf8 -*-

import numpy as np
import pandas as pd

##导入数据
dataset = pd.read_csv('Data.csv')
X = dataset.iloc[ : , :-1].values ## 除了最后一列的值
Y = dataset.iloc[ : , 3].values
#print(X[ : , 1:3],Y)

## 处理缺失数据
from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values = "NaN", strategy = "mean", axis = 0)
imputer = imputer.fit(X[ : , 1:3])
#print(imputer)
#Imputer(axis=0, copy=True, missing_values='NaN', strategy='mean', verbose=0)
X[ : , 1:3] = imputer.transform(X[ : , 1:3])
#print(X[ : , 1:3],Y)

##解析分类数据
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[ : , 0] = labelencoder_X.fit_transform(X[ : , 0])
print(X[:,0])
#[0 2 1 2 1 0 2 0 1 0]
###创建虚拟变量
onehotencoder = OneHotEncoder(categorical_features = [0])
print(0,onehotencoder)
X = onehotencoder.fit_transform(X).toarray()  #也许是某种编码
print(1,X[:,0])
labelencoder_Y = LabelEncoder()
print(2,labelencoder_Y)
Y =  labelencoder_Y.fit_transform(Y)
print(3,Y)