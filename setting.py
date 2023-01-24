import os
import sys
import datetime
import json
import logging

class Setting:
    """
    설정파일을 self.json 로딩, 저장한다. 
    버전이 변경되면 self.version을 변경해야 한다.(소스에서 아직 참조하지 않으나 운영상 필요할 수있음)
    """
    version = '2.1.03'

    currentPath = os.path.realpath(os.path.dirname(__file__))
    configDirPath = currentPath + "/config/"
    settingPath = configDirPath + "setting.json"

    runTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transmissionScriptDirPath = currentPath + "/transmission_script/"
    torrentDoneSHPath = transmissionScriptDirPath + "torrent_done.sh"
    renameSeasonTransmissionPYPath = transmissionScriptDirPath + "rename_season_transmission.py"
    scraperLibraryPYPath = transmissionScriptDirPath + "scraperHelpers.py"
    settingPYPath = transmissionScriptDirPath + "setting.py"

    transPass = None
    json = json.dumps({})
    """설정정보를 가지는 json객체"""

    def __init__(self) -> None:
        if os.path.isfile(self.settingPath):
            self.loadJson()
            self.torrentHistoryPath = self.configDirPath + self.json["torrentHistory"]
            self.torrentFailPath = self.configDirPath + self.json["torrentFail"]
            self.notiHistoryPath = self.configDirPath + self.json["notification"]["history"]
            # 로그 초기화
            loglevel = self.json["logging"]["logLevel"]
            #getattr(logging, loglevel.upper())
            numericLevel = getattr(logging, loglevel.upper(), None)
            if not isinstance(numericLevel, int):
                raise ValueError('Invalid log level: %s' % loglevel)
            logging.basicConfig(level=numericLevel, filename=self.json["logging"]["logFile"]
                , format='%(asctime)s %(levelname)s:%(message)s')

    def loadJson(self)->None:
        # try -> except -> else -> finally
        try:
            settingText = open(self.settingPath, 'r', encoding='utf-8')
        except FileNotFoundError as e:
            print("설정파일("+self.settingPath+")이 없습니다. ./install.sh 를 실행한 후 변경사항을 적용하세요.")
            print(str(e))
            sys.exit()
        else:
            self.json = json.load(settingText)
            settingText.close()

    def saveJson(self)->None:
        with open(self.settingPath, 'w', encoding='utf-8') as dataFile:
            json.dump(self.json, dataFile, sort_keys = True, ensure_ascii=False, indent = 2)

    def getRpcUrl(self)->str:
        transmissionSetting = self.json['transmission']
        url = "http"
        if transmissionSetting['port'] == 443:
            url += "s"
        if self.transPass is None:
            self.transPass = transmissionSetting['pw']
        url += "://%s:%s@%s:%s/transmission/rpc" % (transmissionSetting['id'], self.transPass
                                                    , transmissionSetting['host'], transmissionSetting['port'])
        return url