# !/usr/bin/env python
# -*- coding: utf8 -*-
## __author__: 'zhangqiaoshi'
## mail: zhangqiaoshi@gezhigene.com
import os,re,sys
"""
分析注释结果，过滤低质量sv结果，根据参数的不同
python analyse_sv_result.py -qual 5 -mp 10 -sp 10 -path lumpy_result_dir -o lumpy_result_select
python analyse_sv_result.py -qual 5 -mp 10 -sp 10 -path manta_result_dir -o manta_result_select
使用自建Python脚本对注释结果进行分析和统计，
首先对结果进行质控，对每个sv结果筛选质量条件为5以上(-qual 5 )，
前后最小匹配区域在10bp以上(-mp 10)，
断点区域支持reads数目 10以上(-sp 10 )的sv进行后续分析
"""
import argparse
parser = argparse.ArgumentParser(description='manual to this script, use like python analyse_sv_result.py -qual 5 -mp 10 -sp 10 -path lumpy_result_dir -o lumpy_result_select or python analyse_sv_result.py -qual 5 -mp 10 -sp 10 -path manta_result_dir -o manta_result_select ')
parser.add_argument('--verbose', '-v', action='store_true', help='verbose mode 20190610')
parser.add_argument('-qual', type=int, default = 5,help='sv质量阈值')
parser.add_argument('-mp', type=int, default = 10,help='sv匹配阈值')
parser.add_argument('-sp', type=int, default = 10,help='sv支持reads阈值')
parser.add_argument('-analyse',type=str,default = None,help='如果想要需要分析结果数据，在得到输出文件后启用这个来进行分析即可')
parser.add_argument('-path', type=str, default = None,help='必须是目录')
parser.add_argument('-file', type=str, default = None,help='单独文件分析，不能与-path共同出现')
parser.add_argument('--out','-o', type=str, default = None,help='结果，如果输入是目录，输出也指定为目录，如果输入是文件，输出指定为文件')
args = parser.parse_args()

def dealsvvcfdir():
    dirpath = args.path
    resultdri=args.out
    for file in dirpath:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            fileout = re.sub('.vep.sv.vcf', '', file)
            fileoutfile = resultdri+ "\\" + fileout + "_result_select.txt"
            with open(fileoutfile,'w', encoding='UTF-8') as ww:
                outstr = "#theselectresult v1.0"+'\n'
                ww.write(str(outstr))
            #print('分析样本',fileout)
            f = open(dirpath + "\\" + file, 'r', encoding='UTF-8')  # 打开文件
            lines = f.readlines()
            for line in lines:
                if "#" in line:
                    pass
                else:
                    line = line.strip('\n')
                    linelist = line.split("\t")
                    if linelist[5]<args.qual:
                        pass
                    else:
                        selectset = linelist[7].split(';')
                        if 'BAND' not in selectset[0]:
                            pass
                        else:
                            moreselectset = linelist[9].split(':')
                            if int(moreselectset[-2])+int(moreselectset[-3])<args.mp:
                                pass
                            elif int(moreselectset[6])<args.sp:
                                pass
                            else:
                                with open(fileoutfile, 'a', encoding='UTF-8') as ww:
                                    outstr = line + '\n'
                                    ww.write(str(outstr))

def  dealsvvcffile():
    file = args.file
    resultfile = args.out
    with open(resultfile, 'w', encoding='UTF-8') as ww:
        outstr = "#theselectresult v1.0" + '\n'
        ww.write(str(outstr))
    f = open(file, 'r', encoding='UTF-8')  # 打开文件
    lines = f.readlines()
    for line in lines:
        if "#" in line:
            pass
        else:
            line = line.strip('\n')
            linelist = line.split("\t")
            if linelist[5] < args.qual:
                pass
            else:
                selectset = linelist[7].split(';')
                if 'BAND' not in selectset[0]:
                    pass
                else:
                    moreselectset = linelist[9].split(':')
                    if int(moreselectset[-2]) + int(moreselectset[-3]) < args.mp:
                        pass
                    elif int(moreselectset[6]) < args.sp:
                        pass
                    else:
                        with open(resultfile, 'a', encoding='UTF-8') as ww:
                            outstr = line + '\n'
                            ww.write(str(outstr))


def main():
    if  args.path:
        dealsvvcfdir()
    elif args.file:
        dealsvvcffile()

if __name__ == "__main__" :
    main()