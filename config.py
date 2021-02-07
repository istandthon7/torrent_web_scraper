import os
import time
import json
import os.path
from datetime import datetime as dtime
import csv

class setting(object):
    """description of class"""

    def __init__(self):
        self.version = 'v1.10'
        currentPath = os.path.realpath(os.path.dirname(__file__))
        self.CONFIG_PATH = currentPath + "/config/"
        
        self.SETTING_FILE_NAME_ONLY = "setting.json"
        self.SETTING_FILE_NAME = self.CONFIG_PATH + self.SETTING_FILE_NAME_ONLY
        self.TORRENT_HISTORY_FILE_NAME = self.CONFIG_PATH + "torrent_history.csv"
        self.MAIL_HISTORY_FILE_NAME = self.CONFIG_PATH + "mail_history.csv"
        self.runTime = dtime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.TRANSMISSION_SCRIPT_PATH = currentPath + "/transmission_script/"
        self.TORRENT_DONE_SH = "torrent_done.sh"
        self.RENAME_SEASON_TRANSMISSION_PY = "rename_season_transmission.py"
        self.SCRAPERLIBRARY_PY = "scraperLibrary.py"

    def loadJson(self):

        try:
            dataFile = open(self.SETTING_FILE_NAME, 'r', encoding='utf-8')
        except FileNotFoundError as e:
            print(f"설정파일({self.SETTING_FILE})이 없습니다. ./install.sh 를 실행한 후 변경사항을 적용하세요.")
            print(str(e))
            sys.exit()
        else:
            self.json = json.load(dataFile)
            dataFile.close()

    def saveJson(self):
        with open(self.SETTING_FILE_NAME, 'w', encoding='utf-8') as dataFile:
            json.dump(self.json, dataFile, sort_keys = True, ensure_ascii=False, indent = 4)

class TVShow:
  def __init__(self, setting ):
    self.fileName = setting.CONFIG_PATH + setting.json["program-list"]
    with open(self.fileName,"r", encoding='utf-8') as jsonFile:
      self.json = json.load(jsonFile)

  def checkTitleInTVShow(self, boardTitle):

    boardTitle = boardTitle.lower()

    for prog in self.json['title_list']:
        title = prog['name']
        resolution = prog['option']
        release = prog['option2']

        if not checkTitleWithTitle(title, boardTitle):
            continue

        if not checkResolutionWithTitle(resolution, boardTitle):
            continue

        if not checkVersionWithTitle(release, boardTitle):
            continue

        return title

    return False

class Moive:
    def __init__(self, setting):
        self.fileName = setting.CONFIG_PATH + setting.json["movie"]['list']
        self.movieSetting = setting.json['movie']

    def checkTitleWithMovieFile(self, boardTitle):
        year = dtime.now().strftime("%Y")
        movieFile = open(self.fileName, "r", encoding="utf-8")
        boardTitle = boardTitle.lower()
        lines = movieFile.readlines()

        for line in lines:
            title = line.replace("\n", "")
            title_array = title.split(":")

            if not checkTitleWithTitle(title_array[0], boardTitle):
                continue

            if len(title_array) > 1 and not checkTitleWithTitle(title_array[1], boardTitle):
                continue

            # json에서 불러와서 배열이 아니라서 checkTitleWithTitle 사용
            if not checkTitleWithTitle(self.movieSetting['resolution'], boardTitle):
                continue

            # 위의 이유가 같음.
            if not checkTitleWithTitle(self.movieSetting['video_codec'], boardTitle):
                continue

            if not year in boardTitle:
                continue

            movieFile.close()
            return title

        movieFile.close()
        return False

    #movie_list에서 삭제하기
    def removeLineInMovie(self, matchedName):
        movieFile = open(self.fileName, "r", encoding="utf-8")
        buffer = ""

        for line in movieFile.readlines():

            if not matchedName in line:
                buffer += line
            else:
                # 영화리스트 파일에 매치되어 파일에 기록하지 않으니 다운받았다는 메시지다.
                # 영화는 자주 다운로드 하지 않으니 일단 로그 놔두고, 메일 받는 것으로 하자.
                print(f"info, remove in movie_list, matchedName = {matchedName}, line = {line}")
        movieFile.close()

        movieFile = open(self.fileName, "w", encoding="utf-8")
        movieFile.write(buffer)
        movieFile.close()



def checkMailNotiHistory(csvFile, title):
    if not os.path.isfile(csvFile):
        return False

    with open(csvFile, 'r', encoding="utf-8") as f:
        ff = csv.reader(f)
        for row in ff:
            if title == row[2]:
                #print("\t\t-> magnet was already downloaded at
                #web_scraper_history.csv")
                return True
    return False

def addMailNotiToFile(csvFile, runtime, sitename, title, keyword):

    new = [runtime, sitename, title, keyword]
    with open(csvFile, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(new)
    f.close()
    return



def checkMagnetHistory(csvFile, magnet):

    if not os.path.isfile(csvFile):
        return False

    with open(csvFile, 'r', encoding="utf-8") as f:
        ff = csv.reader(f)
        for row in ff:
            if magnet == row[3]:
                return True
    return False

def addMagnetInfoToFile(setting, sitename, title, magnet, keyword):
    csvFile = setting.TORRENT_HISTORY_FILE_NAME
    runtime = setting.runTime
    new = [runtime, sitename, title, magnet, keyword]
    with open(csvFile, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(new)
    f.close()
    return



def checkTitleWithTitle(title, boardTitle):

    keyArray = title.lower().split()
    for tmp in keyArray:
        if not tmp in boardTitle:
            return False
    return True

def checkResolutionWithTitle(resolution, boardTitle):

    if resolution == "":
        return True
    if resolution.lower() in boardTitle:
        return True
    return False

def checkVersionWithTitle(release, boardTitle):

    if release == "":
        return True

    if release.lower() in boardTitle:
        return True
    return False



