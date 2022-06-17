import unittest
import setting 
import boardScraper

class TorrentWebScraperTest(unittest.TestCase):
    def test_첫번째_사이트_첫번째_카테고리_리스트받기(self):
        # arrange
        mySetting = setting.Setting()
        site = mySetting.json["sites"][0]
        firstBoard = site["categories"][0]
        firstBoard["history"] = 0
        # act
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItemInfos(site["mainUrl"]+firstBoard["url"], 1
            , firstBoard["title"]["tag"], firstBoard["title"]["class"])
        
        # assert
        title = boardItems[0].title
        url = boardItems[0].url
        id = boardItems[0].id
        print(f"title: {title}, url: {url}, id: {id}")
        self.assertGreater(len(title), 0)
        self.assertGreater(len(url), 0)
        self.assertGreater(id, 0)
