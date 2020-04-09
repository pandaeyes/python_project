import os

# for root, dirs, files in os.walk("G:/data/Unity2019.pro/Test2019/ppp/unityLibrary/src/main", topdown=False):
#     for name in dirs:
#         print(name)

path = "G:/data/Unity2019.pro/Test2019/ppp/unityLibrary/src/main"

def get_filelist(dir1, Filelist):
    newdir = dir1
    if os.path.isfile(dir1):
        Filelist.append(dir1)
    elif os.path.isdir(dir1):
        for s in os.listdir(dir1):
            if s == "assets":
                continue
            newdir = os.path.join(dir1, s)
            get_filelist(newdir, Filelist)
    return Filelist

if __name__ =='__main__' :
    list = get_filelist(path, [])
    print(len(list))
    for e in list:
        print(e)
