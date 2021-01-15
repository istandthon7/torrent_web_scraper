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

def getBsObj(addr):
    req = Request(addr, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"})
    c = ssl._create_unverified_context()
    time.sleep(1)
    html = urlopen(req, context=c).read().decode('utf-8','replace')
    data = BeautifulSoup(html, "html.parser")
    return data

def checkUrl(addr):
    try:
        getBsObj(addr)
    except Exception as e:
        print(f"Exception access url : {e}")
        print(f"We can not scrap {addr} , something wrong.\n")
        return False

    return True

def getCateList():
    return categoryList

def getCateIdxFromStr(string):
    return categoryList.index(string)

# targetString: 게시판 제목
def checkTitleWithTitle(title, targetString):
    keyArray = title.lower().split()
    for tmp in keyArray:
        if not tmp in targetString:
            return False
    return True

def checkResolutionWithTitle(resolution, targetString):
  if resolution == "":
    return True
  if resolution.lower() in targetString:
    return True
  return False

def checkVersionWithTitle(release, targetString):
  if release == "":
    return True
  if release.lower() in targetString:
    #print("checkVersionWithTitle, return True, release: "+release+",
    #targetString: "+targetString)
    return True
  #print("checkVersionWithTitle, return False, release: "+release+",
  #targetString: "+targetString)
  return False

def checkTitleWithProgramList(targetString, program_list_file_name):
    targetString = targetString.lower()

    programs = Programs(program_list_file_name)

    for prog in programs.data['title_list']:
        title = prog['name']
        resolution = prog['option']
        release = prog['option2']
        #print(title, resolution, release, targetString)

        if not checkTitleWithTitle(title, targetString):
            #print("checkTitleWithTitle")
            continue
        if not checkResolutionWithTitle(resolution, targetString):
            #print("checkResolutionWithTitle")
            continue
        if not checkVersionWithTitle(release, targetString):
            #print("checkVersionWithTitle")
            continue
        return title
    return False



def check_magnet_history(csv_file, magnet):
    if not os.path.isfile(csv_file):
        return False

    with open(csv_file, 'r', encoding="utf-8") as f:
        ff = csv.reader(f)
        for row in ff:
            if magnet == row[3]:
                #print("\t\t-> magnet was already downloaded at
                #web_scraper_history.csv")
                return True
    return False

def add_magnet_info_to_file(csv_file, runtime, sitename, title, magnet, keyword):

    new = [runtime, sitename, title, magnet, keyword]
    with open(csv_file, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(new)
    f.close()
    return

def check_mail_noti_history(csv_file, title):
    if not os.path.isfile(csv_file):
        return False

    with open(csv_file, 'r', encoding="utf-8") as f:
        ff = csv.reader(f)
        for row in ff:
            if title == row[2]:
                #print("\t\t-> magnet was already downloaded at
                #web_scraper_history.csv")
                return True
    return False

def add_mail_noti_to_file(csv_file, runtime, sitename, title, keyword):

    new = [runtime, sitename, title, keyword]
    with open(csv_file, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(new)
    f.close()
    return

#X-Transmission-Session-Id
def get_session_id_torrent_rpc(JD):

    url = "http://%s:%s@%s:%s/transmission/rpc" % (JD.get('trans-id'), JD.get('trans-pw'), JD.get('trans-host'), JD.get('trans-port'))
    try:
        res = requests.get(url)
        bs = BeautifulSoup(res.text, "html.parser")
        #print("info, get_session_id_torrent_rpc bs = %s" % bs)
        code_text = bs.find('code').text
        #print("info, get_session_id_torrent_rpc code_text =" , code_text)
        #X-Transmission-Session-Id:
        #YeUFW7rotzuLHrx4TfmWCRUF6qVlPd9DcPCEUHzlBcFMXZUd
        array = code_text.split()
        if len(array) == 2 and array[0] == "X-Transmission-Session-Id:":
          session_id = { array[0].replace(":", "") : array[1]}
          return session_id

    except requests.exceptions.ConnectionError:
        print("transmission이 실행중인 아닌 것으로 보입니다. " + url)
    #print("info, get_session_id_torrent_rpc response = ", res)

    
    return

def add_magnet_transmission_remote(magnet_addr, JD, download_dir, session_id):

    payload = {
		"arguments":{
			"filename": magnet_addr
		},
		"method": "torrent-add"
    }

    if len(download_dir) > 0:
        payload["arguments"]["download-dir"] = download_dir

    res = rpc(JD, payload, session_id)

    return

def get_id_transmission_remote(JD, session_id, torrent_title):
    payload = {
		"arguments":{
			"fields": ["id", "name"]
		},
		"method": "torrent-get"
    }

    res = rpc(JD, payload, session_id)
    #print("info, get_id_transmission_remote res\n", res)
    for torrent in res["arguments"]["torrents"]:
        if torrent["name"] == torrent_title:
            return torrent["id"]

    return

def get_files_torrent_remote(JD, session_id, torrent_id):

    payload = {
		"arguments":{
			"fields": ["id", "name", "files"]
		},
		"method": "torrent-get"
    }

    res = rpc(JD, payload, session_id)

    for torrent in res["arguments"]["torrents"]:
        if torrent["id"] == torrent_id:
            return torrent["files"]

    return

def rename_file_torrent_prc(JD, torrent_id, session_id, src_file, dest_file):

    json_input = {
        "method": "torrent-rename-path"
    }
    json_input["arguments"] = {"ids": [int(torrent_id)], "path": src_file, "name": dest_file}

    res = rpc(JD, json_input, session_id)

    return

# 상태가 Finished 이고 contain_name 인 토렌트 id를 구해서 삭제 (리스트에 남아있지 않도록 자동삭제되도록 하는
# 기능이다.)
def remove_transmission_remote(JD, session_id, contain_name):

    payload = {
        "arguments":{
            "fields": ["id", "name", "isFinished"]
            },
        "method": "torrent-get"
    }

    res = rpc(JD, payload, session_id)

    for torrent in res["arguments"]["torrents"]:
        if contain_name in torrent["name"] and torrent["isFinished"]:
            payload = {
                "method": "torrent-remove",
                "arguments":{"ids":[torrent["id"]]}
                }
            res = rpc(JD, payload, session_id)

    return

def rpc(JD, payload, session_id):
    url = "http://%s:%s@%s:%s/transmission/rpc" % (JD.get('trans-id'), JD.get('trans-pw'), JD.get('trans-host'), JD.get('trans-port'))
    headers = {'content-type': 'application/json'}
    headers.update(session_id)
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

        if check_mail_noti_history(mailNotiHistoryFileName, boardTitle):
            return

        if keyword in boardTitle:
            cmd = mailNotiSetting["cmd"]
            cmd = cmd.replace("$board_title", boardTitle)
            cmd = cmd.replace("$address",email)
            subprocess.call(cmd, shell=True)
            add_mail_noti_to_file(mailNotiHistoryFileName, runTime
                                  , siteName, boardTitle, keyword)

class MoiveScraper:
    def __init__(self, movieSetting):
        self.movieSetting = movieSetting

    def checkTitleWithMovieList(self, boardTitle, year):

        movieListFile = open(self.movieSetting['list'], "r", encoding="utf-8")
        boardTitle = boardTitle.lower()
        lines = movieListFile.readlines()

        #print("info, checkTitleWithMovieList targetString = %s, video_codec=
        #%s, resolution = %s, year = %s" % (targetString, video_codec,
        #resolution, year) )
        #sys.exit()

        for line in lines:
            title = line.replace("\n", "")
            title_array = title.split(":")
            #print(titles)

            if not checkTitleWithTitle(title_array[0], boardTitle):
                #print("checkTitleWithTitle")
                continue

            if len(title_array) > 1 and not checkTitleWithTitle(title_array[1], boardTitle):
                #print("checkTitleWithTitle2")
                continue

            # json에서 불러와서 배열이 아니라서 checkTitleWithTitle 사용
            if not checkTitleWithTitle(self.movieSetting['resolution'], boardTitle):
                #print("checkResolutionWithTitle")
                continue

            # 위의 이유가 같음.
            if not checkTitleWithTitle(self.movieSetting['video_codec'], boardTitle):
                #print("checkVersionWithTitle")
                continue

            if not year in boardTitle:
                continue

            #print("info, checkTitleWithMovieList title = ", title)
            #sys.exit()
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

def SaveJson(settingfileName, data):
    with open(settingfileName, 'w', encoding='utf-8') as dataFile:
        json.dump(data, dataFile, sort_keys = True, ensure_ascii=False, indent = 4)

class Programs:
  def __init__(self, program_list_file_name):

    with open(os.path.realpath(os.path.dirname(__file__)) + "/" + program_list_file_name,"r", encoding='utf-8') as json_file:
      self.data = json.load(json_file)

