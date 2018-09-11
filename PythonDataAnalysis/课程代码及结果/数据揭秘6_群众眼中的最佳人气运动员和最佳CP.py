# -*- coding: utf-8 -*-
"""
《数据分析师python微专业》 - 前置课

Part04 数据揭秘：用数据八卦运动员

6、群众眼中的最佳人气运动员和最佳CP

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 分别导入numpy、pandas、matplotlib、seaborn模块
# numpy - Python的数值计算扩展工具包
# pandas - 基于Numpy的数据处理工具包
# matplotlib - Python的2D绘图工具包
# seaborn - matplotlib基础上的高级可视化工具包

import warnings
warnings.filterwarnings('ignore') 
# 不发出警告

import os
os.chdir('C:\\Users\\Hjx\\Desktop\\')
# 创建工作路径

df = pd.read_excel('奥运运动员数据.xlsx',sheetname=0,header=0)
df_length = len(df)
df_columns = df.columns.tolist()
# 查看数据
# pd.read_excel → 读取excel文件，这里得到的是pandas的dataframe数据格式

'''
(1) 分析最佳人气运动员
'''

fig = plt.figure(figsize=(12,6.25))
plt.subplots_adjust(wspace=0.25,hspace=0.35)

n = 0
for i in ['百度搜索结果数量','Bing搜索结果数量','近7天整体搜索指数','近30天整体搜索指数','当月平均','当月最高']:
    c = plt.cm.brg(np.linspace(0, 0.7,6))[n]
    axi = fig.add_subplot(2,3,n+1)
    datai = df[['姓名',i]]
    datai.sort_values(by = i,inplace = True,ascending=False)
    datai.reset_index(inplace=True)
    #print(datai[i])
    datai[i].plot(kind='line',
       style = '--x',
       alpha = 0.8,
       use_index = True,
       title = i,
       subplots = False,
       color = c,
       )
    axi.set_xticklabels(datai['姓名'].tolist())
    plt.grid(linestyle = '--')
    n += 1
    
plt.savefig('pic10.png',dpi=400)
# 图表导出

'''
(2) 分析最佳CP - 数据处理及导出
'''

df2 = pd.read_excel('奥运运动员数据.xlsx',sheetname=2,header=0)
df2_length = len(df2)
df2_columns = df2.columns.tolist()
# 查看数据
# pd.read_excel → 读取excel文件，这里得到的是pandas的dataframe数据格式

df2.replace([np.nan,'无数据','无贴吧'],0,inplace=True)
# 数据清洗

df2['n1'] = (df2['cp微博数量']-df2['cp微博数量'].min())/(df2['cp微博数量'].max()-df2['cp微博数量'].min())
df2['n2'] = (df2['cp微博话题阅读量']-df2['cp微博话题阅读量'].min())/(df2['cp微博话题阅读量'].max()-df2['cp微博话题阅读量'].min())
df2['n3'] = (df2['B站cp视频播放量']-df2['B站cp视频播放量'].min())/(df2['B站cp视频播放量'].max()-df2['B站cp视频播放量'].min())
df2['f'] = df2['n1']*0.5 + df2['n2']*0.3 + df2['n3']*0.2
# 计算综合热度

df2.sort_values(by = 'f',inplace = True,ascending=False)
df2.reset_index(inplace=True)
# 数据重新排序

result = df2[['p1','p2','f']]
writer = pd.ExcelWriter('output.xlsx')
result.to_excel(writer,'sheet1')
writer.save()
# 数据导出excel文件

