# 测试上传文件
import requests
import json
import datetime

if __name__ == "__main__":
    d1 = datetime.datetime.now()
    d2 = datetime.datetime(d1.year, d1.month, d1.day, 15, 0, 1)
    print(d1.year)
    print(d1.month)
    print(d1.day)
    print(d1)
    print(d2)
    print((d2 - d1).seconds)

