# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
"""
对于大部分数据分析应用而言，最关注的功能主要集中在：
用于数据整理和清理、子集构造和过滤、转换等快速的矢量化数组运算。
常用的数组算法，如排序、唯一化、集合运算等。
高效的描述统计和数据聚合/摘要运算。
用于异构数据集的合并/连接运算的数据对齐和关系型数据运算。
将条件逻辑表述为数组表达式（而不是带有if-elif-else分支的循环）。
数据的分组运算（聚合、转换、函数应用等）。。
作者：SeanCheney
链接：https://www.jianshu.com/p/a380222a3292
來源：简书
"""
my_arr = np.arange(1000000)

my_list = list(range(1000000))

#for _ in range(10): my_arr2 = my_arr * 2
#for _ in range(10): my_list2 = [x * 2 for x in my_list]


arr = np.array([[1., 2., 3.], [4., 5., 6.]])
print(arr[1][2])
print(arr[1,2])  # 这是等价的，二维数组的索引方式。轴0作为行，轴1作为列。
# np数组切片与修改会直接作用于原数组上，因为np操作的是内存，复制的话，明确拷贝
#　arr[2:3].copy()

def plotimshow():
    points = np.arange(-5, 5, 0.01)
    xs, ys = np.meshgrid(points, points)
    z = np.sqrt(xs ** 2 + ys ** 2)
    plt.imshow(z)
    plt.colorbar()
    plt.title("Image plot of $\sqrt{x^2 + y^2}$ for a grid of values")
    plt.show()

cond = np.array([True, False, True, True, False])

print(cond.dtype)

obj = pd.Series([4, 7, -5, 3])

print(obj)

pd.isnull(obj)

sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}

obj3 = pd.Series(sdata)

ddd = obj+obj3

ddd = pd.DataFrame(ddd,columns=['value'])

print(ddd)

df1 = pd.DataFrame(np.arange(12.).reshape((3, 4)),columns=list('abcd'))

df2 = pd.DataFrame(np.arange(20.).reshape((4, 5)),columns=list('abcde'))

#print(df2)

df2.loc[1, 'b'] = np.nan  # 赋予空值NaN

#print(df2)

#df1+df2

"""使用df1的add方法，传入df2以及一个fill_value参数："""
#df1.add(df2, fill_value=0)

"""在对Series或DataFrame重新索引时，也可以指定一个填充值"""
#df1.reindex(columns=df2.columns, fill_value=0)
def get_yahoo():
    frame = pd.DataFrame({'b': [4, 7, -3, 2], 'a': [0, 1, 0, 1]})

    import pandas_datareader.data as web
    import  datetime
    import fix_yahoo_finance as yf
    yf.pdr_override()
    start=datetime.datetime(2006, 10, 1)
    end=datetime.datetime(2012, 1, 1)
    #web.get_data_yahoo('AAPL',start,end)

    all_data = {ticker: web.get_data_yahoo(ticker,start,end)
            for ticker in ['AAPL', 'IBM', 'MSFT', 'GOOG']}

    price = pd.DataFrame({ticker: data['Adj Close']
                     for ticker, data in all_data.items()})
    volume = pd.DataFrame({ticker: data['Volume']
                      for ticker, data in all_data.items()})

#print(price.index)

# test pandas
import json
path = 'chr02usrdata.txt'
records = [json.loads(line) for line in open(path)]
from collections import defaultdict
def get_count(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts
def top_counts(count_dict, n=10):
    value_key_pairs = [(count,tz) for tz,count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-10:]
time_zones = [rec['tz'] for rec in records if 'tz' in rec]
counts = get_count(time_zones)
print(counts['America/New_York'])
print(top_counts(counts))
from collections import Counter
counts = Counter(time_zones)
print(counts.most_common(10))
from pandas import DataFrame, Series
import pandas as pd
import numpy as np

frame = DataFrame(records)

tz_counts = frame['tz'].value_counts()
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()

tz_counts[:10].plot(kind = 'barh',rot=0)
plt.show()
results = Series([x.split()[0] for x in frame.a.dropna()])
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
print(operating_system[:5])
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts[:10])
indexer = agg_counts.sum(1).argsort()
count_subset = agg_counts.take(indexer)[-10:]
print(count_subset)
count_subset.plot(kind='barh', stacked=True)
plt.show()

normed_subset = count_subset.div(count_subset.sum(1),axis=0)
normed_subset.plot(kind='barh',stacked=True)
print(count_subset.sum(1))
plt.show()