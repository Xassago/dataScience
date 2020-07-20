import json
import math

data=json.load(open('/data/demo.json','r',encoding='utf-8'))

#demo.json 数据格式
# {
#   ‘user’：
#       {
#           userId xxx
#           type：xxx (如没有则设为undefined，表示计算用户最弱的一个类别)
#           cases：
#               [
#                   {
#                       "case_id": "2908",
#                       "case_type": "字符串",
#                       "case_zip": "xxx",
#                       "final_score": 40,
#                       "upload_records": [(按原数据格式)]
#                   },
#                   {},...
#                ]
#        }
# }

def getPro(case):
    records = case["upload_records"]
    if len(records) >= 4:
        time_span = records[-1]["upload_time"] - records[0]["upload_time"]
        to_cal = (max([i["score"] for i in records]) / 100) / (time_span / 1000 / 60 / 60)
        programRate = math.log(to_cal, math.e) if to_cal > 0 else "*"
    else:
        programRate = "*"
    return programRate

def getDebug(case):
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
                                                                          math.e) if up_times > 0 else "*"
    else:
        debugRate = "*"
    return debugRate

def getEarly(case):
    records = case["upload_records"]
    if len(records) >= 4:
        early_success_degree = records[0]["score"] / 100
        last_success_degree = records[0]["score"] / 100
        for i in range(len(records) - 1):
            last_success_degree = max(last_success_degree, records[i + 1]["score"] / 100)
            early_success_degree += last_success_degree
        to_cal = early_success_degree / len(records)
        early_success_degree = to_cal if to_cal > 0 else "*"
    else:
        early_success_degree = "*"
    return early_success_degree

def getFinish(case):
    records = case["upload_records"]
    if len(records) >= 4:
        finish_degree = 0
        max_score = records[0]["score"]
        for i in range(len(records) - 1):
            max_score = max(max_score, records[i + 1]["score"])
            finish_degree += max_score / ((records[i + 1]["upload_time"] - records[0]["upload_time"]) / 1000 / 60 / 60)
        to_cal = finish_degree / (len(records) - 1) if len(records) > 1 else -1
        finish_degree = math.log(to_cal, math.e) if to_cal > 0 else "*"

    else:
        finish_degree = "*"
    return finish_degree

#把该用户最终在某类别下的得分返回

def getUserScore():
    score=0
    return score

#获得该用户在该type下的下一道题目Id

def getTest(score,type):
    testScore=[]
    testId=0
    return testId


cases=data["user"]["cases"]
type=data["user"]["type"]
score=0

#判断type并进行计算,在结束后type表示即将返回的题目的type,score为该type下的得分

if type=="undefined":
    score=0
    type=""
else:
    score=1
    type=type


testId=getTest(score,type)
print(testId)