import os
from RtxRobot import *


users_list = {
        "zyh_bug_master" : "sy0209"
        ,"hzf_master" : "sy0097"
        ,"zyh_master" : "sy0209"
        ,"xja_master" : "sy0729"
        ,"zln_master" : "sy0671"
        ,"cq_master" : "sy0238"
        ,"szh_master" : "sy803"
        ,"lsx_master" : "sy848"
        ,"fix_hzf_master" : "sy0097"
}

def SendText():
    robot = RtxRobot()
    robot.SetUrlKey("20f43540-32ad-4bb6-ad39-b95c16b41b7d")
    robot.SendText("测试数据", ["sy0019"])

def TestRtx():
    br = "xja_master"
    if br in users_list:
        print(users_list[br])


def send_msg(svnlog):
    # url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a060ccb9-d3c8-4c6b-bcc6-e096c35ee698'
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7249bf22-c2f5-4818-b2ea-9a46da7d2c53"
    content = "%s\n" % (svnlog)
    body = {"msgtype": "text", "text": {"content": content}}
    headers = {'content-type': "application/json"}
    data = json.dumps(body)
    response = requests.post(url, data = data, headers = headers)
    print(response)

if __name__ == '__main__':
    # SendText()
    # TestRtx()
    sstr = "我测试测试的"
    send_msg(sstr)

