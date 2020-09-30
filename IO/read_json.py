import os


def ReadFile():
    path = "C:/Users/panda/Desktop/kkk/1.TXT";
    lists = []
    with open(path, "r") as obj:
        for line in obj:
            if "LoadFromFil" in line and "expMessage" in line:
                lists.append(line.strip())
                # print(line.strip()[line.index("private") - 1:])

    with open(path + ".2.txt", "w") as obj:
        for line in lists:
            obj.write(line + "\n")

    objDict = {}
    for line in lists:
        if "Raw" in line:
            line = line[line.index("Raw") + 3:]
        elif "Documents" in line:
            line = line[line.index("Documents"):]
        if line not in objDict:
            objDict[line] = 1
        else:
            objDict[line] = objDict[line] + 1

    objDict = sorted(objDict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    with open(path + ".sum.txt", "w") as obj:
        for key, val in objDict:
            obj.write(key + " ===> " + str(val) + "\n")
        # print(key + " ===> " + str(val))
        


if __name__ == '__main__':
    ReadFile()
