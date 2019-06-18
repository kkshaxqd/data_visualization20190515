# !/usr/bin/env python
# -*- coding: utf8 -*-
import os, re, sys

import argparse
parser = argparse.ArgumentParser(description='manual to this script, use like python GZ_xiaofeizhe_gene_use.py -filepath E://xxx//xxx//xxx// -samplename xxx.txt -sex woman')
parser.add_argument('-filepath', type=str, default = None,help='输入文件路径，windows下为//或者\ ')
parser.add_argument('-samplename',type=str,default = None,help='读入文件名，23芯片格式文件名带txt')
parser.add_argument('-sex', type=str, default = 'man',help='性别，man or woman ,默认为男')
args = parser.parse_args()

orsstr1='python '+'GZ_customorgene_analyse_01.py '+'-filepath '+str(args.filepath)+' -samplename '+str(args.samplename)+' -sex '+str(args.sex)
#print(orsstr1)
orsstr2='python '+'GZ_customorgene_analyse_02.py '+'-filepath '+str(args.filepath)+' -samplename '+str(args.samplename)+' -sex '+str(args.sex)
orsstr3='python '+'GZ_customorgene_analyse_03.py '+'-filepath '+str(args.filepath)+' -samplename '+str(args.samplename)+' -sex '+str(args.sex)

##药物评估脚本
perlinfile = str(args.filepath)+str(args.samplename)
perlsamplename = re.sub('.txt','',args.samplename)
perloutfile = str(args.filepath)+str(perlsamplename)
orsstr4='perl '+'E://haxqd//python//data_visualization//analyse_pipline//GEZHI_XFZ_project_result//popular_genetic_testing//drug_guideline//drug_evaluator_v1.1.pl '+'--genotype '+str(perlinfile)+' --odir '+str(perloutfile) +' --prefix '+str(perlsamplename)


os.system(orsstr1)
os.system(orsstr2)
os.system(orsstr3)
os.system(orsstr4)
