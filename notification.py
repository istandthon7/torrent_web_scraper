import csv
import logging
import os
import subprocess
import datetime
from typing import List, Dict, Any


class Notification:
    notifications: List[List[str]] = []

    def __init__(self, notiSetting: Dict[str, Any]):
        self.notiSetting = notiSetting  # mySetting.json["notification"]
        if not os.path.isfile(notiSetting["history"]):
            return
        with open(self.notiSetting["history"], 'r', encoding="utf-8") as f:
            self.notifications = list(csv.reader(f))

    def executeNotiScript(self, siteName: str, boardTitle: str) -> bool:
        """
        스크립트를 실행했으면 true를 리턴하고
        이미 실행한 경우나 실행하지 못한 경우는 false를 리턴한다.
        """
        if not self.isValidNotiSetting():
            return False

        for keyword in self.notiSetting["keywords"]:
            if keyword in boardTitle:
                if self.checkNotiHistory(boardTitle):
                    return False
                cmd = self.notiSetting["cmd"]
                cmd = cmd.replace("$board_title", f'[{siteName}]{boardTitle.replace("'", "`")}')
                try:
                    # check가 참이고, 프로세스가 0이 아닌 종료 코드로 종료되면, CalledProcessError 예외가 발생합니다.
                    subprocess.run(cmd, shell=True, check=True)
                    self.addNotiHistory(siteName, boardTitle, keyword)
                    return True
                except subprocess.CalledProcessError as e:
                    logging.error(f"CalledProcessError: {e}")
                except FileNotFoundError as e:
                    logging.error(f"FileNotFoundError: {e}")
                except (PermissionError, OSError) as e:
                    logging.error(f"Error: {e}")
                except Exception as e:
                    logging.error(f"executeNotiScript error, message==>\n{str(e)}")
        return False

    def isValidNotiSetting(self) -> bool:
        """Check if the notification settings are valid."""
        if not isinstance(self.notiSetting, dict):
            logging.error("notiSetting must be a dictionary")
            return False

        if self.notiSetting["cmd"] is None or self.notiSetting["cmd"] == "":
            return False

        return True

    def checkNotiHistory(self, title: str) -> bool:
        """Check if the given title is already in the notification history."""
        for notification in self.notifications:
            if title == notification[2]:
                logging.debug(f"이미 알림 내역에 있어요. [{notification[2]}]")
                return True
        return False

    def addNotiHistory(self, sitename: str, title: str, keyword: str) -> None:
        """Add a new entry to the notification history."""
        runtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new = [runtime, sitename, title, keyword]
        with open(self.notiSetting["history"], 'a', newline='\n', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(new)
        self.notifications.append(new)
