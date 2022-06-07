import unittest
import scraperLibrary
import setting
import os

class ScraperLibraryTest(unittest.TestCase):
    def test_getBsObj(self):
        self.assertIsNotNone(scraperLibrary.getBsObj("http://naver.com"))

    def test_getBsObj_https(self):
        self.assertIsNotNone(scraperLibrary.getBsObj("https://daum.net"))

    def test_executeNotiScript_윈도우(self):
        mySetting = setting.Setting()
        if os.path.isfile(mySetting.notiHistoryPath):
            os.remove(mySetting.notiHistoryPath)
        mySetting.json["notification"]["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "
        mySetting.json["notification"]["keywords"].insert(0, "테스트")
        self.assertTrue(scraperLibrary.executeNotiScript(mySetting, "사이트명", "테스트 제목"))

    def test_executeNotiScript_윈도우_키워드_없으면(self):
        mySetting = setting.Setting()
        if os.path.isfile(mySetting.notiHistoryPath):
            os.remove(mySetting.notiHistoryPath)
        mySetting.json["notification"]["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "
        mySetting.json["notification"]["keywords"].insert(0, "왕밤빵")
        self.assertFalse(scraperLibrary.executeNotiScript(mySetting, "사이트명", "테스트 게시판 제목"))

    def test_executeNotiScript_윈도우_키워드_중복호출_안되나(self):
        mySetting = setting.Setting()
        if os.path.isfile(mySetting.notiHistoryPath):
            os.remove(mySetting.notiHistoryPath)
        mySetting.json["notification"]["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "
        mySetting.json["notification"]["keywords"].insert(0, "테스트")
        scraperLibrary.executeNotiScript(mySetting, "사이트명", "테스트 게시판 제목")
        self.assertFalse(scraperLibrary.executeNotiScript(mySetting, "사이트명", "테스트 게시판 제목"))
if __name__ == '__main__':  
    unittest.main()