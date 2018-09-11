# -*- coding: utf-8 -*-
"""
《数据分析师python微专业》 - 前置课

Part04 数据揭秘：用数据八卦运动员

1、身高越高越容易参加奥运吗?

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

data = df[['event','name','gender','height']]
data.dropna(inplace = True)   # 去掉缺失值
data_male = data[data['gender'] == '男']
data_female = data[data['gender'] == '女']
# 筛选数据，按照目标字段筛选
# 提取男女数据

hmean_male = data_male['height'].mean()
hmean_female = data_female['height'].mean()
# 计算男女平均身高

sns.set_style("ticks")
# 图表风格设置
# 风格选择包括："white", "dark", "whitegrid", "darkgrid", "ticks"

plt.figure(figsize = (8,4))  # 设置作图大小
sns.distplot(data_male['height'],hist = False,kde = True,rug = True,
             rug_kws = {'color':'y','lw':2,'alpha':0.5,'height':0.1} ,   # 设置数据频率分布颜色
             kde_kws={"color": "y", "lw": 1.5, 'linestyle':'--'},        # 设置密度曲线颜色，线宽，标注、线形
             label = 'male_height')
sns.distplot(data_female['height'],hist = False,kde = True,rug = True,
             rug_kws = {'color':'g','lw':2,'alpha':0.5} , 
             kde_kws={"color": "g", "lw": 1.5, 'linestyle':'--'},
             label = 'female_height')
# 绘制男女高度分布密度图

plt.axvline(hmean_male,color='y',linestyle=":",alpha=0.8) 
plt.text(hmean_male+2,0.005,'male_height_mean: %.1fcm' % (hmean_male), color = 'y')
# 绘制男运动员平均身高辅助线

plt.axvline(hmean_female,color='g',linestyle=":",alpha=0.8)
plt.text(hmean_female+2,0.008,'female_height_mean: %.1fcm' % (hmean_female), color = 'g')
# 绘制女运动员平均身高辅助线

plt.ylim([0,0.03])
plt.grid(linestyle = '--')     # 添加网格线
plt.title("Athlete's height")  # 添加图表名
# 图表其他内容

plt.savefig('pic1.png',dpi=400)
# 图表导出