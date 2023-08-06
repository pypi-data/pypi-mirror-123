# -*- encoding: utf-8 -*-
'''
@File        :Ks_allocation.py
@Time        :2021/09/28 11:21:18
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :全基因的ks
'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from famCircle.bez import *
import sys
from scipy.stats.kde import gaussian_kde

class Ks_allocation():
    def __init__(self, options):
        self.vertical = "False"
        self.model = "NG86"
        self.bins = "100"
        self.area = "-0.05,3.5"
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def read_family(self):
        family_list = []
        for line in open(self.family_list,'r'):
            if line != '\n' and '#' not in line:
                line = line.strip('\n').split()
                if line[0] in family_list:
                    continue
                family_list.append(line[0])
        return family_list

    def readks(self,list0):
        read_ks = []
        f = open(self.ks, 'r', encoding='utf-8')
        for row in f:
            if row[0] != '#' and row[0] != '\n':
                row = row.strip('\n').split('\t')
                if row[0] != 'id1' and len(row) != 2:
                    if row[0] in list0 or row[1] in list0:
                        print(row)
                        read_ks.append(row)
        kspd = pd.DataFrame(read_ks)
        kspd.rename(columns={0: 'id1', 1: 'id2',
                                2: 'ka_NG86', 3: 'ks_NG86',
                                4: 'ka_YN00', 5: 'ks_YN00'}, inplace=True)
        return kspd

    # 绘制核密度曲线图
    def KdePlot(self,x):
        # 绘制核密度分布直方图
        plt.figure(figsize=(20,10),dpi=1000)
        plt.grid(c='grey',ls='--',linewidth=0.2)
        dist_space = np.linspace(float(self.area.split(',')[0]),float(self.area.split(',')[1]), 500)
        kdemedian = gaussian_kde(x)
        kdemedian.set_bandwidth(bw_method=kdemedian.factor / 3.)
        plt.fill_between(dist_space, y1=0, y2=kdemedian(dist_space), facecolor='#00a3af', alpha=0.5)
        xx = list(dist_space)[list(kdemedian(dist_space)).index(max(list(kdemedian(dist_space))))]
        xx0 = round(xx,4)
        plt.plot(dist_space, kdemedian(dist_space), color='#00a3af',
                 label='KED_' + str(xx0))
        plt.legend()
        plt.title(self.species_list.replace(",", "_") + ' Ks kernel density estimation')# 设置图片标题
        plt.xlabel('ks')# 设置 x 轴标签
        plt.ylabel('density')# 设置 y 轴标签

    def run(self):
        family_list = self.read_family()
        kspdx = self.readks(family_list)
        if self.model == "NG86":
            kspdx["ks_NG86"] = kspdx["ks_NG86"].astype(float)
            kspdx = kspdx[(kspdx["ks_NG86"] > 0) & (kspdx["ks_NG86"] < 99)]
            y = sorted(list(kspdx["ks_NG86"]))
        elif self.model == "YN00":
            kspdx["ks_YN00"] = kspdx["ks_YN00"].astype(float)
            kspdx = kspdx[(kspdx["ks_YN00"] > 0) & (kspdx["ks_YN00"] < 99)]
            y = sorted(list(kspdx["ks_YN00"]))
        self.KdePlot(y)
        plt.savefig(self.savefile)# 存储图片
        sys.exit(0)
