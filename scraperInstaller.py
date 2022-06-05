#!/usr/bin/env python3
from fileinput import filename
import os
import shutil
import setting
import stat


def addUserX(path: str):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)

class ScraperInstaller:
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
            addUserX(fullPath)
            return True
        return False

if __name__ == '__main__':

    mySetting = setting.Setting()
    installer = ScraperInstaller()
    if os.path.isdir(mySetting.configDirPath) is False:
        os.mkdir(mySetting.configDirPath)
    # setting.json
    if installer.copyConfigIfNotExist(mySetting.settingPath):
        print("\n\ntransmission 연결정보를 "+mySetting.settingPath+"에 설정해주세요\n")
    mySetting.loadJson()

    # Movie.txt
    movieListPath = mySetting.configDirPath + mySetting.json['movie']['list']
    if installer.copyConfigIfNotExist(movieListPath):
        print("다운로드할 영화를 "+movieListPath+"에 추가하세요.\n")
    # TvShow.json
    tvShowListPath = mySetting.configDirPath + mySetting.json["tvshow"]["list"]
    if installer.copyConfigIfNotExist(tvShowListPath) :
        print("다운로드할 tv프로그램을 "+tvShowListPath+"에 추가하세요.\n")
    # 시즌 rename: 기본적으로 폴더명이 tvshow일 경우에 작동함
    if os.path.isdir(mySetting.transmissionScriptDirPath) is False:
        os.mkdir(mySetting.transmissionScriptDirPath)
    if installer.copyConfigIfNotExist(mySetting.torrentDoneSHPath):
        addUserX(mySetting.torrentDoneSHPath)
    installer.copyPythonFileIfNotExist(mySetting.renameSeasonTransmissionPYPath)
    installer.copyPythonFileIfNotExist(mySetting.scraperLibraryPYPath)
    installer.copyPythonFileIfNotExist(mySetting.configHelperPYPath)
    print("설치가 완료되었습니다.\n")


