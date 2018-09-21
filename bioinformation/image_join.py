# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys,re
from PIL import Image
import numpy as np
"""
图片拼接程序
"""

def mergeReport(files,row,colume,outfile):
    baseimg=Image.open(files[0])
    width, height = baseimg.size
    sz=baseimg.size
    print(sz[0], sz[1])
    rowsize = row*sz[1] # 行乘以第一幅图片的高
    colsize = colume*sz[0] # 列乘以第一幅图片的宽
    toImage = Image.new('RGBA', (colsize,rowsize)) # 这个无论new还是paste，坐标第一个参数都是列乘以图片宽，即第一个决定画布宽，第二个决定画布高
    #basemat=np.atleast_2d(baseimg) #atleast_xd 支持将输入数据直接视为 x维。不用这个
    if row:
        print('the image have ',row,' rows.')
    else:
        row = int(len(files))/2+1 #设置行优先
    if colume:
        print('the image have ',colume,' columes.')
    else:
        colume=2
    i = 0
    for y in range(0,colume):
        for x in range(0,row):
            im = Image.open(files[i])
            #resize to same width
            print('begin paste',files[i])
            sz2 = im.size
            if sz2[0] == sz[0] and sz2[1] == sz[1]:
                #print(x,' ',y)
                toImage.paste(im,(y*width,x*height))  #宽，高
            else:
                im=im.resize((sz[0],round(sz2[0] / sz[0] * sz2[1])),Image.ANTIALIAS)
                #print('begin paste ',y,x)
                toImage.paste(im,(y*width,x*height))
            i = i+1
    toImage.save(outfile)
    #toImage.show()
    #没有对图像尺寸进行缩放，出来原图太大，用chrome打开缩略的试试可以
        #mat=np.atleast_2d(im)
        #basemat=np.append(basemat,mat,axis=0)
        #report_img=Image.fromarray(basemat)  #将图像矩阵转化成Image
        #report_img.save('merge.png')

image1 = 'E:\\haxqd\\201806\\ichrCNAPlot\\ovcc12_plasma_genomeWide.png'
image2 = 'E:\\haxqd\\201806\\ichrCNAPlot\\ovcc12_tissue_genomeWide.png'
image3 = 'E:\\haxqd\\201806\\ichrCNAPlot\\ovcc53_plasma_genomeWide.png'
image4 = 'E:\\haxqd\\201806\\ichrCNAPlot\\ovcc53_tissue_genomeWide.png'
image5 = 'E:\\haxqd\\201806\\ichrCNAPlot\\ovcc56_plasma_genomeWide.png'
image6 = 'E:\\haxqd\\201806\\ichrCNAPlot\\ovcc56_tissue_genomeWide.png'
image7 = 'E:\\haxqd\\201806\\ichrCNAPlot\\ovcc57_plasma_genomeWide.png'
image8 = 'E:\\haxqd\\201806\\ichrCNAPlot\\ovcc57_tissue_genomeWide.png'

#files=[image1,image2,image3,image4,image5,image6,image7,image8]
filenew1 ="E:\\haxqd\\201806\\ichrCNAPlot\\01ovcc12_corr.png"
filenew2 ="E:\\haxqd\\201806\\ichrCNAPlot\\01ovcc53_corr.png"
filenew3 ="E:\\haxqd\\201806\\ichrCNAPlot\\01ovcc56_corr.png"
filenew4 ="E:\\haxqd\\201806\\ichrCNAPlot\\01ovcc57_corr.png"
outfile = 'E:\\haxqd\\201806\\ichrCNAPlot\\01merge_cor0709.png'

kk01= 'E:\\haxqd\\201807\\RPOC\\Rplot.png'
kk02= 'E:\\haxqd\\201807\\RPOC\\Rplot01.png'
kk03= 'E:\\haxqd\\201807\\RPOC\\Rplot02.png'
kk04= 'E:\\haxqd\\201807\\RPOC\\Rplot03.png'

#outfile = 'E:\\haxqd\\201807\\RPOC\\Rplot_merge_.png'
files = [filenew1,filenew2,filenew3,filenew4]
mergeReport(files,1,4,outfile)
#mergeReport(file2)