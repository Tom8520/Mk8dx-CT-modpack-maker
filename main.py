import os
import shutil
from constants import *
import json
import random
from bars import *

path = os.getcwd()

def compile(path, tracks, name):
    #create file structure
    opath = path
    os.mkdir(f"{path}/{name}")
    path += f"/{name}"

    os.mkdir(f"{path}/romfs")
    path += "/romfs"

    os.mkdir(f"{path}/Course")
    os.mkdir(f"{path}/UI")
    os.mkdir(f"{path}/Audio")
    os.mkdir(f"{path}/MapObj")

    #copy and rename course files

    for (courseName, over) in tracks:
        shutil.copytree(f"{opath}/Courses/{courseName}/Course/[CN]", f"{path}/Course/[CN]")
        os.rename(f"{path}/Course/[CN]", f"{path}/Course/{over}")

        for file in os.listdir(f"{path}/Course/{over}"):
            if "[CN]" in file:
                os.rename(f"{path}/Course/{over}/{file}", f"{path}/Course/{over}/{file.replace('[CN]', over)}")

    #copy and rename UI files

    os.mkdir(f"{path}/UI/cmn")
    os.mkdir(f"{path}/UI/cmn/menu")
    os.mkdir(f"{path}/UI/cmn/ending")

    for (courseName, over) in tracks:
        if "UI" in os.listdir(f"{opath}/Courses/{courseName}"):
            if "menu" in os.listdir(f"{opath}/Courses/{courseName}/UI/cmn"):
                shutil.copy(f"{opath}/Courses/{courseName}/UI/cmn/menu/ym_CoursePict_[CN]_00^u.bntx", f"{path}/UI/cmn/menu/ym_CoursePict_{over}_00^u.bntx")
            if "ending" in os.listdir(f"{opath}/Courses/{courseName}/UI/cmn"):
                shutil.copy(f"{opath}/Courses/{courseName}/UI/cmn/ending/ym_AwardBG_[CN]_00^o.bntx", f"{path}/UI/cmn/ending/ym_AwardBG_{over}_00^o.bntx")

    #copy map object files

    for (courseName, over) in tracks:
        if "MapObj" in os.listdir(f"{opath}/Courses/{courseName}"):
            for item in os.listdir(f"{opath}/Courses/{courseName}/MapObj"):
                if item in os.listdir(f"{path}/MapObj"):
                    print(f"FATAL ERROR: compiling {courseName} over {over} - MapObj {item} cannot be used twice")
                    print("Exiting compilation")
                    return
                shutil.copytree(f"{opath}/Courses/{courseName}/MapObj/{item}", f"{path}/MapObj/{item}")

    #create credits file

    file = open(f"{path}/../credits.txt", "w+")
    lines = ""
    for ( courseName, over) in tracks:
        data = json.loads(open(f"{opath}/Courses/{courseName}/data.json", "r").read())
        lines += courseName + ":\n"
        lines += f"Creator: {data ['Creator']}\n"
        lines += f"Original link: {data ['Link']}\n\n"
    file.write(lines)
    file.close()

    #copy audio files

    os.mkdir(f"{path}/Audio/Static")
    os.mkdir(f"{path}/Audio/Resource")
    os.mkdir(f"{path}/Audio/Resource/Stream")

    first = True

    for (courseName, over) in tracks:
        data = json.loads(open(f"{opath}/Courses/{courseName}/data.json", "r").read())

        if data ["Audio"] == "Yes":
            if first:
                first = False
                shutil.copy(f"{opath}/Courses/{courseName}/Audio/Static/BGM.bars", f"{path}/Audio/Static/BGM.bars")

            for file in os.listdir(f"{opath}/Courses/{courseName}/Audio/Resource/Stream"):
                shutil.copy(f"{opath}/Courses/{courseName}/Audio/Resource/Stream/{file}", f"{path}/Audio/Resource/Stream/{file}")
                os.rename(f"{path}/Audio/Resource/Stream/{file}", f"{path}/Audio/Resource/Stream/{file.replace('[ACN]', TRACK_TO_AUDIO [over])}")

                if not "BGM.bars" in os.listdir(f"{opath}/Courses/{courseName}/Audio/Static"):
                    continue

                origCourse = TRACK_TO_AUDIO [data ["Original_Course"]]
                fileName = file.split(".") [0]

                replaceBARS(f"{path}/Audio/Static/BGM.bars", f"{opath}/Courses/{courseName}/Audio/Static/BGM.bars", fileName.replace('[ACN]', TRACK_TO_AUDIO [over]), fileName.replace("[ACN]", origCourse))



pack = [[x, ""] for x in TRACK_NAMES]

customTracks = os.listdir("Courses/")

while True:
    cnt = 0
    for x in pack:
        print(f"{cnt}: {x [0]} -> {x [1]}")
        cnt += 1

    print("Enter the track you want to override: ")
    t = input()

    if t == "random":
        random.shuffle(customTracks)
        for x in range(min(len(pack), len(customTracks))):
            pack [x][1] = customTracks [x]
        continue
    if t == "":
        break

    cnt = 0
    for x in customTracks:
        print(f"{cnt}: {x}")
        cnt += 1

    print("Enter the track you want to port: ")
    ct = input()

    if ct == "":
        pack [int(t)][1] = ""
    else:
        pack [int(t)][1] = customTracks [int(ct)]

tracks = []
for x in pack:
    if x [1] != "":
        tracks.append(x [::-1])

print("Enter the name to save the modpack: ")
name = input()

print("Compiling modpack...")

compile(path, tracks, name)

print("Modpack generated!")



