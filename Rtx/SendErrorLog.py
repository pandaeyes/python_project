import requests
import json
import time
import os

def SendMsg(msg):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8736027e-4fb9-4feb-9aae-3c010cd7bad9'
    errorUrl = "http://work.weixin.qq.com/api/doc"
    content = "**" + msg + "** \n" + "[点击这里查看错误日志](" + errorUrl + ")"
    body = {"msgtype": "markdown", "markdown": {"content" : content}}
    headers = {'content-type': "application/json"}
    data = json.dumps(body)
    response = requests.post(url, data = data, headers = headers)


if __name__ == "__main__":
    errorPath = "/data/ysc.dev/zone/ysc_dev_1/lager_log/error.log.0"
    toPath = "/data/ysc.dev/"
    fileName = "error.log." + time.strftime('%Y%m%d%H%M%S', time.localtime()) + ".txt"
    print(fileName)
    os.system("cp " + errorPath + " " + toPath + fileName)
    if os.path.exists(errorPath):
        pass
    else:
        pass
    # SendMsg("测试信息")

