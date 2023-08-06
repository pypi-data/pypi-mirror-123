# -*- encoding: utf-8 -*-
'''
@File        :part.py
@Time        :2021/07/11 12:44:00
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :家族分布染色体
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

class part():
    def __init__(self, options):
        self.makers = 200
        # self.chrolist = "mes,ssu"
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def read_csv(self):
        matrix_chr1 = pd.read_csv(self.lens, sep='\t', header=None, index_col=0)
        # print(matrix_chr1)
        matrix_gff1 = pd.read_csv(self.gff, sep='\t', header=None, index_col=1)
        new_name_list = []
        for item in matrix_gff1.iterrows():
            # print(item[0])
            old_name = str(item[0])
            # new_name = readname(old_name,self.chro_name)
            new_name = old_name
            new_name_list.append(new_name)
            # matrix_gff1.iloc[old_name,0] = new_name
            # print('#####################')
        # print(new_name_list)
        matrix_gff1.index = new_name_list
        matrix_gff1.groupby(by=0)
        # print(matrix_gff1)

        family_list = []
        for row in open(self.genefamily, 'r'):
            if row != '\n':
                name = row.strip('\n')
                # name = readname(name,self.chro_name)
                chro = str(name.split('^')[0])
                if chro == self.chro_name and name not in family_list:
                    family_list.append(name)

        csv_reader = csv.reader(open(self.pairs_file))
        pair_dic = {}
        for row in csv_reader:
            name1,name2 = readname(str(row[0]),self.chro_name), readname(str(row[1]),self.chro_name)
            chro1, chro2 = str(name1.split('^')[0]),str(name2.split('^')[0])
            name1,name2 = str(row[0]),str(row[1])
            if chro1 != self.chro_name or chro2 != self.chro_name:
                continue
            if name1 > name2:
                name = name1 + '%' + name2
            else:
                name = name2 + '%' + name1
            pair_dic[name] = 0
        return matrix_chr1,matrix_gff1,family_list,pair_dic

    def read_colinearscan(self,file):
        pair = []
        pair_list = []
        with open(file) as f:
            for line in f.readlines():
                line = line.strip()
                # print(line)
                if line[0] == "#":
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
                else:
                    lt = line.split()
                    # name1 = readname(str(lt[0]),self.chro_name)
                    # name2 = readname(str(lt[2]),self.chro_name)
                    lt0 = [str(lt[0]),str(lt[2])]
                    # print(lt0)
                    pair_list.append(lt0)
            if len(pair_list) != 0:
                # print(pair_list)#输出
                pair.append(pair_list)
            # print(pair)
            return pair

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
        plot(xt, yt, '-', color='r', lw=.3, alpha=0.3)#alpha 透明度

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

    def make_plot(self,matrix_chr1,matrix_gff1,family_list,pair_dic):
        minin,maxin = int(self.interval.split(',')[0]),int(self.interval.split(',')[1])
        chro_lingth = int(matrix_chr1.loc[self.chro_name,1])
        chro_order = int(matrix_chr1.loc[self.chro_name,2])
        gene_order = chro_lingth/chro_order
        gene_number = abs(minin-maxin)
        chro_lingth1 = gene_number*gene_order
        maker = 0.8 * ((1500 * gene_order)/chro_lingth1)
        fig1 = plt.figure(num=1, figsize=(10, 10))  # 确保正方形在屏幕上显示一致，固定figure的长宽相等
        axes1 = fig1.add_subplot(1, 1, 1)
        plt.xlim((0, 1))
        plt.ylim((0, 1))
        self.map1(axes1,maker,0.1,0.3,0.8,'k')# 长染色体0.8
        # self.map1(axes1,maker2,0.1+((0.8-x2)/2),0.65,x2,'k')# 短染色体
        plt.text(0.45, 0.28, self.chro_name)
        plt.axis('off')
        self.pair_index(axes1,matrix_chr1,matrix_gff1,family_list,pair_dic)
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
        for i in range(int(0.8/maker)+1):
            mx = maker*i
            plt.axvline(x=0.1+mx, ymin=y, ymax=y+(w/2.5), lw=lw, c=color, alpha=alpha)
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

    def map2(self,axes1,x,y,x1,color):
        # makers = 15 #标尺
        # x = 0.1 #起始坐标x
        # y = 0.1 #起始坐标y
        # x1 = 0.8#染色体长度
        # color='k'
        lw = 2  #比例线宽
        alpha = 1
        # print(y+w+y1, x, x+x1,y, x, x+x1, lw)
        plt.axhline(y=y, xmin=x, xmax=x+x1, lw=lw, c=color, alpha=alpha)

    def transform_pt2(self, rad, r):
        return r*cos(rad), r*sin(rad)

    def plot_bez_Ks2(self, ex1x, ex1y, ex2x, ex2y, col, ratio,gene1, gene2):
    #    print "bez Ks 2"
        # print('rad1, r1',rad1, r1)
        # ex1x, ex1y = self.transform_pt2(rad1, r1)
        # ex2x, ex2y = self.transform_pt2(rad2, r2)
        # ratio = -0.7#0.5
        sita = pi / 2
        if ex1x != ex2x:
            sita = atan((ex2y-ex1y)/(ex2x-ex1x))
        d = sqrt((ex2x-ex1x)**2+(ex2y-ex1y)**2)
        L = d * ratio
        P1x = ex1x + L*sin(sita)
        P1y = ex1y - L*cos(sita)
        P2x = ex2x + L*sin(sita)
        P2y = ex2y - L*cos(sita)
        step = .01
        t = arange(0, 1+step, step)
        x=[ex1x, P1x, P2x, ex2x]
        y=[ex1y, P1y, P2y, ex2y]
        # print('x,y,t',x,y,t)
        xt = Bezier(x,t)
        yt = Bezier(y,t)
        xx3 = xt[int(len(xt)/2)]
        yy3 = yt[int(len(yt)/2)]-0.001
        s = '<-'+str(gene1)+'-'+ str(gene2)+'->'
        text(xx3,yy3, s = str(s),color=col, fontsize = 1.5, rotation=30, alpha=0.8)# 添加基因标注
        plot(xt, yt, '-', color = col, lw = 0.3)#0.1

    def classify(self, start1, start2, grade):
        colorlist = ['red', 'lime', 'orange', 'chocolate', 'yellow', 'palegreen', 'teal', 'dodgerblue', 'blueviolet', 'fuchsia']
        # lt = self.ks_concern.strip('\n').split(',')
        # length = len(lt)
        color = colorlist[grade]
        class1 = grade
        return color, class1

    def pair_index(self,axes1,matrix_chr1,matrix_gff1,family_list,pair_dic):
        minin,maxin = int(self.interval.split(',')[0]),int(self.interval.split(',')[1])
        chro_lingth = int(matrix_chr1.loc[self.chro_name,1])
        chro_order = int(matrix_chr1.loc[self.chro_name,2])
        gene_order = chro_lingth/chro_order
        gene_number = abs(minin-maxin)
        chro_lingth1 = gene_number*gene_order
        maker = 0.8 * ((1500 * gene_order)/chro_lingth1)
        indexx = 0.8/chro_lingth
        inde3 = minin
        name_length = len(str(family_list[0]))-len(str(self.chro_name))-1
        while 1:
            i = self.chro_name + '^' +str(inde3).zfill(name_length)
            # print(i)
            try:
                start0 = max(int(matrix_gff1.loc[i,2]),int(matrix_gff1.loc[i,3]))
                break
            except:
                # print(inde3)
                inde3 = inde3 + 1


        inde3 = maxin
        while 1:
            if inde3 >= chro_order:
                start9 = chro_lingth
                break
            i = self.chro_name + '^' +str(inde3).zfill(name_length)
            # print(i)
            try:
                start9 = min(int(matrix_gff1.loc[i,2]),int(matrix_gff1.loc[i,3]))
                break
            except:
                # print(inde3)
                inde3 = inde3 + 1

        # print(chro_lingth,chro_order)
        # laststart = start
        gene_list = []
        gene_index_dic = {}
        shiftlevel = 0
        gene2shift = {}
        gene2pos = {}
        gene2location = {}
        for i in family_list:
            # print(i)
            if str(i.split('^')[0]) != self.chro_name:
                continue
            # print(int(matrix_gff1.loc[i,5]) , minin , int(matrix_gff1.loc[i,5]) , maxin)
            if int(matrix_gff1.loc[i,2]) < start0 or int(matrix_gff1.loc[i,3]) > start9:
                continue
            gene_list.append(i)
            start = min(int(matrix_gff1.loc[i,2]),int(matrix_gff1.loc[i,3]))
            gene_index_dic[i] = 0.8*((start-start0)/(chro_lingth-start0))
            gene2pos[i] = start
            # print(start)
        # print(gene_list)
        gene_list.sort()
        start = gene_index_dic[str(gene_list[0])]
        gene2location[str(gene_list[0])] = start
        gene2shift[str(gene_list[0])] = shiftlevel
        laststart = start
        shiftlist = []
        space_ = 0

        for i in gene_list:
            start = gene_index_dic[str(i)]
            # print(start-laststart)
            if(start-laststart < float(self.space)):
                shiftlevel = shiftlevel + 1
                space_ = space_ + (start-laststart)
                shiftlist.append(space_)
            else:
                shiftlevel=0
            self.map2(axes1,start+0.1,(shiftlevel-1)*0.005+0.32+(shiftlevel-1)*0.001,0.002,'blue')
            gene2location[i] = start
            gene2shift[i] = shiftlevel
            laststart = start
        gene_size_ = max(shiftlist)
        ks = read_ks0(self.ks)
        for genepair in pair_dic.keys():
            # print(genepair)
            gene1, gene2 = str(genepair.split('%')[0]),str(genepair.split('%')[1])
            if gene1 not in gene2location.keys() or gene2 not in gene2location:
                continue# 此处还要修改
            start1 = gene2location[gene1]
            shift1 = gene2shift[gene1]
            start2 = gene2location[gene2]
            shift2 = gene2shift[gene2]
            if abs(start1 - start2) > gene_size_:
                continue
            if gene1 + str('_') + gene2 in ks:
                ks_v = ks[gene1 + str('_') + gene2]
                color = return_col(Ks_v,float(self.ks_concern.split(',')[0]),float(self.ks_concern.split(',')[1]))
            if gene2 + str('_') + gene1 in ks:
                ks_v = ks[gene1 + str('_') + gene2]
                color = return_col(Ks_v,float(self.ks_concern.split(',')[0]),float(self.ks_concern.split(',')[1]))
            else:
                color = 'block'
            print(color)
            ratio = 0.5
            if (color != None):
                # print(start1, start2)
                if (self.clusters == "True"):
                    self.plot_bez_Ks2(start1+0.101, (shift1-1) * 0.006+0.32, start2+0.101, (shift2-1)*0.006+0.32, color, ratio,gene1, gene2)
                else:
                    self.plot_bez_Ks2(start1+0.101, (shift1-1) * 0.006+0.32, start2+0.101, (shift2-1)*0.006+0.32, 'red', ratio,gene1, gene2)
            else :
                # print('间距不达标')
                pass
    def run(self):
        matrix_chr1,matrix_gff1,family_list,pair_dic = self.read_csv()
        # pair = self.read_colinearscan(self.pairs_file)
        self.make_plot(matrix_chr1,matrix_gff1,family_list,pair_dic)
