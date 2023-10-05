import os
import unittest
from unittest.mock import patch

import notification
import setting
from model.BoardItem import BoardItem


class NotificationTest(unittest.TestCase):

    def setUp(self):
        mySetting = setting.Setting()
        self.notiSetting = mySetting.json["notification"]
        self.configDirPath = mySetting.configDirPath
        self.notiSetting["history"] = os.path.join(self.configDirPath, 'test_notification.csv')
        open(self.notiSetting["history"], 'w').close()
        self.notiSetting["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "

    def tearDown(self):
        os.remove(self.notiSetting["history"])

    def test_processNotification_keyword_not_in_title(self):
        self.notiSetting["keywords"].insert(0, "왕밤빵")
        noti = notification.Notification(self.configDirPath, self.notiSetting)
        boardItem = BoardItem(title="테스트 게시판 제목")
        with patch.object(noti, 'runNotiScript') as mocked_run:
            result = noti.processNotification("사이트명", boardItem)
            self.assertFalse(result)
            mocked_run.assert_not_called()

    def test_processNotification_title_in_history(self):
        self.notiSetting["keywords"].insert(0, "키워드")
        noti = notification.Notification(self.configDirPath, self.notiSetting)
        noti.notifications = [["2023-09-13 22:57:22", "사이트명", "테스트 게시판 제목 키워드", "키워드"]]
        boardItem = BoardItem(title="테스트 게시판 제목 키워드")
        with patch.object(noti, 'runNotiScript') as mocked_run:
            result = noti.processNotification("사이트명", boardItem)
            self.assertFalse(result)
            mocked_run.assert_not_called()

    def test_runNotiScript(self):
        noti = notification.Notification(self.configDirPath, self.notiSetting)
        with patch('subprocess.run') as mocked_run:
            mocked_run.return_value.returncode = 0
            result = noti.runNotiScript("사이트명", "테스트 게시판 제목")
            self.assertEqual(result, 0)

    def test_isTitleInNotificationHistory(self):
        noti = notification.Notification(self.configDirPath, self.notiSetting)
        noti.notifications = [["2023-09-13 22:57:22", "사이트명", "테스트 게시판 제목", "키워드", "https://example.com"]]
        result = noti.isTitleInNotificationHistory("테스트 게시판 제목")
        self.assertTrue(result)

    def test_isTitleInNotificationHistory2(self):
        noti = notification.Notification(self.configDirPath, self.notiSetting)
        noti.notifications = [
            ["2023-09-13 22:57:22", "사이트명", "특별시 귀신들,2009.720p.WEBRip.H264.AAC", "키워드", "https://example.com"],
            ["2023-09-13 22:57:22", "사이트명", "특별시 귀신들,2009 720p WEBRip H264 AAC", "키워드", "https://example.com"],
            ["2023-09-13 22:57:22", "사이트명", "[한국영화] 특별시 귀신들,2009.720p.WEBRip.H264.AAC", "키워드", "https://example.com"]
        ]
        result = noti.isTitleInNotificationHistory("N 특별시 귀신들,2009.720p.WEBRip.H264.AAC")
        self.assertTrue(result)

    def test_isTitleInNotificationHistory3(self):
        noti = notification.Notification(self.configDirPath, self.notiSetting)
        noti.notifications = [
            ["2023-09-13 22:57:22", "사이트명", "특별시 귀신들,2009.720p.WEBRip.H264.AAC", "키워드", "https://example.com"],
            ["2023-09-13 22:57:22", "사이트명", "특별시 귀신들,2009 720p WEBRip H264 AAC", "키워드", "https://example.com"],
            ["2023-09-13 22:57:22", "사이트명", "[한국영화] 특별시 귀신들,2009.720p.WEBRip.H264.AAC", "키워드", "https://example.com"]
        ]
        result = noti.isTitleInNotificationHistory("특별시 귀신들.2009.720p.WEBRip.H264.AAC")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
