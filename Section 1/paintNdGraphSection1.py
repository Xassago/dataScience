import numpy as np
import matplotlib.pyplot as plt
import math
import json
import os


def gd(x, mu=0, sigma=1):
    """根据公式，由自变量x计算因变量的值
    Argument:
        x: array
            输入数据（自变量）
        mu: float
            均值
        sigma: float
            方差
    """
    left = 1 / (np.sqrt(2 * math.pi) * np.sqrt(sigma))
    right = np.exp(-(x - mu) ** 2 / (2 * sigma))
    return left * right  # 此处为正态分布的概率密度公式


f = open('data/ndDataForGraphSection1.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

# 这两行设置使得图中可以显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

numOfData = 0  # 数据量，共80个
for key in data.keys():
    print(len(data[key]))
    numOfData += len(data[key])
titleAndColor = {'program_rate': 'blue', 'debug_rate': 'red',
                 'early_success_degree': 'orange', 'finish_degree': 'pink'}
# path = 'E:/大二下/数据科学基础/大作业/dataScience/Section 1/graph/ndGraph'
path = './graph/ndGraph'
isNeedToSave = (len(os.listdir(path)) == 0)

print("画图进度：")
numToPaintOfEachType = 5  # 每种指标要画的图的个数
count = 1  # 计已画的图的个数

for attribute in data.keys():
    values = data[attribute]
    for i in range(numToPaintOfEachType):
        item = values[i]
        avg = np.mean(item)
        var = np.var(item)
        #  自变量
        x = np.arange(math.floor(avg - 5), math.ceil(avg + 5), 0.05)  # 参数：起点，终点，步长
        #  因变量
        y = gd(x, avg, var)
        #  绘图
        plt.plot(x, y, color=titleAndColor[attribute])
        #  设置坐标系
        plt.xlim(math.floor(avg - 5), math.ceil(avg + 5))
        plt.ylim(-0.2, math.ceil(gd(avg, avg, var)))

        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))

        signal = '$\mu=' + str(round(avg, 2)) + ', \sigma^2=' + str(round(var, 2)) + '$'
        title = attribute + str(i)
        plt.title(title, fontsize=15)
        plt.legend(labels=[signal])

        if isNeedToSave:  # 如果该文件夹为空，保存（防止再运行时重复保存）
            plt.savefig(path + '/' + title + '.png')  # 保存图片

        plt.show()

        print(str(round(count / (numToPaintOfEachType * 4), 4) * 100) + '%')  # 打印进度
        count += 1
