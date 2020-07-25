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


f = open('data/ndDataForGraphSection2.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

# 这两行设置使得图中可以显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

numOfData = 0  # 数据量，共330个
for key in data.keys():
    numOfData += len(data[key])
titleAndColor = {'str': ['字符串', 'green'], 'line': ['线性表', 'blue'], 'arr': ['数组', 'purple'],
                 'find': ['查找算法', 'red'], 'num': ['数字操作', 'black'], 'sort': ['排序算法', 'yellow'],
                 'tree': ['树', 'pink'], 'gra': ['图', 'orange']}
path = 'E:/大二下/数据科学基础/大作业/dataScience/Section 2/graph/ndGraph'
isNeedToSave = (len(os.listdir(path)) == 0)

print("画图进度：")
numToPaintOfEachType = 3  # 每种题型要画的图的个数
count = 1  # 计已画的图的个数
for caseType in data.keys():
    values = data[caseType]
    for i in range(numToPaintOfEachType):
        item = values[i]
        avg = np.mean(item)
        var = np.var(item)
        #  自变量
        x = np.arange(-4, 4, 0.05)  # 参数：起点，终点，步长
        #  因变量
        y = gd(x, avg, var)
        #  绘图
        plt.plot(x, y, color=titleAndColor[caseType][1])
        #  设置坐标系
        plt.xlim(-3.0, 3.0)
        plt.ylim(-0.2, math.ceil(gd(avg, avg, var)))

        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))

        signal = '$\mu=' + str(round(avg, 2)) + ', \sigma^2=' + str(round(var, 2)) + '$'
        title = titleAndColor[caseType][0] + str(i)
        plt.title(title, fontsize=15)
        plt.legend(labels=[signal])

        if isNeedToSave:  # 如果该文件夹为空，保存（防止再运行时重复保存）
            plt.savefig(path + '/' + title + '.png')  # 保存图片

        plt.show()

        print(str(round(count / (numToPaintOfEachType * 8), 4) * 100) + '%')  # 打印进度
        count += 1
