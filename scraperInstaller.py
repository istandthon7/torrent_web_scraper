#!/usr/bin/python3
import os
import shutil
from typing import Optional
import setting
import osHelper

class ScraperInstaller:

    mySetting = setting.Setting()

    def __init__(self, configDir: Optional[str] = None) -> None:
        if configDir is not None:
            self.mySetting.configDirPath = os.path.join(self.mySetting.currentPath, configDir)
            self.mySetting.settingPath = os.path.join(self.mySetting.configDirPath, "setting.json")

    def copyFileIfNotExist(self, fullPath: str, isSample: bool = True) -> bool:
        """
        파일이 없으면 .sample파일을 복사하고 true를 반환한다.
        파일이 있으면 false를 반환한다.
        """
        if os.path.isfile(fullPath) is False:
            dirPath = os.path.dirname(fullPath)
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            sampleFile = os.path.join('.', os.path.basename(fullPath))
            if isSample:
                sampleFile += ".sample"
            shutil.copyfile(sampleFile, fullPath)
            return True
        return False


    def installConfig(self)->None:
        if os.path.isdir(self.mySetting.configDirPath) is False:
            os.mkdir(self.mySetting.configDirPath)
        # setting.json
        if self.copyFileIfNotExist(self.mySetting.settingPath):
            print("\n\ntorrent client 연결정보와 사이트 정보를 "+ self.mySetting.settingPath+"에 설정해주세요\n")
        self.mySetting.loadJson()

        # downloadRules 섹션에서 각 규칙을 처리합니다.
        for rule in self.mySetting.json['downloadRules']:
            listPath = os.path.join(self.mySetting.configDirPath, rule['list'])
            if self.copyFileIfNotExist(listPath):
                print(f"키워드는 {listPath}에 추가하세요.\n")

    def installTransmissionScript(self)->None:
        if os.path.isdir(self.mySetting.transmissionScriptDirPath) is False:
            os.mkdir(self.mySetting.transmissionScriptDirPath)
        if self.copyFileIfNotExist(self.mySetting.torrentDoneSHPath):
            osHelper.addXToUser(self.mySetting.torrentDoneSHPath)

if __name__ == '__main__':
    installer = ScraperInstaller()
    installer.installConfig()
    installer.installTransmissionScript()
    print("설치가 완료되었습니다.\n")
