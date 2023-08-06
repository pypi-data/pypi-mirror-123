# -*- encoding: utf-8 -*-
'''
@File        :line.py
@Time        :2021/07/11 12:44:00
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :共线性局部
'''

import csv
import sys
import re
from math import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import *
from matplotlib.patches import Circle, Ellipse, Arc
from pylab import *
from famCircle.bez import *

class line():
    def __init__(self, options):
        self.makers = 200
        class1 = False
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def lower_(self,name):
        name = name.lower()
        return name

    def readgff_(self,file):
        myList = []
        for line in open(file,'r'):
            lt = line.strip('\n').split()
            lt[0],lt[1] = lt[1],lt[0]
            lt[0] = self.lower_(lt[0])
            myList.append(lt)
        matrix_gff0 = pd.DataFrame(data = myList)
        matrix_gff0 = matrix_gff0.set_index(0)
        return matrix_gff0

    def read_csv(self):
        self.chrolist = [self.chr1_name,self.chr2_name]
        gff1 = read_gff(self.gff1)
        gff2 = read_gff(self.gff2)
        gff = dict( gff1, **gff2 )
        print(gff)
        matrix_chr1 = pd.read_csv(self.lens1, sep='\t', header=None, index_col=0)
        length1 = matrix_chr1.loc[self.chr1_name,2]
        matrix_chr2 = pd.read_csv(self.lens2, sep='\t', header=None, index_col=0)
        length2 = matrix_chr2.loc[self.chr2_name,2]
        if length1 >= length2:
            x1 = 0.8
            x2 = length2*(0.8/length1)
            maker_str = True
        else :
            x1 = 0.8
            x2 = length1*(0.8/length2)
            maker_str = False
        maker1 ,maker2 = int(max(length2,length1)/self.makers), int(min(length2,length1)/self.makers)
        chro1 = self.chr1_name
        chro2 = self.chr2_name
        matrix_gff1 = self.readgff_(self.gff1)
        matrix_gff2 = self.readgff_(self.gff2)
        matrix_gff1.groupby(by=0)
        matrix_gff2.groupby(by=0)
        return x1,x2,maker1,maker2,matrix_gff1,matrix_gff2,chro1,chro2,maker_str,length1,length2

    def read_colinearity(self,file):
        pair = []
        pair_list = []
        if self.pairfile_type == 'famCircle':
            with open(file) as f:
                for line in f.readlines():
                    line = line.strip()
                    if  line[0] == "\n":
                        continue
                    elif line[0] == "#":
                        if len(pair_list) != 0:
                            # print(pair_list)#输出
                            pair.append(pair_list)
                        pair_list = []
                        block_dict = {}
                        lt = line.split()
                        block_number = str(lt[2])[:-1]
                        # print(lt)
                        for i in lt:
                            if "=" in i:
                                lt0 = i.split('=')
                                block_dict[str(lt0[0])] = str(lt0[1])
                        if int(block_dict['N']) > int(self.block):
                            class1 = True
                        else:
                            class1 = False
                    else:
                        if class1:
                            lt = line.split()
                            name1 = readname(str(lt[0]),self.chr1_name+self.chr2_name)
                            name2 = readname(str(lt[1]),self.chr1_name+self.chr2_name)
                            lt0 = [name1,name2]
                            # print(lt0)
                            pair_list.append(lt0)
                if len(pair_list) != 0 and class1:
                    # print(pair_list)#输出
                    pair.append(pair_list)
                # print(pair)
                return pair
        elif self.pairfile_type == 'WGDI':
            with open(file) as f:
                for line in f.readlines():
                    line = line.strip()
                    if  line[0] == "\n":
                        continue
                    elif line[0] == "#":
                        if len(pair_list) != 0:
                            # print(pair_list)#输出
                            pair.append(pair_list)
                        pair_list = []
                        block_dict = {}
                        lt = line.split()
                        block_number = str(lt[2])[:-1]
                        # print(lt)
                        for i in lt:
                            if "=" in i:
                                lt0 = i.split('=')
                                block_dict[str(lt0[0])] = str(lt0[1])
                        if int(block_dict['N']) > int(self.block):
                            class1 = True
                        else:
                            class1 = False
                    else:
                        if class1:
                            lt = line.split()
                            name1 = readname(str(lt[0]),self.chr1_name+self.chr2_name)
                            name2 = readname(str(lt[2]),self.chr1_name+self.chr2_name)
                            lt0 = [name1,name2]
                            # print(lt0)
                            pair_list.append(lt0)
                if len(pair_list) != 0 and class1:
                    # print(pair_list)#输出
                    pair.append(pair_list)
                # print(pair)
                return pair
        elif self.pairfile_type == 'MCScanX':
            with open(file) as f:
                for line in f.readlines():
                    line = line.strip()
                    if line[0] == "\n":
                        continue
                    elif line[:12] == '## Alignment':
                        # print(line)
                        if len(pair_list) != 0:
                            pair.append(pair_list)
                        pair_list = []
                        block_dict = {}
                        lt = line.split()
                        block_number = str(lt[2])[:-1]
                        # print(lt)
                        for i in lt:
                            if "=" in i:
                                lt0 = i.split('=')
                                block_dict[str(lt0[0])] = str(lt0[1])
                        if int(block_dict['N']) > int(self.block):
                            class1 = True
                        else:
                            class1 = False
                    else:
                        if class1:
                            lt = line.split()
                            if len(lt) == 5:
                                id1, id2 = str(lt[2]),str(lt[3])
                            elif len(lt) == 4:
                                id1, id2 = str(lt[1]),str(lt[2])
                            elif len(lt) == 6:
                                id1, id2 = str(lt[3]),str(lt[4])
                            else:
                                print(line)
                                print('Parse error!')
                                exit()
                            name1 = readname(id1,self.chr1_name+self.chr2_name)
                            name2 = readname(id2,self.chr1_name+self.chr2_name)
                            lt0 = [name1,name2]
                            pair_list.append(lt0)
                if len(pair_list) != 0 and class1:
                    pair.append(pair_list)
                return pair

        if self.pairfile_type == 'ColinearScan':
            with open(file) as f:
                for line in f.readlines():
                    line = line.strip()
                    # print(line)
                    if line[0] == "+" or line[0] == "\n" or line[0] == ">":
                        continue
                    elif line[:3] == "the":
                        if len(pair_list) != 0:
                            pair.append(pair_list)
                        pair_list = []
                        block_dict = {}
                        lt = line.split()
                        block_number = str(lt[1])[:-2]
                        # print(lt)
                        for i in lt:
                            if "=" in i:
                                lt0 = i.split('=')
                                block_dict[str(lt0[0])] = str(lt0[1])
                        if int(lt[-1]) > int(self.block):
                            class1 = True
                        else:
                            class1 = False
                    else:
                        if class1:
                            lt = line.split()
                            name1 = readname(str(lt[0]),self.chr1_name+self.chr2_name)
                            name2 = readname(str(lt[2]),self.chr1_name+self.chr2_name)
                            lt0 = [name1,name2]
                            # print(lt0)
                            pair_list.append(lt0)
                if len(pair_list) != 0 and class1:
                    # print(pair_list)#输出
                    pair.append(pair_list)
                # print(pair)
                return pair
        elif self.pairfile_type == 'BLAST':
            num = 0
            name_list = []
            with open(file) as f:
                for line in f.readlines():
                    line = line.strip()
                    if  line[0] == "\n":
                        continue
                    lt = line.split()
                    if lt[0] == lt[1]:
                        continue
                    if str(lt[0]) not in name_list:
                        name_list.append(str(lt[0]))
                        num = 1
                    else:
                        if num <= int(self.block):
                            name1 = readname(str(lt[0]),self.chr1_name+self.chr2_name)
                            name2 = readname(str(lt[1]),self.chr1_name+self.chr2_name)
                            lt0 = [name1,name2]
                            pair.append(lt0)
                        else:
                            continue
                return pair
        else:
            print('genepairsfile_type error: File Format not recognized!')
            exit()

    def plot_bez_inner(self, ex1x, ex1y, ex2x, ex2y):
        x = [ex1x, ex1x+((ex2x - ex1x)/3+0.1), ex2x-((ex2x - ex1x)/3+0.1), ex2x]
        y = [ex1y, ex1y+((ex2y - ex1y)/3), ex2y-((ex2y - ex1y)/3), ex2y]
        # ratiox = 0.5
        # ratioy = 1
        # x = [ex1x, ex1x*ratiox, ex2x*ratiox, ex2x]
        # y = [ex1y, ex1y*ratioy, ex2y*ratioy, ex2y]
        # x = [ex1x, ex1x+((ex2x - ex1x)/3), ex2x-((ex2x - ex1x)/3), ex2x]
        # y = [ex1y, ex1y+((ex2y - ex1y)/3), ex2y-((ex2y - ex1y)/3), ex2y]
        step = .01
        t = arange(0, 1+step, step)
        xt = self.Bezier(x, t)# 贝塞尔曲线
        yt = self.Bezier(y, t)
        plot(xt, yt, '-', color='#7ebea5', lw=1, alpha=0.3)#alpha 透明度

    def calculate_coef(self,p0, p1, p2, p3):
        c = 3*(p1 - p0)
        b = 3*(p2 - p1) -c
        a = p3 - p0 - c - b
        return c, b, a
    def Bezier(self,plist, t):
        # p0 : origin, p1, p2 :control, p3: destination
        p0, p1, p2, p3 = plist
        # calculates the coefficient values
        c, b, a = self.calculate_coef(p0, p1, p2, p3)
        tsquared = t**2
        tcubic = tsquared*t
        return a*tcubic + b*tsquared + c*t + p0

    def make_plot(self,maker1,maker2,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2):
        fig1 = plt.figure(num=1, figsize=(10, 10))  # 确保正方形在屏幕上显示一致，固定figure的长宽相等
        axes1 = fig1.add_subplot(1, 1, 1)
        plt.xlim((0, 1))
        plt.ylim((0, 1))
        self.map1(axes1,maker1,0.1,0.3,x1,'#ffec47')# 长染色体0.8
        self.map1(axes1,maker2,0.1+((0.8-x2)/2),0.65,x2,'#ffec47')# 短染色体
        if maker_str:
            plt.text(0.45, 0.28, chro1)
            plt.text(0.45, 0.67, chro2)
        else:
            plt.text(0.45, 0.28, chro2)
            plt.text(0.45, 0.67, chro1)
        plt.axis('off')
        self.pair_index(axes1,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2)
        plt.savefig(self.savefile,dpi=1000)

    def map1(self,axes1,maker,x,y,x1,color):
        # makers = 15 #标尺
        # x = 0.1 #起始坐标x
        # y = 0.1 #起始坐标y
        # x1 = 0.8#染色体长度
        # color='k'
        lw = 1  #比例线宽
        y1 = 0.001
        w = 0.01
        alpha = 1
        # print(y+w+y1, x, x+x1,y, x, x+x1, lw)
        plt.axhline(y=y, xmin=x, xmax=x+x1, lw=lw, c=color, alpha=alpha)
        plt.axhline(y=y+w+y1, xmin=x, xmax=x+x1, lw=lw, c=color, alpha=alpha)
        for i in range(maker):
            mx = x + ((x1/maker)*i)
            plt.axvline(x=mx, ymin=y, ymax=y+(w/2.5), lw=lw, c=color, alpha=alpha)
        base1 = Arc(xy=(x, y+((w+y1)/2)),    # 椭圆中心，（圆弧是椭圆的一部分而已）
                width=w+y1,    # 长半轴
                height=w+y1,    # 短半轴
                angle=90,    # 椭圆旋转角度（逆时针） 
                theta1=0,    # 圆弧的起点处角度
                theta2=180,    # 圆度的终点处角度
                color=color,
                alpha=alpha,
                linewidth=lw
                )
        base2 = Arc(xy=(x1+x, y+((w+y1)/2)),    # 椭圆中心，（圆弧是椭圆的一部分而已）
                width=w+y1,    # 长半轴
                height=w+y1,    # 短半轴
                angle=-90,    # 椭圆旋转角度（逆时针） 
                theta1=0,    # 圆弧的起点处角度
                theta2=180,    # 圆度的终点处角度
                color=color,
                alpha=alpha,
                linewidth=lw   #线宽像素
                )
        axes1.add_patch(base1)
        axes1.add_patch(base2)
        
    def pair_index(self,axes1,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2):
        pairs = []
        for i in pair:
            for j in i:
                if str(str(j[0]).split('^')[0]) == self.chr1_name and str(str(j[1]).split('^')[0]) == self.chr2_name:
                    name11 = str(j[0]).replace("^", "g")
                    name22 = str(j[1]).replace("^", "g")
                    index1 = float(matrix_gff1.loc[name11,5])
                    index2 = float(matrix_gff2.loc[name22,5])
                    # print(index1,index2,'index')
                    if maker_str:
                        prop1 = x1/length1
                        prop2 = x2/length2
                        # print(length1,length2)
                        # pair_lt = [[0.1+index1*prop1,0.3],[0.1+((0.8-x2)/2)+index2*prop2,0.65]]
                        # pairs.append(pair_lt)
                        self.plot_bez_inner(0.1+((0.8-x2)/2)+index2*prop2,0.65-0.004,0.1+index1*prop1,0.3+0.01+0.004)
                        # plt.plot([0.1+((0.8-x2)/2)+index2*prop2,0.1+index1*prop1],[0.65-0.004,0.3+0.01+0.004],c='g')
                    else:
                        prop1 = x2/length1
                        prop2 = x1/length2
                        # pair_lt = [[0.1+index2*prop2,0.3],[0.1+((0.8-x2)/2)+index1*prop1,0.65]]
                        # pairs.append(pair_lt)

                        self.plot_bez_inner(0.1+((0.8-x2)/2)+index1*prop1,0.65-0.004,0.1+index2*prop2,0.3+0.01+0.004)
                        # plt.plot([0.1+((0.8-x2)/2)+index1*prop1,0.1+index2*prop2],[0.65-0.004,0.3+0.01+0.004],c='r')
    def run(self):
        x1,x2,maker1,maker2,matrix_gff1,matrix_gff2,chro1,chro2,maker_str,length1,length2 = self.read_csv()
        pair = self.read_colinearity(self.pairs_file)
        self.make_plot(maker1,maker2,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2)
# iclmap0 = iclmap()
# x1,x2,maker1,maker2,matrix_gff1,matrix_gff2,chro1,chro2,maker_str,length1,length2 = iclmap0.read_csv()
# pair = iclmap0.read_colinearscan('ssu_mes.collinearity')
# iclmap0.make_plot(maker1,maker2,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2)
