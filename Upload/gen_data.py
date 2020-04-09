#!/usr/bin/env python
#coding:utf8
#-----------------------------------------------------
# 翻译打包实现
#
# @author whjing2012@gmail.com
#-----------------------------------------------------
import sys
import re
import os

import requests
import urllib.request


http_host="http://dldl-dev.shiyuegame.com/dev/index.php"

# 获取文件内容
def get_file_content(filepath):
    filestr=""
    if os.path.isfile(filepath):
        f = open(filepath, "r", encoding='utf-8')
        filestr = f.read()
        f.close()
    return filestr

#  # web访问
#  def fun_web_req(request):
#      response = urllib2.urlopen(request)
#      ret = response.read()
#      return ret
#  # web访问
def fun_web_req(url):
    response = urllib.request.urlopen(url, data=None, timeout=10) 
    ret = response.read()
    return ret

# web下载处理
# def fun_web_download(url, savepath):
#     f = urllib2.urlopen(url) 
#     with open(savepath, "wb") as code:
#         code.write(f.read())
#         print("download savepath:", savepath)
# web下载处理
def fun_web_download(url, savepath):
    f = urllib.request.urlopen(url) 
    with open(savepath, "wb") as code:
        code.write(f.read())
        print("download savepath:", savepath)
  
# 上传配置文件
def fun_upcfg(RootDir, Mod, filestr):
    fun_upfile(RootDir + "/tools/gen_data/cfg/" + Mod + ".erl", "cfg", Mod)
    hrl_list = re.findall(r"([a-z_A-Z]+\.hrl)", filestr)
    for hrl in hrl_list:
        if hrl != "data_config.hrl" and hrl != "common.hrl" and hrl != "scene.hrl":
            fun_upfile(RootDir + "/server/include/" + hrl, "hrl", Mod)

def fun_upfile(filepath, ftype, mod):
    if not os.path.isfile(filepath):
        return
    print("upfile===>>", filepath, ftype)
    #  f=open(filepath, "rb")
    #  # headers 包含必须的 Content-Type 和 Content-Length
    #  # datagen 是一个生成器对象，返回编码过后的参数
    #  datagen, headers = multipart_encode({"myFile": f})
    #  # 创建请求对象
    #  request = urllib2.Request(http_host + "/tools/upload_file?type="+ftype, datagen, headers)
    #  return fun_web_req(request)
    upload_url = http_host + "/tools/upload_file";
    files = {"myFile":(mod, open(filepath, "rb"), "text/plain",  {})}
    response = requests.request("POST", upload_url, data={"type":"" + ftype}, files=files)
    print(response.text)


# 下载beam文件
def fun_down_beam(RootDir, Mod):
    if not os.path.isdir(RootDir + "/server/dbin"):
        return False
    url = http_host + "/tools/web_get_beam?mod="+Mod
    print("doing fun_down_beam", Mod)
    return fun_web_download(url, RootDir + "/server/dbin/" + Mod + ".beam")

# 下载lua文件
def fun_down_luac(RootDir, Mod):
    if not os.path.isdir(RootDir + "/client/src/config"):
        return False
    url = http_host + "/tools/web_get_luac?mod="+Mod
    print("doing fun_down_luac", Mod)
    return fun_web_download(url, RootDir + "/client/src/config/" + Mod + ".luac")

# 生成文件
def fun_gen_data(RootDir, Mod):
    cfgfile = RootDir + "/tools/gen_data/cfg/" + Mod + ".erl"
    filestr = get_file_content(cfgfile)
    print("doing upcfg for ", Mod)
    fun_upcfg(RootDir, Mod, filestr)
    # request = urllib2.Request(http_host + "/tools/web_gen_data?mod="+Mod)
    gen_data_ret = fun_web_req(http_host + "/tools/web_gen_data?mod="+Mod)
    tpl_list = re.findall(r"temp_erl_data\/([a-z_A-Z]+)\.erl", gen_data_ret)
    for tpl in tpl_list:
        fun_down_beam(RootDir, tpl)
    #tpl_list = re.findall(r"temp_cli_config\/([a-z_A-Z]+)\.lua", gen_data_ret)
    #for tpl in tpl_list:
    #    fun_down_luac(RootDir, tpl)

# 生成文件配置XML
def fun_gen_xml(RootDir, Mod):
    url = http_host + "/tools/web_gen_xml?mod="+Mod
    print("doing fun_gen_xml", Mod)
    return fun_web_download(url, RootDir + "/tools/gen_data/template/" + Mod + ".xml")

# 帮助输出
def fun_help():
    print("gen_data RootDir Mod")
    print("gen_xml RootDir Mod")
    exit()

if len(sys.argv) < 2: fun_help

# register_openers()
cmd = sys.argv[1]
if(cmd == "gen_data" and len(sys.argv) >= 4) : fun_gen_data(sys.argv[2], sys.argv[3])
if(cmd == "gen_xml" and len(sys.argv) >= 4) : fun_gen_xml(sys.argv[2], sys.argv[3])
else : fun_help
