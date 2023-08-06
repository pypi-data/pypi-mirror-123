# -*- encoding: utf-8 -*-
'''
@File        :hmmer.py
@Time        :2021/09/28 11:23:06
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :扫描hmm
'''



import Bio
from glob import glob
from Bio.Align.Applications import ClustalwCommandline
from Bio import Seq
from Bio import SeqIO
from Bio import AlignIO
from Bio.SeqRecord import SeqRecord
import subprocess
from subprocess import Popen


import re
import os
from math import *
import csv
import pandas as pd
from matplotlib.patches import *
from pylab import *
from famCircle.bez import *
#system 阻塞

class hmmer():
    def __init__(self, options):
        self.cds = None
        base_conf = config()
        for k, v in base_conf:
            setattr(self, str(k), v)
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readlist(self,filename,value):
        name = []
        f = open(filename, 'r', encoding='utf-8')
        for row in f:
            if row != '\n' and row[0] != '#':
                row = row.strip('\n').split()
                if eval(row[6]) < float(value):
                    if ('>' + str(row[0]) not in name):
                        name.append('>' + str(row[0]))
        if len(name) == 0:
            print("Warning: Screening is too strict!")
        return name

    def readpep(self):
        peplist = {}
        f =open(self.pep, 'r', encoding='utf-8')
        s = ''
        name = ''
        for row in f:
            if row[0] == '>':
                if s != '' and name != '':
                    peplist[name] = s
                    s = ''
                    name = ''
                name = row.strip('\n')
            elif row == '\n':
                pass
            else:
                s = s + row
        if s != '' and name != '':
            peplist[name] = s
        del name, s
        return peplist

    def readcds(self):
        cdslist = {}
        f =open(self.cds, 'r', encoding='utf-8')
        s = ''
        name = ''
        for row in f:
            if row[0] == '>':
                if s != '' and name != '':
                    cdslist[name] = s
                    s = ''
                    name = ''
                name = row.strip('\n')
            elif row == '\n':
                pass
            else:
                s = s + row
        if s != '' and name != '':
            cdslist[name] = s
        del name, s
        return cdslist

    def writepep(self,pash0,name,seq,file):
        f = open(pash0 + file, 'a+', encoding='utf-8')
        f.write(name + '\n')
        f.write(seq)
        f.close()


    def runhmm(self, hmmmold, path):
        names = hmmmold[:-4]
        hmmer = self.hmmer_path
        hmmsearch = hmmer + 'hmmsearch'
        hmmbuild = hmmer + 'hmmbuild'
        m1 = hmmsearch + ' --domtblout one.out -E ' + self.e_value1 + ' ' + hmmmold + ' ' + self.pep
        if os.path.exists('one.out'):
            os.remove ('one.out')
        d = os.system(m1)# 第一次搜索
        # x = input()######################
        list1 = self.readlist('one.out',self.e_value1)# 第一次筛选
        os.remove ('one.out')
        # print(list1)
        if len(list1) == 0:
            print('STEP 1 :No data fit the model')
            return 0
        peplist = self.readpep()
        if os.path.exists('one.pep'):
            os.remove ('one.pep')
        for i in list1:# 第一次生成筛选之后的pep
            if i in peplist.keys():
                seq = peplist[i]
                pash0 = './'
                self.writepep(pash0,i,seq,'one.pep')
            else:
                pass
        # Clustalw = '/usr/bin/clustalw'
        in_file = 'one.pep'
        # if os.path.exists(name + 'out.aln'):
        #     os.remove (name + 'out.aln')
        name0 = str(names.split('/')[-1])
        out_file ='./out_aln/' + name0 + '.aln'
        # 第一次生成aln比对文件
        if (self.comparison == "clustal"):
            self.clustalw_path = self.clustalw_path
            # print(self.clustalw_path)
            Clustalw_cline = ClustalwCommandline(cmd = self.clustalw_path, infile=in_file, outfile=out_file, align=True, outorder="ALIGNED", convert=True, output="pir")
            # x = input()
            a, b = Clustalw_cline()
        elif (self.comparison == 'muscle'):
            out_file1 = out_file[:-4] + '.aln'
            ml4 = self.muscle_path + 'muscle -in ' + in_file + ' -clw -out ' + out_file1
            d = os.system(ml4)
            ml5 = hmmbuild + ' ./out_hmm/' + name0 + '.hmm ' + out_file1
            d = os.system(ml5)
        elif (self.comparison == 'mafft'):
            out_file1 = out_file[:-4] + '.aln'
            ml6 = self.mafft_path + 'mafft --auto --clustalout '+ in_file + ' > ' + out_file1
            d = os.system(ml6)
            ml7 = hmmbuild + ' ' + name0 + '.hmm ' + out_file1
            d = os.system(ml7)
        os.remove ('one.pep')
        if (os.path.exists('one.dnd')):
            os.remove ('one.dnd')
        # x = input()
        # print(Clustalw_cline)
        m2 = hmmbuild + ' ./out_hmm/' + name0 + '.hmm ./out_aln/' + name0 + '.aln'
        # print(m2)
        d = os.system(m2)# 格式转换
        # print(m2)
        m3 = hmmsearch + ' --domtblout ./out_list/' + name0 + '.out -E ' + self.e_value2 + ' ./out_hmm/' + name0 + '.hmm ' + self.pep
        # x = input()##################
        d = os.system(m3)# 第二次搜索，生成out文件
        # print(m3)
        hmmlist = './out_list/' + name0 + '.out'
        # print(hmmlist)
        list2 = self.readlist(hmmlist,self.e_value2)# 第二次筛选
        print('Number of gene families: ',len(list2))
        peplist = self.readpep()
        curb = 0
        if self.cds != None:
            cdslist = self.readcds()
            curb = 1
        if len(peplist) == 0:
            print('SETP 2 :No data fit the newmodel')
            return 0
        for i in list2:
            if i in peplist.keys():
                seq = peplist[i]
                file = name0 + '.pep'
                pash0 = './out_pep/'
                self.writepep(pash0,i, seq, file)
            if curb == 1:
                if i in cdslist.keys():
                    cdsseq = cdslist[i]
                    file = name0 + '.cds'
                    pash0 = './out_cds/'
                    self.writepep(pash0,i, cdsseq, file)
        return 1
    def changefile(file,list, hmmpath):
        lix = []
        for i in list:
            name = str(i) + '.hmm'
            oldname = str(i) + '.txt'
            d = os.system("hmmbuild %s %s" % (name, oldname))
            lix.append(str(i))
        return lix

    def readpwd(self, path):
        filelist = []
        path_list=os.listdir(path)
        path_list.sort() #对读取的路径进行排序
        for filename in path_list:
            name = os.path.join(path,filename)
            filelist.append(name[:-4])
        return filelist
    def run(self):
        # pa = os.getcwd()
        if os.path.isdir('./out_hmm') and os.path.isdir('./out_cds') and os.path.isdir('./out_pep') and os.path.isdir('./out_list') and os.path.isdir('./out_aln'):
            pass
        else:
            d = os.mkdir("out_hmm")
            d = os.mkdir("out_cds")
            d = os.mkdir("out_pep")
            d = os.mkdir("out_list")
            d = os.mkdir("out_aln")
            print('successfully mkdir')
        hmmpath = self.hmmmoldpath
        hmmlistname = self.readpwd(hmmpath)
        if self.format_conversion == 'True':
            hmmlistname = self.changefile(hmmlistname, hmmpath)
        else:
            pass
        # print(hmmlistname)
        for i in hmmlistname:# 遍历模型文件
            i = i + '.hmm'
            # print(i, '******', hmmpath)
            x = self.runhmm(i, hmmpath)
            if x == 0:
                continue