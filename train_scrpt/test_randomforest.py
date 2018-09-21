# !/usr/bin/env python
# -*- coding: utf8 -*-

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

iris = load_iris()   # 这里是sklearn中自带的一部分数据
df = pd.DataFrame(iris.data, columns=iris.feature_names) # 格式化数据
#print (df)          #
# 新增的两列
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)  ## 新接口 数据 # pandas的高级应用
print(df.head())

train, test = df[df['is_train']==True], df[df['is_train']==False]

features = df.columns[:4]
clf = RandomForestClassifier(n_jobs=2) # 并行job个数。1=不并行；n：n个并行；-1：CPU有多少core，就启动多少job
y, _ = pd.factorize(train['species']) # factorize函数的返回值是一个tuple（元组），元组中包含两个元素。第一个元素是一个array，其中的元素是标称型元素映射为的数字；第二个元素是Index类型，其中的元素是所有标称型元素，没有重复。
# _ 单下划线表示临时变量，不用在意
clf.fit(train[features], y)  # 用train来训练样本

test_pred=clf.predict(test[features])   #用测试数据来做预测
preds = iris.target_names[test_pred]
aa = pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds'])
print(aa)