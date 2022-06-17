
# 스크래핑시 사용하는 함수들

from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import subprocess
import time
import subprocess
import csv
import random
import json
import os
import setting
import ssl

def getSoup(url: str):
    try:
        html = getHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        return soup
    except Exception as e:
        print("Exception getSoup url: "+url+" , error: " + str(e))


def getHtml(url: str):
    try:
        time.sleep(random.randrange(1,4))
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        # python 3.6이상에서
        context = ssl._create_unverified_context()
        # urlopen(request, context=context) as response
        return urlopen(request, context=context).read().decode('utf-8','replace')
    except Exception as e:
        print("Exception getHtml url: "+url+" , error: " + str(e))


def getSoupFromFile(filePath: str):
    try:
        soup = BeautifulSoup(open(filePath), "html.parser")
        return soup
    except Exception as e:
        print("Exception getSoupFromFile path: "+filePath+" , error: " + str(e))


def checkUrl(url: str)->bool:
    try:
        if getSoup(url) is None:
            return False
    except Exception:# as e:
        #print(f"Exception access url : {e}")
        #print(f"We can not scrap {url} , something wrong.\n")
        return False
    return True


#X-Transmission-Session-Id
def getSessionIdTorrentRpc(jsonOfSetting):
    url = getUrl(jsonOfSetting)
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

def addMagnetTransmissionRemote(magnetAddr: str, jsonOfSetting, downloadDir: str, sessionId)->None:
    payload = {
		"arguments":{
			"filename": magnetAddr
		},
		"method": "torrent-add"
    }

    if len(downloadDir) > 0:
        payload["arguments"]["download-dir"] = downloadDir
    rpc(jsonOfSetting, payload, sessionId)

def getIdTransmissionRemote(jsonOfSetting, sessionId, torrentTitle: str):
    payload = {
		"arguments":{
			"fields": ["id", "name"]
		},
		"method": "torrent-get"
    }

    res = rpc(jsonOfSetting, payload, sessionId)
    #print("info, get_id_transmission_remote res\n", res)
    for torrent in res["arguments"]["torrents"]:
        if torrent["name"] == torrentTitle:
            return torrent["id"]

def getFilesTorrentRemote(jsonOfSetting, sessionId, torrentId):
    payload = {
		"arguments":{
			"fields": ["id", "name", "files"]
		},
		"method": "torrent-get"
    }

    res = rpc(jsonOfSetting, payload, sessionId)

    for torrent in res["arguments"]["torrents"]:
        if torrent["id"] == torrentId:
            return torrent["files"]

def renameFileTorrentRpc(jsonOfSetting, torrentId, sessionId, srcFile: str, destFile: str)->None:
    json_input = {
        "method": "torrent-rename-path"
    }
    json_input["arguments"] = {"ids": [int(torrentId)], "path": srcFile, "name": destFile}

    rpc(jsonOfSetting, json_input, sessionId)

# 상태가 Finished 이고 contain_name 인 토렌트 id를 구해서 삭제 (리스트에 남아있지 않도록 자동삭제되도록 하는
# 기능이다.)
def removeTransmissionRemote(jsonOfSetting, sessionId, containName: str)->None:
    payload = {
        "arguments":{
            "fields": ["id", "name", "isFinished"]
        },
        "method": "torrent-get"
    }

    res = rpc(jsonOfSetting, payload, sessionId)

    for torrent in res["arguments"]["torrents"]:
        if containName in torrent["name"] and torrent["isFinished"]:
            payload = {
                "method": "torrent-remove",
                "arguments":{"ids":[torrent["id"]]}
            }
            res = rpc(jsonOfSetting, payload, sessionId)

def rpc(jsonOfSetting, payload, sessionId):
    url = getUrl(jsonOfSetting)
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

def getUrl(json)->str:
    transmissionSetting = json['transmission']
    url = "http://%s:%s@%s:%s/transmission/rpc" % (transmissionSetting['id'], transmissionSetting['pw']
                                                   , transmissionSetting['host'], transmissionSetting['port'])
    return url


def executeNotiScript(mySetting: setting.Setting, siteName: str, boardTitle: str)->bool:
    """
    스크립트를 실행했으면 true를 리턴하고
    이미 실행한 경우나 실행하지 못한 경우는 false를 리턴한다.
    """
    notiSetting = mySetting.json["notification"]

    if notiSetting == "":
        return False

    if notiSetting["cmd"] == "":
        return False

    for keyword in notiSetting["keywords"]:
        
        if keyword in boardTitle:
            if checkNotiHistory(mySetting.notiHistoryPath, boardTitle):
                return False
            cmd = notiSetting["cmd"]
            cmd = cmd.replace("$board_title", "["+siteName+"]" + boardTitle)
            try:
                subprocess.run(cmd, check=True)

            except Exception as e:
                print("executeNotiScript error, message: "+str(e))
                return False
            else:
                addNotiHistory(mySetting.notiHistoryPath, mySetting.runTime
                                  , siteName, boardTitle, keyword)
                return True


def checkNotiHistory(csvFile: str, title: str)->bool:
        if os.path.isfile(csvFile) is False:
            return False

        with open(csvFile, 'r', encoding="utf-8") as f:
            ff = csv.reader(f)
            for row in ff:
                if title == row[2]:
                    #print("\t\t-> magnet was already downloaded at
                    #web_scraper_history.csv")
                    return True
        return False


def addNotiHistory(csvFile: str, runtime: str, sitename: str, title: str, keyword: str)->None:
    new = [runtime, sitename, title, keyword]
    with open(csvFile, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(new)
    f.close()