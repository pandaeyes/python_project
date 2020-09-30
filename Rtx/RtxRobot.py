# Rtx机器人基本操作
# @author huangqy

import requests
import json
import time
import os

class RtxRobot():

    def __init__(self, rtxUrl = ""):
        self.rtxUrl = rtxUrl

    def SetUrlKey(self, key):
        self.rtxUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + key

    def SetUrl(self, url):
        self.rtxUrl = url

    def SendMarkDown(self, content):
        body = {"msgtype": "markdown", "markdown": {"content" : content}}
        headers = {'content-type': "application/json"}
        data = json.dumps(body)
        response = requests.post(self.rtxUrl, data = data, headers = headers)

    # mentioned_list为@all, 或者是工号如sy0019
    def SendText(self, content, mentionedList = []):
        body = {"msgtype": "text", "text": {"content" : content, "mentioned_list":mentionedList}}
        headers = {'content-type': "application/json"}
        data = json.dumps(body)
        response = requests.post(self.rtxUrl, data = data, headers = headers)

