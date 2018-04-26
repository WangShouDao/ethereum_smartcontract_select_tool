# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd

# 读取日期数据
def read_data(filename):
    contracts_date = {}
    with open(filename, 'r+') as f:
        line = f.read().strip().split('\n')
        for items in line:
            items = eval(items)
            if items['dateVf'] not in contracts_date.keys():
                contracts_date[items['dateVf']] = 1
            else:
                contracts_date[items['dateVf']] += 1
    # 合约的创建数量按时间排序
    contracts_date1 = {}
    for items in contracts_date:
        tmp = list(items.split('/'))[::-1]
        string = str(tmp[0])+'/'
        string += (str(0)+str(tmp[2])+'/' if int(tmp[2])<10 else str(tmp[2])+'/')
        string += (str(0) + str(tmp[1]) if int(tmp[1]) < 10 else str(tmp[1]) )
        contracts_date1[string] = contracts_date[items]
    contracts_date1 = [(k, contracts_date1[k]) for k in sorted(contracts_date1.keys())]
    temp1, temp2 = [], []
    for i in range(len(contracts_date1)):
        temp1.append(contracts_date1[i][0])
        temp2.append(contracts_date1[i][1])
    return temp1, temp2

# 画出折线图
def draw_plot1(filename):
    x, y =read_data(filename)
    y2 = [y[0]]
    for i in range(1,len(y)):
        tmp=y[i]+y2[-1]
        y2.append(tmp)
    x = [datetime.strptime(d, '%Y/%m/%d').date() for d in x]
    # 配置横坐标
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # 设置时间间隔
    # plt.xticks(pd.date_range(start=x[0], end=x[-1],freq='90D'))
    plt.plot(x,y,color='r',linewidth=1,label='contracts count')
    # 设置中文字体
    plt.title(u'每天创建的合约数',fontproperties='SimHei')
    plt.xlabel('Date')
    plt.ylabel('Contracts  Number')
    # 自动旋转日期标记
    # plt.gcf().autofmt_xdate()
    # 图例
    # plt.legend(loc='upper center', shadow = True)
    plt.grid(True, linestyle='--',linewidth=1,c='gray')
    plt.show()

def draw_plot2(filename):
    x, y = read_data(filename)
    y2 = [y[0]]
    for i in range(1, len(y)):
        tmp = y[i] + y2[-1]
        y2.append(tmp)
    x = [datetime.strptime(d, '%Y/%m/%d').date() for d in x]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.plot(x,y2,color='g',linestyle='-',linewidth=1,label='contracts sum')
    plt.title(u"累计创建的合约数",fontproperties='SimHei')
    plt.xlabel('Date')
    plt.ylabel('Contracts Number')
    plt.grid(True, linestyle='--', linewidth=1, c='gray')
    plt.show()

# 画出散点图
def draw_scatter(filename):
    x, y = read_data(filename)
    y2 = [y[0]]
    for i in range(1, len(y)):
        tmp = y[i] + y2[-1]
        y2.append(tmp)
    x = [datetime.strptime(d, '%Y/%m/%d').date() for d in x]
    # 设置双y轴
    fig,ax1=plt.subplots()
    ax1.scatter(x, y, c='r', linewidth=1, s=1)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('contracts count')
    ax1.set_title(u'以太坊上的合约',fontproperties='SimHei')
    ax1.set_ylim(0,250,5)
    ax2 = ax1.twinx()
    ax2.scatter(x, y2, s=1)
    ax2.set_ylabel('contracts sum')
    ax2.set_ylim(0,25000,5)
    plt.grid(True, linestyle='--', linewidth=1, c='gray')
    plt.show()