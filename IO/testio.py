import os


if __name__ == '__main__':
    for root, dirs, files in os.walk("D:/data/fsjx.dev/android_project/libs"):
        print(root)
        print(dirs)
        print(files)
        print(len(files))
        print("===================")
