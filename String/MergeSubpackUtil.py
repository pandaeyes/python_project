import os
import re
import io


mergePath = "D:/data/fsjx.dev/client/subpackfile"

pattern = re.compile(r'<file file=\"(.*?)\"/>', re.I)
def Merge():
    subFileList = []
    files = os.listdir(mergePath)
    for filename in files:
        logpath = os.path.join(mergePath, filename)
        if os.path.isfile(logpath) and "merge" not in filename:
            with open(logpath, "r") as obj:
                for line in obj:
                    subFileList.append(line.strip())
    subFileSet = set(subFileList)
    subFileSorted = sorted(subFileSet)

    outPath = mergePath + "/merge.txt"
    fw = open(outPath, 'w', encoding='utf-8')
    writeSet = []
    for fpath in subFileSorted:
        cpath = Cut(fpath)
        if cpath != "" and cpath not in writeSet:
            fw.write(cpath + "\n")
            writeSet.append(cpath)
    print("Done!")

def Cut(filepath):
    m = pattern.search(filepath)
    if m:
        filename = m.group(1)
        splitArr = filename.split("/")
        fname = splitArr[len(splitArr) - 1]
        fname = fname.replace("ui_pc", "ui_android")
        return "<file file=\"" + fname + "\"/>"
    return ""



    








if __name__ == "__main__":
    Merge()

