import os
import re
import io


pattern = re.compile(r'"clientip":"(.*?)"', re.I)
def FindIP():
    path = "C:/Users/panda/Desktop/kkk/ysc.entry.log/ysc.entry.log";
    ipMap = {}
    with open(path, "r") as obj:
        for line in obj:
            m = pattern.search(line)
            if m:
                ip = m.group(1)
                if ip in ipMap:
                    ipMap[ip] = ipMap[ip] + 1
                else:
                    ipMap[ip] = 1
    iplist = sorted(ipMap.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
    for value in iplist:
        print(value[0] + " => " + str(value[1]))

if __name__ == "__main__":
    FindIP()
