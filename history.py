import datetime
import os
import csv
import keywords


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

    def isMagnetAppended(self, magnet: str) -> bool:
        for row in reversed(self.data):
            if magnet == row[3]:
                return True
        return False

    def appendMagnet(self, siteName: str, boardTitle: str, magnet: str, keyword: str) -> None:
        runtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # "": tag
        magnetInfo = [runtime, siteName, boardTitle, magnet, keyword, ""]
        self.data.append(magnetInfo)
        with open(self.historyFileName, 'a', newline='\n', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(magnetInfo)

    def appendTorrentFail(self, siteName: str, boardTitle: str, boardUrl: str, keyword: str, downloadDir: str) -> None:
        runtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        torrentFailInfo = [runtime, siteName, boardTitle, boardUrl, keyword, downloadDir]
        with open(self.failFileName, 'a', newline='\n', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(torrentFailInfo)

    def isEpisodeDownloaded(self, keyword: str, episodeNumber: int) -> bool:
        if episodeNumber is None:
            return False
        for row in reversed(self.data):
            if row[4] == keyword:
                myKeywords = keywords.Keywords()
                if myKeywords.getEpisodeNumber(row[2]) == episodeNumber:
                    return True
        return False