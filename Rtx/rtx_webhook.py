#!/usr/bin/python
# coding:utf-8

import os
import re
import io
import sys
reload(sys) 
sys.setdefaultencoding('utf8')
import subprocess
import requests
import json
import time

testurl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=-7f1c-4133-a23c-7a32b8e5a27a'
url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=-99d7-48f8-8f97-6405950593bc'
urlSkill = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=-55aa-41ba-886e-e85ab293abd8'
pattern = re.compile(r'.*\[ERROR\]\[(.*)\]\[(\w+):(\d+)\](.*)', re.I)
msgDict = {}
def SendMsg(msg):
    m = pattern.search(msg)
    if m:
        tm = m.group(1)
        mod = m.group(2)
        line = m.group(3)
        inf = m.group(4)
        indof = inf.find("[m")
        if indof < 3 and indof > 0:
            inf = inf[3:]

        now = int(time.time())
        if inf in msgDict:
            inftime = msgDict[inf]
            if (now - inftime) < 120:
                return
        msgDict[inf] = now
        content = "**ErrorReport**:\n >**Mod**:" + mod + "\n >**Line**:" + str(line) + "\n >**Time**:" + str(tm) + "\n \t" + inf
        body = {"msgtype": "markdown", "markdown": {"content" : content}}
        headers = {'content-type': "application/json"}
        data = json.dumps(body)
        if (inf.find("技能") > -1) or ("skill" in inf) or ("Skill" in inf):
            response = requests.post(urlSkill, data = data, headers = headers)
        response = requests.post(url, data = data, headers = headers)
    else:
        os.system("echo 不匹配:" + msg)

if __name__ == "__main__":
    current_encoding = "utf8"

    popen = subprocess.Popen(['tailf', 'zone/gamename_dev_1/screenlog.0'],
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE,
                         bufsize=1)

    while popen.poll() is None:
        msg = popen.stdout.readline().decode(current_encoding)
        msg = msg.strip()
        if (len(msg) > 0) and ("[ERROR]" in msg):
            if (len(msg) > 250):
                SendMsg(msg[:250])
            else:
                SendMsg(msg)

            
    if popen.poll() != 0:
        err = popen.stderr.read().decode(current_encoding)
        if (len(err) > 0):
            os.system("echo " + err.strip())
