# -*- coding: utf-8 -*-
"""
《数据分析师python微专业》 - 前置课

Part04 数据揭秘：用数据八卦运动员

2、运动员身材都是完美型吗?

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

data = df[['event','name','height','weight']]
# 筛选数据，按照目标字段筛选

event_count = data['event'].value_counts()
event_drop = event_count[event_count<15]   # 这里是通过判断做索引
# 查看数据样本中少于15人的项目

data2 = data[data['event'] != 'swim']
data2.dropna(inplace = True)
# 数据清洗，去掉运动员少于15人的项目数据 + 去掉缺失值

data2['BMI'] = data2['weight']/(data2['height']/100)**2   # **2 → 平方
data2['BMI_range'] = pd.cut(data2['BMI'],
                            [0,18.5,24,28,50],            # 划分区间
                            labels=["Thin", "Normal", "Strong",'ExtremelyStrong'])   # 区间标签   
# 计算运动员BMI指数，并整理出BMI区间值
# 这里根据运动员特点，设置为四挡：低于18.5纤瘦，18.5-23.9适中，24-27强壮，28-32极壮
# pandas.cut → 划分区间，并返回shape相同的dataframe

sns.set_style("ticks")
# 图表风格设置
# 风格选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"

plt.figure(figsize = (8,4))  # 设置作图大小
sns.violinplot(x="event", y="BMI", data=data2,   # 设置数据
               scale = 'count',      # 宽度以样本数量来显示 → 数据样本越多，小提琴图越宽
               palette = "hls",      # 设置调色盘      
               inner = "quartile")   # 内部显示为分位数
# 绘制小提琴图

sns.swarmplot(x="event", y="BMI", data=data2, color="w", alpha=.8,s=2)
# 绘制内部散点图

plt.grid(linestyle = '--')     # 添加网格线
plt.title("Athlete's BMI")  # 添加图表名
# 图表其他内容

plt.savefig('pic2.png',dpi=400)
# 图表导出

data2[data2['BMI']>30]
# 查看BMI大于30的运动员