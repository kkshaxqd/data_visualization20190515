# !/usr/bin/env python
# -*- coding: utf8 -*-
from PIL import Image, ImageFilter

tupath = "E:\\20180815092803.jpg"  #PLEASE  注意中文，否则会出现莫名其妙的错误
"""
aa = Image.open(tupath)

#maxF =  aa.filter(ImageFilter.MaxFilter(5)) # 最大滤波值

#maxF.show()


# 轮廓滤波
#contF = aa.filter(ImageFilter.CONTOUR)
#contF.show()

#
im = aa.filter(ImageFilter.SHARPEN )
im.show()
"""
import numpy as np
import cv2

im = cv2.imread(tupath) #默认是0的话，直接得到灰度图。
#im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)   #转换了灰度化
#cv2.imshow("gray",im_gray)  #显示图片
#cv2.waitKey(0)

image = im.point(lambda x:255 if x>128 else 0)
image = image.convert('1')
image.show()
