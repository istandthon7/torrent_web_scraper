import abc
import argparse
import base64
import json
import logging
import sys
from typing import Dict, List, Optional

import requests

import setting
import tvshow


class TorrentClient(abc.ABC):
    @abc.abstractmethod
    def addTorrent(self, magnetLink: str, downloadDir: Optional[str] = None) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def deleteOlderEpisodes(self, regKeyword: str, episode: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def getAllTorrents(self) -> List[Dict]:
        raise NotImplementedError

# https://github.com/transmission/transmission/blob/main/docs/rpc-spec.md
class TransmissionClient(TorrentClient):
    def __init__(self, transmissionSetting: Dict[str, str], pw: str):
        self.statusCode = -1
        self.transmissionSetting = transmissionSetting
        self.url = self.getRpcUrl()
        if len(self.transmissionSetting['id']) > 0:
            # 사용자 이름과 비밀번호를 콜론으로 구분하여 문자열을 만듭니다.
            credentials = f"{self.transmissionSetting['id']}:{pw}"

            # 문자열을 base64로 인코딩합니다.
            b64_credentials = base64.b64encode(credentials.encode()).decode()

            # 인증 헤더를 만듭니다.
            self.headers = {
                'Authorization': f'Basic {b64_credentials}'
            }
        sessionId = self.getRpcSessionId()
        
        self.headers['X-Transmission-Session-Id'] = sessionId
        self.headers['Content-Type'] = 'application/json'

    def getRpcUrl(self) -> str:
        url = "http"
        if self.transmissionSetting['port'] == 443:
            url += "s"
        url += "://"
        url += self.transmissionSetting['host'] + ":" + str(self.transmissionSetting['port']) + "/transmission/rpc"
        return url

    def getRpcSessionId(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            self.statusCode = response.status_code
            if response.status_code == 409:
                return response.headers['X-Transmission-Session-Id']
            else:
                logging.error(f'HTTP error occurred: {err}')
                print(f'Error: {err}', file=sys.stderr)
        except Exception as e:
            logging.critical(f'Transmission 세션아이디를 구하지 못했습니다. {self.url}', exc_info=True)
            print(f'Error: {e}', file=sys.stderr)
        else:
            self.statusCode = response.status_code
            return response.headers.get('X-Transmission-Session-Id')

    def addTorrent(self, magnetLink: str, downloadDir: Optional[str] = None) -> int:
        payload = {
            "method": "torrent-add",
            "arguments":{
                "filename": magnetLink
            }
        }
        if downloadDir is not None and len(downloadDir) > 0:
            payload["arguments"]["download-dir"] = downloadDir
        argumentsJson = self.rpc(payload)

        # 토렌트 객체를 가져옵니다.
        torrent = argumentsJson.get('torrent-added') or argumentsJson.get('torrent-duplicate')

        if torrent:
            # 토렌트 객체의 id, name, hashString 필드를 확인합니다.
            id = torrent.get('id')
            name = torrent.get('name')
            hashString = torrent.get('hashString')

            if id and name and hashString:
                logging.info(f"토렌트가 성공적으로 추가되었습니다: {name} ({id}, {hashString})")
            else:
                logging.info("토렌트가 추가되었지만, 일부 정보가 누락되었습니다.")
            return self.statusCode
        logging.error(f"(트랜스미션)토렌트 추가에 실패하였습니다. {magnetLink}")
        return self.statusCode

    def deleteOlderEpisodes(self, regKeyword: str, episode: int) -> None:
        """ 상태가 Finished 이고 regKeyword 인 토렌트 id를 구해서 삭제 (리스트에 남아있지 않도록 자동삭제되도록 하는
        기능이다.) """
        if episode is None:
            return
        torrents = self.getAllTorrents()
        for torrent in torrents:
            myTvShow = tvshow.TVShow()
            episodeNumber = myTvShow.getEpisodeNumber(torrent["name"])
            if regKeyword in torrent["name"] and torrent["isFinished"] and episodeNumber < episode:
                self.deleteTorrent(torrent["id"])
                logging.info(f'(트랜스미션)tvshow 이전 에피소드를 리스트에서 삭제했습니다. {torrent["name"]}')

    def deleteTorrent(self, torrentId: int) -> int:
        payload = {
            "method": "torrent-remove",
            "arguments":{
                "ids": [torrentId]
            }
        }
        self.rpc(payload)
        return self.statusCode

    def getAllTorrents(self) -> List[Dict]:
        payload = {
            "method": "torrent-get",
            "arguments":{
                "fields": ["id", "name", "isFinished"]
            }
        }
        return self.rpc(payload)["torrents"]
    
    def rpc(self, payload: dict) -> Dict:
        if self.headers['X-Transmission-Session-Id'] == None:
            return {"arguments":{}}
        response = requests.post(f"{self.url}", headers=self.headers, data=json.dumps(payload))
        self.statusCode = response.status_code
        resJson = response.json()
        if resJson['result'] != 'success':
            logging.error(f"트랜스미션 RPC통신 결과가 성공이 아니예요. {resJson['result']}")
        return resJson['arguments']


class QBittorrentClient(TorrentClient):
    def __init__(self, qbittorrentSetting: Dict[str, str], pw: str):
        self.cookies = None
        self.qbittorrentSetting = qbittorrentSetting
        self.url = self.getApiUrl()
        self.auth = (self.qbittorrentSetting['id'], pw)
        self.login(self.auth[0], self.auth[1])

    def __del__(self):
        try:
            if self.cookies == None:
                return
            response = requests.post(f"{self.url}/auth/logout", headers=self.headers, cookies=self.cookies)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f'로그아웃에 실패했습니다: {e}')
            print(f'Error: {e}', file=sys.stderr)

    def getApiUrl(self) -> str:
        url = "http"
        if self.qbittorrentSetting['port'] == 443:
            url += "s"
        url += "://"
        url += self.qbittorrentSetting['host'] + ":" + str(self.qbittorrentSetting['port']) 
        self.headers = {'Referer': url}
        url += "/api/v2"
        return url

    def login(self, id: str, pw: str) -> bool:
        try:
            data = {'username': id, 'password': pw}
            response = requests.post(f"{self.url}/auth/login", headers=self.headers, data=data)
            response.raise_for_status()
            # 로그인 요청의 응답으로 받은 쿠키를 저장합니다.
            self.cookies = response.cookies

            # SID가 쿠키에 포함되어 있는지 확인합니다.
            if 'SID' not in self.cookies:
                logging.critical(f'SID가 쿠키에 포함되어 있지 않습니다. id: [{id}]')
                print('Error: SID not in cookies', file=sys.stderr)
                return False

            return True
        except requests.exceptions.RequestException as e:
            logging.critical(f'QBittorrent 접속에 실패했습니다. id: [{id}], error: {e}')
            print(f'Error: {e}', file=sys.stderr)
            return False

    def addTorrent(self, magnetLink: str, downloadDir: Optional[str] = None) -> int:
        data = {'urls': magnetLink}
        if downloadDir is not None:
            data['savepath'] = downloadDir
        response = requests.post(f"{self.url}/torrents/add", auth=self.auth, headers=self.headers, data=data, cookies=self.cookies)
        return response.status_code

    def deleteOlderEpisodes(self, regKeyword: str, episode: int) -> None:
        """ 상태가 downloading 이고 regKeyword 인 토렌트 id를 구해서 삭제 (리스트에 남아있지 않도록 자동삭제되도록 하는
        기능이다.) """
        if episode is None:
            return
        torrents = self.getAllTorrents()
        for torrent in torrents:
            myTvShow = tvshow.TVShow()
            episodeNumber = myTvShow.getEpisodeNumber(torrent["name"])
            if regKeyword in torrent["name"] and torrent["progress"] == 1.0 and episodeNumber < episode:
                self.deleteTorrent(torrent["hash"])
                logging.info(f'(qBittorrent)tvshow 이전 에피소드를 리스트에서 삭제했습니다. {torrent["name"]}')

    def getAllTorrents(self) -> List[Dict]:
        response = requests.get(f"{self.url}/torrents/info", headers=self.headers, auth=self.auth, cookies=self.cookies)
        return response.json()

    def deleteTorrent(self, torrentHash: str) -> int:
        data = {'hashes': torrentHash, "deleteFiles": False}
        response = requests.post(f"{self.url}/torrents/delete", auth=self.auth, headers=self.headers, data=data, cookies=self.cookies)
        return response.status_code

def main():
    mySetting = setting.Setting()
    logging.debug(f'magnet 추가 시작.')
    parser = argparse.ArgumentParser()
    parser.add_argument("magnet", help="magnet")
    parser.add_argument("--downloadPath", help="다운로드 경로")
    parser.add_argument("--password", help="토렌트 클라이언트 접속 비밀번호")
    parser.add_argument("--clientType", choices=['transmission', 'qBittorrent'], default='transmission', help="클라이언트 타입")
    args = parser.parse_args()
    logging.debug(f'폴더: {args.downloadPath}')
    
    logging.info(f"magnet을 추가합니다. {args.magnet}, download: [{args.downloadPath}]")
    torrentClientSetting = mySetting.json["torrentClient"]
    if args.clientType == 'transmission':
        client = TransmissionClient(torrentClientSetting, args.password)
    elif args.clientType == 'qBittorrent':
        client = QBittorrentClient(torrentClientSetting, args.password)
    client.addTorrent(args.magnet, args.downloadPath)

if __name__ == '__main__':
    main()