import datetime

# print(datetime.datetime.now().hour + "")

strs = "lua/data_animation.lua | fdfsf"

strs2 = "/private/var/containers/Bundle/Application/8E7BC14D-44C9-44A0-8FF3-791C73003F8B/cheng.app/Data/Raw/textures/ui_ios/textures$ui_ios$farmerbattle.folder"

if "|" in strs:
    print(strs[:strs.index("|")])
    print(strs[:strs.index("|")])
else:
    print(strs)
print(strs2[strs2.index("Raw") + 3:])


if "lua" in strs and "data1" not in strs:
    print("lua")


strs3 = " <uses-permission android:name=\"getui.permission.GetuiService.com.shiyuegame.yscthird\" /> <uses-permission android:name=\"getui.permission.GetuiService.com.shiyuegame.yscthird\" /> <uses-permission android:name=\"getui.permission.GetuiService.com.shiyuegame.yscthird\" /> <uses-permission android:name=\"getui.permission.GetuiService.com.shiyuegame.yscthird\" /> <uses-permission android:name=\"getui.permission.GetuiService.com.shiyuegame.yscthird\" />"
print(strs3.replace("com.shiyuegame.yscthird", "com.shiyuegame.ysc"))
