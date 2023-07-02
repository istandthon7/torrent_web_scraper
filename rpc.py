import argparse
import imp
import json
import logging
import requests
from bs4 import BeautifulSoup
import setting
import tvshow
#from requests.auth import HTTPBasicAuth

# https://github.com/transmission/transmission/blob/main/docs/rpc-spec.md

def getSessionIdTransRpc(url:str):
    """
    :param url: The URL of the Transmission RPC.('http://localhost:9091/transmission/rpc')
    """
    try:
        #basic = HTTPBasicAuth(id, pw)
        res = requests.get(url)#, auth=basic)
        if res.status_code != 409 and res.status_code > 400:
            logging.error(f"트랜스미션에 접속할 수 없어요. {res.status_code} {res.reason}")
            logging.debug(f"접속 url: {url}")
            return;
        bs = BeautifulSoup(res.text, "html.parser")
        # CSRF protection
        # <code>X-Transmission-Session-Id: pI8na8XboVoe04bDOo1F0bVE5t89al766MJd3eWXa59kLYKp</code>
        code_text = bs.find('code').text
        array = code_text.split()
        logging.debug(f"array: {array}")
        if len(array) == 2 and array[0] == "X-Transmission-Session-Id:":
            return array[1]
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

    if downloadDir is not None and len(downloadDir) > 0:
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
        "method": "torrent-rename-path",
        "arguments": {
            "ids": [int(torrentId)],
            "path": srcFile,
            "name": destFile
        }
    }

    rpc(url, json_input, sessionId)

def removeTransmissionRemote(url: str, sessionId, regKeyword: str, episode: int)->None:
    """ 상태가 Finished 이고 containName 인 토렌트 id를 구해서 삭제 (리스트에 남아있지 않도록 자동삭제되도록 하는
    기능이다.) """
    if episode is None:
            return
    payload = {
        "arguments":{
            "fields": ["id", "name", "isFinished"]
        },
        "method": "torrent-get"
    }

    res = rpc(url, payload, sessionId)

    for torrent in res["arguments"]["torrents"]:
        myTvShow = tvshow.TVShow()
        episodeNumber = myTvShow.getEpisodeNumber(torrent["name"])
        if regKeyword in torrent["name"] and torrent["isFinished"] and episodeNumber<episode:
            payload = {
                "method": "torrent-remove",
                "arguments":{"ids":[torrent["id"]]}
            }
            res = rpc(url, payload, sessionId)
            logging.info(f'tvshow 이전 에피소드를 Transmission에서 삭제했습니다. {torrent["name"]}')

def rpc(url:str, payload: dict, sessionId: str):
    """지정된 URL에 RPC 호출을 합니다.

    Args:
        url: RPC 서비스의 URL입니다.
        payload: RPC 호출의 페이로드입니다.
        sessionId: RPC 호출의 세션 ID입니다.

    return: result json

    """
    headers = {
        'content-type': 'application/json',
        'X-Transmission-Session-Id': sessionId,
    }

    jsonObject = requests.post(url, data=json.dumps(payload), headers=headers).json()

    if jsonObject["result"] != "success":
        logging.error(f"error입니다. rpc response ==>\n{json.dumps(jsonObject, indent=4)}")
    logging.debug(f"rpc payload==> \n{json.dumps(payload, indent=4)}")
    logging.debug(f"rpc result==> \n{json.dumps(jsonObject, indent=4)}")
    return jsonObject

def getDownloadDir(url:str)->str:
    payload = {
		"arguments":{
			"fields": ["download-dir"]
		},
		"method": "session-get"
    }
    res = rpc(url, payload, getSessionIdTransRpc(url))
    downloadDir = res["arguments"]["download-dir"]
    logging.debug(f"다운로드 디렉토리를 구했어요.{downloadDir}")
    return downloadDir


def main():
    mySetting = setting.Setting()
    logging.debug(f'magnet 추가 시작.')
    parser = argparse.ArgumentParser()
    parser.add_argument("magnet", help="magnet")
    parser.add_argument("--downloadPath", help="다운로드 경로")
    parser.add_argument("--transPass", help="트랜스미션 접속 비밀번호")
    args = parser.parse_args()
    logging.debug(f'폴더: {args.downloadPath}')
    
    mySetting.transPass = args.transPass
    logging.info(f"magnet을 추가합니다. {args.magnet}, download: [{args.downloadPath}]")
    url = mySetting.getRpcUrl()
    addMagnetTransmissionRemote(args.magnet, url, args.downloadPath, getSessionIdTransRpc(url))

if __name__ == '__main__':
    main()