# !/usr/bin/env python
# -*- coding: utf8 -*-
# @author: zqs
# @email: 514079685@qq.com
import pandas as pd
data = pd.DataFrame({'Qu1': [1, 3, 4, 3, 4],
                      'Qu2': [2, 3, 1, 2, 3],
                      'Qu3': [1, 5, 2, 4, 4]})

result = data.apply(pd.value_counts).fillna('null')

print(result)

obj = """
{"name": "Wes",
 "places_lived": ["United States", "Spain", "Germany"],
 "pet": null,
 "siblings": [{"name": "Scott", "age": 30, "pets": ["Zeus", "Zuko"]},
              {"name": "Katie", "age": 38,
               "pets": ["Sixes", "Stache", "Cisco"]}]
}
"""
import json
result = json.loads(obj)

print(result)

import requests
url = 'https://api.github.com/repos/pandas-dev/pandas/issues'
resp = requests.get(url)
data = resp.json()
issues = pd.DataFrame(data, columns=['number', 'title',
                                     'labels', 'state'])
print(issues)

import sqlite3
query = """
  CREATE TABLE test
  (a VARCHAR(20), b VARCHAR(20),
  c REAL,        d INTEGER
  );"""
con = sqlite3.connect('mydata.sqlite')
#print(con.execute(query))
con.commit()
data = [('Atlanta', 'Georgia', 1.25, 6),
         ('Tallahassee', 'Florida', 2.6, 3),
         ('Sacramento', 'California', 1.7, 5)]

stmt = "INSERT INTO test VALUES(?, ?, ?, ?)"

con.executemany(stmt, data)

cursor = con.execute('select * from test')
rows = cursor.fetchall()

newdata=pd.DataFrame(rows, columns=[x[0] for x in cursor.description])

print(newdata)

import sqlalchemy as sqla

db = sqla.create_engine('sqlite:///mydata.sqlite')

pd.read_sql('select * from test', db)

import numpy as np
empty_unit32 = np.empty(8,dtype='u4')

print(empty_unit32)