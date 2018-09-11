# -*- coding: utf-8 -*-
"""
《数据分析师python微专业》 - 前置课

Part04 数据揭秘：用数据八卦运动员

5、谁是身材最佳的运动员？

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
(1) 分析运动员全样本数据的身材分布情况
'''

data = df[['event','name','birthday','height','arm','leg','weight','age']]
data.dropna(inplace = True)   # 去掉缺失值
# 筛选数据，按照目标字段筛选

data['BMI'] = data['weight']/(data['height']/100)**2   
# 求BMI

data['arm/h'] = data['arm'] / data['height']
data['leg/h'] = data['leg'] / data['height']
data = data[data['leg/h']<0.7]
data = data[data['arm/h']>0.7]
# 分别计算“臂展/身高”、“腿长/身高”，并删除异常数据

data_re = data[['event','name','arm/h','leg/h','BMI','age']]
# 重新新建结果数据data_re

data_re['BMI_assess'] = np.abs(data['BMI'] - 22)   # BMI评估 → 最接近22，差值绝对值越小分数越高
data_re['leg_assess'] = data['leg/h']              # 腿长评估 → 与身高比值，越大分数越高
data_re['arm_assess'] = np.abs(data['arm/h'] - 1)  # 手长评估 → 与身高比值最接近1，差值绝对值越小分数越高
data_re['age_assess'] = data['age']                # 年龄评估 → 最小，越小分数越高

data_re['BMI_nor'] = (data_re['BMI_assess'].max() - data_re['BMI_assess'])/(data_re['BMI_assess'].max()-data_re['BMI_assess'].min())
data_re['leg_nor'] = (data_re['leg_assess'] - data_re['leg_assess'].min())/(data_re['leg_assess'].max()-data_re['leg_assess'].min())              
data_re['arm_nor'] = (data_re['arm_assess'].max() - data_re['arm_assess'])/(data_re['arm_assess'].max()-data_re['arm_assess'].min()) 
data_re['age_nor'] = (data_re['age_assess'].max() - data_re['age_assess'])/(data_re['age_assess'].max()-data_re['age_assess'].min())
# 标准化

data_re['final'] = (data_re['BMI_nor']+data_re['leg_nor']+data_re['arm_nor']+data_re['age_nor'])/4
# 计算总体评价结果

plt.figure(figsize = (10,6))
data_re.sort_values(by = 'final',inplace = True,ascending=False)
data_re.reset_index(inplace=True)
# 排序并重新设定index

data_re[['age_nor','BMI_nor','leg_nor','arm_nor']].plot.area(colormap = 'PuRd',alpha = 0.5,figsize = (10,6))
plt.ylim([0,4])
plt.grid(linestyle = '--')
plt.savefig('pic7.png',dpi=400)
# 绘制运动员身材数据分布图表，并导出

'''
(2) 解读身材最好的前8位运动员
'''

datatop8 = data_re[:8]
# 数据筛选

fig = plt.figure(figsize=(15,6))
plt.subplots_adjust(wspace=0.35,hspace=0.5)

n = 0
for i in datatop8['name'].tolist():
    n += 1
    c = plt.cm.BuPu_r(np.linspace(0, 0.7,10))[n-1]
    axi = plt.subplot(2,4,n, projection = 'polar')
    datai = datatop8[['BMI_nor','leg_nor','arm_nor','age_nor']][datatop8['name']==i].T
    scorei = datatop8['final'][datatop8['name']==i]
    angles = np.linspace(0, 2*np.pi, 4, endpoint=False)
    #axi.plot(angles,datai,linestyle = '-',lw=1,color = c)
    plt.polar(angles, datai, 'o-', linewidth=1,color = c)
    axi.fill(angles,datai,alpha=0.5,color=c)
    axi.set_thetagrids(np.arange(0.0, 360.0, 90),['BMI','腿长/身高','臂长/身高','年龄'])
    axi.set_rgrids(np.arange(0.2,1.5,0.2),'--')
    plt.title('Top%i %s: %.3f\n' %(n,i,scorei))
# 分别绘制每个运动员的评分雷达图

plt.savefig('pic8.png',dpi=400)
# 图表导出

'''
(3) 看不同项目的运动员身材情况
'''

plt.figure(figsize = (12,6))  # 设置作图大小
sns.boxplot(x="event", y="final",data = data_re,
            linewidth = 1,   # 线宽
            width = 0.6,     # 箱之间的间隔比例
            fliersize = 2,   # 异常点大小
            palette = 'YlGnBu', # 设置调色板
            whis = 1.5,      # 设置IQR 
            #order = ['Thur','Fri','Sat','Sun'],  # 筛选类别
           )
sns.swarmplot(x="event", y="final",data = data_re,color ='k',size = 3,alpha = 0.8)
plt.grid(linestyle = '--')
plt.ylabel('Final score')
plt.savefig('pic9.png',dpi=400)
# 图表导出