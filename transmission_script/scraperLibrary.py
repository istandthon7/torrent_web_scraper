#!/usr/bin/env python3
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import subprocess

import sys
import re
import os.path
from pathlib import Path
import ssl
import time
import subprocess
import config
import random
import json

def getBsObj(url):

    try:
        time.sleep(random.randrange(1,4))
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        c = ssl._create_unverified_context()
        html = urlopen(req, context=c).read().decode('utf-8','replace')
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



#X-Transmission-Session-Id
def getSessionIdTorrentRpc(json):

    url = "http://%s:%s@%s:%s/transmission/rpc" % (json['trans-id'], json['trans-pw']
                                                   , json['trans-host'], json['trans-port'])
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

def addMagnetTransmissionRemote(magnetAddr, json, downloadDir, sessionId):

    payload = {
		"arguments":{
			"filename": magnetAddr
		},
		"method": "torrent-add"
    }

    if len(downloadDir) > 0:
        payload["arguments"]["download-dir"] = downloadDir

    res = rpc(json, payload, sessionId)

    return

def getIdTransmissionRemote(json, sessionId, torrentTitle):
    payload = {
		"arguments":{
			"fields": ["id", "name"]
		},
		"method": "torrent-get"
    }

    res = rpc(json, payload, sessionId)
    #print("info, get_id_transmission_remote res\n", res)
    for torrent in res["arguments"]["torrents"]:
        if torrent["name"] == torrentTitle:
            return torrent["id"]

    return

def getFilesTorrentRemote(json, sessionId, torrentId):

    payload = {
		"arguments":{
			"fields": ["id", "name", "files"]
		},
		"method": "torrent-get"
    }

    res = rpc(json, payload, sessionId)

    for torrent in res["arguments"]["torrents"]:
        if torrent["id"] == torrentId:
            return torrent["files"]

    return

def renameFileTorrentRpc(json, torrentId, sessionId, srcFile, destFile):

    json_input = {
        "method": "torrent-rename-path"
    }
    json_input["arguments"] = {"ids": [int(torrentId)], "path": srcFile, "name": destFile}

    res = rpc(json, json_input, sessionId)

    return

# 상태가 Finished 이고 contain_name 인 토렌트 id를 구해서 삭제 (리스트에 남아있지 않도록 자동삭제되도록 하는
# 기능이다.)
def removeTransmissionRemote(json, sessionId, containName):

    payload = {
        "arguments":{
            "fields": ["id", "name", "isFinished"]
            },
        "method": "torrent-get"
    }

    res = rpc(json, payload, sessionId)

    for torrent in res["arguments"]["torrents"]:
        if containName in torrent["name"] and torrent["isFinished"]:
            payload = {
                "method": "torrent-remove",
                "arguments":{"ids":[torrent["id"]]}
                }
            res = rpc(json, payload, sessionId)

    return

def rpc(js, payload, sessionId):
    url = "http://%s:%s@%s:%s/transmission/rpc" % (js['trans-id'], js['trans-pw']
                                                   , js['trans-host'], js['trans-port'])
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



def notiEmail(cfg, siteName, boardTitle):

    mailNotiSetting = cfg.json["mail-noti"]
    mailNotiHistoryFileName = cfg.MAIL_HISTORY_FILE_NAME
    runTime = cfg.runTime
    if mailNotiSetting == "":
        return

    email = mailNotiSetting["address"]

    if email == "":
        return

    for keyword in mailNotiSetting["keywords"]:

        if config.checkMailNotiHistory(mailNotiHistoryFileName, boardTitle):
            return

        if keyword in boardTitle:
            cmd = mailNotiSetting["cmd"]
            cmd = cmd.replace("$board_title", "["+siteName+"]" + boardTitle)
            cmd = cmd.replace("$address",email)
            subprocess.call(cmd, shell=True)
            config.addMailNotiToFile(mailNotiHistoryFileName, runTime
                                  , siteName, boardTitle, keyword)

