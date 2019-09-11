import re
import os
import sys
import json

class CfgReader():

    def __init__(self):
        self.path = "config/config.json"
        self.cfgInitPath = "config/tpl/cfg.ini.tpl"
        self.envCfgPath = "config/tpl/env.cfg.tpl"
        self.envErlPath = "config/tpl/env_cfg.erl.tpl"
        self.toCfgInitPath = "cfg.ini"
        self.toEnvCfgPath = "zone/fsjx_mysvr_1/env.cfg"
        self.toEnvErlPath = "tools/gen_data/env_cfg.erl"
        self.userName = None
        self.root = None
        self.ParseJson()

    def ParseJson(self):
        with open(self.path, "r") as fileObj:
            jsonDict = json.load(fileObj)
            self.userName = jsonDict["user_name"]
            self.root = jsonDict["root"]

    def GenCfg(self, tplPath, targetPath, repList):
        with open(tplPath, "r", encoding='utf-8') as fileObj:
            content = fileObj.read()
            for item in repList:
                repStr = item[0]
                newStr = item[1]
                content = content.replace(repStr, newStr)
            with open(targetPath, "w", encoding='utf-8') as wObj:
                wObj.write(content)

    def GenAll(self):
        tupList = [("{env_root}", self.root), ("{user_name}", self.userName)]
        self.GenCfg(self.cfgInitPath, self.toCfgInitPath, tupList)
        cmd = "tr -d '\\r' <" + self.toCfgInitPath + "> _tmp.txt"
        os.system(cmd)
        cmd = "mv _tmp.txt cfg.ini"
        os.system(cmd)
        self.GenCfg(self.envCfgPath, self.toEnvCfgPath, tupList)
        self.GenCfg(self.envErlPath, self.toEnvErlPath, tupList)

    def GenToolEnvCfg(self):
        tupList = [("{env_root}", self.root), ("{user_name}", self.userName)]
        self.GenCfg(self.envErlPath, self.toEnvErlPath, tupList)
            
        


