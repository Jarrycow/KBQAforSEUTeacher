import json
import pandas as pd


csvData = pd.read_csv('data/teachers.csv', header = 0, encoding='utf-8')  # 读取CSV文件
columns = csvData.columns.tolist()  # 读取CSV文件包含的列名并转换为list# 读取CSV文件包含的列名并转换为list
outPut = {}  # 创建空字典
for col in columns:  # 将CSV文件转为字典
	outPut[col] = str(csvData.loc[0, col])  # 这里一定要将数据类型转成字符串，否则会报错
jsonData = json.dumps(outPut) # 将字典转为json格式
with open('data/teachers.json', 'w') as jsonFile:  # 保存json文件
	jsonFile.write(jsonData)