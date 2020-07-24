#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 先跑calculate，再跑此文件
"""验证 masterValue.json 数据是否正态"""
import json
import math
import matplotlib.pyplot as plt
import numpy as np

f = open('data/masterValue.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

attributes = ['str', 'line', 'arr', 'find', 'num', 'sort', 'tree', 'gra']
ratio = []
dataForGraph = []  # 存放各指标下服从与不服从正态的数据个数
for choose in attributes:  # 依次计算每个指标
    dataOfEachUser = data[choose]
    # print(choose + "类型题目下的数据：")
    # print(dataOfEachUser)
    canBeUsed = []  # 筛选后可被使用的数据
    num_all = 0
    for item in dataOfEachUser:
        if len(item) > 5:  # 筛选
            canBeUsed.append(item)
            num_all += 1
    print(choose + "类型下共有" + str(num_all) + "个学生的数据")

    '''以下为偏度峰度检验部分'''
    # Zα常用值
    z_alpha = {
        0.001: 3.09,
        0.005: 2.576,
        0.01: 2.326,
        0.025: 1.96,
        0.05: 1.645,
        0.1: 1.282
    }
    alpha = 0.004  # 取α为0.004
    refuse_bound = z_alpha[alpha / 4]  # 拒绝域临界值为Zα/4
    # print(refuse_bound)
    n = len(canBeUsed)
    var1 = math.sqrt((6 * (n - 2)) / ((n + 1) * (n + 3)))
    var2 = math.sqrt((24 * n * (n - 2) * (n - 3)) / (((n + 1) ** 2) * (n + 3) * (n + 5)))
    miu2 = 3 - (6 / (n + 1))
    u1u2_ofEachCase = []  # 各题的U1, U2
    pianDu_fengDu_ofEachCase = []  # 各题的偏度峰度观察值[g1, g2]
    for item in canBeUsed:
        # case_data = data[choose][item]
        # 计算k阶原点矩
        ak = [sum([xi ** k for xi in item]) / len(item) for k in range(1, 5)]
        # 计算中心距B2,B3,B4
        B2 = ak[1] - ak[0] ** 2
        B3 = ak[2] - 3 * ak[1] * ak[0] + 2 * ak[0] ** 3
        B4 = ak[3] - 4 * ak[2] * ak[0] + 6 * ak[1] * ak[0] ** 2 - 3 * ak[0] ** 4
        if B2 != 0:
            # 偏度观察值
            g1 = B3 / math.sqrt(B2 ** 3)
            # 峰度观察值
            g2 = B4 / B2 ** 2
            pianDu_fengDu_ofEachCase.append([g1, g2])
            u1 = abs(g1 / var1)
            u2 = abs(g2 - miu2) / var2
            if u1 < refuse_bound and u2 < refuse_bound:
                u1u2_ofEachCase.append([u1, u2])
    # print("该题型数据中各user偏度、峰度：")
    # for i in pianDu_fengDu_ofEachCase:
    #     print(i)
    # print("该题型数据中满足正态的各user的u1, u2：")
    num_valid = 0
    for i in u1u2_ofEachCase:
        # print(i)
        num_valid += 1
    print("有效占比:", num_valid, "/", num_all, "=", str((num_valid / num_all) * 100) + "%")
    ratio.append((num_valid / num_all) * 100)
    dataForGraph.append([num_valid, num_all - num_valid])

print()
print("各题型下学生对所做题掌握值服从正态分布的比例：")
for i in range(0, 8):
    print(attributes[i] + ": " + str(ratio[i]) + "%")

print()
avgOfRatio = sum(ratio) / len(ratio)
print("八种题型下学生对所做题掌握值服从正态比例的均值：" + str(avgOfRatio) + "%")

# ----------绘制直方图----------
# 这两行设置使得图中可以显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

# labels = ['str', 'line', 'arr', 'find', 'num', 'sort', 'tree', 'gra']
labels = ['字符串', '线性表', '数组', '查找算法', '数字操作', '排序', '树', '图']

X = np.array([1, 2, 3, 4, 5, 6, 7, 8])
nd = np.array([i[0] for i in dataForGraph])
not_nd = np.array([i[1] for i in dataForGraph])

plt.bar(X, nd, width=0.4, bottom=not_nd, tick_label=labels, label='服从正态')
plt.bar(X, not_nd, width=0.4, label='不服从正态')
plt.title('学生在八种题型下的数据服从正态与不服从正态的数据情况')
plt.legend()
plt.show()
