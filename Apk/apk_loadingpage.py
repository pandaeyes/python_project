# 生成渠道包

import sys
import os
import io
import subprocess
from common_cmd import CommonCmd 
from shutil import copyfile

class GenChannelApk():
    def __init__(self, apkName, fileName):
        if "png" not in fileName and "jpg" not in fileName:
            raise RuntimeError("loadingpage file name is errror:must be png or jpg file")
        self.apktoolPath = "apktool/apktool-2.3.2.jar"
        self.keystorePath = "apktool/ysc.keystore"
        self.keyAlias = "ysc"
        self.keystoreKey = "sygame888"
        self.apkName = apkName
        self.fileName = fileName
        self.apkNameNoExt = apkName[:len(apkName) - 4]
        self.apkNameOutputName = self.apkNameNoExt + "_" + self.fileName + ".apk"
        self.cmd = CommonCmd()
        self.cmd.Log("apkName:" + apkName)
        self.cmd.Log("fileName:" + fileName)
    
    # 反编译
    def Decompile(self):
        self.MyLog("Decompile")
        if os.path.exists(self.apkNameOutputName):
            os.remove(self.apkNameOutputName)
            self.cmd.Log("remove:" + self.apkNameOutputName)
        cmd = "java -jar " + self.apktoolPath + " d -f " + self.apkName + " -o apk_unpack"
        self.cmd.CallCmdPopen(cmd)

    # 重编译
    def Recompile(self):
        self.MyLog("Recompile")
        cmd = "java -jar " + self.apktoolPath + " b -o " + self.apkNameOutputName + " apk_unpack"
        self.cmd.CallCmdPopen(cmd)

    def ChangeConfig(self):
        self.MyLog("ChangeConfig")
        path = "apk_unpack/res/values/strings.xml"
        newLine = []
        with io.open(path, "r+", encoding = "utf-8") as configObj:
            for line in configObj:
                if "sy_loadingpage_name" in line:
                    newLine.append("<string name=\"sy_loadingpage_name\">" + self.fileName + "</string>")
                else:
                    newLine.append(line.strip())
        if len(newLine) > 0:
            with io.open(path, 'w', encoding='utf-8') as fwriter:
                for line in newLine:
                    fwriter.write(line + "\n")
        else:
            raise RuntimeError("ChangeConfig Error:strings.xml is null")
        self.cmd.Log(path)

    def CopyLoadindPageFile(self, source, target):
        try:
            copyfile(source, target)
        except:
            raise RuntimeError("CopyLoadindPageFile Error")


    def Jarsigner(self):
        self.MyLog("Jarsigner")
        cmd = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore " + self.keystorePath + " -storepass " + self.keystoreKey + " -keypass " + self.keystoreKey + " " + self.apkNameOutputName + " " + self.keyAlias
        self.cmd.CallCmdPopen(cmd)

    def Clean(self, dirPath):
        self.MyLog("Clean")
        for root, dirs, files in os.walk(dirPath, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def MyLog(self, msg):
        if msg != "":
            self.cmd.Log("")
            self.cmd.Log("--------------- " + msg + " ---------------")
            self.cmd.Log("")



if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding='utf-8')
    if len(sys.argv) == 1:
        apkName = "local-202005121557-first-enc.apk"
        fileName = "ysc_loadingpage.png"
        # apkName = sys.argv[1]
        # fileName = sys.argv[2]
        gen = GenChannelApk(apkName, fileName)
        gen.Decompile()
        gen.ChangeConfig()
        gen.CopyLoadindPageFile(fileName, "apk_unpack/assets/" + fileName)
        gen.Recompile()
        gen.Jarsigner()
        gen.Clean("apk_unpack")
        print("NewApk:" + gen.apkNameOutputName)
        print("Finish")
    else:
        print("param error")
