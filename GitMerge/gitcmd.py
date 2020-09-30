import os
import re
import io
import sys
import subprocess
import branch
import json
import requests

branchFileList = {}
users_list = {
    "zyh_bug_master" : "sy0209"
    ,"hzf_master" : "sy0097"
    ,"zyh_master" : "sy0209"
    ,"xja_master" : "sy0729"
    ,"zln_master" : "sy0671"
    ,"cq_master" : "sy0238"
    ,"szh_master" : "sy803"
    ,"lsx_master" : "sy848"
    ,"fix_hzf_master" : "sy0097"
}
def CallCmdPopen(cmd):
    current_encoding = "utf8"
    popen = subprocess.Popen(cmd,
                     shell=True,
                     stdout = subprocess.PIPE,
                     stderr = subprocess.PIPE,
                     bufsize=1)
    retList = []
    while popen.poll() is None:
        msg = popen.stdout.readline().decode(current_encoding)
        msg = msg.strip()
        if msg == "":
            continue
        retList.append(msg)
    return retList

def CallCmd(cmd):
    print("CallCmd:" + cmd)
    r = os.system(cmd)
    if r == 0:
        return True 
    else:
        raise RuntimeError('CallCmd Failed:' + cmd)
    

def CallBack(msg):
    os.system(msg)

def LogWhite(msg):
    if msg != "":
        print('\033[32m' + msg + '\033[0m')

def LogRed(msg):
    if msg != "":
        print('\033[31m' + msg + '\033[0m')

def LogList(logs):
    for log in logs:
        print(log)

def GetLocalBranch():
    cmd = "git br"
    ret = CallCmdPopen(cmd)
    branchList = []
    pattern = re.compile(r'(\w+)', re.I)
    for br in ret:
        m = pattern.search(br.strip())
        if m:
            branchList.append(m.group(1))
    return branchList

def CoMaster():
    cmd = "git co master"
    if not CallCmd(cmd):
        raise RuntimeError('CoMaster Failed')

def GitPull():
    cmd = "git pull"
    if not CallCmd(cmd):
        raise RuntimeError('GitPull Failed')

def CoBranch(brName):
    cmd = "git co " + brName
    if not CallCmd(cmd):
        raise RuntimeError('CoBranch Failed')

def CoNewBranch(brName):
    cmd = "git co --track -b " + brName + " origin/" + brName
    if not CallCmd(cmd):
        raise RuntimeError('CoNewBranch Failed:' + brName)

def MergeSubBranch(brName):
    cmd = "git merge " + brName
    ret = CallCmdPopen(cmd)
    fileList = []
    branchFileList[brName] = {"branch" : brName, "modify" : fileList}
    for line in ret:
        if "lua" in line:
            fileList.append(line)
        if "冲突" in line:
            raise RuntimeError('合并分支失败:' + brName)

def SendModifyResult():
    for rec in branchFileList.values():
        brName = rec["branch"]
        fileList = rec["modify"]
        LogRed(brName)
        for fname in fileList:
            LogWhite("    " + fname)

def SendMsg():
    if len(branchFileList) == 0:
        return
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
    content = "**合并分支信息，请确认:**\n"
    notifyList = []
    for rec in branchFileList.values():
        brName = rec["branch"]
        fileList = rec["modify"]
        LogRed(brName)
        userNum = GetUser(brName)
        if userNum:
            notifyList.append(userNum)
        content = content + ">**" + brName + "**\n"
        for fname in fileList:
            LogWhite("    " + fname)
            if "|" in fname:
                content = content + ">    " + fname[:fname.index("|")] + "\n"
            else:
                content = content + ">    " + fname + "\n"
    body = {"msgtype": "markdown", "markdown": {"content" : content}}
    headers = {'content-type': "application/json"}
    data = json.dumps(body)
    body = {"msgtype": "text", "text": {"content" : "请确认更新信息", "mentioned_list":notifyList}}
    data = json.dumps(body)
    response = requests.post(url, data = data, headers = headers)

def GetUser(brName):
    if brName in users_list:
        return users_list[brName]
    else:
        return None

def MergeLocalBranchToMaster(brName):
    CoMaster()
    GitPull()
    CoBranch(brName)
    GitPull()
    CoMaster()
    MergeSubBranch(brName)
    # cmd = "git merge " + brName
    # if not CallCmd(cmd):
    #     raise RuntimeError('MergeLocalBranchToMaster Failed')

if __name__ == '__main__':
    CoMaster()
    GitPull()
    brList = GetLocalBranch()
    for br in branch.mergeBrList:
        if br.strip() == "":
            continue
        if br not in brList:
            CoNewBranch(br)
        MergeLocalBranchToMaster(br)
    SendMsg()

