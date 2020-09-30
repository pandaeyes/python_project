#!/usr/bin/python
# coding=utf-8
import os
import requests
import json
import io
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class HtmlGenerator():
    def __init__(self, root, timestr, fileList):
        self.root = root
        self.timestr = timestr
        self.fileList = fileList
        self.urlroot = "http://log-collect-ysc.shiyuegame.com"

    def WriteHead(self, fw):
        fw.write(u"<html>\n")
        fw.write(u"<head>\n")
        fw.write(u"<title>Ysc后台错误日志报告" + self.timestr + "</title>\n")
        fw.write(u"<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n")
        fw.write(u"</head>\n")
        fw.write(u"<style type=\"text/css\">\n")
        fw.write(u"table{border-collapse:collapse;border-spacing:0;border-left:1px solid #888;border-top:1px solid #888;background:#FFFFFF;}\n")
        fw.write(u"th,td{border-right:1px solid #888;border-bottom:1px solid #888;padding:5px 10px; font-size:13px;}\n")
        fw.write(u"th{font-weight:bold;background:#ccc;}\n")
        fw.write(u".container{width:98%; overflow: auto;}\n")
        fw.write(u".logspan{width:230px;float: left;}\n")
        fw.write(u"</style>\n")
        fw.write(u"<body>\n")
        fw.write(u"<div><font style=\"font-size:18px; font-weight:bold;\">后台错误日志报告" + self.timestr + "</font></div>\n")
        fw.write(u"<br/>\n")
        fw.write(u"<div style=\"width:98%;background:#FAEBD7;font-size:14px;font-weight:bold;\">日志来源</div>\n")

    def GenHref(self, efile):
        return "<a href=\"" + self.urlroot + "/log/" + self.timestr + "/" + efile + "\" target=\"_blank\">" + efile + "</a>"

    def WriteErrorList(self, fw):
        fw.write(u"<div class= \"container\">\n")
	flist = sorted(self.fileList)
        if len(flist) > 0:
            for filename in flist:
                fw.write(u"<span class=\"logspan\">" + self.GenHref(filename) + "</span>\n")
        fw.write(u"</div>\n")

    def WriteTable(self, fw, errorInfo):
        fw.write(u"<br/>\n")
        fw.write(u"<table width=\"98%\">\n")
        fw.write(u"<tr bgcolor=\"#F0F8FF\" >\n")
        fw.write(u"<td width=\"8px\" style=\"font-size:15px; font-weight:bold;\"></td>\n")
        fw.write(u"<td width=\"40%\" style=\"font-size:15px; font-weight:bold;\">错误信息</td>\n")
        fw.write(u"<td width=\"5%\" style=\"font-size:15px; font-weight:bold;\">数量</td>\n")
        fw.write(u"<td width=\"55%\" style=\"font-size:15px; font-weight:bold;\">来源</td>\n")
        fw.write(u"</tr>\n")

        d_order= sorted(errorInfo.items(), key = lambda x:x[1]["count"], reverse = True)
	index = 1
        for detail in d_order:
            einfo = detail[1] 
            fw.write(u"<tr>\n")
            fw.write(u"<td>" + str(index) + "</td>\n")
            fw.write(u"<td>" + einfo["key"] + "</td>\n")
            fw.write(u"<td>" + str(einfo["count"]) + "</td>\n")
            fw.write(u"<td>\n")
            for efile in einfo["ref"]:
                fw.write(self.GenHref(efile) + u"&nbsp;\n")
            fw.write(u"</td>\n")
            fw.write(u"</tr>\n")
            index = index + 1
        fw.write(u"</table>\n")
        fw.write(u"</body>\n")
        fw.write(u"</html>\n")

class ScanLog():

    def __init__(self):
        self.root = "/data/ysc_log/log"
        self.timestr = time.strftime("%Y%m%d", time.localtime())
        self.fileList = []
        self.errorInfo = {}
        self.htmlPath = "html/error_report_" + self.timestr + ".html"

    def ScanFile(self):
        files = os.listdir(self.root + "/" + self.timestr)
        for filename in files:
            logpath = os.path.join(self.root + "/" + self.timestr, filename)
            if os.path.isfile(logpath):
                self.fileList.append(filename)

        if len(self.fileList) > 0:
            for filename in self.fileList:
                self.ReadLogFile(filename)

    def ReadLogFile(self, filename):
        filePath = self.root + "/" + self.timestr + "/" + filename
        # fp = open(filePath + ".bak", 'w', encoding='utf-8')
        with io.open(filePath, 'r', encoding='utf-8') as logObj:
            for line in logObj:
                self.ParseLine(line, filename)

    def ParseLine(self, line, filename):
        index = line.find("@")
        key = line[index:140].strip()
        if key in self.errorInfo:
            detail = self.errorInfo[key]
            ref = detail["ref"]
            if filename not in ref:
                ref.append(filename)
            detail["count"] = detail["count"]+ 1
            detail["ref"] = ref
        else:
            self.errorInfo[key] = {"key" : key, "count": 1, "ref" : [filename]}

    def GenHtml(self):
        genHtml = HtmlGenerator(self.root, self.timestr, self.fileList)
        with io.open("/data/ysc_log/" + self.htmlPath, 'w+', encoding='utf-8') as fwriter:
            genHtml.WriteHead(fwriter)
            genHtml.WriteErrorList(fwriter)
            genHtml.WriteTable(fwriter, self.errorInfo)

    def SendRtxMsg(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a90ebab6-d1b8-42e1-bbdc-91041fe23aeb'
        mainurl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7e4ef424-b0d0-418a-b122-339a8212c943'
        msg = "这是昨天今天线上的服务端错误日志报告, 大家都看一下，有问题记得及时修复!客户端同学请查看Bugly信息。"
	h = datetime.datetime.now().hour
	if h > 12:
	    msg = "晚间报告:服务端错误日志报告, 大家都看一下，有问题及时修复!客户端同学请查看Bugly信息。"
        # url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8736027e-4fb9-4feb-9aae-3c010cd7bad9'
        # mainurl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8736027e-4fb9-4feb-9aae-3c010cd7bad9'
        errorUrl = "http://log-collect-ysc.shiyuegame.com/" + self.htmlPath
        body = {"msgtype": "text", "text": {"content" : msg + "\n" + errorUrl, "mentioned_list":["@all"]}}
        headers = {'content-type': "application/json"}
        data = json.dumps(body)
        response = requests.post(url, data = data, headers = headers)
        response = requests.post(mainurl, data = data, headers = headers)

if __name__ == '__main__':
    scanLog = ScanLog()
    scanLog.ScanFile()
    scanLog.GenHtml()
    scanLog.SendRtxMsg()

