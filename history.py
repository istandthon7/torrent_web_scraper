import datetime
import os
import csv

class MagnetHistory:
    def __init__(self, historyFileName: str, failFileName: str):
        self.failFileName = failFileName
        self.historyFileName = historyFileName
        self.data = []
        if os.path.isfile(historyFileName):
            with open(historyFileName, 'r', encoding="utf-8") as f:
                ff = csv.reader(f)
                for row in ff:
                    if len(row) != 0:
                        self.data.append(row)

    def checkMagnetHistory(self, magnet: str) -> bool:
        for row in self.data:
            if magnet == row[3]:
                return True
        return False

    def addMagnetToHistory(self, siteName: str, boardTitle: str, magnet: str, keyword: str) -> None:
        runtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        magnetInfo = [runtime, siteName, boardTitle, magnet, keyword]
        self.data.append(magnetInfo)
        with open(self.historyFileName, 'a', newline='\n', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(magnetInfo)

    def addTorrentFailToFile(self, siteName: str, boardTitle: str, boardUrl: str, keyword: str, downloadDir: str) -> None:
        runtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        torrentFailInfo = [runtime, siteName, boardTitle, boardUrl, keyword, downloadDir]
        with open(self.failFileName, 'a', newline='\n', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(torrentFailInfo)
