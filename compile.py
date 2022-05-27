import os
import shutil
from constants import *
import json
import random
from bars import *

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
        if over == "Du_Animal":
            names = ["Du_Animal_Autumn", "Du_Animal_Spring", "Du_Animal_Summer", "Du_Animal_Winter"]
        else:
            names = [over]

        for name in names:
            shutil.copytree(f"{opath}/Courses/{courseName}/Course/[CN]", f"{path}/Course/[CN]")
            os.rename(f"{path}/Course/[CN]", f"{path}/Course/{name}")

            for file in os.listdir(f"{path}/Course/{name}"):
                if "[CN]" in file:
                    os.rename(f"{path}/Course/{name}/{file}", f"{path}/Course/{name}/{file.replace('[CN]', name)}")

    #copy and rename UI files

    os.mkdir(f"{path}/UI/cmn")
    os.mkdir(f"{path}/UI/cmn/menu")
    os.mkdir(f"{path}/UI/cmn/ending")

    for (courseName, over) in tracks:
        if over == "Du_Animal":
            names = ["Du_Animal_Autumn", "Du_Animal_Spring", "Du_Animal_Summer", "Du_Animal_Winter"]
        else:
            names = [over]

        for name in names:
            if "UI" in os.listdir(f"{opath}/Courses/{courseName}"):
                if "menu" in os.listdir(f"{opath}/Courses/{courseName}/UI/cmn"):
                    shutil.copy(f"{opath}/Courses/{courseName}/UI/cmn/menu/ym_CoursePict_[CN]_00^u.bntx", f"{path}/UI/cmn/menu/ym_CoursePict_{name}_00^u.bntx")
                if "ending" in os.listdir(f"{opath}/Courses/{courseName}/UI/cmn"):
                    shutil.copy(f"{opath}/Courses/{courseName}/UI/cmn/ending/ym_AwardBG_[CN]_00^o.bntx", f"{path}/UI/cmn/ending/ym_AwardBG_{name}_00^o.bntx")

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
            if first and "BGM.bars" in os.listdir(f"{opath}/Courses/{courseName}/Audio/Static"):
                first = False
                shutil.copy(f"{opath}/Courses/{courseName}/Audio/Static/BGM.bars", f"{path}/Audio/Static/BGM.bars")

            for file in os.listdir(f"{opath}/Courses/{courseName}/Audio/Resource/Stream"):
                if over == "Du_Animal":
                    names = ["Du_Animal_Autumn", "Du_Animal_Spring", "Du_Animal_Summer", "Du_Animal_Winter"]
                else:
                    names = [over]

                for name in names:
                    shutil.copy(f"{opath}/Courses/{courseName}/Audio/Resource/Stream/{file}", f"{path}/Audio/Resource/Stream/{file}")
                    os.rename(f"{path}/Audio/Resource/Stream/{file}", f"{path}/Audio/Resource/Stream/{file.replace('[ACN]', TRACK_TO_AUDIO [name])}")

                    if not "BGM.bars" in os.listdir(f"{opath}/Courses/{courseName}/Audio/Static"):
                        continue


                    origCourse = TRACK_TO_AUDIO [data ["Original_Course"]]
                    fileName = file.split(".") [0]

                    replaceBARS(f"{path}/Audio/Static/BGM.bars", f"{opath}/Courses/{courseName}/Audio/Static/BGM.bars", fileName.replace('[ACN]', TRACK_TO_AUDIO [name]), fileName.replace("[ACN]", origCourse))

    #generate message.SARC file



path = os.getcwd()

for file in os.listdir(f"{path}/Courses"):
    data = json.loads(open(f"{path}/Courses/{file}/data.json", "r").read())

    print(f"{file} By {data ['Creator']} ({data ['Link']})")

