import logging
import os
import unittest
import boardScraper
import setting
import urllib.parse
from unittest.mock import patch

class BoardScraperTest(unittest.TestCase):
    @patch('scraperHelpers.getResponse')
    def test_getBoardList(self, mock_getResponse):
        file_path = os.path.join(os.path.dirname(__file__), 'test_board.html')
        with open(file_path, 'rb') as f:
            mock_response = f.read()
            mock_getResponse.return_value.read.return_value = mock_response
        mySetting = setting.Setting()
        site = mySetting.json["sites"][0]
        category = site["boards"][0]
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems(site["mainUrl"]+category["url"], 1
                        , category["title"].get("tag"), category["title"].get("class"), category["title"].get("selector"))
        self.assertTrue(boardItems)

    def test_getBoardListFromFile(self):
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems("test/test.html", 1, "div", "wr-subject", "")
        self.assertTrue(boardItems)
        
    @patch('scraperHelpers.getResponse')
    def test_첫번째_사이트_첫번째_카테고리_리스트받기(self, mock_getResponse):
        file_path = os.path.join(os.path.dirname(__file__), 'test_board.html')
        with open(file_path, 'rb') as f:
            mock_response = f.read()
            mock_getResponse.return_value.read.return_value = mock_response
        # arrange
        mySetting = setting.Setting()
        site = mySetting.json["sites"][0]
        firstBoard = site["boards"][0]
        firstBoard["history"] = 0
        # act
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems(site["mainUrl"]+firstBoard["url"], 1
            , firstBoard["title"].get("tag"), firstBoard["title"].get("class"), firstBoard["title"].get("selector"))
        
        # assert
        title = boardItems[0].title
        url = boardItems[0].url
        id = boardItems[0].id
        print(f"title: {title}, url: {url}, id: {id}")
        self.assertGreater(len(title), 0)
        self.assertGreater(len(url), 0)
        self.assertGreater(id, 0)

    def test_getBoardItems(self):
        logging.basicConfig(level=logging.DEBUG)
        file_path = os.path.join(os.path.dirname(__file__), 'board_q.html')
        
        # act
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems(file_path, 1, "", "", "ul.list-body > li.list-item")
        
        # assert
        title = boardItems[0].title
        url = boardItems[0].url
        id = boardItems[0].id
        print(f"title: {title}, url: {url}, id: {id}")
        self.assertEqual((title), "제목 하우스2.E04.230622.1080p.H264-F1RST.")
        self.assertEqual((url), "https://qq22.com/torrent/med/1112811.html")
        self.assertEqual(id, 1112811)
        self.assertEqual(boardItems[0].number, 113553)

    def test_getBoardItem2(self):
        logging.basicConfig(level=logging.DEBUG)
        file_path = os.path.join(os.path.dirname(__file__), 'board_q_type2.html')
        
        # act
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems(file_path, 1, "", "", "ul.list-body > li.list-item")
        
        # assert
        title = boardItems[0].title
        url = boardItems[0].url
        id = boardItems[0].id
        print(f"title: {title}, url: {url}, id: {id}")
        self.assertEqual((title), "제목은 찬가2.E02.230622.1080p.H264-F1RST")
        self.assertEqual((url), "https://qq22.com/torrent/med/1112787.html")
        self.assertEqual(id, 1112787)
        self.assertEqual(boardItems[0].number, 113545)

    def test_getBoardItems_ten(self):
        logging.basicConfig(level=logging.DEBUG)
        file_path = os.path.join(os.path.dirname(__file__), 'board_ten.html')
        
        # act
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems(file_path, 1, "", "", "div.list-item")
        
        # assert
        title = boardItems[0].title
        url = boardItems[0].url
        id = boardItems[0].id
        print(f"title: {title}, url: {url}, id: {id}")
        self.assertIn("칠일 Seven.Days.2000.KOREAN.1080p.BluRay.H264.AAC-VXT", title)
        self.assertEqual((url), "https://www.ten12.com/bbs/board.php?bo_table=tmovie&wr_id=10078")
        self.assertEqual(id, 10078)
        self.assertIsNone(boardItems[0].number)


    @patch('scraperHelpers.getResponse')
    def test_getMagnet(self, mock_getResponse):
        file_path = os.path.join(os.path.dirname(__file__), 'test_board.html')
        with open(file_path, 'rb') as f:
            mock_response = f.read()
            mock_getResponse.return_value.read.return_value = mock_response
        mySetting = setting.Setting()
        site = mySetting.json["sites"][0]
        category = site["boards"][0]
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems(site["mainUrl"]+category["url"], 1
                        , category["title"].get("tag"), category["title"].get("class"), category["title"].get("selector"))
        boardItems = list(filter(lambda x: "예고편" not in x.title, boardItems))
        file_path = os.path.join(os.path.dirname(__file__), 'test_magnet.html')
        with open(file_path, 'rb') as f:
            mock_response = f.read()
            mock_getResponse.return_value.read.return_value = mock_response
        magnet = myBoardScraper.getMagnet(urllib.parse.urljoin(site["mainUrl"], boardItems[0].url))

        self.assertGreater(len(magnet), 0)
