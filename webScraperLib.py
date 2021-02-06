#!/usr/bin/env python3
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import subprocess
import csv
import sys
import re
import json
import os.path
from pathlib import Path
import ssl
import time
import subprocess

def getBsObj(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    #c = ssl._create_unverified_context()
    time.sleep(3)
    try:
        html = urlopen(req).read().decode('utf-8','replace')
        data = BeautifulSoup(html, "html.parser")
        return data
    except Exception as e:
        print(f"Exception getBsObj url: {url}, error: {e}")

def checkUrl(url):
    try:
        if getBsObj(url) == None:
            return False
    except Exception as e:
        #print(f"Exception access url : {e}")
        #print(f"We can not scrap {url} , something wrong.\n")
        return False

    return True

def updateUrl(url):
    return re.sub("([\d]+)[\.]", lambda m: str(int(m.group(1))+1), url)

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

def checkTitleWithProgramList(boardTitle, programListFileName):

    boardTitle = boardTitle.lower()

    programs = Programs(programListFileName)

    for prog in programs.data['title_list']:
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

def checkMagnetHistory(csvFile, magnet):

    if not os.path.isfile(csvFile):
        return False

    with open(csvFile, 'r', encoding="utf-8") as f:
        ff = csv.reader(f)
        for row in ff:
            if magnet == row[3]:
                return True
    return False

def addMagnetInfoToFile(csvFile, runtime, sitename, title, magnet, keyword):

    new = [runtime, sitename, title, magnet, keyword]
    with open(csvFile, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(new)
    f.close()
    return

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

#X-Transmission-Session-Id
def getSessionIdTorrentRpc(setttings):

    url = "http://%s:%s@%s:%s/transmission/rpc" % (setttings['trans-id'], setttings['trans-pw']
                                                   , setttings['trans-host'], setttings['trans-port'])
    try:
        res = requests.get(url)
        bs = BeautifulSoup(res.text, "html.parser")
        code_text = bs.find('code').text
        #X-Transmission-Session-Id:
        #YeUFW7rotzuLHrx4TfmWCRUF6qVlPd9DcPCEUHzlBcFMXZUd
        array = code_text.split()
        if len(array) == 2 and array[0] == "X-Transmission-Session-Id:":
          session_id = { array[0].replace(":", "") : array[1]}
          return session_id

    except requests.exceptions.ConnectionError:
        print("transmission이 실행중인 아닌 것으로 보입니다. " + url)

    return

def addMagnetTransmissionRemote(magnetAddr, settings, downloadDir, sessionId):

    payload = {
		"arguments":{
			"filename": magnetAddr
		},
		"method": "torrent-add"
    }

    if len(downloadDir) > 0:
        payload["arguments"]["download-dir"] = downloadDir

    res = rpc(settings, payload, sessionId)

    return

def getIdTransmissionRemote(settings, sessionId, torrentTitle):
    payload = {
		"arguments":{
			"fields": ["id", "name"]
		},
		"method": "torrent-get"
    }

    res = rpc(settings, payload, sessionId)
    #print("info, get_id_transmission_remote res\n", res)
    for torrent in res["arguments"]["torrents"]:
        if torrent["name"] == torrentTitle:
            return torrent["id"]

    return

def getFilesTorrentRemote(settings, sessionId, torrentId):

    payload = {
		"arguments":{
			"fields": ["id", "name", "files"]
		},
		"method": "torrent-get"
    }

    res = rpc(settings, payload, sessionId)

    for torrent in res["arguments"]["torrents"]:
        if torrent["id"] == torrentId:
            return torrent["files"]

    return

def renameFileTorrentRpc(settings, torrentId, sessionId, srcFile, destFile):

    json_input = {
        "method": "torrent-rename-path"
    }
    json_input["arguments"] = {"ids": [int(torrentId)], "path": srcFile, "name": destFile}

    res = rpc(settings, json_input, sessionId)

    return

# 상태가 Finished 이고 contain_name 인 토렌트 id를 구해서 삭제 (리스트에 남아있지 않도록 자동삭제되도록 하는
# 기능이다.)
def removeTransmissionRemote(settings, sessionId, containName):

    payload = {
        "arguments":{
            "fields": ["id", "name", "isFinished"]
            },
        "method": "torrent-get"
    }

    res = rpc(settings, payload, sessionId)

    for torrent in res["arguments"]["torrents"]:
        if containName in torrent["name"] and torrent["isFinished"]:
            payload = {
                "method": "torrent-remove",
                "arguments":{"ids":[torrent["id"]]}
                }
            res = rpc(settings, payload, sessionId)

    return

def rpc(settings, payload, sessionId):
    url = "http://%s:%s@%s:%s/transmission/rpc" % (settings['trans-id'], settings['trans-pw']
                                                   , settings['trans-host'], settings['trans-port'])
    headers = {'content-type': 'application/json'}
    headers.update(sessionId)
    #print("info, rpc header = ", headers)

    #print("info, rpc payload = \n", json.dumps(payload, indent=4))
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()

    #print("info, rpc resonse =", response.text)

    #print("info, rpc response = \n", json.dumps(response, indent=4))
    if response["result"] != "success":
        print("error입니다. rpc response = \n", json.dumps(response, indent=4))
    #assert response["jsonrpc"]
    #assert response["id"] == 0

    return response

def create(path):
    p = Path(path)
    if p.is_file() == False:
      f = open(path, "w+")
      f.close()
      return True
    return False

def notiEmail(mailNotiSetting, mailNotiHistoryFileName, siteName, boardTitle, runTime):

    if mailNotiSetting == "":
        return

    email = mailNotiSetting["address"]

    if email == "":
        return

    for keyword in mailNotiSetting["keywords"]:

        if checkMailNotiHistory(mailNotiHistoryFileName, boardTitle):
            return

        if keyword in boardTitle:
            cmd = mailNotiSetting["cmd"]
            cmd = cmd.replace("$board_title", "["+siteName+"]" + boardTitle)
            cmd = cmd.replace("$address",email)
            subprocess.call(cmd, shell=True)
            addMailNotiToFile(mailNotiHistoryFileName, runTime
                                  , siteName, boardTitle, keyword)

class MoiveScraper:
    def __init__(self, movieSetting):
        self.movieSetting = movieSetting

    def checkTitleWithMovieList(self, boardTitle, year):

        movieListFile = open(self.movieSetting['list'], "r", encoding="utf-8")
        boardTitle = boardTitle.lower()
        lines = movieListFile.readlines()

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

            movieListFile.close()
            return title

        movieListFile.close()
        return False

    #movie_list에서 삭제하기
    def removeLineFromMovieListFile(self, matchedName):
        movieListFile = open(self.movieSetting['list'], "r", encoding="utf-8")
        buffer = ""

        for line in movieListFile.readlines():

            if not matchedName in line:
                buffer += line
            else:
                # 영화리스트 파일에 매치되어 파일에 기록하지 않으니 다운받았다는 메시지다.
                # 영화는 자주 다운로드 하지 않으니 일단 로그 놔두고, 메일 받는 것으로 하자.
                print(f"info, remove in movie_list, matchedName = {matchedName}, line = {line}")
        movieListFile.close()

        movieListFile = open(self.movieSetting['list'], "w", encoding="utf-8")
        movieListFile.write(buffer)
        movieListFile.close()


def loadJson(settingfileName):

    try:
        dataFile = open(settingfileName, 'r', encoding='utf-8')
    except FileNotFoundError as e:
        print(str(e))
        print(f"Please, set your file path.{settingfileName}")
        sys.exit()
    else:
        return json.load(dataFile)
        dataFile.close()

def saveJson(settingfileName, data):
    with open(settingfileName, 'w', encoding='utf-8') as dataFile:
        json.dump(data, dataFile, sort_keys = True, ensure_ascii=False, indent = 4)

class Programs:
  def __init__(self, programListFileName):

    with open(os.path.realpath(os.path.dirname(__file__)) + "/" + programListFileName,"r", encoding='utf-8') as json_file:
      self.data = json.load(json_file)

