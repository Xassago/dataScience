#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import math

# 先跑get，再跑此文件
# 此文件完成推荐代码功能

f = open('data/userCase.json', encoding='utf-8')
res = f.read()
data = json.loads(res)
INVALID = "*"
UNDEFINED = "undefined"
typeList = ["字符串", "线性表", "数组", "数字操作", "查找算法", "排序算法", "树结构", "图结构"]


# demo.json 数据格式
# {
#     "user_id"：xxx
#     "type"：xxx (如没有则设为undefined，表示计算用户最弱的一个类别)
#     "cases"：
#         [
#             {
#                 "case_id": "2908",
#                 "case_type": "字符串",
#                 "case_zip": "xxx",
#                 "final_score": 40,
#                 "upload_records": [(按原数据格式)]
#             },
#             {},...
#         ]
# }

def getPro(case):
    INVALID = "*"
    records = case["upload_records"]
    if len(records) >= 4:
        time_span = records[-1]["upload_time"] - records[0]["upload_time"]
        to_cal = (max([i["score"] for i in records]) / 100) / (time_span / 1000 / 60 / 60) if time_span != 0 else -1
        programRate = math.log(to_cal + 1, math.e) if to_cal > 0 else INVALID
        if max([i["score"] for i in records]) == 0:
            programRate = 0
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
        debugRate = math.log(math.sqrt(debug_rate / up_times) + 1,
                             math.e) if up_times > 0 else INVALID
        if max([i["score"] for i in records]) == 0:
            debugRate = 0
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
        early_success_degree = math.log(to_cal + 1, math.e) if to_cal > 0 else INVALID
        if max([i["score"] for i in records]) == 0:
            early_success_degree = 0
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
        finish_degree = math.log(to_cal + 1, math.e) if to_cal > 0 else INVALID
        if max([i["score"] for i in records]) == 0:
            finish_degree = 0

    else:
        finish_degree = INVALID
    return finish_degree


def getPositionData():
    INVALID = "*"

    # 由以上函数计算的结果下的所有有效指标得出均值与方差，以tuple格式存储在position_data中
    test_data = json.load(open('../Section 1/data/test_data.json', 'r', encoding='utf-8'))
    score_data = {"program_rate": [], "debug_rate": [], "early_success_degree": [], "finish_degree": []}
    for userId in test_data.keys():
        cases = test_data[userId]['cases']
        for case in cases:
            tmp_score = {"program_rate": getPro(case), "debug_rate": getDebug(case),
                         "early_success_degree": getEarly(case),
                         "finish_degree": getFinish(case)}
            for value in tmp_score.keys():
                if tmp_score[value] != INVALID:
                    score_data[value].append(tmp_score[value])
    for tmpList in score_data.values():
        if not tmpList:
            print("test_data not good enough, positionData failed to load")
            return ""
    position_data = {}
    for value in score_data.keys():
        tmp_list = score_data[value]
        avg = sum(tmp_list) / len(tmp_list)
        var = math.sqrt(
            sum(map(lambda x: (x - avg) * (x - avg), tmp_list)) / (
                    len(tmp_list) - 1))  # 因为取指标时需要满足严苛的筛选，比总数少很多，故认为取出的数据为样本
        position_data[value] = (avg, var)
    return position_data


def standardNormalDistribution(data, position_tuple):
    return (data - position_tuple[0]) / position_tuple[1]


# 计算某用户在某题目上得分
def getScore(case, positionData):
    tmp_score = {"program_rate": getPro(case), "debug_rate": getDebug(case),
                 "early_success_degree": getEarly(case),
                 "finish_degree": getFinish(case)}
    sum_ = 0
    for value in tmp_score.keys():
        if tmp_score[value] != INVALID:
            sum_ += standardNormalDistribution(tmp_score[value], positionData[value])
    return sum_ / len(tmp_score.keys())  # 若计算所得掌握值无效（各指标均无效），则视作其各指标均为平均数0，返回默认掌握值0


# 把该用户最终在某类别下的得分返回
def getUserScore(cases, type, positionData):
    scores = []
    for case in cases:
        if case["case_type"] == type:
            scores.append(getScore(case, positionData))
    return sum(scores) / len(scores) if scores else 0  # 返回该类别下题目得分的均值，若无做题记录则按照默认掌握值0返回


