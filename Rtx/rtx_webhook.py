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

testurl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=eb0c363d-7f1c-4133-a23c-7a32b8e5a27a'
url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8d92063f-99d7-48f8-8f97-6405950593bc'
urlSkill = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8c7b59a6-55aa-41ba-886e-e85ab293abd8'
urlz = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4edaa266-9c72-4deb-af73-72da5910d4ad"

pattern = re.compile(r'.*\[ERROR\]\[(.*)\]\[(\w+):(\d+)\](.*)', re.I)
msgDict = {}
def SendMsg(msg):
    # os.system("echo " + msg)
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
        try:
            inf = re.sub(r'file,\[([\d,\s\v\t]*)\]', Asc2Char, inf)
            inf = re.sub(r'<<([\d,\s\v\t]*)>>', Asc2Char2, inf)
        except:
            pass
        content = "**ErrorReport**:\n >**Time**:" + str(tm) + "\n**Mod**: <font color='#FF0000'>" + mod + " , " + str(line) + "</font>\n" + inf
        body = {"msgtype": "markdown", "markdown": {"content" : content}}
        headers = {'content-type': "application/json"}
        data = json.dumps(body)
        if (inf.find("技能") > -1) or ("skill" in inf) or ("Skill" in inf):
            response = requests.post(urlSkill, data = data, headers = headers)
        if (inf.find("非法物品数据") > -1) or (inf.find("不存在的道具") > -1) or (inf.find("创建单位时转换失败") > -1) or (inf.find("无法获取随机坐标") > -1):
            response = requests.post(urlz, data = data, headers = headers)
        response = requests.post(url, data = data, headers = headers)
    else:
        os.system("echo 不匹配:" + msg)
    
def Asc2Char(s):
    g = s.group(1)
    slist = g.split(",")
    if len(slist) < 2:
        return "file,[" + g + "]"
    out = "";
    for c in slist:
        ic = int(c.strip())
        if ic < 0 or ic > 256:
            return "file,[" + g + "]"
        out = out + unichr(ic)
    return "file,<font color='#FF0000'>[" + out + "]</font>"

def Asc2Char2(s):
    g = s.group(1)
    slist = g.split(",")
    if len(slist) < 2:
        return "<<" + g + ">>"
    out = "";
    for c in slist:
        ic = int(c.strip())
        if ic < 0 or ic > 256:
            return "<<" + g + ">>"
        out = out + chr(ic)
    return "<<" + out + ">>"


if __name__ == "__main__":
    current_encoding = "utf8"

    popen = subprocess.Popen(['tailf', 'zone/fssj2_dev_1/screenlog.0'],
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE,
                         bufsize=1)

    while popen.poll() is None:
        msg = popen.stdout.readline().decode(current_encoding)
        msg = msg.strip()
        if (len(msg) > 0) and ("[ERROR]" in msg):
            if (len(msg) > 420):
                SendMsg(msg[:420])
            else:
                SendMsg(msg)

            
    if popen.poll() != 0:
        err = popen.stderr.read().decode(current_encoding)
        if (len(err) > 0):
            os.system("echo " + err.strip())

