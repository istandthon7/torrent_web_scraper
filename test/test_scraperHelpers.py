import unittest
import scraperHelpers
import setting
import os
import rpc

class ScraperHelpersTest(unittest.TestCase):
    def test_getSoup(self):
        self.assertIsNotNone(scraperHelpers.getSoup("http://naver.com"))

    def test_getSoup_https(self):
        self.assertIsNotNone(scraperHelpers.getSoup("https://daum.net"))

    # def test_executeNotiScript_윈도우(self):
    #     mySetting = setting.Setting()
    #     if os.path.isfile(mySetting.notiHistoryPath):
    #         os.remove(mySetting.notiHistoryPath)
    #     mySetting.json["notification"]["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "
    #     mySetting.json["notification"]["keywords"].insert(0, "테스트")
    #     self.assertTrue(scraperHelpers.executeNotiScript(mySetting, "사이트명", "테스트 제목"))

    def test_executeNotiScript_윈도우_키워드_없으면(self):
        mySetting = setting.Setting()
        if os.path.isfile(mySetting.notiHistoryPath):
            os.remove(mySetting.notiHistoryPath)
        mySetting.json["notification"]["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "
        mySetting.json["notification"]["keywords"].insert(0, "왕밤빵")
        self.assertFalse(scraperHelpers.executeNotiScript(mySetting, "사이트명", "테스트 게시판 제목"))

    def test_executeNotiScript_윈도우_키워드_중복호출_안되나(self):
        mySetting = setting.Setting()
        if os.path.isfile(mySetting.notiHistoryPath):
            os.remove(mySetting.notiHistoryPath)
        mySetting.json["notification"]["cmd"] = "C:\\windows\\system32\\cmd.exe /C echo 'torrent_web_scraper keyword notification. $board_title' "
        mySetting.json["notification"]["keywords"].insert(0, "테스트")
        scraperHelpers.executeNotiScript(mySetting, "사이트명", "테스트 게시판 제목")
        self.assertFalse(scraperHelpers.executeNotiScript(mySetting, "사이트명", "테스트 게시판 제목"))

    # def test_transmissionSetting(self):
    #     ''' getSessionIdTransRpc 은 현재 안 된다. '''
    #     mySetting = setting.Setting()
    #     self.assertIsNotNone(rpc.getSessionIdTransRpc(mySetting.getRpcUrl()))

    # def test_rpc_다운로드_경로를_가져올수_있나(self):
    #     ''' rpc 통신을 하는 건 안돼'''
    #     mySetting = setting.Setting()
    #     dir = rpc.getDownloadDir(mySetting.getRpcUrl())
        
    #     self.assertIsNotNone(dir)

if __name__ == '__main__':  
    unittest.main()