# 获得该用户在该type下的下一道题目Id
def getTest(cases, type, userScore, positionData):
    oldTests = []
    newTests = []
    caseIds = set([i["case_id"] for i in cases])
    classifiedData = json.load(open('../Section 1/data/classified_data.json', 'r', encoding='utf-8'))
    all_cases = classifiedData[type]
    testIdList = set(all_cases.keys()) - caseIds
    if testIdList:  # 对没做过的题目进行排序
        avgUserScores = {}  # 键值对为(testId:score)
        for testId in testIdList:
            userCases = all_cases[testId]
            scores = []
            tmpUserIds = []
            for case in userCases:
                if case["user_id"] not in tmpUserIds:  # 可能有重复
                    tmpUserIds.append(case["user_id"])
                    scores.append(getScore(case, positionData))
            avgUserScores[testId] = sum(scores) / len(scores) if scores else 0
        newTests = sorted(avgUserScores.keys(),
                          key=lambda x: abs(avgUserScores[x] - userScore))  # 未做过的题目按平均掌握值与用户掌握值的差值绝对值从小到大排序
        print("userScore（用户在该题型上的掌握值）:", userScore)
        print("testIds not tried",
              sorted(avgUserScores.items(), key=lambda x: abs(x[1] - userScore)))
    if caseIds:  # 对做过的题目进行排序
        casesClean = []
        tmpCaseIds = []
        for case in cases:
            if case["case_id"] not in tmpCaseIds:  # 可能有重复
                tmpCaseIds.append(case["case_id"])
                casesClean.append(case)
        oldTests = [i["case_id"] for i in
                    sorted(casesClean, key=lambda x: getScore(x, positionData))]  # 已做过的题目按掌握值从小到大排序
        print("testIds tried",
              sorted(map(lambda x: (x["case_id"], getScore(x, positionData)), casesClean), key=lambda x: x[1]))
    return (newTests, oldTests)


cases = data["cases"]
type = data["type"]
score = float('inf')
print("用户ID:", data["user_id"], ";指定推荐题目类型:", type, end="")

# 判断type并进行计算,在结束后type表示即将返回的题目的type,score为该type下的得分
position_data = getPositionData()
if type == UNDEFINED:
    for value in typeList:
        tmpScore = getUserScore(cases, type, position_data)
        if tmpScore < score:
            score = tmpScore
            type = value
else:
    score = getUserScore(cases, type, position_data)
print(";最终推荐题目类型:", type)
print()

# 获取可推荐题目的列表
tests_available = getTest(cases, type, score, position_data)
print()
print("[duplicate]" if len(tests_available[0]) != len(set(tests_available[0])) else "[not duplicate]", end="")
print("testIds not tried available in order:", tests_available[0])
print("[duplicate]" if len(tests_available[1]) != len(set(tests_available[1])) else "[not duplicate]", end="")
print("testIds tried available in order:", tests_available[1])
all_tests_available = tests_available[0] + tests_available[1]
print("next recommended testId:", all_tests_available[0] if all_tests_available else "none")
print()

# 罗列已经做过的题目(去重后)
print("all tests tried are listed below(duplicate one removed):")
test_data = json.load(open('../Section 1/data/test_data.json', 'r', encoding='utf-8'))
userCases = test_data[str(data["user_id"])]["cases"]
casesClean = []
tmpCaseIds = []
for case in userCases:
    if case["case_id"] not in tmpCaseIds:  # 可能有重复
        tmpCaseIds.append(case["case_id"])
        casesClean.append(case)
for case in casesClean:
    if case["case_id"] in tests_available[1]:
        print(case)

# 同一个cases中存在重复case_id的例子
# {'case_id': '2908', 'case_type': '字符串', 'case_zip': 'http://mooctest-site.oss-cn-shanghai.aliyuncs.com/target/单词分类_1581144899702.zip', 'final_score': 40, 'upload_records': [{'upload_id': 236494, 'upload_time': 1582023290656, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4238/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582023289869.zip', 'score': 40.0}, {'upload_id': 252563, 'upload_time': 1582557830339, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582557829552.zip', 'score': 0.0}, {'upload_id': 252565, 'upload_time': 1582557836610, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582557835991.zip', 'score': 0.0}, {'upload_id': 252576, 'upload_time': 1582558130645, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582558130012.zip', 'score': 0.0}, {'upload_id': 252577, 'upload_time': 1582558139684, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582558139071.zip', 'score': 0.0}, {'upload_id': 252578, 'upload_time': 1582558144348, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582558143538.zip', 'score': 0.0}]}
# {'case_id': '2908', 'case_type': '字符串', 'case_zip': 'http://mooctest-site.oss-cn-shanghai.aliyuncs.com/target/单词分类_1581144899702.zip', 'final_score': 0, 'upload_records': [{'upload_id': 236494, 'upload_time': 1582023290656, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4238/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582023289869.zip', 'score': 40.0}, {'upload_id': 252563, 'upload_time': 1582557830339, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582557829552.zip', 'score': 0.0}, {'upload_id': 252565, 'upload_time': 1582557836610, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582557835991.zip', 'score': 0.0}, {'upload_id': 252576, 'upload_time': 1582558130645, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582558130012.zip', 'score': 0.0}, {'upload_id': 252577, 'upload_time': 1582558139684, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582558139071.zip', 'score': 0.0}, {'upload_id': 252578, 'upload_time': 1582558144348, 'code_url': 'http://mooctest-dev.oss-cn-shanghai.aliyuncs.com/data/answers/4249/3544/%E5%8D%95%E8%AF%8D%E5%88%86%E7%B1%BB_1582558143538.zip', 'score': 0.0}]}
