import csv
import os
import subprocess
import datetime

class Notification:
    def __init__(self, notiSetting: dict):
        self.notiSetting = notiSetting  # mySetting.json["notification"]
        if os.path.isfile(self.notiSetting["history"]):
            with open(self.notiSetting["history"], 'r', encoding="utf-8") as f:
                self.history = list(csv.reader(f))
        else:
            self.history = []

    def executeNotiScript(self, siteName: str, boardTitle: str) -> bool:
        """
        스크립트를 실행했으면 true를 리턴하고
        이미 실행한 경우나 실행하지 못한 경우는 false를 리턴한다.
        """
        notiSetting = self.notiSetting

        if notiSetting == "":
            return False

        if notiSetting["cmd"] == "":
            return False

        for keyword in notiSetting["keywords"]:
            if keyword in boardTitle:
                if self.checkNotiHistory(boardTitle):
                    return False
                cmd = notiSetting["cmd"]
                cmd = cmd.replace("$board_title", "[" + siteName + "]" + boardTitle.replace("'", "`"))
                try:
                    # check가 참이고, 프로세스가 0이 아닌 종료 코드로 종료되면, CalledProcessError 예외가 발생합니다.
                    subprocess.run(cmd, shell=True, check=True)

                except Exception as e:
                    print("executeNotiScript error, message: " + str(e))
                    return False
                else:
                    self.addNotiHistory(siteName, boardTitle, keyword)
                    return True

    def checkNotiHistory(self, title: str) -> bool:
        for row in self.history:
            if title == row[2]:
                # print("\t\t-> magnet was already downloaded at web_scraper_history.csv")
                return True
        return False

    def addNotiHistory(self, sitename: str, title: str, keyword: str) -> None:
        runtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new = [runtime, sitename, title, keyword]
        with open(self.notiSetting["history"], 'a', newline='\n', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(new)
            self.history.append(new)
