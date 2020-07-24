#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import urllib.request, urllib.parse
import os
import math
import functools

# 先跑update，再跑此文件，最后NDT
# 此文件计算四个指标（指标用来计算掌握值），更新intermediate_case_data.json

# data_to_process = {"排序算法":{},"数字操作":{},"数组":{},"树结构":{},"图结构":{},"查找算法":{},"字符串":{},"线性表":{}}
data_to_process = {}

f = open('data/case_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)
pure_case_num = 0
for name in data.keys():
    pure_case_num += 1
    data_to_process[name] = {}
    cases = data[name]
    for case in cases:
        data_to_process[name][case["user_id"]] = {}
print("pure_case_num = " + str(pure_case_num))
print("data_to_process结构：", data_to_process)
print()

INVALID = "*"

# program_rate
# 理由：攻克题目速度越快越好
for caseid in data.keys():
    cases = data[caseid]
    for case in cases:
        records = case["upload_records"]
        if len(records) >= 4:
            time_span = records[-1]["upload_time"] - records[0]["upload_time"]
            to_cal = (max([i["score"] for i in records]) / 100) / (
                        time_span / 1000 / 60 / 60) if time_span != 0 else -1  # 只考虑大于0的数据，单位：h^(-1)
            data_to_process[caseid][case["user_id"]]["program_rate"] = math.log(to_cal + 1,
                                                                                math.e) if to_cal > 0 else INVALID
            if max([i["score"] for i in records]) == 0:
                data_to_process[caseid][case["user_id"]]["program_rate"] = 0
        else:
            data_to_process[caseid][case["user_id"]]["program_rate"] = INVALID

# debug_rate
# 理由：攻克用例速度越快越好
valid_interval = 1 * 60 * 60 * 1000
for caseid in data.keys():
    cases = data[caseid]
    for case in cases:
        records = case["upload_records"]
        if len(records) >= 3:
            debug_rate = 0
            last_pair = [records[0]["score"], records[0]["upload_time"]]
            up_times = 0
            for i in range(len(records) - 1):
                if records[i + 1]["score"] > last_pair[0]:
                    if (records[i + 1]["upload_time"] - last_pair[1]) < valid_interval:  # 只考虑在一定时间范围内增长的分数，否则不算做debug范畴
                        debug_rate += math.pow(((records[i + 1]["score"] - last_pair[0]) / 100) / (
                                    (records[i + 1]["upload_time"] - last_pair[1]) / 1000 / 60 / 60), 2)
                        up_times += 1
                    last_pair = [records[i + 1]["score"], records[i + 1]["upload_time"]]
                elif records[i + 1]["score"] == last_pair[0]:
                    last_pair[1] = records[i + 1]["upload_time"]
            to_cal = math.sqrt(debug_rate / up_times) if up_times > 0 else -1  # 只考虑大于0的数据，单位：h^(-1)
            data_to_process[caseid][case["user_id"]]["debug_rate"] = math.log(to_cal + 1,
                                                                              math.e) if to_cal > 0 else INVALID
            if max([i["score"] for i in records]) == 0:
                data_to_process[caseid][case["user_id"]]["debug_rate"] = 0
        else:
            data_to_process[caseid][case["user_id"]]["debug_rate"] = INVALID

# early_success_degree
# 理由：分数提高越早越好
for caseid in data.keys():
    cases = data[caseid]
    for case in cases:
        records = case["upload_records"]
        if len(records) >= 4:
            # 此为折线下面积所占比例的计算方法
            # early_success_degree = 0
            # last_success_degree = records[0]["score"]/100
            # up_span = 1
            # span = 0
            # for i in range(len(records)-1):
            #     if records[i+1]["score"]/100 >= last_success_degree:
            #         early_success_degree += (records[i+1]["score"]/100 + last_success_degree)/(2*up_span)
            #         last_success_degree = records[i+1]["score"]/100
            #         span += up_span
            #         up_span = 1
            #     else:
            #         up_span += 1
            # if records[-1]["score"]/100 < last_success_degree:
            #     early_success_degree += last_success_degree*up_span
            #     span += up_span
            # to_cal = early_success_degree/span if span else last_success_degree #只考虑大于0的数据，单位：1
            # data_to_process[caseid][case["user_id"]]["early_success_degree"] = math.log(to_cal+1,math.e) if to_cal>0 else INVALID

            # 此为折线值求平均的计算方法
            early_success_degree = records[0]["score"] / 100
            last_success_degree = records[0]["score"] / 100
            for i in range(len(records) - 1):
                last_success_degree = max(last_success_degree, records[i + 1]["score"] / 100)
                early_success_degree += last_success_degree
            to_cal = early_success_degree / len(records) if len(records) > 0 else -1  # 只考虑大于0的数据，单位：1
            data_to_process[caseid][case["user_id"]]["early_success_degree"] = math.log(to_cal + 1,
                                                                                        math.e) if to_cal > 0 else INVALID
            if max([i["score"] for i in records]) == 0:
                data_to_process[caseid][case["user_id"]]["early_success_degree"] = 0
        else:
            data_to_process[caseid][case["user_id"]]["early_success_degree"] = INVALID

# finish_degree
# 理由：题目完成度越高越好
show_once = True
for caseid in data.keys():
    cases = data[caseid]
    for case in cases:
        records = case["upload_records"]
        if len(records) >= 4:
            finish_degree = 0
            max_score = records[0]["score"]
            for i in range(len(records) - 1):
                max_score = max(max_score, records[i + 1]["score"])
                finish_degree += (max_score / 100) / (
                            (records[i + 1]["upload_time"] - records[0]["upload_time"]) / 1000 / 60 / 60)
            to_cal = finish_degree / (len(records) - 1) if len(records) > 1 else -1  # 单位：h^(-1)
            data_to_process[caseid][case["user_id"]]["finish_degree"] = math.log(to_cal + 1,
                                                                                 math.e) if to_cal > 0 else INVALID
            if max([i["score"] for i in records]) == 0:
                data_to_process[caseid][case["user_id"]]["finish_degree"] = 0

        else:
            data_to_process[caseid][case["user_id"]]["finish_degree"] = INVALID

ma = -float('inf')
mi = float('inf')
avg = 0
num = 0
for caseid in data_to_process.values():
    for case in caseid.values():
        if case["program_rate"] != INVALID:
            ma = max(ma, case["program_rate"])
            num += 1
            avg += case["program_rate"]
            mi = min(mi, case["program_rate"])
avg /= num
print("program_rate max for all caseids:", ma)
print("program_rate min for all caseids:", mi)
print("program_rate avg for all caseids:", avg)

ma = -float('inf')
mi = float('inf')
avg = 0
num = 0
for caseid in data_to_process.values():
    for case in caseid.values():
        if case["debug_rate"] != INVALID:
            ma = max(ma, case["debug_rate"])
            num += 1
            avg += case["debug_rate"]
            mi = min(mi, case["debug_rate"])
avg /= num
print("debug_rate max for all caseids:", ma)
print("debug_rate min for all caseids:", mi)
print("debug_rate avg for all caseids:", avg)

ma = -float('inf')
mi = float('inf')
avg = 0
num = 0
for caseid in data_to_process.values():
    for case in caseid.values():
        if case["early_success_degree"] != INVALID:
            ma = max(ma, case["early_success_degree"])
            num += 1
            avg += case["early_success_degree"]
            mi = min(mi, case["early_success_degree"])
avg /= num
print("early_success_degree max for all caseids:", ma)
print("early_success_degree min for all caseids:", mi)
print("early_success_degree avg for all caseids:", avg)

ma = -float('inf')
mi = float('inf')
avg = 0
num = 0
for caseid in data_to_process.values():
    for case in caseid.values():
        if case["finish_degree"] != INVALID:
            ma = max(ma, case["finish_degree"])
            num += 1
            avg += case["finish_degree"]
            mi = min(mi, case["finish_degree"])
avg /= num
print("finish_degree max for all caseids:", ma)
print("finish_degree min for all caseids:", mi)
print("finish_degree avg for all caseids:", avg)

# 打印各caseid的各指标的有效数量
valid_program_rate = ""
valid_debug_rate = ""
valid_early_success_degree = ""
valid_finish_degree = ""
for caseid in data_to_process.values():
    tmp_program_rate = 0
    tmp_debug_rate = 0
    tmp_early_success_degree = 0
    tmp_finish_degree = 0
    for case in caseid.values():
        if case["program_rate"] != INVALID:
            tmp_program_rate += 1
        if case["debug_rate"] != INVALID:
            tmp_debug_rate += 1
        if case["early_success_degree"] != INVALID:
            tmp_early_success_degree += 1
        if case["finish_degree"] != INVALID:
            tmp_finish_degree += 1
    valid_program_rate += (str(tmp_program_rate) + " ")
    valid_debug_rate += (str(tmp_debug_rate) + " ")
    valid_early_success_degree += (str(tmp_early_success_degree) + " ")
    valid_finish_degree += (str(tmp_finish_degree) + " ")
print("valid_program_rate_num for each caseid:", valid_program_rate)
print("valid_debug_rate_num for each caseid:", valid_debug_rate)
print("valid_early_success_degree_num for each caseid:", valid_early_success_degree)
print("valid_finish_degree_num for each caseid:", valid_finish_degree)
print()

print("caseid sample:")
show_num = 10
for caseid in data_to_process.keys():
    show_num -= 1
    print(caseid, ":", data_to_process[caseid])
    if not show_num:
        break
print()

print("user condition sample:")
show_num = 10
avg = 0
for caseid in data_to_process.keys():
    users = data_to_process[caseid]
    userNum = len(users)
    validUserNum = 0
    for userId in users.keys():
        userCondition = users[userId]
        valid = True
        for value in userCondition:
            if userCondition[value] == INVALID:
                valid = False
                break
        if valid:
            validUserNum += 1
    if show_num:
        show_num -= 1
        print(caseid, ":", end="")
        print("validUserNum/userNum =", validUserNum, "/", userNum, "=", validUserNum / userNum)
    avg += validUserNum / userNum
if len(data_to_process.keys()) > 0:
    print("avg_validUser_rate:", avg / len(data_to_process.keys()))
print()

intermediate_case_data = {"program_rate": {}, "debug_rate": {}, "early_success_degree": {}, "finish_degree": {}}
# intermediate_classified_data = {}
intermediate_user_data = {}

case_data_num = {"program_rate": 0, "debug_rate": 0, "early_success_degree": 0, "finish_degree": 0}
for caseid in data_to_process.keys():
    tmp_program_rate = []
    tmp_debug_rate = []
    tmp_early_success_degree = []
    tmp_finish_degree = []
    cases = data_to_process[caseid]
    for case in cases.values():
        if case["program_rate"] != INVALID:
            tmp_program_rate.append(case["program_rate"])
        if case["debug_rate"] != INVALID:
            tmp_debug_rate.append(case["debug_rate"])
        if case["early_success_degree"] != INVALID:
            tmp_early_success_degree.append(case["early_success_degree"])
        if case["finish_degree"] != INVALID:
            tmp_finish_degree.append(case["finish_degree"])
    filterCondition = 15
    if len(tmp_program_rate) >= filterCondition:
        intermediate_case_data["program_rate"][caseid] = tmp_program_rate
        case_data_num["program_rate"] += 1
    if len(tmp_debug_rate) >= filterCondition:
        intermediate_case_data["debug_rate"][caseid] = tmp_debug_rate
        case_data_num["debug_rate"] += 1
    if len(tmp_early_success_degree) >= filterCondition:
        intermediate_case_data["early_success_degree"][caseid] = tmp_early_success_degree
        case_data_num["early_success_degree"] += 1
    if len(tmp_finish_degree) >= filterCondition:
        intermediate_case_data["finish_degree"][caseid] = tmp_finish_degree
        case_data_num["finish_degree"] += 1
print("intermediate_case_data中各指标的case样本数：", case_data_num)
print()

# 对 intermediate_case_data 中数据排序
for attribute in intermediate_case_data.keys():
    for caseId in intermediate_case_data[attribute].keys():
        origin = intermediate_case_data[attribute][caseId]  # 读初始数据
        intermediate_case_data[attribute][caseId] = sorted(origin)  # 排序后重新写入

with open('data/intermediate_case_data.json', 'w', encoding='utf-8') as w:
    json.dump(intermediate_case_data, w, ensure_ascii=False, indent=4)

user_validCase_num = {}
score_data = {"program_rate": [], "debug_rate": [], "early_success_degree": [], "finish_degree": []}
for caseid in data_to_process.keys():
    users = data_to_process[caseid]
    for userId in users.keys():
        if user_validCase_num.get(userId, INVALID) == INVALID:
            user_validCase_num[userId] = 0
        userCondition = users[userId]
        valid = True
        for value in userCondition.keys():
            if userCondition[value] == INVALID:
                valid = False
                break
        if valid:
            if intermediate_user_data.get(userId, INVALID) == INVALID:
                intermediate_user_data[userId] = {}
            intermediate_user_data[userId][caseid] = users[userId]
            user_validCase_num[userId] += 1
        for value in userCondition.keys():
            if userCondition[value] != INVALID:
                score_data[value].append(userCondition[value])
print("拥有有效做题记录（任意一题目的所有指标均有效）的用户:", len([1 for i in user_validCase_num.keys() if i > 0]), "/",
      len(user_validCase_num.keys()), "=",
      len([1 for i in user_validCase_num.keys() if i > 0]) / len(user_validCase_num.keys()))
print("总题目数:", len(data_to_process.keys()))
print("intermediate_user_data中各用户的有效做题数：", user_validCase_num)
print("intermediate_user_data中各用户的有效做题比例：", end="{")
for userId in user_validCase_num.keys():
    print(str(userId) + ":", user_validCase_num[userId] / len(data_to_process.keys()), end=", ")
print("}")
# position_data = {"program_rate":[],"debug_rate":[],"early_success_degree":[],"finish_degree":[]}
position_data = {}
for value in score_data.keys():
    data = score_data[value]
    avg = sum(data) / len(data) if len(data) > 0 else INVALID
    var = math.sqrt(
        sum(map(lambda x: (x - avg) * (x - avg), data)) / (len(data) - 1))  # 因为取指标时需要满足严苛的筛选，比总数少很多，故认为取出的数据为样本
    position_data[value] = (avg, var)
print("各指标的均值与标准差，格式：(avg,var)，", position_data)
print()
