import unittest
from notification import Notification
import setting
import os

class NotificationTest(unittest.TestCase):

    # def test_executeNotiScript_윈도우(self):
    #     mySetting = setting.Setting()
    #     if os.path.isfile(mySetting.json["notification"]["history"]):
    #         os.remove(mySetting.json["notification"]["history"])
    #     mySetting.json["notification"]["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "
    #     mySetting.json["notification"]["keywords"].insert(0, "테스트")
    #     noti = Notification(mySetting.json["notification"])
    #     self.assertTrue(noti.executeNotiScript("사이트명", "테스트 제목"))

    def test_executeNotiScript_윈도우_키워드_없으면(self):
        mySetting = setting.Setting()
        if os.path.isfile(mySetting.json["notification"]["history"]):
            os.remove(mySetting.json["notification"]["history"])
        mySetting.json["notification"]["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "
        mySetting.json["notification"]["keywords"].insert(0, "왕밤빵")
        noti = Notification(mySetting.json["notification"])
        self.assertFalse(noti.executeNotiScript("사이트명", "테스트 게시판 제목"))

    def test_executeNotiScript_윈도우_키워드_중복호출_안되나(self):
        mySetting = setting.Setting()
        if os.path.isfile(mySetting.json["notification"]["history"]):
            os.remove(mySetting.json["notification"]["history"])
        mySetting.json["notification"]["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "
        mySetting.json["notification"]["keywords"].insert(0, "테스트")
        noti = Notification(mySetting.json["notification"])
        noti.executeNotiScript("사이트명", "테스트 게시판 제목")
        self.assertFalse(noti.executeNotiScript("사이트명", "테스트 게시판 제목"))


if __name__ == '__main__':
    unittest.main()
