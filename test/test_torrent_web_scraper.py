from turtle import title
import unittest

import setting 
import gnBoardBasicSkin
import torrent_web_scraper

class TorrentWebScraperTest(unittest.TestCase):
    def test_첫번째_사이트_첫번째_카테고리_리스트받기(self):
        # arrange
        mySetting = setting.Setting()
        site = mySetting.json["sites"][0]
        firstBoard = site["category"][0]
        firstBoard["history"] = 0
        # act
        myBoardScraper = gnBoardBasicSkin.GNBoardBasicSkin()
        boardList = myBoardScraper.getParseData(site["mainUrl"], firstBoard["url"], 1)
        
        # assert
        title = boardList[0].Title
        url = boardList[0].Url
        id = boardList[0].ID
        print(f"title: {title}, url: {url}, id: {id}")
        self.assertGreater(len(title), 0)
        self.assertGreater(len(url), 0)
        self.assertTrue(url.startswith("http"))
        self.assertGreater(id, 0)

    def test_wrID(self):
        myBoardScraper = gnBoardBasicSkin.GNBoardBasicSkin()
        wrID = 111111
        url = "https://torrentsir58.com/bbs/board.php?bo_table=entertain&wr_id="+str(wrID)
        self.assertEqual(wrID, myBoardScraper.getWrID(url))