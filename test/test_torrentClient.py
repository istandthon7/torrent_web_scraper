import logging
import unittest
from unittest.mock import MagicMock, patch

import requests

import setting
import torrentClient


class TorrentClientTest(unittest.TestCase):
    @patch('requests.get')
    def test_sessionID(self, mock_get):
        # 가짜 응답을 설정합니다.
        mock_response = mock_get.return_value
        mock_response.status_code = 409
        mock_response.headers = {'X-Transmission-Session-Id': 'mock_session_id'}
        
        mySetting = setting.Setting()
        # 더미 호스트
        mySetting.json["torrentClient"]["host"] = "127.0.0.1"
        mySetting.json["torrentClient"]["id"] = "transmission"
        mySetting.json["torrentClient"]["port"] = 9091
        client = torrentClient.TransmissionClient(mySetting.json["torrentClient"], "dummyPassword")
        
        self.assertIsNotNone(client.headers['X-Transmission-Session-Id'])

    @patch('torrentClient.requests.get')
    def test_sessionIDOfConfigFile(self, mock_get):
        sessionId = "pI8na8XboVoe04bDOo1F0bVE5t89al766MJd3eWXa59kLYKp"
        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 409
        mock_response.headers = {'X-Transmission-Session-Id': sessionId}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        # specify the return value of the get() method
        mock_get.return_value = mock_response

        mySetting = setting.Setting()
        client = torrentClient.TransmissionClient(mySetting.json["torrentClient"], "dummyPassword")
        logging.debug(f'session id: {client.sessionId}')
        self.assertEqual(sessionId, client.sessionId)

    @patch('torrentClient.requests.get')
    def test_패스워드가_다르면(self, mock_get):
        # mock the response
        mock_response = MagicMock()
        # Unauthorized
        mock_response.status_code = 401
        mock_response.text = ""
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        # specify the return value of the get() method
        mock_get.return_value = mock_response

        mySetting = setting.Setting()
        client = torrentClient.TransmissionClient(mySetting.json["torrentClient"], "5555")
        
        self.assertIsNone(client.sessionId)

    @patch('torrentClient.TransmissionClient.addTorrent')
    @patch('torrentClient.TransmissionClient.getRpcSessionId')
    @patch('requests.post')
    def test_addMagnet(self, mock_post, mock_get_session_id, mock_add_torrent):
        mock_get_session_id.return_value = 'dummy_session_id'
        mockResponse = MagicMock()
        mock_post.return_value = mockResponse
        mockResponse.status_code = 200
        mockResponse.json.return_value = {"result":"success"}

        test_args = ["test_magnet", '--downloadPath', 'test_download_path', '--password', 'test_trans_pass']
                      
        with patch('sys.argv', ['torrentClient.py'] + test_args):
             torrentClient.main()
        # Check that the addMagnetTransmissionRemote function was called with the correct arguments
        mock_add_torrent.assert_called_once_with('test_magnet', 'test_download_path')

    @patch('requests.post')
    def test_qbitLogin(self, mock_post):
        # 가짜 응답을 설정합니다.
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.cookies = {'SID': 'mock_sid'}
        
        # QBittorrent 설정
        qbittorrentSetting = {
            'id': 'admin',  # 여기에 사용자 ID를 입력하세요.
            'host': '127.0.0.1',  # 여기에 호스트 주소를 입력하세요.
            'port': 8080  # 여기에 포트 번호를 입력하세요.
        }

        # QBittorrentClient 인스턴스 생성
        client = torrentClient.QBittorrentClient(qbittorrentSetting, "dummyPassword")

        # 연결 상태 확인
        isLogined = client.login()

        self.assertTrue(isLogined)

    @patch('requests.post')
    @patch('requests.get')
    def test_getAllTorrentsQbit(self, mock_get, mock_post):
        # 가짜 응답을 설정합니다.
        mock_login_response = mock_post.return_value
        mock_login_response.status_code = 200
        mock_login_response.cookies = {'SID': 'mock_sid'}
        
        mock_torrents_response = mock_get.return_value
        mock_torrents_response.json.return_value = [{'name': 'torrent1'}, {'name': 'torrent2'}]
        
        # QBittorrent 설정
        qbittorrentSetting = {
            'id': 'admin',  # 여기에 사용자 ID를 입력하세요.
            'host': '127.0.0.1',  # 여기에 호스트 주소를 입력하세요.
            'port': 8080  # 여기에 포트 번호를 입력하세요.
        }

        # QBittorrentClient 인스턴스 생성
        client = torrentClient.QBittorrentClient(qbittorrentSetting, "dummyPassword")

        # 연결 상태 확인
        isLogined = client.login()

        self.assertTrue(isLogined)

        # 모든 토렌트 정보 가져오기
        torrents = client.getAllTorrents()

        # 반환된 토렌트 정보가 리스트인지 확인
        self.assertIsInstance(torrents, list)

    @patch('requests.post')
    def test_addTorrentQbit(self, mock_post):
        # 가짜 응답을 설정합니다.
        mock_login_response = mock_post.return_value
        mock_login_response.status_code = 200
        mock_login_response.cookies = {'SID': 'mock_sid'}
        
        mock_add_torrent_response = mock_post.return_value
        mock_add_torrent_response.status_code = 200
        
        # QBittorrent 설정
        qbittorrentSetting = {
            'id': 'admin',  # 여기에 사용자 ID를 입력하세요.
            'host': '127.0.0.1',  # 여기에 호스트 주소를 입력하세요.
            'port': 8080  # 여기에 포트 번호를 입력하세요.
        }

        # QBittorrentClient 인스턴스 생성
        client = torrentClient.QBittorrentClient(qbittorrentSetting, "dummyPassword")

        # 연결 상태 확인
        isLogined = client.login()
        self.assertTrue(isLogined)

        # 토렌트 추가
        magnet_link = "your_magnet_link"  # 여기에 토렌트 링크를 입력하세요.
        response_code = client.addTorrent(magnet_link)

        # 반환된 응답 코드가 200인지 확인
        self.assertEqual(response_code, 200)

    @patch('requests.post')
    def test_deleteTorrentQbit(self, mock_post):
        # 가짜 응답을 설정합니다.
        mock_login_response = mock_post.return_value
        mock_login_response.status_code = 200
        mock_login_response.cookies = {'SID': 'mock_sid'}
        
        mock_delete_torrent_response = mock_post.return_value
        mock_delete_torrent_response.status_code = 200
        
        # QBittorrent 설정
        qbittorrentSetting = {
             'id': 'admin',  # 여기에 사용자 ID를 입력하세요.
            'host': '127.0.0.1',  # 여기에 호스트 주소를 입력하세요.
            'port': 8080  # 여기에 포트 번호를 입력하세요.
        }

        # QBittorrentClient 인스턴스 생성
        client = torrentClient.QBittorrentClient(qbittorrentSetting, "dummyPassword")

        # 연결 상태 확인
        isLogined = client.login()
        self.assertTrue(isLogined)
        
         # 토렌트 삭제
        response_code = client.deleteTorrent('mock_hash')

         # 반환된 응답 코드가 200인지 확인
        self.assertEqual(response_code, 200)

    @patch('requests.post')
    @patch.object(torrentClient.TransmissionClient, 'getRpcSessionId')
    def test_addTorrentTrans(self, mock_getRpcSessionId, mock_post):
        # 가짜 응답을 설정합니다.
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'arguments': {
                'torrent-added': {
                    'id': 1,
                    'name': 'mock_torrent',
                    'hashString': 'mock_hash'
                }
            },
            'result': 'success'
        }
        
        # 가짜 세션 ID를 설정합니다.
        mock_getRpcSessionId.return_value = 'mock_session_id'
        
        # Transmission 설정
        clientSetting = {
            'id': 'dummy_id',  # 여기에 사용자 ID를 입력하세요.
            'host': 'dummy_host',  # 여기에 호스트 주소를 입력하세요.
            'port': 9091  # 여기에 포트 번호를 입력하세요.
        }

        # TransmissionClient 인스턴스 생성
        client = torrentClient.TransmissionClient(clientSetting, "dummyPassword")

        # 토렌트 추가
        response_code = client.addTorrent("your_magnet_link", "/path/to/download")

        # 반환된 응답 코드가 200인지 확인
        self.assertEqual(response_code, 200)

    @patch('requests.post')
    @patch.object(torrentClient.TransmissionClient, 'getRpcSessionId')
    def test_getAllTorrentsTrans(self, mock_getRpcSessionId, mock_post):
        # 가짜 응답을 설정합니다.
        mock_login_response = mock_post.return_value
        mock_login_response.status_code = 200
        mock_login_response.cookies = {'SID': 'mock_sid'}
        
        mock_get_all_torrents_response = mock_post.return_value
        mock_get_all_torrents_response.status_code = 200
        mock_get_all_torrents_response.json.return_value = {
            'arguments': {
                'torrents': [
                    {'id': 1, 'name': 'mock_torrent', 'isFinished': True},
                    {'id': 2, 'name': 'another_mock_torrent', 'isFinished': False}
                ]
            },
            'result': 'success'
        }
        
        # 가짜 세션 ID를 설정합니다.
        mock_getRpcSessionId.return_value = 'mock_session_id'
        
        # Transmission 설정
        clientSetting = {
            'id': 'dummy_id',  # 여기에 사용자 ID를 입력하세요.
            'host': 'dummy_host',  # 여기에 호스트 주소를 입력하세요.
            'port': 9091  # 여기에 포트 번호를 입력하세요.
        }

        # TransmissionClient 인스턴스 생성
        client = torrentClient.TransmissionClient(clientSetting, "dummyPassword")

        # 모든 토렌트 정보 가져오기
        torrents = client.getAllTorrents()

        # 반환된 토렌트 정보가 리스트인지 확인
        self.assertIsInstance(torrents, list)

    @patch('requests.post')
    @patch.object(torrentClient.TransmissionClient, 'getRpcSessionId')
    def test_deleteTorrentTrans(self, mock_getRpcSessionId, mock_post):
        # 가짜 응답을 설정합니다.
        mock_login_response = mock_post.return_value
        mock_login_response.status_code = 200
        mock_login_response.cookies = {'SID': 'mock_sid'}
        
        mock_delete_torrent_response = mock_post.return_value
        mock_delete_torrent_response.status_code = 200
        
        # 가짜 세션 ID를 설정합니다.
        mock_getRpcSessionId.return_value = 'mock_session_id'
        
        # Transmission 설정
        clientSetting = {
            'id': 'dummy_id',  # 여기에 사용자 ID를 입력하세요.
            'host': 'dummy_host',  # 여기에 호스트 주소를 입력하세요.
            'port': 9091  # 여기에 포트 번호를 입력하세요.
        }

        # TransmissionClient 인스턴스 생성
        client = torrentClient.TransmissionClient(clientSetting, "dummyPassword")

        # 토렌트 삭제
        response_code = client.deleteTorrent(7)

        # 반환된 응답 코드가 200인지 확인
        self.assertEqual(response_code, 200)


if __name__ == '__main__':  
    unittest.main()
