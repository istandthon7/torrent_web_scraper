#!/usr/bin/python3
import os
import shutil
import setting
import osHelper

class ScraperInstaller:

    mySetting = setting.Setting()

    def __init__(self, configDir: str = None) -> None:
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
            print("\n\ntransmission 연결정보를 "+ self.mySetting.settingPath+"에 설정해주세요\n")
        self.mySetting.loadJson()

        # Movie.json
        movieListPath = os.path.join(self.mySetting.configDirPath, self.mySetting.json['movie']['list'])
        if self.copyFileIfNotExist(movieListPath):
            print("다운로드할 영화를 "+movieListPath+"에 추가하세요.\n")
        # TvShow.json
        tvShowListPath = os.path.join(self.mySetting.configDirPath, self.mySetting.json["tvshow"]["list"])
        if self.copyFileIfNotExist(tvShowListPath) :
            print("다운로드할 tv프로그램을 "+tvShowListPath+"에 추가하세요.\n")

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
