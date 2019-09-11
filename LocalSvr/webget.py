# webget
import urllib.request
import re
import os
import sys

class Webget():

    def __init__(self, url, root):
        self.url = url
        self.pattern = re.compile(r'<a href="(.*)">', re.I)
        self.root = root
        self.ignore = [
                "tools/gen_battle/ebin"
                ,"tools/gen_data/ebin"
                ,"tools/gen_data/out"
                ,"tools/gen_map/ebin"
        ]

    def ParseUrl(self, urlPath):
        fileList = []
        dirList = []
        resu = urllib.request.urlopen(urlPath, data=None, timeout=10)
        data = resu.read().decode("utf-8")
        lines = data.split("\n")
        for line in lines:
            if (len(line.split("href")) == 2):
                m = self.pattern.search(line.strip())
                if m:
                    fileName = m.group(1)
                    if (fileName.endswith("/")) and (".." not in fileName):
                        dirList.append(fileName[:-1])
                    else:
                        if ".." not in fileName and "env_cfg" not in fileName and "erl_crash.dump" not in fileName:
                            fileList.append(fileName)
        return fileList, dirList

    def DownloadCur(self):
        fileList, dirList = self.ParseUrl(self.url)
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        if (len(fileList) > 0):
            self.Download(self.url, fileList, self.root)

    def DownloadAll(self):
        self.DoDownloadAll(self.url, self.root)

    def DoDownloadAll(self, url, root):
        fileList, dirList = self.ParseUrl(url)
        if not os.path.exists(root):
            os.makedirs(root)
        if (len(fileList) > 0):
            self.Download(url, fileList, root)
        for dirName in dirList:
            self.DoDownloadAll(url + "/" + dirName, root + "/" + dirName)


    def Download(self, url, fileList, root):
        if root in self.ignore:
            return
        for name in fileList:
            path = url + "/" + name
            try:
                resu = urllib.request.urlopen(path, data=None)
                data = resu.read()
                with open(root + "/" + name, "wb") as fileObj:
                    fileObj.write(data)
                    fileObj.close()
                resu.close()
            except:
                # print("Download Faile:", path)
                exType,exValue,exTrace = sys.exc_info()
                print("[ERROR]:", exType, exValue, path)

    def DownloadSingle(self, name):
        path = self.url
        try:
            resu = urllib.request.urlopen(path, data=None)
            data = resu.read()
            with open(self.root + "/" + name, "wb") as fileObj:
                fileObj.write(data)
                fileObj.close()
            resu.close()
        except:
            # print("Download Faile:", path)
            exType,exValue,exTrace = sys.exc_info()
            print("[ERROR]:", exType, exValue, path)


if __name__ == "__main__":
    # web = Webget("http://192.168.1.20/sygame/fsjx/testebin")
    # web = Webget("http://127.0.0.1/test/cb_fun.erl", "test")
    web = Webget("http://192.168.1.121/fsjx_tools/gen_data", "test")
    # web = Webget("http://192.168.1.121/fsjx_inc", "test")
    web.DownloadCur()
    print("Done!")
