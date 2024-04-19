
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from typing import Dict, Any


class Setting:
    """
    설정파일을 self.json에 로딩, 저장한다. 
    버전이 변경되면 self.version을 변경해야 한다.(소스에서 아직 참조하지 않으나 필요할 수있음)
    """
    version = '2.4.1'

    currentPath = os.path.realpath(os.path.dirname(__file__))
    configDirPath = os.path.join(currentPath, "config")
    settingPath = os.path.join(configDirPath, "setting.json")

    transmissionScriptDirPath = os.path.join(currentPath, "transmission_script")
    torrentDoneSHPath = os.path.join(transmissionScriptDirPath, "torrent_done.sh")

    json: Dict[str, Any] = {}
    """설정정보를 가지는 json객체"""

    def __init__(self) -> None:
        if os.path.isfile(self.settingPath):
            self.loadJson()
            
            # 로그 초기화
            loglevel = self.json["logging"]["logLevel"]
            #getattr(logging, loglevel.upper())
            numericLevel = getattr(logging, loglevel.upper(), None)
            if not isinstance(numericLevel, int):
                raise ValueError('Invalid log level: %s' % loglevel)
            # 로그 파일 경로
            logFilePath = os.path.join(self.configDirPath, self.json["logging"]["logFile"])

            # 로그 회전 핸들러 생성 및 설정
            handler = RotatingFileHandler(logFilePath, maxBytes=self.json["logging"].get("maxBytes", 1048576), backupCount=self.json["logging"].get("backupCount", 5))
            handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))

            # 기본 로거 설정
            logging.basicConfig(level=numericLevel, handlers=[handler])

    def loadJson(self)->None:
        try:
            with open(self.settingPath, 'r', encoding='utf-8') as settingText:
                self.json = json.load(settingText)
        except FileNotFoundError as e:
            print("설정파일("+self.settingPath+")이 없습니다. ./install.sh 를 실행한 후 변경사항을 적용하세요.")
            print(str(e))
            sys.exit()

    def saveJson(self)->None:
        with open(self.settingPath, 'w', encoding='utf-8') as dataFile:
            json.dump(self.json, dataFile, sort_keys = True, ensure_ascii=False, indent = 2)
