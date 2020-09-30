import os
import requests
import json
import time
import os

def send_msg(svnlog):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a060ccb9-d3c8-4c6b-bcc6-e096c35ee698'
    # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7249bf22-c2f5-4818-b2ea-9a46da7d2c53"
    content = "%s\n" % (svnlog)
    body = {"msgtype": "text", "text": {"content": content}}
    headers = {'content-type': "application/json"}
    data = json.dumps(body)
    response = requests.post(url, data = data, headers = headers)
    print(response)

if __name__ == '__main__':
    sstr = "收到我信息了吗"
    send_msg(sstr)

