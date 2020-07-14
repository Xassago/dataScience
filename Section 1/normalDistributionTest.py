"""验证 intermediate_case_data.json 数据是否正态"""
import json
import math
import matplotlib.pyplot as plt

# from scipy import stats

f = open('data/intermediate_case_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

attributes = ['program_rate', 'debug_rate', 'early_success_degree', 'finish_degree']
ratio = []
for choose in attributes:  # 依次计算每个指标
    caseIds = [x for x in data[choose].keys()]
    print("给定样本:")
    for caseId in data[choose].keys():
        print(caseId, end=":")
        print(data[choose][caseId])
    count = []  # 各题有效数据个数
    canBeUsed = []  # 有效数据多于一定数目的可用题目
    num_all = 0
    for caseId in caseIds:
        if len(data[choose][caseId]) >= 0:  # 按有效数据个数筛选
            count.append(len(data[choose][caseId]))
            canBeUsed.append(caseId)
            num_all += 1
    print("各题有效数据个数:", count, "共：" + str(len(count)))
    print("有效数据多于一定数目的可用题目", canBeUsed, "共：" + str(len(canBeUsed)))

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
    print(refuse_bound)
    n = len(canBeUsed)
    var1 = math.sqrt((6 * (n - 2)) / ((n + 1) * (n + 3)))
    var2 = math.sqrt((24 * n * (n - 2) * (n - 3)) / (((n + 1) ** 2) * (n + 3) * (n + 5)))
    miu2 = 3 - (6 / (n + 1))
    u1u2_ofEachCase = {}  # 各题的U1, U2
    pianDu_fengDu_ofEachCase = {}  # 各题的偏度峰度观察值[g1, g2]
    for caseId in canBeUsed:
        case_data = data[choose][caseId]
        # 计算k阶原点矩
        ak = [sum([xi ** k for xi in case_data]) / len(case_data) for k in range(1, 5)]
        # 计算中心距B2,B3,B4
        B2 = ak[1] - ak[0] ** 2
        B3 = ak[2] - 3 * ak[1] * ak[0] + 2 * ak[0] ** 3
        B4 = ak[3] - 4 * ak[2] * ak[0] + 6 * ak[1] * ak[0] ** 2 - 3 * ak[0] ** 4
        if B2 != 0:
            # 偏度观察值
            g1 = B3 / math.sqrt(B2 ** 3)
            # 峰度观察值
            g2 = B4 / B2 ** 2
            pianDu_fengDu_ofEachCase[caseId] = [g1, g2]
            u1 = abs(g1 / var1)
            u2 = abs(g2 - miu2) / var2
            if u1 < refuse_bound and u2 < refuse_bound:
                u1u2_ofEachCase[caseId] = [u1, u2]
    print("各题偏度、峰度：")
    for key in pianDu_fengDu_ofEachCase.keys():  # 输出各题偏度峰度观察值
        print(key, pianDu_fengDu_ofEachCase[key])
    print("满足正态的各题u1, u2：")
    num_valid = 0
    for key in u1u2_ofEachCase.keys():  # 输出满足正态的各题的u1,u2
        print(key, u1u2_ofEachCase[key])
        num_valid += 1
    print("有效占比:", num_valid, "/", num_all, "=", str((num_valid / num_all) * 100) + "%")
    ratio.append((num_valid / num_all) * 100)

print()
print("各指标下数据服从正态分布的比例：")
for i in range(0, 4):
    print(attributes[i] + ": " + str(ratio[i]) + "%")