import os
import time
import io
import re

def get_all_file(fileDir):
    fileList = []
    files = os.listdir(fileDir)
    for filename in files:
        filepath = os.path.join(fileDir, filename)
        if os.path.isfile(filepath):
            fileList.append(filepath)
        else:
            if filename != ".git":
                dlist = get_all_file(fileDir + "/" + filename)
                fileList.extend(dlist)
    return fileList 

if __name__ == '__main__':
    pattern = re.compile(r'\{b,(\d+),', re.I)
    listFile = get_all_file("D:/data/fsjx.dev/lua")
    dic = {}
    for path in listFile:
        with open(path, 'r', encoding='utf-8') as luaObj:
            for line in luaObj:
                m = pattern.search(line)
                if m:
                    channel = m.group(1)
                    dic[channel] = channel

    for ch in dic.keys():
        print(ch)

                
        
