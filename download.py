import fsspec
import os
import json
from datetime import datetime

#path = Path.cwd() / "temp"

#path.mkdir()

#fs = fsspec.filesystem("github", org="Nathan8520", repo="Mk8dx-CT-modpack-maker")
#fs.get(fs.ls("__pycache__/"), os.getcwd(), recursive=True)

def updateTrackList():
    path = os.getcwd()
    fs = fsspec.filesystem("github", org="Nathan8520", repo="Mk8dx-CT-modpack-maker")

    if "trackList.txt" in os.listdir(path):
        os.remove("trackList.txt")

    fs.get("trackList.txt", path)

    file = open("trackList.txt", "r")
    tracks = file.read().split("\n")
    file.close()

    os.mkdir(f"{path}/temp")

    for track in tracks:
        if track in os.listdir(f"{path}/Courses"):
            data = json.loads(open(f"{path}/Courses/{track}/data.json", "r").read())

            currentDate = datetime.strptime(data ["Released"], "%d/%m/%Y")

            fs.get(f"Courses/{track}/data.json", f"{path}/temp")

            data = json.loads(open(f"{path}/temp/data.json", "r").read())

            onlineDate = datetime.strptime(data ["Released"], "%d/%m/%Y")

            os.remove(f"{path}/temp/data.json")

            if onlineDate > currentDate:
                os.remove(f"{path}/Courses/{track}")
            else:
                continue

        os.mkdir(f"{path}/Courses/{track}")

        fs.get(f"Courses/{track}/data.json", f"{path}/Courses/{track}")
        fs.get(f"Courses/{track}/icon.jpg", f"{path}/Courses/{track}")

    os.remove(f"{path}/temp")