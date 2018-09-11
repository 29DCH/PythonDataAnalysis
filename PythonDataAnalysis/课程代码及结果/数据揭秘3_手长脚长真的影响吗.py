# -*- coding: utf-8 -*-
"""
《数据分析师python微专业》 - 前置课

Part04 数据揭秘：用数据八卦运动员

3、手长脚长真的影响吗?

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

data = df[['event','name','height','arm','leg']]
data.dropna(inplace = True)   # 去掉缺失值
# 筛选数据，按照目标字段筛选

data['arm/h'] = data['arm'] / data['height']
data['leg/h'] = data['leg'] / data['height']
data = data[data['leg/h']<0.7]
data = data[data['arm/h']>0.7]
#data[['arm/h','leg/h']].boxplot(whis = 3)   # 用直方图查看数据分布
# 分别计算“臂展/身高”、“腿长/身高”

events = data['event'].value_counts().index.tolist()
# 提取样本数据的所有项目

event_data = []
for i in events:
    data_i = data[data['event'] == i]   # 获取项目数据
    event_data.append(data_i)
# 将数据按照项目类型拆分

pla = sns.color_palette('hls',len(events))
sns.palplot(pla)
# 设置调色盘

sns.set_style("darkgrid")
# 图表风格设置
# 风格选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"

g = sns.jointplot(x=data['arm/h'], y=data['leg/h'],data = data,
                  kind="kde", color='k',   # 这里color = color中，第一个color为参数，第二个color为变量
                  alpha = 0.6,shade_lowest=False)
g.plot_joint(plt.scatter,c='w',s=15, linewidth=1, marker="+")
plt.savefig('pic3.png',dpi=400)
# 绘制二维散点图并导出图表


sns.lmplot(x='arm/h', y='leg/h', col="event", hue="event",data=data, palette="Set1",
           x_jitter=.30,  # 给x或者y轴随机增加噪音点
           col_wrap=3,   # 每行的列数
           size = 2.5,markers='.'
          )
plt.savefig('pic4.png',dpi=400)
# 绘制回归矩阵图，并导出图表