import csv
import logging
import os
import subprocess
import datetime
from typing import List, Dict, Any

# Constants
HISTORY = "history"
CMD = "cmd"
KEYWORDS = "keywords"
ENCODING = "utf-8"

class Notification:
    notifications: List[List[str]] = []

    def __init__(self, configDirPath: str, notiSetting: Dict[str, Any]):
        self.notiSetting = notiSetting  # mySetting.json["notification"]
        self.historyFilePath = os.path.join(configDirPath, self.notiSetting[HISTORY])
        if not os.path.isfile(self.historyFilePath):
            logging.error(f"File {self.historyFilePath} not found")
            return
        with open(self.historyFilePath, 'r', encoding=ENCODING) as f:
            self.notifications = list(csv.reader(f))

    def executeNotiScript(self, siteName: str, boardTitle: str) -> bool:
        """
        Execute the notification script.
        If the script is executed, return True.
        If the script has already been executed or cannot be executed, return False.
        """
        if not self.isValidNotiSetting():
            return False

        for keyword in self.notiSetting[KEYWORDS]:
            if keyword in boardTitle:
                if self.checkNotiHistory(boardTitle):
                    logging.debug(f"Already in the notification history. [{boardTitle}]")
                    return False
                try:
                    cmd = self.notiSetting[CMD]
                    cmd = cmd.replace("$board_title", "[" + siteName + "]" + boardTitle.replace("'", "`"))
                    self.run_command(cmd)
                    self.addNotiHistory(siteName, boardTitle, keyword)
                    return True
                except Exception as e:
                    logging.error(f"Error executing notification script: {e}")
        return False

    def run_command(self, cmd: str) -> None:
        """Run a command using subprocess."""
        try:
            subprocess.run(cmd, shell=True, check=True)
            logging.debug(f"run_command: [{cmd}]")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running command: {e}")

    def isValidNotiSetting(self) -> bool:
        """Check if the notification settings are valid."""
        if not isinstance(self.notiSetting, dict):
            logging.error("Notification settings must be a dictionary.")
            return False

        if self.notiSetting[CMD] is None or self.notiSetting[CMD] == "":
            logging.error("Command for notification settings is missing.")
            return False

        return True

    def checkNotiHistory(self, title: str) -> bool:
        """Check if the given title is already in the notification history."""
        for notification in self.notifications:
            if title == notification[2]:
                logging.info(f"Already in the notification history. [{title}]")
                return True
        return False

    def addNotiHistory(self, sitename: str, title: str, keyword: str) -> None:
        """Add a new entry to the notification history."""
        runtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new = [runtime, sitename, title, keyword]
        try:
            with open(self.historyFilePath, 'a', newline='\n', encoding=ENCODING) as f:
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
