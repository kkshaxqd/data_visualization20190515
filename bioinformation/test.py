#!/usr/bin/env python
# --coding:utf-8 --

import os,re
def test1():
    inputfile01 ="E:\\haxqd\\myscript\\GeneticdetectionPipline\\test.hg19_multianno.txt.variant_function"
    inputfile01_adjust ="E:\\haxqd\\myscript\\GeneticdetectionPipline\\test.hg19_multianno.txt.variant_function_adjusttt"
    os.system('perl -F"\t" -alne "{$out=join(\"\t\",@F[0..127]);print \"$out\"}" %s > %s' %(inputfile01,inputfile01_adjust))

def test2():
    site1="c.657A>C"
    newsite1=re.sub(r'c.(\d+)(\w)>\S+',r'c.\2\1',site1)
    print(newsite1)

#test2()

def test3():
    import os
    file1="test1.txt"
    file2="test2.txt"
    file3="test3.txt"
    os.system('paste -d "\t" %s %s > %s'%(file1,file2,file3))

def test4():
    str1="Benign/Likely_benign"
    str2="Benign sdfag"
    if "benign" in str1:
        print("ok1")
    if "Benign" in str2:
        print("ok2")

test4()