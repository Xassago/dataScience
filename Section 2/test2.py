#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import math


def getPro(case):
    INVALID = "*"
    records = case["upload_records"]
    if len(records) >= 4:
        time_span = records[-1]["upload_time"] - records[0]["upload_time"]
        to_cal = (max([i["score"] for i in records]) / 100) / (time_span / 1000 / 60 / 60) if time_span != 0 else -1
        programRate = math.log(to_cal, math.e) if to_cal > 0 else INVALID
    else:
        programRate = INVALID
    return programRate


def getDebug(case):
    INVALID = "*"
    valid_interval = 1 * 60 * 60 * 1000
    records = case["upload_records"]
    if len(records) >= 3:
        debug_rate = 0
        last_pair = [records[0]["score"], records[0]["upload_time"]]
        up_times = 0
        for i in range(len(records) - 1):
            if records[i + 1]["score"] > last_pair[0]:
                if (records[i + 1]["upload_time"] - last_pair[1]) < valid_interval:
                    debug_rate += math.pow(((records[i + 1]["score"] - last_pair[0]) / 100) / (
                            (records[i + 1]["upload_time"] - last_pair[1]) / 1000 / 60 / 60), 2)
                    up_times += 1
                last_pair = [records[i + 1]["score"], records[i + 1]["upload_time"]]
            elif records[i + 1]["score"] == last_pair[0]:
                last_pair[1] = records[i + 1]["upload_time"]
        debugRate = math.log(math.sqrt(debug_rate / up_times),
                             math.e) if up_times > 0 else INVALID
    else:
        debugRate = INVALID
    return debugRate


def getEarly(case):
    INVALID = "*"
    records = case["upload_records"]
    if len(records) >= 4:
        early_success_degree = records[0]["score"] / 100
        last_success_degree = records[0]["score"] / 100
        for i in range(len(records) - 1):
            last_success_degree = max(last_success_degree, records[i + 1]["score"] / 100)
            early_success_degree += last_success_degree
        to_cal = early_success_degree / len(records) if len(records) > 0 else -1
        early_success_degree = to_cal if to_cal > 0 else INVALID
    else:
        early_success_degree = INVALID
    return early_success_degree


def getFinish(case):
    INVALID = "*"
    records = case["upload_records"]
    if len(records) >= 4:
        finish_degree = 0
        max_score = records[0]["score"]
        for i in range(len(records) - 1):
            max_score = max(max_score, records[i + 1]["score"])
            finish_degree += (max_score / 100) / (
                        (records[i + 1]["upload_time"] - records[0]["upload_time"]) / 1000 / 60 / 60)
        to_cal = finish_degree / (len(records) - 1) if len(records) > 1 else -1
        finish_degree = math.log(to_cal, math.e) if to_cal > 0 else INVALID

    else:
        finish_degree = INVALID
    return finish_degree


def standardNormalDistribution(data, position_tuple):
    return (data - position_tuple[0]) / position_tuple[1]


data = json.load(open('../Section 1/data/test_data.json', 'r', encoding='utf-8'))
i = 0
INVALID = "*"

# 由以上函数计算的结果下的所有有效指标得出均值与方差，以tuple格式存储在position_data中
score_data = {"program_rate": [], "debug_rate": [], "early_success_degree": [], "finish_degree": []}
for userId in data.keys():
    cases = data[userId]['cases']
    for case in cases:
        tmp_score = {"program_rate": getPro(case), "debug_rate": getDebug(case), "early_success_degree": getEarly(case),
                     "finish_degree": getFinish(case)}
        for value in tmp_score.keys():
            if tmp_score[value] != INVALID:
                score_data[value].append(tmp_score[value])
position_data = {}
for value in score_data.keys():
    tmp_list = score_data[value]
    avg = sum(tmp_list) / len(tmp_list) if len(tmp_list) > 0 else INVALID
    var = math.sqrt(
        sum(map(lambda x: (x - avg) * (x - avg), tmp_list)) / (len(tmp_list) - 1))  # 因为取指标时需要满足严苛的筛选，比总数少很多，故认为取出的数据为样本
    position_data[value] = (avg, var)
print("各指标的均值与方差，格式：(avg,var)，", position_data)
print()

# 为每个同学计算掌握值，无效的指标用平均值代替
# dataToWrite = []
dataToWrite = {}
for userId in data.keys():
    cases = data[userId]['cases']

    string_score = []
    line_score = []
    arr_score = []
    find_score = []
    num_score = []
    sort_score = []
    tree_score = []
    gra_score = []

    for case in cases:
        tmp_score = {"program_rate": getPro(case), "debug_rate": getDebug(case), "early_success_degree": getEarly(case),
                     "finish_degree": getFinish(case)}
        count = 0
        sum = 0

        for value in tmp_score.keys():
            if tmp_score[value] != INVALID:
                count += 1
                # sum += tmp_score[value]
                sum += standardNormalDistribution(tmp_score[value], position_data[value])

        if count > 0:
            # res = sum / count
            res = sum / len(tmp_score.keys())
            if case["case_type"] == "排序算法":
                sort_score.append(res)
            if case["case_type"] == "数字操作":
                num_score.append(res)
            if case["case_type"] == "数组":
                arr_score.append(res)
            if case["case_type"] == "树结构":
                tree_score.append(res)
            if case["case_type"] == "图结构":
                gra_score.append(res)
            if case["case_type"] == "查找算法":
                find_score.append(res)
            if case["case_type"] == "字符串":
                string_score.append(res)
            if case["case_type"] == "线性表":
                line_score.append(res)

    # direc = {"userId": userId, "str": string_score, "line": line_score, "arr": arr_score, "find": find_score,
    #          "num": num_score, "sort": sort_score, "tree": tree_score, "gra": gra_score}
    # dataToWrite.append(direc)
    direc = {"str": sorted(string_score), "line": sorted(line_score), "arr": sorted(arr_score),
             "find": sorted(find_score),
             "num": sorted(num_score), "sort": sorted(sort_score), "tree": sorted(tree_score), "gra": sorted(gra_score)}
    dataToWrite[userId] = direc

# with open("score.json", "w", encoding='utf-8') as f:
#     json.dump(dataToWrite, f, ensure_ascii=False, indent=4)
#     print("加载入文件完成...")

# 输出score.json文件中数据的统计情况
userCount = 0
for userId in dataToWrite.keys():
    userCount += 1
    print(userId,
          len(dataToWrite[userId]['str']),
          len(dataToWrite[userId]['line']),
          len(dataToWrite[userId]['arr']),
          len(dataToWrite[userId]['find']),
          len(dataToWrite[userId]['num']),
          len(dataToWrite[userId]['sort']),
          len(dataToWrite[userId]['tree']),
          len(dataToWrite[userId]['gra']), )
print("共计" + str(userCount) + "个学生")

# 对score.json进一步按照题型分类，每个题型下对应不同学生在该题型上的数据
classifyByType = {'str': [], 'line': [], 'arr': [], 'find': [], 'num': [], 'sort': [], 'tree': [], 'gra': []}
for userId in dataToWrite.keys():
    dataOfThisStudent = dataToWrite[userId]
    for caseType in dataOfThisStudent.keys():
        dataOfThisType = dataOfThisStudent[caseType]
        if len(dataOfThisType) > 0:
            classifyByType[caseType].append(dataOfThisType)
with open("data/furtherScore.json", "w", encoding='utf-8') as f:
    json.dump(classifyByType, f, ensure_ascii=False, indent=4)
