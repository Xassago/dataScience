#!/usr/bin/env python
# -*- coding:utf-8 -*-

#   本文件用于改变    /data/demo.json
#   给出一个用户id，可以将数据写入json文件中

import json

# 先跑此文件，再跑recommend
# 此文件获取推荐代码所需的条件（用户的userId和题目的type），更新userCase.json

data = json.load(open('../Section 1/data/test_data.json', 'r', encoding='utf-8'))
INVALID = "*"
UNDEFINED = "undefined"
userData = INVALID
type = INVALID
typeList = {"0": "字符串", "1": "线性表", "2": "数组", "3": "数字操作", "4": "查找算法", "5": "排序算法", "6": "树结构", "7": "图结构"}
auto = True
done = False

# 选择自动还是手动添加userId和type
instruc = input("input userId automatically?[yes/no] ")
if instruc == "yes":
    pass
elif instruc == "no":
    auto = False
else:
    print("then we assume that you have answered yes")

# 为userId和type赋值
if auto:
    # 待改进
    userId = "3544"
    type = UNDEFINED

    userData = data.get(userId, INVALID)
    userData["type"] = type
    done = True
else:
    while True:
        userId = input("input userId here: ")
        if userId == "exit":
            break
        userData = data.get(userId, INVALID)
        if userData == INVALID:
            print("userId not found, please input userId here again: ", end="")
        else:
            break

    if userData != INVALID:
        while True:
            print(typeList)
            print("choose types by keys listed here(", end="")
            print(",".join(typeList.keys()), end=") ")
            key = input()
            if key == "exit":
                break
            if key == UNDEFINED:
                type = key
                break
            type = typeList.get(key, INVALID)
            if type == INVALID:
                print("type not found, please input again:", end="")
            else:
                break
        if type != INVALID:
            userData["type"] = type
            done = True

# 加载demo.json
if done:
    with open('data/userCase.json', 'w', encoding='utf-8') as w:
        json.dump(userData, w, ensure_ascii=False, indent=4)
    print("update demo.json succeeded")
else:
    print("update demo.json failed")
