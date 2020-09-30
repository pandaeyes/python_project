import sys
import os
import io
import subprocess

class CommonCmd():
    def __init__(self, encoding = "gbk", showlog = True):
        self.encoding = encoding
        self.showlog = showlog

    def CallCmd(self, cmd):
        r = os.system(cmd)
        if r == 0:
            return True 
        else:
            raise RuntimeError('CallCmd Failed:' + cmd)

    def CallCmdPopen(self, cmd):
        popen = subprocess.Popen(cmd,
                         shell=True,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE,
                         bufsize=1)
        retList = []
        while popen.poll() is None:
            msg = popen.stdout.readline().decode(self.encoding)
            msg = msg.strip()
            if msg == "":
                continue
            if self.showlog:
                self.Log(msg)
            retList.append(msg)
        return retList
    
    def Log(self, msg):
        if msg != "":
            os.system("echo " + msg)

    def LogPrint(self, msg):
        if msg != "":
            print(msg)
