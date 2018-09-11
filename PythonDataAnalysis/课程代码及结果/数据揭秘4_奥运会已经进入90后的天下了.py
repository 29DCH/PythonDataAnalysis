# -*- coding: utf-8 -*-
"""
《数据分析师python微专业》 - 前置课

Part04 数据揭秘：用数据八卦运动员

4、奥运会已经进入90后的天下了？

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

df = pd.read_excel('奥运运动员数据.xlsx',sheetname=1,header=0)
df_length = len(df)
df_columns = df.columns.tolist()
# 查看数据
# pd.read_excel → 读取excel文件，这里得到的是pandas的dataframe数据格式

'''
(1) 按照项目分类做年龄数据分布图
'''

data = df[['event','name','birthday']]
data.dropna(inplace = True)   # 去掉缺失值
# 筛选数据，按照目标字段筛选

data.index = pd.to_datetime(data['birthday'])   # 将出生年月改为时间序列
data['birthyear'] = data.index.year
data['age'] = 2016 - data['birthyear']# 计算出年龄
data['age_range'] = pd.cut(data['age'],
                          [0,26,60],            # 划分区间
                          labels=["90s", "not 90s"])   # 区间标签 

sns.set_style("ticks")  # 图表风格设置
g = sns.FacetGrid(data, col="event", hue = 'age_range',palette="Set2_r",
                  size=2.5,    # 图表大小
                  aspect=1.2,
                 col_wrap=3,sharex=False,
                xlim=[15,40], ylim=[0,14]) # 图表长宽比
# 创建绘图区域及读取数据

g.map(sns.stripplot,"age",jitter=True,
     size = 10, edgecolor = 'w',linewidth=1,marker = 'o')
g.add_legend()  # 图例
plt.savefig('pic5.png',dpi=400)
# 按照项目分类绘制年龄数据分布图，并图表导出

'''
(2) 按照项目分类做年龄划分曲线图
'''

data['age_range'] = pd.cut(data['age'],
                          [0,26,36,60],            # 划分区间
                          labels=[1,2,3])          # 区间标签 
data2 = data.groupby(['event','age_range']).count()
data2.reset_index(inplace=True)
data2.fillna(0,inplace = True)
data2['count'] = data2['name']
# 得到不同项目的年龄划分数据

g = sns.FacetGrid(data2, col="event", col_wrap=3,   # 设置每行的图表数量
                  size=2.5,    # 图表大小
                  aspect=1.2,sharex=False,)
g.map(plt.plot, "age_range", "count", 
      marker="o",color = 'gray',linewidth = 2)
# 绘制图表矩阵
g.set(xlim = (0,4),
      ylim = (-10,40),
      xticks = [0,1,2,3,4],
      xticklabels = ['',"90s", "80s",">80s",''],
      yticks = [0,10,20,30,40])
# 图表设置
g.add_legend()  # 图例
plt.savefig('pic6.png',dpi=400)
# 图表导出

