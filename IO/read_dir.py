import os

path = "D:/data/fsjx.dev/bak"
dirs= os.listdir(path)
for dirname in dirs:
    if "ysc_sqwan" in dirname:
        logPath = path + "/" + dirname + "/lager_log/error.log.0"
        if os.path.exists(logPath):
        

