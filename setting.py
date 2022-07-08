import os
import sys
import datetime 
import json

class Setting:
    """
    설정파일을 self.json 로딩, 저장한다. 
    버전이 변경되면 self.version을 변경해야 한다.(소스에서 아직 참조하지 않으나 운영상 필요할 수있음)
    """
    version = '2.0.00-beta1'

    currentPath = os.path.realpath(os.path.dirname(__file__))
    configDirPath = currentPath + "/config/"
    settingPath = configDirPath + "setting.json"
    
    runTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transmissionScriptDirPath = currentPath + "/transmission_script/"
    torrentDoneSHPath = transmissionScriptDirPath + "torrent_done.sh"
    renameSeasonTransmissionPYPath = transmissionScriptDirPath + "rename_season_transmission.py"
    scraperLibraryPYPath = transmissionScriptDirPath + "scraperHelpers.py"
    configHelperPYPath = transmissionScriptDirPath + "configHelper.py"

    def __init__(self) -> None:
        if os.path.isfile(self.settingPath):
            self.loadJson()
            self.torrentHistoryPath = self.configDirPath + self.json["torrentHistory"]
            self.torrentFailPath = self.configDirPath + self.json["torrentFail"]
            self.notiHistoryPath = self.configDirPath + self.json["notification"]["history"]

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