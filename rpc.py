import argparse
import json
import logging
import requests
from bs4 import BeautifulSoup
import setting

#X-Transmission-Session-Id
def getSessionIdTransRpc(url:str):
    
    try:
        res = requests.get(url)
        if res.status_code != 409 and res.status_code > 400:
            logging.error(f"트랜스미션에 접속할 수 없어요. {res.status_code} {res.reason}")
            logging.debug(f"접속 url: {url}")
            return;
        bs = BeautifulSoup(res.text, "html.parser")
        code_text = bs.find('code').text
        # CSRF protection
        #X-Transmission-Session-Id:
        #YeUFW7rotzuLHrx4TfmWCRUF6qVlPd9DcPCEUHzlBcFMXZUd
        array = code_text.split()
        if len(array) == 2 and array[0] == "X-Transmission-Session-Id:":
            session_id = { array[0].replace(":", "") : array[1]}
            return session_id
    except requests.exceptions.ConnectionError:
        logging.error(f"transmission이 실행중인 아니거나 네트워크 등의 문제로 접속할 수 없어요.")
        logging.debug(f"접속 url: {url}")

def addMagnetTransmissionRemote(magnetAddr: str, url: str, downloadDir: str, sessionId)->None:
    payload = {
		"arguments":{
			"filename": magnetAddr
		},
		"method": "torrent-add"
    }

    if len(downloadDir) > 0:
        payload["arguments"]["download-dir"] = downloadDir
    rpc(url, payload, sessionId)

def getIdTransmissionRemote(url:str, sessionId, torrentTitle: str):
    payload = {
		"arguments":{
			"fields": ["id", "name"]
		},
		"method": "torrent-get"
    }

    res = rpc(url, payload, sessionId)
    #print("info, get_id_transmission_remote res\n", res)
    for torrent in res["arguments"]["torrents"]:
        if torrent["name"] == torrentTitle:
            return torrent["id"]

def getFilesTorrentRemote(url:str, sessionId, torrentId):
    payload = {
		"arguments":{
			"fields": ["id", "name", "files"]
		},
		"method": "torrent-get"
    }

    res = rpc(url, payload, sessionId)

    for torrent in res["arguments"]["torrents"]:
        if torrent["id"] == torrentId:
            return torrent["files"]

def renameFileTorrentRpc(url:str, torrentId, sessionId, srcFile: str, destFile: str)->None:
    json_input = {
        "method": "torrent-rename-path"
    }
    json_input["arguments"] = {"ids": [int(torrentId)], "path": srcFile, "name": destFile}

    rpc(url, json_input, sessionId)

def removeTransmissionRemote(url: str, sessionId, containName: str)->None:
    """ 상태가 Finished 이고 containName 인 토렌트 id를 구해서 삭제 (리스트에 남아있지 않도록 자동삭제되도록 하는
    기능이다.) """
    payload = {
        "arguments":{
            "fields": ["id", "name", "isFinished"]
        },
        "method": "torrent-get"
    }

    res = rpc(url, payload, sessionId)

    for torrent in res["arguments"]["torrents"]:
        if containName in torrent["name"] and torrent["isFinished"]:
            payload = {
                "method": "torrent-remove",
                "arguments":{"ids":[torrent["id"]]}
            }
            res = rpc(url, payload, sessionId)
            logging.info(f'tvshow 이전 에피소드를 Transmission에서 삭제했습니다. {torrent["name"]}')

def rpc(url:str, payload, sessionId):
    
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

def getDownloadDir(url:str)->str:
    payload = {
		"arguments":{
			"fields": ["download-dir"]
		},
		"method": "session-get"
    }

    res = rpc(url, payload, getSessionIdTransRpc(url))
    #print("info, get_id_transmission_remote res\n", res)
    return res["arguments"]["download-dir"]

def addMagnet(magnet: str, downloadPath: str, url: str):
    sessionId = getSessionIdTransRpc(url)
    addMagnetTransmissionRemote(magnet, url, downloadPath, sessionId)



if __name__ == '__main__':
    """매그넷으로 바로 다운받기"""
    parser = argparse.ArgumentParser()
    parser.add_argument("magnet", help="magnet")
    parser.add_argument("downloadPath", help="다운로드 경로")
    args = parser.parse_args()
    mySetting = setting.Setting()
    addMagnet(args.magnet, args.downloadPath, mySetting.getRpcUrl())