# -*- coding:utf-8 -*-
import json
import pathlib
import sys
import os

def readJson(jsonPath):  # 读取json文件
    with open(jsonPath, 'r', encoding='utf-8') as f:
        jsonData = json.load(f)
        return jsonData


def writeJson(jsonList):  # 写入json文件
    with open('data/test.json', 'w') as f:
        jsonData = json.dumps(jsonList, ensure_ascii=False)
        f.write(jsonData)


