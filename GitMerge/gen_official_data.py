# 自动生成外服表的差异文件
import os
import re
import io
import sys
import subprocess

def CallCmdPopen(cmd):
    current_encoding = "gbk"
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
        Log(msg)
        retList.append(msg)
    return retList

def CallCmd(cmd):
    print("CallCmd:" + cmd)
    r = os.system(cmd)
    if r == 0:
        return True 
    else:
        raise RuntimeError('CallCmd Failed:' + cmd)

def Log(msg):
    if msg != "":
        os.system("echo " + msg)


if __name__ == '__main__':
    fileList = CallCmdPopen("svn update")
    pattern = re.compile(r'config_official\\(\w+)\\(\w+).xml', re.I)
    files = ""
    for line in fileList:
        m = pattern.search(line.strip(), re.I)
        if m:
            if files == "":
                files = "[" + m.group(2)
            else：
                files =  files + "," + m.group(2)
    if files != "":
        files = files + "]"
        cmd = "./dev.sh gen_data " + files
        CallCmdPopen(cmd)
        Log("cmd:" + cmd)
    
