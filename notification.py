import csv
import datetime
import logging
import os
import subprocess
from typing import List, Final
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase

import stringHelper
from model.BoardItem import BoardItem

ENCODING:Final[str] = "utf-8"

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class NotificationSetting:
    cmd: str = ""
    history: str = ""
    keywords: List[str] = field(default_factory=list)
    exclude_keywords: List[str] = field(default_factory=list)

class Notification(stringHelper.StringHelper):
    notifications: List[List[str]] = []

    def __init__(self, configDirPath: str, notiSetting: dict):
        self.notiSetting: NotificationSetting = NotificationSetting.from_dict(notiSetting) # type: ignore[attr-defined]
        self.historyFilePath = os.path.join(configDirPath, self.notiSetting.history)
        if os.path.isfile(self.historyFilePath):
            with open(self.historyFilePath, 'r', encoding=ENCODING) as f:
                self.notifications = list(csv.reader(f))

    def processNotification(self, siteName: str, boardItem: BoardItem) -> bool:
        """ Process the notification for a given site and board item."""

        notification_processed = False
        for keyword in self.notiSetting.keywords:
            if keyword in boardItem.title and all(ex not in boardItem.title for ex in self.notiSetting.exclude_keywords):
                if self.isTitleInNotificationHistory(boardItem.title):
                    logging.info(f"[{siteName}] Already in the notification history. [{boardItem.title}]")
                    continue
                try:
                    self.runNotiScript(siteName, boardItem.title)
                    # 알림 중복 방지 및 내역에서 직접 확인
                    self.appendNotiHistory(siteName, boardItem.title, keyword, boardItem.url)
                    notification_processed = True
                except Exception as e:
                    logging.error(f"Error processing notification for {siteName} and {boardItem.title}: {e}")

        return notification_processed

    def runNotiScript(self, siteName: str, boardTitle: str) -> int:
        """Run the notification script and return the exit code."""
        cmd = self.notiSetting.cmd
        if cmd is not None and cmd != "":
            cmd = cmd.replace("$board_title", "[" + siteName + "]" + boardTitle.replace("'", "`"))
            try:
                result = subprocess.run(cmd, shell=True, check=True)
                logging.debug(f"run command: [{cmd}]")
                return result.returncode
            except subprocess.CalledProcessError as e:
                logging.error(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
                return e.returncode
        else:
            logging.debug("Command for notification settings is missing.")
            return 1  # Return a non-zero exit code to indicate an error

    def isTitleInNotificationHistory(self, title: str) -> bool:
        """Check if the given title is already in the notification history."""
        for notification in self.notifications:
            if self.isExactWordInParam(title, notification[2]):
                return True
        return False

    def appendNotiHistory(self, sitename: str, title: str, keyword: str, url: str) -> None:
        """Add a new entry to the notification history."""
        runtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new = [runtime, sitename, title, keyword, url]
        try:
            with open(self.historyFilePath, 'a', encoding=ENCODING) as f:
                writer = csv.writer(f)
                writer.writerow(new)
            self.notifications.append(new)
            logging.info(f"addNotiHistory. [{new}]")
        except PermissionError:
            logging.error(f"Permission denied when trying to write to {self.historyFilePath}")
        except FileNotFoundError:
            logging.error(f"File {self.historyFilePath} not found")
        except OSError as e:
            logging.error(f"OS error occurred when trying to write to {self.historyFilePath}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error occurred when trying to write to {self.historyFilePath}: {e}")
