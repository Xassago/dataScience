import json

f = open('data/score.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

INVALID = '*'
dataForPCA = {}
for userId in data.keys():
    grades = data[userId]
    for caseType in grades.keys():
        scoreInThisType = grades[caseType]
        if len(scoreInThisType) > 0:
            grades[caseType] = sum(scoreInThisType) / len(scoreInThisType)
        else:
            grades[caseType] = INVALID
    dataForPCA[userId] = grades

# 生成初始数据（未去除八类数据不全的学生）
with open('data/dataForPCA.json', 'w', encoding='utf-8') as w:
    json.dump(dataForPCA, w, ensure_ascii=False, indent=4)

# 筛选八类题目均有数据的学生
furtherData = {}
studentNum = 0
count = 0  # 统计八类题目均有数据的学生人数
for userId in dataForPCA.keys():
    studentNum += 1
    grades = dataForPCA[userId]
    judge = True
    for score in grades.values():
        if score == INVALID:
            judge = False
            break
    if judge:
        furtherData[userId] = grades
        count += 1
print("八类题目均有数据的学生人数为：" + str(count))
print("占比：" + str(count) + " / " + str(studentNum) + " = " + str((count / studentNum) * 100) + "%")

with open('data/furtherDataForPCA.json', 'w', encoding='utf-8') as w:
    json.dump(furtherData, w, ensure_ascii=False, indent=4)
