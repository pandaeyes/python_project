import os
import re
import io
import sys
import subprocess

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
    r = os.system(cmd)
    if r == 0:
        return True 
    else:
        raise RuntimeError('CallCmd Failed:' + cmd)
    

def CallBack(msg):
    os.system(msg)

def Log(msg):
    if msg != "":
        print(msg)

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

def MergeLocalBranchToMaster(brName):
    CoMaster()
    GitPull()
    CoBranch(brName)
    GitPull()
    CoMaster()
    cmd = "git merge " + brName
    if not CallCmd(cmd):
        raise RuntimeError('MergeLocalBranchToMaster Failed')

# mergeBrList = [
#     "master_third"
#     ,"develop"
# ]

if __name__ == '__main__':
    mergeBrListTmp = []
    mergeBrList = []
    with open("../mergebranch.txt") as fileObject:
        mergeBrListTmp = fileObject.readlines()
    for mbr in mergeBrListTmp:
        mergeBrList.append(mbr.strip())
    CoMaster()
    brList = GetLocalBranch()
    for br in mergeBrList:
        if br not in brList:
            CoNewBranch(br)
        MergeLocalBranchToMaster(br)



