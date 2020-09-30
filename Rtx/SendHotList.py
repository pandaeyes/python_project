import os
from RtxRobot import *

def SendText():
    robot = RtxRobot()
    robot.SetUrlKey("7249bf22-c2f5-4818-b2ea-9a46da7d2c53")
    robot.SendText(GetHotTxt)

def GetHotTxt():
    content = ""
    with open("hot_res_list.txt", 'r', encoding='utf-8') as fileObj:
        content = fileObj.read()
    return content

if __name__ == '__main__':
    SendText()
