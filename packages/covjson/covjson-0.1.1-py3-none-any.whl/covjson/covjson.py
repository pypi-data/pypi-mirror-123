import json
import time
import re
import sys
import os
# save data to json file
def store(fileName,data):
    with open(fileName, 'w') as fw:
        # 将字典转化为字符串
        # json_str = json.dumps(data)
        # fw.write(json_str)
        # 上面两句等同于下面这句
        json.dump(data,fw,indent=4)
# load json data from file
def load(fileName):
    with open(fileName,'r') as f:
        data = json.load(f)
        return data

def toSnake(s):
    snake = re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
    return snake

def convert(item):
    keyList = list(item.keys())
    for key in keyList:
        snake = toSnake(key)
        if snake!=key:
            item[snake] = item[key]
            del item[key]
    return

def process():
    if len(sys.argv) <=1:
        print("请输入需要转换的文件名!\n格式：covjson srcFile dstFile； srcFile为待转换文件，dstFile为转换后生成待文件；如果dstFile不指定，则覆盖srcFile")
        return
    fileName = sys.argv[1]
    outFile = fileName
    if len(sys.argv)>2:
        outFile = sys.argv[2]

    if not os.path.exists(fileName):
        print("文件%s不存在！\n"%fileName)
        return
    rawData = load(fileName)

    data = rawData["result"]

    for item in data:
        if "request_json" in item:
            if "body_param" in item["request_json"]:
                convert(item["request_json"]["body_param"])
            if "query_param" in item["request_json"]:
                convert(item["request_json"]["query_param"])
    store(outFile,rawData)
    print("转换成功😊")