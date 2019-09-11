#!/usr/bin/python

import sys
import os
import io

from config.webget import Webget
from config.cfgreader import CfgReader 

# 安装
def DoInstall():
    MakeEmptyDir()
    DoDownload()

def DoDownload():
    DoDownloadServer()
    DoDownloadTools()


def DoDownloadServer():
    Log("Download Server")
    DoDownloadCur("http://192.168.1.121/fsjx_cbin", "server/cbin")
    DoDownloadCur("http://192.168.1.121/fsjx_ebin", "server/ebin")
    DoDownloadCur("http://192.168.1.121/fsjx_inc", "server/include")
    DoDownloadCur("http://192.168.1.121/fsjx_sh", "server/sh")
    output = os.popen('cp server/sh/srv.sh server/ -f')
    DoDownloadCur("http://192.168.1.121/fsjx_tpl", "server/tpl")
    MakeDir()
    Log("Download Server Finish")

def DoDownloadTools():
    Log("Download Tools")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/bin", "tools/bin")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/ebin", "tools/ebin")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/gen_ai", "tools/gen_ai")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/gen_battle", "tools/gen_battle")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/gen_data", "tools/gen_data")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/gen_map", "tools/gen_map")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/include", "tools/include")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/jsx", "tools/jsx")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/py", "tools/py")
    DoDownloadAll("http://192.168.1.121/fsjx_tools/xbin", "tools/xbin")
    DoDownloadSingle("http://192.168.1.121/fsjx_tools/completion", "tools", "completion")
    DoDownloadSingle("http://192.168.1.121/fsjx_tools/dev.sh", "tools", "dev.sh")
    DoDownloadSingle("http://192.168.1.121/fsjx_tools/tools.sh", "tools", "tools.sh")
    os.system("rm dev.sh -rf && ln tools/dev.sh dev.sh -s")
    reader = CfgReader()
    reader.GenToolEnvCfg()
    MakeDir()
    Log("Download Tools Finish")

def Log(msg):
    os.system("echo " + msg)

def MakeEmptyDir():
    tmpPaths = [
        "data/lua"
        ,"data/map"
        ,"resources"
        ,"server/src/ai_data"
        ,"server/src/data"
        ,"server/src/data/battle_data"
        ,"server/src/apps/lager"
        ,"server/src/apps/lager/ebin"

        ,"zone"
        ,"zone/fsjx_mysvr_1/dets"
        ,"zone/fsjx_mysvr_1/log"
        ,"zone/fsjx_mysvr_1/log_file"
        ,"zone/fsjx_mysvr_1/var"
    ]
    for path in tmpPaths:
        if not os.path.exists(path):
            os.makedirs(path)
    os.system("cp config/zone_cfg/* zone/fsjx_mysvr_1 -rf")

def MakeDir():
    tmpPaths = [
        "data/lua"
        ,"data/map"
        ,"resources"
        ,"server/src/ai_data"
        ,"server/src/data"
        ,"server/src/data/battle_data"
        ,"server/src/apps/lager"
        ,"server/src/apps/lager/ebin"

        ,"zone"
        ,"zone/fsjx_mysvr_1/dets"
        ,"zone/fsjx_mysvr_1/log"
        ,"zone/fsjx_mysvr_1/log_file"
        ,"zone/fsjx_mysvr_1/var"
    ]
    for path in tmpPaths:
        if not os.path.exists(path):
            os.makedirs(path)

def DoDownloadAll(url, root):
    web = Webget(url, root)
    web.DownloadAll()
    Log("Download:" + url)

def DoDownloadCur(url, root):
    web = Webget(url, root)
    web.DownloadCur()
    Log("Download:" + url)

def DoDownloadSingle(url, root, fileName):
    web = Webget(url, root)
    web.DownloadSingle(fileName)
    Log("Download:" + url)

def DoStartSvr():
    os.system("sh dev.sh server_start mysvr 1")

def DoUpdateConfig():
    MakeEmptyDir()

def DoClearData():
    dataPaths = [
        "data/lua"
        ,"server/src/ai_data"
        ,"server/src/data"
    ]
    for path in dataPaths:
        DelFile(path)

def DelFile(dirPath):
    for p in os.listdir(dirPath):
        path_file = os.path.join(dirPath, p)
        if os.path.isfile(path_file):
            os.remove(path_file)

def DoGenConfig():
    reader = CfgReader()
    reader.GenAll()
    os.system("rm -rf dev.sh && ln tools/dev.sh dev.sh -s")

def DoGenData(data):
    os.system("sh dev.sh gen_data " + data)

def DoMakeData():
    os.system("sh dev.sh server_make_mod data")

def DoMakeBattleData():
    os.system("sh dev.sh server_make_mod battle_data")

def DoMakeAIData():
    os.system("sh dev.sh server_make_mod ai_data")

def DoTruncate(platform, count):
    if count == 0:
        os.system("sh dev.sh server_truncate " + platform + " 1")
    else:
        os.system("sh dev.sh server_truncate " + platform + " 1 " + str(count))
        delPaths = [
            "zone/fsjx_mysvr_1/dets"
            ,"zone/fsjx_mysvr_1/log"
            ,"zone/fsjx_mysvr_1/log_file"
            ,"zone/fsjx_mysvr_1/lager_log"
        ]
        for path in delPaths:
            DelFile(path)
        os.system("rm -rf zone/fsjx_mysvr_1/screenlog.*")

def DoGenMap():
    os.system("sh dev.sh gen_map")

def DoGenBattle():
    os.system("sh dev.sh gen_battle")

def DoGenAi():
    os.system("sh dev.sh copy_ai")

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding='utf-8')
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    else:
        cmd = "error"

    if cmd == "install":
        DoInstall()
    elif cmd == "download":
        DoDownload()
    elif cmd == "download_server":
        DoDownloadServer()
    elif cmd == "download_tools":
        DoDownloadTools()
    elif cmd == "update_config":
        print("[ERROR]该命令不再使用")
        # DoUpdateConfig()
    elif cmd == "start":
        DoStartSvr()
    elif cmd == "gen_data":
        dataName = sys.argv[2]
        DoGenData(dataName)
    elif cmd == "make_data":
        DoMakeData()
    elif cmd == "gen_map":
        DoGenMap()
    elif cmd == "gen_battle":
        DoGenBattle()
    elif cmd == "copy_ai":
        DoGenAi()
    elif cmd == "make_ai_data":
        DoMakeAIData()
    elif cmd == "make_battle_data":
        DoMakeBattleData()
    elif cmd == "clear_data":
        DoClearData()
    elif cmd == "truncate":
        platform = sys.argv[2]
        count = 0
        if len(sys.argv) == 4:
            count = sys.argv[3]
        DoTruncate(platform, count)
    elif cmd == "gen_config":
        DoGenConfig()
    elif cmd == "gen_dir":
        MakeDir()
    else:
        print("------请输入以下命令-----------")
        print("install          安装")
        print("download         下载server和tools")
        print("download_server  下载server")
        print("download_tools   下载tools")
        print("gen_config       生成配置文件[form config.json]")
        print("start            启动server")
        print("gen_map          生成地图配置")
        print("gen_data         生成数据")
        print("gen_battle       生成战斗配置")
        print("gen_dir          创建必要的空目录")
        print("copy_ai          复制ai数据到指定目录")
        print("make_data        编译服务端数据")
        print("make_ai_data     编译AI数据")
        print("make_battle_data 编译战斗数据")
        print("clear_data       清除数据")
        print("truncate         清档")
    Log("Cmd Finish!")














