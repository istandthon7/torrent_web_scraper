
import os
import csv
import setting

def checkMagnetHistory(csvFileName: str, magnet: str)->bool:
    if not os.path.isfile(csvFileName):
        return False

    with open(csvFileName, 'r', encoding="utf-8") as f:
        ff = csv.reader(f)
        for row in ff:
            if magnet == row[3]:
                return True
    return False

def addMagnetToHistory(mySetting: setting.Setting, siteName: str, boardTitle: str
    , magnet: str, keyword: str)->None:
    runtime = mySetting.runTime
    magnetInfo = [runtime, siteName, boardTitle, magnet, keyword]
    with open(mySetting.torrentHistoryPath, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(magnetInfo)
    f.close()

def addTorrentFailToFile(mySetting: setting.Setting, siteName: str, boardTitle: str
    , boardUrl: str, keyword: str, downloadDir: str)->None:
    runtime = mySetting.runTime
    torrentFailInfo = [runtime, siteName, boardTitle, boardUrl, keyword, downloadDir]
    with open(mySetting.torrentFailPath, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(torrentFailInfo)
    f.close()