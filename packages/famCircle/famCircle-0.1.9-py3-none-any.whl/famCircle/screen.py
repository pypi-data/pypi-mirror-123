# -*- encoding: utf-8 -*-
'''
@File        :screen.py
@Time        :2021/09/28 09:03:54
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :分染色体展示家族分布折线图
'''


from famCircle.bez import *
import os
import sys
from pylab import *

class screen():
    def __init__(self, options):
        # self.color = ['red', 'fuchsia', 'aquamarine', 'orangered', 'violet', 'lime', 'chocolate', 'blueviolet', 'limegreen', 'orange', 'royalblue', 'gold', 'dodgerblue', 'yellow', 'cyan', 'yellowgreen', 'teal', 'palegreen']
        self.marker = ['.','o','^','v','<','>','s','+','x']
        self.color = ['red', 'fuchsia', 'aquamarine', 'orangered', 'violet', 'lime', 'chocolate', 'blueviolet', 'limegreen', 'orange', 'royalblue', 'gold', 'dodgerblue', 'yellow', 'cyan', 'yellowgreen', 'teal', 'palegreen']
        self.ls = ['-','-','-']
        self.series = "25"
        self.position = 'order'
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def run_plot(self,x_axis_data,y_axis_data,name,tup,domain):
        linestyle = str(tup[0])
        marker = str(tup[1])
        color = str(tup[2])
        # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
        plt.plot(x_axis_data, y_axis_data, marker = marker, markersize = 0.5, linestyle = linestyle, color = color, alpha = 0.5, linewidth = 1, label = domain)
        # 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
        plt.xlabel('chr')
        plt.ylabel('gene')

    def readgf(self,file):
        f = open(self.domainpath + '/' + file, 'r', encoding='utf-8')
        genef = []
        for row in f:
            if row[0] != "#" or row != '\n':
                row = row.strip('\n').split()
                name = readname(str(row[0]),self.chro_name)
                if name not in genef:
                    genef.append(name)
        for i in genef:
            if i == None:
                genef.remove(None)
        return genef

    def readgff(self):# 基因开始位点 字典嵌套
        f = open(self.gff,'r', encoding='utf-8')
        genechrs = {}
        gene = {}
        genechr = []
        a = 0
        for row in f:
            if row[0] != '\n' and row[0] != '#':
                row = row.strip('\n').split('\t')
                name = readname(str(row[1]),self.chro_name)
                if name in gene.keys():
                    continue
                if str(row[0]) not in genechr:
                    if a == 1:
                        genechrs[str(genechr[-1])] = gene
                        gene = {}
                        a = 0
                    genechr.append(str(row[0]))
                    gene[name] = str(row[2])
                else:
                    gene[name] = str(row[2])
                    a = 1
        if a == 1:
            genechrs[str(genechr[-1])] = gene
        f.close()
        # print(genechrs)
        return genechrs

    def readlens(self):# 基因开始位点
        f = open(self.lens,'r', encoding='utf-8')
        chrs = {}
        for row in f:
            if row[0] != '\n' and row[0] != '#':
                row = row.strip('\n').split('\t')
                chrs[str(row[0])] = str(row[1])
        f.close()
        return chrs

    def numb(self,i):
        ls = self.ls[i % 3]
        marker = self.marker[i % 9]
        color = self.color[i % 18]
        return ls,marker,color

    def chrlist(self,chrs,length):
        newchrlength = {}
        for chr0 in chrs.keys():
            newlength = int(chrs[chr0]) + length * (int(self.series) - ((int(chrs[chr0]) \
                + (length - (int(chrs[chr0]) % length))) % int(self.series)))
            jishu = newlength / (length * int(self.series))# 级数
            newchrlength[chr0] = jishu
        return newchrlength

    def run(self):
        if os.path.isdir(self.outpath):
            pass
        else:
            d = os.mkdir(self.outpath)
        length = gene_length(self.gff)
        gene = self.readgff()
        chrs = self.readlens()
        name = os.listdir(self.domainpath)
        domains = {}
        for i in range(len(name)):

            domain = name[i]
            # print(domain)
            nm = str(str(domain).split('.')[0])
            # print(nm)
            domains[nm] = self.readgf(domain) + [self.numb(i)]
        data = {}
        for key in domains.keys():# 遍历结构域
            # print(key)
            chrx = {}
            
            sx = domains[key][-1]
            lt = domains[key][:-1]
            # print(key)
            # print(lt)
            chrx['att'] = sx
            for j in range(len(lt) - 1):# 遍历基因
                jishu = {}
                i = lt[j]
                chrg = str(str(i).split('^')[0])
                start = gene[chrg][i]
                
                jishug = int(int(start)/(int(self.series) * length))
                # print(chrg,jishug)
                if chrg not in chrx.keys():
                    jishu[jishug] = 1
                    chrx[chrg] = jishu
                else:
                    if jishug in chrx[chrg].keys():
                        chrx[chrg][jishug] += 1
                    else:
                        chrx[chrg][jishug] = 1
            for i in list(chrx.keys()):
                # print(type(chrx[i]))
                try:
                    length0 = max(list(chrx[i].keys()))
                    # print(length0)
                    for j in range(length0 + 1):
                        if j in list(chrx[i].keys()):
                            pass
                        else:
                            chrx[i][j] = 0
                except:
                    pass
                
            # print("#####################################")
            data[key] = chrx
            chrx = {}
        chry = []
        for domain in data.keys():
            for ch in data[domain].keys():
                if str(ch) == 'att':
                    continue
                else:
                    chry.append(ch)
            break
        domains = list(data.keys())
        # print(data['PF05659_seed']['ath4'])
        # print(data['PF05659_seed']['ath3'])
        # print(domains)
        for i in chry:
            for j in domains:
                tup = data[j]['att']
                name = str(i) + '_' + str(j) + '.png'
                x = sorted(data[j][i].keys())
                # x = list(data[domain][ch].keys())
                y = []
                for o in x:
                    y.append(data[j][i][o])
                self.run_plot(x,y,name,tup,j)
            plt.title(i)
            plt.savefig(self.outpath + '/' +str(i),dpi = 1000,bbox_inches='tight')  # 保存该图片
            plt.cla()
        sys.exit(0)
