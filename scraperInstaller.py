#!/usr/bin/python3
import os
import shutil
import setting
import osHelper

class ScraperInstaller:

    mySetting = setting.Setting()

    def copyConfigIfNotExist(self, fullPath: str) -> bool:
        """
        파일이 없으면 .sample파일을 복사하고 true를 반환한다.
        파일이 있으면 false를 반환한다.
        """
        if os.path.isfile(fullPath) is False:
            shutil.copyfile("./"+os.path.basename(fullPath)+".sample", fullPath)
            return True
        return False

    def copyPythonFileIfNotExist(self, fullPath: str) -> bool:
        """
        파일이 없으면 복사하고 true를 반환한다.
        파일이 있으면 false를 반환한다.
        """
        if os.path.isfile(fullPath) is False:
            shutil.copyfile("./"+os.path.basename(fullPath), fullPath)
            osHelper.addXToUser(fullPath)
            return True
        return False

    def installConfig(self)->None:
        
        if os.path.isdir(self.mySetting.configDirPath) is False:
            os.mkdir(self.mySetting.configDirPath)
        # setting.json
        if self.copyConfigIfNotExist(self.mySetting.settingPath):
            print("\n\ntransmission 연결정보를 "+ self.mySetting.settingPath+"에 설정해주세요\n")
        self.mySetting.loadJson()

        # Movie.txt
        movieListPath = self.mySetting.configDirPath + self.mySetting.json['movie']['list']
        if self.copyConfigIfNotExist(movieListPath):
            print("다운로드할 영화를 "+movieListPath+"에 추가하세요.\n")
        # TvShow.json
        tvShowListPath = self.mySetting.configDirPath + self.mySetting.json["tvshow"]["list"]
        if self.copyConfigIfNotExist(tvShowListPath) :
            print("다운로드할 tv프로그램을 "+tvShowListPath+"에 추가하세요.\n")

    def installTransmissionScript(self)->None:
        mySetting = setting.Setting()
        # 시즌 rename: 기본적으로 폴더명이 tvshow일 경우에 작동함
        if os.path.isdir(mySetting.transmissionScriptDirPath) is False:
            os.mkdir(mySetting.transmissionScriptDirPath)
        if self.copyConfigIfNotExist(mySetting.torrentDoneSHPath):
            osHelper.addXToUser(mySetting.torrentDoneSHPath)
        self.copyPythonFileIfNotExist(mySetting.renameSeasonTransmissionPYPath)
        self.copyPythonFileIfNotExist(mySetting.scraperLibraryPYPath)
        self.copyPythonFileIfNotExist(mySetting.settingPYPath)

if __name__ == '__main__':
    installer = ScraperInstaller()
    installer.installConfig()
    installer.installTransmissionScript()
    print("설치가 완료되었습니다.\n")


