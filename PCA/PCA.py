#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 先跑calculate，再跑produce，最后此文件
# 此文件进行降维计算

import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA


def draw_points(dataset1, dataset2):  # 画图，dataset1是没降维的数据，dataset2是数据映射到新空间的数据
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.scatter(dataset1[:, 0], dataset1[:, 1], marker='s', s=40, color='red')
    dataset2 = np.array(dataset2)
    ax2.scatter(dataset2[:, 0], dataset2[:, 1], s=40, color='blue')
    plt.show()  # 红点为降维前，蓝点为降维后


f = open('data/furtherDataForPCA.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

dataChart = np.array([[score for score in data[userId].values()] for userId in data.keys()])
# print(dataChart)

pca = PCA(0.8)  # 保留原数据的百分之多少
pca.fit(dataChart)  # 训练
print("将数据降到了" + str(pca.n_components_) + "维")
dataAfterPCA = pca.fit_transform(dataChart)  # 降维后的数据
print(list(pca.explained_variance_ratio_))  # 输出贡献率
# 输出降维后的数据
print("输出降维后的数据：")
for x in list(dataAfterPCA):
    print(list(x))

# 绘图
draw_points(dataChart, dataAfterPCA)
