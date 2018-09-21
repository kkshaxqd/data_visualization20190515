# !/usr/bin/env python
# -*- coding: utf8 -*-
from matplotlib_venn import venn2,venn3
import pylab as plt
figure, axes = plt.subplots(2, 2)
venn2(subsets=(4,16,8),set_labels = ('ovcc12 plasma', 'ovcc12 tissue'), ax=axes[0][0])
venn2(subsets=(1,9,4),set_labels = ('ovcc57 plasma', 'ovcc57 tissue'), ax=axes[1][1])
venn2(subsets=(0,54,14),set_labels = ('ovcc56 plasma', 'ovcc56 tissue'), ax=axes[0][1])
venn2(subsets=(7,10,17),set_labels = ('ovcc53 plasma', 'ovcc53 tissue'), ax=axes[1][0])
#plt.title('Venn figures')
plt.savefig('E:\haxqd\\venn_tu1.png')
