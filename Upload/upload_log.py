import requests
import os 
import re
import urllib.request


def fun_upfile(filepath, ctype, name):
    upload_url = 'http://log-collect-ysc.shiyuegame.com/upload_file.php'
    files = {"myfile":(name, open(filepath, "rb"), ctype,  {})}
    response = requests.request("POST", upload_url, data={"name":"" + name}, files=files)
    return response.text

# web下载处理
def fun_web_download(url, savepath):
    f = urllib.request.urlopen(url) 
    with open(savepath, "wb") as code:
        code.write(f.read())
        print("download savepath:", savepath)

def get_file_content(filepath):
    filestr=""
    if os.path.isfile(filepath):
        f = open(filepath, "r", encoding='utf-8')
        filestr = f.read()
        f.close()
    return filestr

def fun_web_req(url):
    response = urllib.request.urlopen(url, data=None, timeout=10) 
    ret = response.read()
    return ret

if __name__ == "__main__":
    # print(get_file_content("D:/data/fsjx.dev/server/src/mod/agenda/agenda.erl"))
    txt = fun_upfile( "D:/data/fsjx.dev/server_/src/mod/agenda/agenda.erl" ,"text/plain" ,"agenda_pphp.erl")
    print(txt)



