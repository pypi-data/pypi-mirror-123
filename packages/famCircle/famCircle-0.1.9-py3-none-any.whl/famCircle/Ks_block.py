# -*- encoding: utf-8 -*-
'''
@File        :Ks_block.py
@Time        :2021/09/28 11:20:59
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :block的ks
'''


from scipy.stats.kde import gaussian_kde
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from famCircle.bez import *
import sys
import csv


class Ks_block():
    def __init__(self, options):
        self.vertical = "False"
        self.model = "NG86"
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readks(self):
        read_ks = {}
        f = open(self.ks, 'r', encoding='utf-8')
        for row in f:
            if row[0] != '#' and row[0] != '\n':
                row = row.strip('\n').split('\t')
                if row[0] != 'id1' and len(row) != 2:
                    pair = str(row[0]) + '_' + str(row[1])
                    lt = row[2:]
                    read_ks[pair] = lt
        # print(read_ks)
        return read_ks

    def readblock(self,read_ks):
        model = self.model
        lt0 = ['number', 'id1', 'id2', 'start1','end1', 'start2', 'end2','length','density1','density2','median','average','score','e_value']
        with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file ,delimiter=',')
            writer.writerow(lt0)
        num = 0
        if self.blockfile_type == 'famCircle':
            f = open(self.blockfile, 'r', encoding='utf-8')
            id1s,id2s = [],[]
            index1,index2 = [],[]
            score,pvalue = 0,0
            for row in f:
                if row[0] != '#' and row[0] != '\n':
                    row = row.strip('\n').split()
                    id10, id20 = str(row[0]),str(row[1])
                    # print(id10)
                    id1s.append(id10)
                    id2s.append(id20)
                    # print(readname(id10,self.species_list))
                    index1.append(int(readname(id10,self.species_list).split('^')[1]))
                    index2.append(int(readname(id20,self.species_list).split('^')[1]))
                elif (row[0] == '#'):
                    # print(row)
                    if len(id1s) == 0:
                        id1s,id2s = [],[]
                        index1,index2 = [],[]
                        doc = {}
                        row = row.strip('\n').split()
                        for i in row:
                            if '=' in i:
                                lt = i.split('=')
                                doc[str(lt[0])] = str(lt[1])
                            else:
                                continue
                        score,pvalue = float('inf'),float(1)
                    else:
                        num += 1
                        ks_list = []
                        for i in range(len(id1s)):
                            id1 = str(id1s[i])
                            id2 = str(id2s[i])
                            try:
                                id_ks = read_ks[id1 + '_' + id2]
                            except:
                                try:
                                    id_ks = read_ks[id2 + '_' + id1]
                                except:
                                    # print ("not found " + id1 + '_' + id2)
                                    continue
                            # print(id_ks)
                            if model == 'NG86':
                                ks0 = id_ks[1]
                            elif model == 'YN00':
                                ks0 = id_ks[3]
                            if eval(ks0) >= 10:
                                continue
                            ks_list.append(eval(ks0))
                        # print(ks_list)
                        if ks_list == []:
                            continue
                        ks_list0 = sorted(ks_list)
                        median = np.median(ks_list0)
                        # print(len(ks_list0))
                        average = sum(ks_list0)/float(len(ks_list0))
                        density1 = len(index1)/float(abs(index1[-1] - index1[0]))
                        density2 = len(index2)/float(abs(index2[-1] - index2[0]))
                        print(id1,id2,len(index2),pvalue)
                        # if  len(index2) < eval(self.blocklength) or pvalue < eval(self.e_value):
                        if  len(index2) < eval(self.blocklength):
                            # print(lt)
                            pass
                        else:
                            # print(lt)
                            lt = [num,id1,id2,int(index1[0]),int(index1[-1]),int(index2[0]),int(index2[-1]),len(ks_list0),density1,density2,median,average,score,pvalue]
                            print(lt)
                            with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                                writer = csv.writer(file ,delimiter=',')
                                writer.writerow(lt)
                        id1s,id2s = [],[]
                        index1,index2 = [],[]
                        doc = {}
                        row = row.strip('\n').split()
                        for i in row:
                            if '=' in i:
                                lt = i.split('=')
                                doc[str(lt[0])] = str(lt[1])
                            else:
                                continue
                        score,pvalue = float('inf'),float(0)
        elif self.blockfile_type == 'WGDI':
            f = open(self.blockfile, 'r', encoding='utf-8')
            id1s,id2s = [],[]
            index1,index2 = [],[]
            score,pvalue = 0,0
            for row in f:
                if row[0] != '#' and row[0] != '\n':
                    row = row.strip('\n').split()
                    id1s.append(str(row[0]))
                    id2s.append(str(row[2]))
                    index1.append(eval(row[1]))
                    index2.append(eval(row[3]))
                elif (row[0] == '#'):
                    if len(id1s) == 0:
                        id1s,id2s = [],[]
                        index1,index2 = [],[]
                        doc = {}
                        row = row.strip('\n').split()
                        for i in row:
                            if '=' in i:
                                lt = i.split('=')
                                doc[str(lt[0])] = str(lt[1])
                            else:
                                continue
                        score,pvalue = float(doc['score']),float(doc['pvalue'])
                    else:
                        num += 1
                        ks_list = []
                        for i in range(len(id1s)):
                            id1 = str(id1s[i])
                            id2 = str(id2s[i])
                            try:
                                id_ks = read_ks[id1 + '_' + id2]
                            except:
                                try:
                                    id_ks = read_ks[id2 + '_' + id1]
                                except:
                                    # print ("not found " + id1 + '_' + id2)
                                    continue
                            # print(id_ks)
                            if model == 'NG86':
                                ks0 = id_ks[1]
                            elif model == 'YN00':
                                ks0 = id_ks[3]
                            if eval(ks0) >= 10:
                                continue
                            ks_list.append(eval(ks0))
                        # print(ks_list)
                        if ks_list == []:
                            continue
                        ks_list0 = sorted(ks_list)
                        median = np.median(ks_list0)
                        # print(len(ks_list0))
                        average = sum(ks_list0)/float(len(ks_list0))
                        density1 = len(index1)/float(abs(index1[-1] - index1[0]))
                        density2 = len(index2)/float(abs(index2[-1] - index2[0]))
                        if  len(index2) < eval(self.blocklength) or pvalue < eval(self.e_value):
                            pass
                        else:
                            lt = [num,id1,id2,int(index1[0]),int(index1[-1]),int(index2[0]),int(index2[-1]),len(ks_list0),density1,density2,median,average,score,pvalue]
                            with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                                writer = csv.writer(file ,delimiter=',')
                                writer.writerow(lt)
                        id1s,id2s = [],[]
                        index1,index2 = [],[]
                        doc = {}
                        row = row.strip('\n').split()
                        for i in row:
                            if '=' in i:
                                lt = i.split('=')
                                doc[str(lt[0])] = str(lt[1])
                            else:
                                continue
                        score,pvalue = float(doc['score']),float(doc['pvalue'])
        elif self.blockfile_type == 'ColinearScan':
            f = open(self.blockfile, 'r', encoding='utf-8')
            id1s,id2s = [],[]
            index1,index2 = [],[]
            score,pvalue = 0,0
            for row in f:
                if row[0] != '+' and row[0] != '\n':
                    row = row.strip('\n').split()
                    id10, id20 = str(row[0]),str(row[2])
                    id1s.append(id10)
                    id2s.append(id20)
                    index1.append(int(readname(id10,self.species_list).split('^')[1]))
                    index2.append(int(readname(id20,self.species_list).split('^')[1]))
                elif (row[0] == '#'):
                    if len(id1s) == 0:
                        id1s,id2s = [],[]
                        index1,index2 = [],[]
                        doc = {}
                        row = row.strip('\n').split()
                        for i in row:
                            if '=' in i:
                                lt = i.split('=')
                                doc[str(lt[0])] = str(lt[1])
                            else:
                                continue
                        score,pvalue = float('inf'),float(0)
                    else:
                        num += 1
                        ks_list = []
                        for i in range(len(id1s)):
                            id1 = str(id1s[i])
                            id2 = str(id2s[i])
                            try:
                                id_ks = read_ks[id1 + '_' + id2]
                            except:
                                try:
                                    id_ks = read_ks[id2 + '_' + id1]
                                except:
                                    # print ("not found " + id1 + '_' + id2)
                                    continue
                            # print(id_ks)
                            if model == 'NG86':
                                ks0 = id_ks[1]
                            elif model == 'YN00':
                                ks0 = id_ks[3]
                            if eval(ks0) >= 10:
                                continue
                            ks_list.append(eval(ks0))
                        # print(ks_list)
                        if ks_list == []:
                            continue
                        ks_list0 = sorted(ks_list)
                        median = np.median(ks_list0)
                        # print(len(ks_list0))
                        average = sum(ks_list0)/float(len(ks_list0))
                        density1 = len(index1)/float(abs(index1[-1] - index1[0]))
                        density2 = len(index2)/float(abs(index2[-1] - index2[0]))
                        if  len(index2) < eval(self.blocklength) or pvalue < eval(self.e_value):
                            pass
                        else:
                            lt = [num,id1,id2,int(index1[0]),int(index1[-1]),int(index2[0]),int(index2[-1]),len(ks_list0),density1,density2,median,average,score,pvalue]
                            with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                                writer = csv.writer(file ,delimiter=',')
                                writer.writerow(lt)
                        id1s,id2s = [],[]
                        index1,index2 = [],[]
                        doc = {}
                        row = row.strip('\n').split()
                        for i in row:
                            if '=' in i:
                                lt = i.split('=')
                                doc[str(lt[0])] = str(lt[1])
                            else:
                                continue
                        score,pvalue = float('inf'),float(0)
        elif self.blockfile_type == 'MCScanX':
            f = open(self.blockfile, 'r', encoding='utf-8')
            id1s,id2s = [],[]
            index1,index2 = [],[]
            score,pvalue = 0,0
            for row in f:
                if row[0] != '#' and row[0] != '\n':
                    row = row.strip('\n').split()
                    if len(row) == 5:
                        id10, id20 = str(row[2]),str(row[3])
                    elif len(row) == 4:
                        id10, id20 = str(row[1]),str(row[2])
                    elif len(row) == 6:
                        id10, id20 = str(row[3]),str(row[4])
                    else:
                        print(row)
                        print('Parse error!')
                        exit()
                    id1s.append(id10)
                    id2s.append(id20)
                    index1.append(int(readname(id10,self.species_list).split('^')[1]))
                    index2.append(int(readname(id20,self.species_list).split('^')[1]))
                elif (row[:12] == '## Alignment'):
                    if len(id1s) == 0:
                        id1s,id2s = [],[]
                        index1,index2 = [],[]
                        doc = {}
                        row = row.strip('\n').split()
                        for i in row:
                            if '=' in i:
                                lt = i.split('=')
                                doc[str(lt[0])] = str(lt[1])
                            else:
                                continue
                        score,pvalue = float(doc['score']),float(doc['e_value'])
                    else:
                        num += 1
                        ks_list = []
                        for i in range(len(id1s)):
                            id1 = str(id1s[i])
                            id2 = str(id2s[i])
                            try:
                                id_ks = read_ks[id1 + '_' + id2]
                            except:
                                try:
                                    id_ks = read_ks[id2 + '_' + id1]
                                except:
                                    # print ("not found " + id1 + '_' + id2)
                                    continue
                            # print(id_ks)
                            if model == 'NG86':
                                ks0 = id_ks[1]
                            elif model == 'YN00':
                                ks0 = id_ks[3]
                            if float(ks0) >= 10 or float(ks0) <= 0.0:
                                continue
                            ks_list.append(float(ks0))
                        # print(ks_list)
                        if ks_list == []:
                            continue
                        ks_list0 = sorted(ks_list)
                        median = np.median(ks_list0)
                        # print(len(ks_list0))
                        average = sum(ks_list0)/float(len(ks_list0))
                        density1 = len(index1)/float(abs(index1[-1] - index1[0]))
                        density2 = len(index2)/float(abs(index2[-1] - index2[0]))
                        if  len(index2) < eval(self.blocklength) or pvalue > eval(self.e_value):
                            pass
                        else:
                            lt = [num,id1,id2,int(index1[0]),int(index1[-1]),int(index2[0]),int(index2[-1]),len(ks_list0),density1,density2,median,average,score,pvalue]
                            with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                                writer = csv.writer(file ,delimiter=',')
                                writer.writerow(lt)
                        id1s,id2s = [],[]
                        index1,index2 = [],[]
                        doc = {}
                        row = row.strip('\n').split()
                        for i in row:
                            if '=' in i:
                                lt = i.split('=')
                                doc[str(lt[0])] = str(lt[1])
                            else:
                                continue
                        score,pvalue = float(doc['score']),float(doc['e_value'])
        else:
            print('blockfile_type error: File Format not recognized!')
            exit()

        if len(id1s) != 0:
            num += 1
            ks_list = []
            for i in range(len(id1s)):
                id1 = str(id1s[i])
                id2 = str(id2s[i])
                # print(id1,id2)
                try:
                    id_ks = read_ks[id1 + '_' + id2]
                except:
                    try:
                        id_ks = read_ks[id2 + '_' + id1]
                    except:
                        print("not found " + id1 + '_' + id2)
                        continue
                if model == 'NG86':
                    ks0 = id_ks[1]
                elif model == 'YN00':
                    ks0 = id_ks[3]
                # print(ks0)
                ks_list.append(eval(ks0))
            ks_list0 = sorted(ks_list)
            median = np.median(ks_list0)
            average = sum(ks_list0)/float(len(ks_list0))
            density1 = len(index1)/float(abs(index1[-1] - index1[0]))
            density2 = len(index2)/float(abs(index2[-1] - index2[0]))
            if  len(index2) < eval(self.blocklength) or pvalue < eval(self.e_value):
                pass
            else:
                print(ks0)
                lt = [num,id1,id2,int(index1[0]),int(index1[-1]),int(index2[0]),int(index2[-1]),len(ks_list0),density1,density2,median,average,score,pvalue]
                with open(self.savecsv, "a", newline='', encoding='utf-8') as file:
                    writer = csv.writer(file ,delimiter=',')
                    writer.writerow(lt)
            id1s,id2s = [],[]
            index1,index2 = [],[]
            score,pvalue = 0,0

    def readcsv(self): 
        data = pd.read_csv(self.savecsv,encoding='utf-8')
        lt = [list(data['median']),list(data['average'])]
        return lt

        # 绘制核密度曲线图
    def KdePlot(self,list0):
        vertical = 'False'
        x = list0[0]# 中位数x = list(map(int, x))
        y = list0[1]# 平均数
        plt.figure(figsize=(20,10),dpi=800)
        plt.grid(c='grey',ls='--',linewidth=0.3)
        # print(y)
        dist_space = np.linspace(float(self.area.split(',')[0]),float(self.area.split(',')[1]), 500)
        # print(y)
        kdemedian = gaussian_kde(y)
        kdemedian.set_bandwidth(bw_method=kdemedian.factor / 3.)
        # plt.fill_between(dist_space, y1=0, y2=kdemedian(dist_space), facecolor='#00a3af', alpha=0.5)
        xx = list(dist_space)[list(kdemedian(dist_space)).index(max(list(kdemedian(dist_space))))]
        xx0 = round(xx,4)
        plt.plot(dist_space, kdemedian(dist_space), color='#00a3af',
                 label='average_KDE_' + str(xx0))

        dist_space = np.linspace(float(self.area.split(',')[0]),float(self.area.split(',')[1]), 500)
        kdemedian = gaussian_kde(x)
        kdemedian.set_bandwidth(bw_method=kdemedian.factor / 3.)
        plt.fill_between(dist_space, y1=0, y2=kdemedian(dist_space), facecolor='#d3381c', alpha=0.5)
        xx = list(dist_space)[list(kdemedian(dist_space)).index(max(list(kdemedian(dist_space))))]
        xx0 = round(xx,4)
        plt.plot(dist_space, kdemedian(dist_space), color='#d3381c',
                 label='median_KED_' + str(xx0))
        plt.legend()
        plt.title(self.species_list + ' block Ks kernel density estimation')# 设置图片标题
        plt.xlabel('ks')# 设置 x 轴标签
        plt.ylabel('density')# 设置 y 轴标签

    def run(self):
        if (os.path.exists(self.savecsv)):
            os.remove(self.savecsv)
        read_ks = self.readks()
        self.readblock(read_ks)
        lt = self.readcsv()
        print(lt)
        self.KdePlot(lt)
        plt.savefig(self.savefile)# 存储图片
        sys.exit(0)
