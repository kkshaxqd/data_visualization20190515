# !/usr/bin/env python
# -*- coding: utf8 -*-
# use like this: python create_contral_base.py dirpath outbasefile
import sys, getopt
import os, re

""" 参数读取 帮助说明"""
# dirpath = sys.argv[1]
# outfile = sys.argv[2]
def usage():
    print("The version v1.0")
    print("The script use like this: python create_contral_base.py -i dirpath -o outbasefile \n")


try:
    if sys.argv[1] is None:
        print("Give the args")
except IndexError:
    usage()
    sys.exit()

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
dirpath = ""
outfile = ""
for op, value in opts:
    if op == "-i":
        dirpath = value
    elif op == "-o":
        outfile = value
    elif op == "-h":
        usage()
        sys.exit()

"""遍历文件夹寻找特定文件,然后处理文件"""


def chuli_file(dirpath, file):
    # 打开并处理文件
    fa = dirpath + "/" + file
    with open(fa, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            if re.findall('NA|start|X', line)：
            continue
        elif

    files = os.listdir(dirpath)
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            if re.findall('correctedDepth.txt', file):
