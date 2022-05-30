import httplib2
import os
import json
import datetime
import zipfile

def connect():
    return httplib2.HTTPConnectionWithTimeout("95.217.33.147", 26032)

def downloadFile(filename, conn = None):
    conn = conn if not conn is None else connect()

    filename = filename.replace(" ", "[SPACE]")

    conn.request("GET", filename)

    r = conn.getresponse()

    data = r.read()

    return data

def getTrackUpdateStatus(track, conn=None):
    path = os.getcwd()

    if not track in os.listdir(f"{path}/Courses"):
        return 0

    data = str(downloadFile(track + ".json", conn)) [2:-1]
    data = data.replace("\\r", "").replace("\\t", "").replace("\\n", "")

    newData = json.loads(data)

    oldData = json.loads(open(f"{path}/Courses/{track}/data.json", "r").read())

    newDate = datetime.datetime.strptime(newData ["Updated"], "%d/%m/%Y")
    oldDate = datetime.datetime.strptime(oldData ["Updated"], "%d/%m/%Y")

    if newDate > oldDate:
        return 2

    return 1

def updateTracks():
    conn = connect()

    files = str(downloadFile("LISTDIR", conn)) [2:-1].split(",")

    tracks = []
    for x in files:
        if ".zip" in x:
            tracks.append(x.split(".zip") [0])

    trackStatus = [getTrackUpdateStatus(t, conn) for t in tracks]

    path = os.getcwd()

    for x in range(len(trackStatus)):
        if trackStatus [x] == 1:
            continue

        if trackStatus [x] == 2:
            os.rmdir(f"{path}/Courses/{tracks [x]}")

        os.mkdir(f"{path}/Courses/{tracks [x]}")

        data = downloadFile(f"{tracks [x]}.json", conn)
        file = open(f"{path}/Courses/{tracks [x]}/data.json", "wb")
        file.write(data)
        file.close()

        data = downloadFile(f"{tracks[x]}.jpg", conn)
        file = open(f"{path}/Courses/{tracks[x]}/icon.jpg", "wb")
        file.write(data)
        file.close()

def downloadTrack(track):
    path = os.getcwd()

    data = downloadFile(f"{track}.zip")

    file = open(f"{path}/Courses/{track}/temp.zip", "wb")
    file.write(data)
    file.close()

    with zipfile.ZipFile(f"{path}/Courses/{track}/temp.zip", "r") as zip:
        zip.extractall(f"{path}/Courses/{track}")

    os.remove(f"{path}/Courses/{track}/temp.zip")


