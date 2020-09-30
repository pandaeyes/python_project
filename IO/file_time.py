import os
import time

# os.path.getatime(file) 输出文件访问时间
# os.path.getctime(file) 输出文件的创建时间
# os.path.getmtime(file) 输出文件最近修改时间

if __name__ == '__main__':
    path = "D:/data/UploadLog.py"
    ts = os.path.getmtime(path)
    print(str(ts))
    now_time = time.time()
    tdiff = (now_time - ts)/(60*60*24) 
    if tdiff < 3:
        print((now_time - ts)/(60*60*24))
    else:
        print("pass" + str(tdiff))
