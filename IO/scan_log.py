import os
import time


class HtmlGenerator():
    def __init__(self, root, timestr, fileList):
        self.root = root
        self.timestr = timestr
        self.fileList = fileList

    def WriteHead(self, fw):
        fw.write("<html>\n")
        fw.write("<head>\n")
        fw.write("<title>ServerError</title>\n")
        fw.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n")
        fw.write("</head>\n")
        fw.write("<style type=\"text/css\">\n")
        fw.write("table{border-collapse:collapse;border-spacing:0;border-left:1px solid #888;border-top:1px solid #888;background:#FFFFFF;}\n")
        fw.write("th,td{border-right:1px solid #888;border-bottom:1px solid #888;padding:5px 10px; font-size:13px;}\n")
        fw.write("th{font-weight:bold;background:#ccc;}\n")
        fw.write(".container{width:98%;}\n")
        fw.write(".logspan{width:230px;float: left;}\n")
        fw.write("</style>\n")
        fw.write("<body>\n")
        fw.write("<b><font style=\"font-size:15px;\">" + self.timestr + "错误日志信息</font></b>\n")
        fw.write("<br></br>\n")
        fw.write("<b  style=\"width:98%;background:#FAEBD7;font-size:14px;\">日志来源</b>\n")

    def GenHref(self, efile):
        return "<a href=\"" + efile + "\">" + efile + "</a>"

    def WriteErrorList(self, fw):
        fw.write("<div class= \"container\">\n")
        if len(self.fileList) > 0:
            for filename in self.fileList:
                fw.write("<span class=\"logspan\">" + self.GenHref(filename) + "</span>\n")
        fw.write("</div>\n")

    def WriteTable(self, fw, errorInfo):
        fw.write("<br/>\n")
        fw.write("<br/>\n")
        fw.write("<table width=\"98%\">\n")
        fw.write("<tr bgcolor=\"#F0F8FF\" >\n")
        fw.write("<td width=\"8px\" style=\"font-size:15px; font-weight:bold;\"></td>\n")
        fw.write("<td width=\"40%\" style=\"font-size:15px; font-weight:bold;\">错误信息</td>\n")
        fw.write("<td width=\"5%\" style=\"font-size:15px; font-weight:bold;\">数量</td>\n")
        fw.write("<td width=\"55%\" style=\"font-size:15px; font-weight:bold;\">来源</td>\n")
        fw.write("</tr>\n")

        d_order= sorted(errorInfo.items(), key = lambda x:x[1]["count"], reverse = True)
        index = 1
        for detail in d_order:
            einfo = detail[1] 
            fw.write("<tr>\n")
            fw.write("<td>" + str(index) + "</td>\n")
            fw.write("<td>" + einfo["key"] + "</td>\n")
            fw.write("<td>" + str(einfo["count"]) + "</td>\n")
            fw.write("<td>\n")
            for efile in einfo["ref"]:
                fw.write(self.GenHref(efile) + "&nbsp;\n")
            fw.write("</td>\n")
            fw.write("</tr>\n")
            index = index + 1
        fw.write("</table>\n")
        fw.write("</body>\n")
        fw.write("</html>\n")

class ScanLog():

    def __init__(self):
        self.root = "C:/Users/panda/Desktop/kkk/log"
        self.timestr = time.strftime("%Y%m%d", time.localtime())
        self.fileList = []
        self.errorInfo = {}

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
        with open(filePath, 'r', encoding='utf-8') as logObj:
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
        with open("log.html", 'w', encoding='utf-8') as fwriter:
            genHtml.WriteHead(fwriter)
            genHtml.WriteErrorList(fwriter)
            genHtml.WriteTable(fwriter, self.errorInfo)

    def PrintError(self):
        d_order= sorted(self.errorInfo.items(), key = lambda x:x[1]["count"], reverse = True)
        for detail in d_order:
            print(detail[1]["key"] + "   [" + str(detail[1]["count"]) + "]")

if __name__ == '__main__':
    scanLog = ScanLog()
    scanLog.ScanFile()
    scanLog.GenHtml()
