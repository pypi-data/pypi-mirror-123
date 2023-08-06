# -*- encoding: utf-8 -*-
'''
@File        :inner.py
@Time        :2021/09/28 11:21:41
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :内卷的圈图
'''


import re
import os
import sys
from math import *
import csv
import pandas as pd
from matplotlib.patches import *
from pylab import *

# from io import BytesIO
# import base64
# from lxml import etree

from famCircle.bez import *


class inner():
    def __init__(self, options):
        self.genessorted = []
        self.file_type = "coliearity"
        self.geneno = 0
        self.genepair2Ks = {}
        self.genepair2Ka = {}
        ##### circle parameters
        self.GAP_RATIO = 4 #gaps between chromosome circle, chr:gap = 4: 1
        self.radius = 0.33
        # figurefile = "_".join(sys.argv[1:len(sys.argv)])+".genefam"
        #### gene block parameters
        self.space = "0.01" # radian 0.01
        self.peripheral = 'False'
        self.block= 0.005 #block scize
        self.blockthick = 0.004 #0.006
        self.shiftratio = 1.1 # define the distance between overlapping glocks
        self.clusters = "True"
        self.specieslist = []
        self.iscompletegenome = {}
        self.chro2len = {}
        self.vvchrolist = []
        self.otherchrolist = []
        self.labels = []
        self.start_list = []
        self.gene2pos={}
        self.gene2chain = {}
        self.orderlist = {}
        self.genes = []
        self.genepair0 = []
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    # def ks(self, figurefile, fpchrolen, fpgff, fpgenefamilyinf, chrolist):
    def ksrun(self):
        # print('kaishi')
        figure(1, (8, 8))  ### define the a square, or other rectangle of the figure, if to produce an oval here
        root =axes([0, 0, 1, 1])
        if self.species1 != self.species2:
            # fpgenefamilyinf = open(self.ks, 'r', encoding='utf-8')
            genefamily = open(self.genefamily, 'r', encoding='utf-8')

            fpchrolen1 = open(self.lens1, 'r', encoding='utf-8')
            for row in fpchrolen1:
                # print('ceshi')
                chro,length,order = row.split('\t')[0],row.split('\t')[1],row.split('\t')[2]
                self.labels.append(chro)
                self.chro2len[chro] = int(length)
                self.orderlist[chro] = int(order)
                # self.otherchrolist.append(chro)
            ## input gff
            fpchrolen1.close()
            fpchrolen2 = open(self.lens2, 'r', encoding='utf-8')
            for row in fpchrolen2:
                # print('ceshi')
                chro,length,order = row.split('\t')[0],row.split('\t')[1],row.split('\t')[2]
                self.labels.append(chro)
                self.chro2len[chro] = int(length)
                self.orderlist[chro] = int(order)
                # self.otherchrolist.append(chro)
            ## input gff
            fpchrolen2.close()


            familylist = []

            for row in genefamily:
                if (row != '\n'):
                    familyname = readname(row.strip('\n').split()[0],self.species1+self.species2)
                    chro = str(familyname.split('^')[0])
                    if chro not in self.chro2len.keys():
                        continue
                    familylist.append(familyname)
                    self.genepair0.append(familyname)
            genefamily.close()

            fpgff1 = open(self.gff1, 'r', encoding='utf-8')
            for row in fpgff1:
                ch, gene, start, end = row.split()[0],row.split()[1],row.split()[2],row.split()[3]    #mrna, , software
                gene = readname(gene,self.species1+self.species2)
                if (gene in familylist):
                    start = int(start)
                    end = int(end)
                    self.gene2pos[gene] = int(start)# 基因位置
                    self.gene2chain[gene] = int((end-start)/abs(end -start))# 基因正负
                else:
                    pass
            fpgff1.close()
            fpgff2 = open(self.gff2, 'r', encoding='utf-8')
            for row in fpgff2:
                ch, gene, start, end = row.split()[0],row.split()[1],row.split()[2],row.split()[3]    #mrna, , software
                gene = readname(gene,self.species1+self.species2)
                if (gene in familylist):
                    start = int(start)
                    end = int(end)
                    self.gene2pos[gene] = int(start)# 基因位置
                    self.gene2chain[gene] = int((end-start)/abs(end -start))# 基因正负
                else:
                    pass
            fpgff2.close()


        else:
            fpchrolen = open(self.lens1, 'r', encoding='utf-8')
            fpgff = open(self.gff1, 'r', encoding='utf-8')
            
            genefamily = open(self.genefamily, 'r', encoding='utf-8')
            for row in fpchrolen:
                # print('ceshi')
                chro,length,order = row.split('\t')[0],row.split('\t')[1],row.split('\t')[2]
                self.labels.append(chro)
                self.chro2len[chro] = int(length)
                self.orderlist[chro] = int(order)
                # self.otherchrolist.append(chro)
            ## input gff
            familylist = []
            for row in genefamily:
                if (row != '\n'):
                    familyname = readname(row.strip('\n').split()[0],self.species1)
                    chro = str(familyname.split('^')[0])
                    if chro not in self.chro2len.keys():
                        continue
                    familylist.append(familyname)
                    self.genepair0.append(familyname)
            genefamily.close()

            for row in fpgff:
                ch, gene, start, end = row.split()[0],row.split()[1],row.split()[2],row.split()[3]    #mrna, , software
                gene = readname(gene,self.species1)
                if (gene in familylist):
                    start = int(start)
                    end = int(end)
                    self.gene2pos[gene] = int(start)# 基因位置
                    self.gene2chain[gene] = int((end-start)/abs(end -start))# 基因正负
                else:
                    pass
            fpgff.close()


        ### input gene family gene1 gene2 Ka Ks
        fpgenefamilyinf = open(self.ks, 'r', encoding='utf-8')
        for row in fpgenefamilyinf:
            if (row.split()[0] == 'id1' or len(row.split()) < 4):
                continue
            gene1, gene2, Ka, Ks = row.split()[0],row.split()[1],row.split()[2],row.split()[3]
            gene1 = readname(gene1,self.species1+self.species2)
            gene2 = readname(gene2,self.species1+self.species2)
            if (gene1 not in self.gene2pos.keys() or gene2 not in self.gene2pos.keys()):
                continue
            genepair = ""
            # print(type(gene1))
            if gene1 < gene2:
               genepair = gene1 + " " + gene2
            else:
               genepair = gene2 + " " + gene1
            if len(gene1.split("^")[0]) < 10 and len(gene2.split("^")[0]) < 10:#数字筛选chr名字长度
               self.genepair2Ks[genepair] = float(Ks)
        fpgenefamilyinf.close()
        # print("genes ", self.genes, "genes")
        return root

    def rad_to_coord(self,angle, radius):
        return radius*cos(angle), radius*sin(angle)

    def to_deg(self,bp, total):
        # from basepair return as degree 从碱基对返回为学位
        return bp*360./total

    def to_radian(self,bp, total):# 返回弧度
        return radians(bp*360./total)

    def plot_arc(self,start, stop, radius):
        # start, stop measured in radian
        #print start, stop
        t = arange(start, stop, pi/720.)
        x, y = radius*cos(t), radius*sin(t)
        plot(x, y, "k-", alpha=.5)

    def plot_cap(self,angle, clockwise=True):
        radius=self.sm_radius
        # angle measured in radian, clockwise is boolean
        if clockwise: t = arange(angle, angle+pi, pi/30.)
        else: t = arange(angle, angle-pi, -pi/30.)
        x, y = radius*cos(t), radius*sin(t)
        middle_r = (self.radius_a+self.radius_b)/2
        x, y = x + middle_r*cos(angle), y + middle_r*sin(angle)
        plot(x, y, "k-", alpha=.5)

    def plot_arc_block1(self,start, chain, radius, end):
        t = arange(start, start+end, pi/720.)
        x,y = radius * cos(t), radius*sin(t)
        plot(x, y, "g-", alpha=0.5)

    def plot_arc_block(self,start, chain, radius):
        t = arange(start, start+self.block, pi/720.)
        x,y = radius * cos(t), radius*sin(t)
        plot(x, y, "b-", alpha=0.5)

    def zj(self):
        fullchrolen = int(pd.DataFrame(self.chro2len.values()).sum())
        chr_number = len(self.labels) # total number of chromosomes
        GAP = fullchrolen/self.GAP_RATIO/chr_number # gap size in base pair
        total_size = fullchrolen + chr_number * GAP # base pairs
        for i in range(chr_number):
            self.start_list.append(0)
        # self.start_list = [0]*chr_number
        for i in range(1, chr_number):
            self.start_list[i] = self.start_list[i-1] + self.chro2len[self.labels[i-1]] + GAP
        stop_list = [(self.start_list[i] + self.chro2len[self.labels[i]]) for i in range(chr_number)]
        # print("start list", self.start_list)
        return stop_list, total_size, chr_number

    def transform_deg(self,ch, pos, total_size):
        return self.to_deg(pos + self.start_list[ch], total_size)

    def transform_pt(self,ch, pos, r, total_size):
        # convert chromosome position to axis coords
        # print("transform", ch, pos, r)
    #    print "startlist", self.start_list[ch]
        rad = self.to_radian(pos + self.start_list[ch], total_size)
        return r*cos(rad), r*sin(rad)

    def transform_pt1(self,ch, pos, r, total_size):
        # convert chromosome position to axis coords
        # print("transform", ch, pos, r)
    #    print "startlist", self.start_list[ch]
        rad = self.to_radian(pos + self.start_list[ch], total_size)
        return r*cos(rad), r*sin(rad),rad

    def transform_pt2(self,rad, r):
        return r*cos(rad), r*sin(rad)

    def plot_scale(self,length,number):
        plot([0.5-length-0.05,0.5-0.05],[-0.45,-0.45], color='#333631',linestyle='-', lw = 1.5)
        plot([0.5-length-0.05,0.5-length-0.05],[-0.45,-0.44], color='red',linestyle='-', lw = 1)
        plot([0.5-0.05,0.5-0.05],[-0.45,-0.44], color='#333631',linestyle='-', lw = 1)
        text(0.5-length-0.05+(length/2)-0.02,-0.43, s = str(number),color='black', fontsize = 8, alpha=0.8)# 添加基因标注

    def plot_bez_inner(self,p1, p2, cl, total_size):
    #    print "inner"
        a, b, c = p1
        ex1x, ex1y = self.transform_pt(a, b, c, total_size)
        a, b, c = p2
        ex2x, ex2y = self.transform_pt(a, b, c, total_size)
        # Bezier ratio, controls curve, lower ratio => closer to center
        ratio = .5
        x = [ex1x, ex1x*ratio, ex2x*ratio, ex2x]
        y = [ex1y, ex1y*ratio, ex2y*ratio, ex2y]
        step = .01
        t = arange(0, 1+step, step)
        xt = Bezier(x, t)
        yt = Bezier(y, t)
        plot(xt, yt, '-', color=cl, lw=.1)

    def plot_bez_Ks2(self,rad1, r1, rad2, r2, col, ratio, gene1, gene2):
        ex1x, ex1y = self.transform_pt2(rad1, r1)
        ex2x, ex2y = self.transform_pt2(rad2, r2)
        sita = pi/2
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
        xt = Bezier(x,t)
        yt = Bezier(y,t)
        # i = int(len(xt)/2)
        # xx,yy = xt[i],yt[i]
        # # print(xx,yy)
        # buoy = '<-' + str(gene1) + '-' + str(gene2) + '->'
        # text(xx,yy, s = buoy,color=col, fontsize = 1,alpha=0.8)# 添加基因标注
        plot(xt, yt, '-', color = col, lw = 0.1)

    def run_plot(self, Ks, start1, start2, grade):
        colorlist = ['red', 'lime', 'orange', 'chocolate', 'yellow', 'palegreen', 'teal', 'dodgerblue', 'blueviolet', 'fuchsia']
        lt = self.ks_concern.strip('\n').split(',')
        length = len(lt)
        if (Ks > eval(lt[1]) or Ks < eval(lt[0])):
            color = 'gray'
            class1 = 'None'
            if self.peripheral == 'True':
                return color, class1
            else:
                return None,None
        else:
            color = colorlist[grade]
            class1 = grade
            return color, class1

    def run(self):
        self.radius_a = float(self.radius)
        self.radius_b = self.radius_a + 0.005
        self.sm_radius=(self.radius_b-self.radius_a)/2 #telomere capping
        if (os.path.exists(self.savecsv)):
            os.remove(self.savecsv)
        lt = ['gene1', 'gene2', 'start1', 'shift1', 'start2', 'shift2', 'class1']
        with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file ,delimiter=',')
            writer.writerow(lt)
        root = self.ksrun()
        stop_list, total_size, chr_number = self.zj()
        gene2pos = self.gene2pos
        ## sort gene according to lacation on circle

        for i in range(len(self.genepair0)):
            if self.geneno == 0:
                self.genessorted.append(self.genepair0[0])
                self.geneno = self.geneno + 1
            else:
                firstgene = self.genessorted[0]
                # print(firstgene)
                lastgene = self.genessorted[-1]
                chf = firstgene.split("^")[0]
                chl = lastgene.split("^")[0]
             
                # print(firstgene, lastgene, chf, chl, gene2pos[firstgene])
                posf = gene2pos[firstgene] + self.start_list[self.labels.index(chf)]
                posl = gene2pos[lastgene] + self.start_list[self.labels.index(chl)]
                chi = self.genepair0[i].split("^")[0]
                posi = gene2pos[self.genepair0[i]] + self.start_list[self.labels.index(chi)]
        #       print posf, posl, posi
                if posi <= posf:
                   self.genessorted[0:0] = [self.genepair0[i]]
                elif posi >= posl:
                    self.genessorted.append(self.genepair0[i])
                else:
                    for j in range(len(self.genessorted)-1):
                        chj = self.genessorted[j].split("^")[0]
                        posj = gene2pos[self.genessorted[j]] + self.start_list[self.labels.index(chj)]
                        chj1 = self.genessorted[j+1].split("^")[0]
                        posj1 = gene2pos[self.genessorted[j+1]]+self.start_list[self.labels.index(chj1)]
                        # print(posj, posj1, posi)
                        if posi > posj and posi < posj1:
                            self.genessorted[j+1:j+1] = [self.genepair0[i]]
                # print("genesort ", self.genessorted)

        # the chromosome layout
        j = 0
        for start, stop in zip(self.start_list, stop_list):# 绘制染色体
            start, stop = self.to_radian(start, total_size), self.to_radian(stop, total_size)
            # shaft
            self.plot_arc(start, stop, self.radius_a)# 染色体内圈
            self.plot_arc(start, stop, self.radius_b)# 染色体外圈
            # telemere capping
            self.plot_cap(start, clockwise=False)# 右鸭舌部分
            self.plot_cap(stop)# 左鸭舌部分
            # chromosome self.labels
            label_x, label_y = self.rad_to_coord((start+stop)/2, self.radius_b*1.1)
            text(label_x, label_y, self.labels[j], horizontalalignment="center", verticalalignment="center")
            j += 1

        ### Again: define shift level and draw gene blocks
        shiftlevel = 0
        gene2shift = {}
        gene2location = {}
        cho = self.genessorted[0].split("^")[0]
        pos0 = self.gene2pos[self.genessorted[0]] + self.start_list[self.labels.index(cho)]
        chain = self.gene2chain[self.genessorted[0]]
        start = self.to_radian(pos0, total_size)
        # self.plot_arc_block(start, chain, self.radius_a - shiftlevel * self.shiftratio * self.blockthick)
        #gene2location[self.genessorted[0]]= start
        #gene2shift[self.genessorted[0]] = shiftlevel
        laststart = start
        shiftlist = []
        space_ = 0
        for i in range(len(self.genessorted)):
            if self.genessorted[i] not in self.genepair0:
                continue
            chi = self.genessorted[i].split("^")[0]
            posi = self.gene2pos[self.genessorted[i]] + self.start_list[self.labels.index(chi)]
            chain = self.gene2chain[self.genessorted[i]]
            start = self.to_radian(posi, total_size)
            if(start-laststart < float(self.space)):
                shiftlevel = shiftlevel + 1
                space_ = space_ + (start-laststart)
                shiftlist.append(space_)
            else:
                 shiftlevel=0
                 space_ = 0
            shiftradius = self.radius_a - shiftlevel * self.shiftratio * self.blockthick
        #    print "draw block: ", start, chain, shiftlevel, self.shiftratio, self.blockthick, shiftradius, self.radius_a
            self.plot_arc_block(start, chain, self.radius_a - (shiftlevel+1) * self.shiftratio * self.blockthick)
            laststart = start

        gene_size_ = max(shiftlist)

        ### define shift level and draw gene blocks
        shiftlevel = 0
        gene2shift = {}
        gene2location = {}
        cho = self.genessorted[0].split("^")[0]
        pos0 = self.gene2pos[self.genessorted[0]] + self.start_list[self.labels.index(cho)]
        chain = self.gene2chain[self.genessorted[0]]
        # print('pos0,total_size:',pos0, total_size)
        start = self.to_radian(pos0, total_size)
        self.plot_arc_block1(start, chain, self.radius_a - shiftlevel * self.shiftratio * self.blockthick, gene_size_)
        gene2location[self.genessorted[0]]= start
        gene2shift[self.genessorted[0]] = shiftlevel
        laststart = start

        for i in range(len(self.genessorted)):
            if self.genessorted[i] not in self.genepair0:
                continue
            chi = self.genessorted[i].split("^")[0]
            posi = self.gene2pos[self.genessorted[i]] + self.start_list[self.labels.index(chi)]
            chain = self.gene2chain[self.genessorted[i]]
            # print('pos0,total_size:',pos0, total_size)# pos0,total_size: 2120381 466090045.0
            start = self.to_radian(posi, total_size)
            if(start-laststart < float(self.space)):
                shiftlevel = shiftlevel + 1
            else:
                 shiftlevel=0
            shiftradius = self.radius_a - shiftlevel * self.shiftratio * self.blockthick

        #    print "draw block: ", start, chain, shiftlevel, self.shiftratio, self.blockthick, shiftradius, self.radius_a
            gene2location[self.genessorted[i]] = start
            gene2shift[self.genessorted[i]] = shiftlevel
            laststart = start
        ### draw Ks lines between genes
        # print("***************************************************")
        if self.file_type == 'famCircle':
            pair_list = read_famCircle(self.pair_file,self.species1)
        elif self.file_type == 'coliearity':
            pair_list = read_coliearity0(self.pair_file,self.species1)
        elif self.file_type == 'BLAST':
            pair_list = read_blast(self.pair_file,self.species1)
        else:
            print("Exception string: File is of unknown type")
            exit()
        for genepair in pair_list:
            if genepair not in self.genepair2Ks.keys():
                continue
        # for genepair in self.genepair2Ks.keys():
        #    print genepair
            gene1, gene2 = genepair.split(' ')
            Ks = self.genepair2Ks[genepair]
            if (gene1 not in gene2location.keys() or gene2 not in gene2location.keys()):
                # print(gene1)
                continue
            start1 = gene2location[gene1]
            # print(start1)
            shift1 = gene2shift[gene1]
            start2 = gene2location[gene2]
            # print(start2)
            shift2 = gene2shift[gene2]
            # print ("start", start1, start2)# start 6.015783710157899 6.133748376342092
            if abs(start1 - start2) > gene_size_:
                continue
            space_ks = (abs(float(self.ks_concern.strip('\n').split(',')[1]) - float(self.ks_concern.strip('\n').split(',')[0])))/3
            grade = int(Ks / space_ks)# 分级
            color = return_col(Ks,float(self.ks_concern.split(',')[0]),float(self.ks_concern.split(',')[1]))
            ratio = 0.5
            if (color != None):
                if (self.clusters == "True"):
                    lt = [gene1, gene2, start1, shift1, start2, shift2]
                    with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                        writer = csv.writer(file ,delimiter=',')
                        writer.writerow(lt)
                    self.plot_bez_Ks2(start1, self.radius_a - (shift1+1) * self.shiftratio * self.blockthick, start2, self.radius_a - (shift2+1) * self.shiftratio * self.blockthick, color, ratio, gene1, gene2)
                else:
                    self.plot_bez_Ks2(start1, self.radius_a - (shift1+1) * self.shiftratio * self.blockthick, start2, self.radius_a - (shift2+1) * self.shiftratio * self.blockthick, 'red', ratio, gene1, gene2)
                    lt = [gene1, gene2, start1, shift1, start2, shift2]
                    with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                        writer = csv.writer(file ,delimiter=',')
                        writer.writerow(lt)
        #### draw tick showing scale of chromosomes
        order_length = (gene_length_order(self.lens1)+gene_length_order(self.lens2))/2
        angle2 = 0
        angle0,angle1 = 0,0
        # print(order_length)
        for i in range(chr_number):
            pos = 0
            # print(self.orderlist[self.labels[i]])
            while pos < self.orderlist[self.labels[i]]:
                # print(pos)
                if pos == 0 :
                    color = "red"
                else:
                    color = 'blue'
                index_order = pos * order_length
                xx1, yy1 = self.transform_pt(i, int(index_order), self.radius_b-0.001, total_size)
                xx2, yy2 = self.transform_pt(i, int(index_order), self.radius_b-0.004, total_size)
                if pos == 1500:
                    xx3, yy3, angle0 = self.transform_pt1(i, int(index_order), self.radius_b-0.003, total_size)
                elif pos == 3000:
                    xx3, yy3, angle1 = self.transform_pt1(i, int(index_order), self.radius_b-0.003, total_size)
                    angle2 = abs(angle0 - angle1)
                # xx3, yy3, angle0 = self.transform_pt1(i, int(index_order), self.radius_b+0.006, total_size)
                # if xx3 > 0:
                #     xx3 = xx3 - 0.005
                #     yy3 = yy3 - 0.005
                # if xx3 < 0:
                #     xx3 = xx3 - 0.006
                #     yy3 = yy3 - 0.006
                # # print('xx3, yy3, angle0, pi/2 - angle0',xx3, yy3, (pi/2)-angle0)
                # angle1 = ((angle0 - (pi/2))/(2*pi))*360
                plot([xx1, xx2], [yy1, yy2], color=color,linestyle='-', lw = .5)
                # text(xx3,yy3, s = str(pos),color='b', fontsize = 5, rotation=angle1, alpha=0.8)# 添加基因标注
                pos = pos + 1500
        self.plot_scale(angle2*self.radius_b,1500)
        #
        root.set_xlim(-.5, .5)
        root.set_ylim(-.5, .5)
        root.set_axis_off()
        savefig(self.savefile, dpi=1000)

        sys.exit(0)
