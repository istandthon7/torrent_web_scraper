import unittest
import notification
import setting
import os

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

    def test_executeNotiScript_윈도우_키워드_없으면(self):
        self.notiSetting["keywords"].insert(0, "왕밤빵")
        noti = notification.Notification(self.configDirPath, self.notiSetting)
        self.assertFalse(noti.executeNotiScript("사이트명", "테스트 게시판 제목"))

    def test_executeNotiScript_윈도우_키워드_중복호출_안되나(self):
        self.notiSetting["keywords"].insert(0, "테스트")
        noti = notification.Notification(self.configDirPath, self.notiSetting)
        noti.executeNotiScript("사이트명", "테스트 게시판 제목")
        self.assertFalse(noti.executeNotiScript("사이트명", "테스트 게시판 제목"))


if __name__ == '__main__':
    unittest.main()
