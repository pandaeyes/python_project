import requests
import os 
import re
import urllib.request


def fun_upfile(filepath, ctype, mod):
    upload_url = 'http://127.0.0.1/fsjx/tools/upload_file.php'
    files = {"myfile":(mod, open(filepath, "rb"), ctype,  {})}
    response = requests.request("POST", upload_url, data={"mod":"" + mod}, files=files)
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
    # txt = fun_upfile( "D:/data/fsjx.dev/server/src/mod/agenda/agenda.erl" ,"text/plain" ,"agenda_php")
    # print(txt)
    ret = fun_web_req("http://127.0.0.1/fsjx.dev/server/src/mod/arena/arena_rpc.erl")
    # print(ret)
    # pattern = re.compile(r"temp_erl_data\/([a-z_A-Z]+)\.erl")
    pattern = re.compile(r"arena")
    regular_v1 = re.findall(pattern, ret.decode('utf-8'))
    print (regular_v1)



