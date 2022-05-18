from utils import *
import struct
from constants import *

def extractTrackBARS(filename, track):
    nameIndex = AUDIO_FILE_NAMES.index(track)

    file = open(filename, "rb")
    bars = file.read()
    file.close()

    if bars[0x8:0xA] == b"\xFF\xFE":
        bom = '<'
    else:
        bom = '>'

    file_size = len(bars)
    pos = 0

    header = Header(bom)
    header.data(bars, pos)

    pos += header.size + header.count * 4

    track_struct = TRKStruct(bom, header.count)
    track_struct.data(bars, pos)

    infoPosStart = track_struct.offsets [2 * nameIndex]

    dataPosStart = track_struct.offsets[2 * nameIndex + 1]

    fwav = FWAVHeader(bom)
    fwav.data(bars, dataPosStart)

    dataPosEnd = dataPosStart + fwav.size_

    amta = AMTAHeader(bom)
    amta.data(bars, infoPosStart)

    infoPosEnd = infoPosStart + amta.length

    data = bars [dataPosStart:dataPosEnd]
    info = bars[infoPosStart:infoPosEnd]

    return info, data

def getOffsets(bars):
    if bars[0x8:0xA] == b"\xFF\xFE":
        bom = '<'
    else:
        bom = '>'

    file_size = len(bars)
    pos = 0

    header = Header(bom)
    header.data(bars, pos)

    pos += header.size + header.count * 4

    track_struct = TRKStruct(bom, header.count)
    track_struct.data(bars, pos)

    return track_struct.offsets

def getBom(bars):
    if bars[0x8:0xA] == b"\xFF\xFE":
        return '<'
    else:
        return '>'

def replaceBARS(filenameTO, filenameFROM, trackTO, trackFROM):
    file = open(filenameTO, "rb")
    bars = file.read()
    file.close()

    bom = getBom(bars)

    offsets = [x for x in getOffsets(bars)]

    nameIndex = 2 * AUDIO_FILE_NAMES.index(trackTO)

    infoFROM, dataFROM = extractTrackBARS(filenameFROM, trackFROM)
    infoTO, dataTO = extractTrackBARS(filenameTO, trackTO)

    amta = [x for x in struct.unpack_from("4s2H5I", infoFROM, 0)]
    amta [3] += len(trackTO)-len(trackFROM)

    infoFROM = struct.pack("4s2H5I", *amta) + infoFROM [struct.calcsize("4s2H5I"):]

    infoFROM = infoFROM.replace(bytes(trackFROM, "utf-8"), bytes(trackTO, "utf-8"))

    infoLenDiff = len(infoFROM) - len(infoTO)
    dataLenDiff = len(dataFROM) - len(dataTO)

    for x in range(len(offsets)):
        td = 0
        if offsets [x] > offsets [nameIndex]:
            td += infoLenDiff

        if offsets [x] > offsets [nameIndex+1]:
            td += dataLenDiff

        offsets [x] += td

    bars = bars.replace(infoTO, infoFROM)
    bars = bars.replace(dataTO, dataFROM)

    header = Header(bom)
    header.data(bars, 0)

    fmt = f"{bom}{2*header.count}I"

    off = struct.pack(fmt, *offsets)

    pos = header.size + 4 * header.count
    size = struct.calcsize(fmt)

    bars = bars.replace(bars [pos:pos+size], off)

    file = open(filenameTO, "wb")
    file.write(bars)
    file.close()