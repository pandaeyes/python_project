# 通过字符表查看内存地址的堆栈信息
# @author huangyq
# @date 20200526

import sys
import os
import re
import io
import subprocess

# 命令路径设置，注意空格处理,最好不要带空格
cmdpath = "D:/android-ndk-r9d/toolchains/arm-linux-androideabi-4.8/prebuilt/windows-x86_64/bin/arm-linux-androideabi-addr2line.exe";
sopath = "C:/Program Files/Unity2017430/Editor/Data/PlaybackEngines/AndroidPlayer/Variations/mono/Release/Symbols/armeabi-v7a/libunity.sym.so";
# filepath = "C:/Users/panda/Desktop/res/error.txt"
pattern = re.compile(r' ([\w]{8}) ', re.I)

def FindIP(filepath):
    memaddr = []
    with open(filepath, "r") as obj:
        for line in obj:
            if "libunity.so" in line:
                m = pattern.search(line)
                if m:
                    addr = m.group(1)
                    memaddr.append(addr)
    for addr in memaddr:
        resList = CallCmdPopen(ToCmd(addr))
        if len(resList) > 0:
            print(resList[0])

def ToCmd(addr):
    return cmdpath + " -f -C -e \"" + sopath + "\" " + addr

def CallCmdPopen(cmd):
    popen = subprocess.Popen(cmd,
                     shell=True,
                     stdout = subprocess.PIPE,
                     stderr = subprocess.PIPE,
                     bufsize=1)
    retList = []
    while popen.poll() is None:
        msg = popen.stdout.readline().decode("gbk")
        msg = msg.strip()
        if msg == "":
            continue
        retList.append(msg)
    return retList

if __name__ == "__main__":
    if len(sys.argv) == 2:
        FindIP(sys.argv[1])
    else:
        print("[ERROR]please input your file")
