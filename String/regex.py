import os
import re
import io


if __name__ == "__main__":
    pattern = re.compile(r'\{b,(\d+),(.+),(.+),(\d+),(\w+),(\d+)\}', re.I)
    msg = "你好啊{b,99,hf11a,hf12a,7,liuconglocal,1}来啊啊{}"
    m = pattern.search(msg)
    if m:
        channel = m.group(1)
        selfName = m.group(2)
        targetname = m.group(3)
        print(channel)
        print(selfName)
        print(targetname)
    else:
        print("no match")


