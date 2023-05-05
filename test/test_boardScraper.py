import unittest
import boardScraper
import setting
import urllib.parse

class BoardScraperTest(unittest.TestCase):
    def test_getBoardList(self):
        mySetting = setting.Setting()
        site = mySetting.json["sites"][0]
        category = site["categories"][0]
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems(site["mainUrl"]+category["url"], 1
                        , category["title"]["tag"], category["title"]["class"], category["title"].get("selector"))
        self.assertTrue(boardItems)

    def test_getBoardListFromFile(self):
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems("test/test.html", 1, "div", "wr-subject", "")
        self.assertTrue(boardItems)

    def test_첫번째_사이트_첫번째_카테고리_리스트받기(self):
        # arrange
        mySetting = setting.Setting()
        site = mySetting.json["sites"][0]
        firstBoard = site["categories"][0]
        firstBoard["history"] = 0
        # act
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems(site["mainUrl"]+firstBoard["url"], 1
            , firstBoard["title"]["tag"], firstBoard["title"]["class"], firstBoard["title"].get("selector"))
        
        # assert
        title = boardItems[0].title
        url = boardItems[0].url
        id = boardItems[0].id
        print(f"title: {title}, url: {url}, id: {id}")
        self.assertGreater(len(title), 0)
        self.assertGreater(len(url), 0)
        self.assertGreater(id, 0)

    def test_getID(self):
        myBoardScraper = boardScraper.BoardScraper()
        id = 999333
        url = "https://xxx22.com/bbs/board.php?bo_table=torrent_movieko2&wr_id="+str(id)
        self.assertEqual(myBoardScraper.getID(url), id)

    def test_getID_찾을수_없는(self):
        myBoardScraper = boardScraper.BoardScraper()
        id = 99934
        url = "https://xxx22.com/bbs/board.php?bo_table=torrent_movieko2&post_id="+str(id)
        self.assertEqual(myBoardScraper.getID(url), -1)


    def test_getID_id_로만_끝나는(self):
        myBoardScraper = boardScraper.BoardScraper()
        id = 999355
        url = "https://www.xxxxxxx89.top/view.php?b_id=tmovie&id="+str(id)
        self.assertEqual(myBoardScraper.getID(url), id)


    def test_getID_숫자_html(self):
        myBoardScraper = boardScraper.BoardScraper()
        id = 999365
        url = "https://xxxx146.com/torrent/mov/"+str(id)+".html"
        self.assertEqual(myBoardScraper.getID(url), id)


    def test_getID_숫자(self):
        myBoardScraper = boardScraper.BoardScraper()
        id = 999365
        url = "https://xxxxxxxxx3333.com/komovie/"+str(id)
        self.assertEqual(myBoardScraper.getID(url), id)


    def test_getID_wr_id_뒤에_더_있어(self):
        myBoardScraper = boardScraper.BoardScraper()
        id = 999377
        url = "https://xxxxxxx62.com/bbs/board.php?bo_table=netflix&wr_id="+str(id)+"&sca=%EB%84%B7%ED%94%8C%EB%A6%AD%EC%8A%A4"
        self.assertEqual(myBoardScraper.getID(url), id)

    def test_getMagnet(self):
        mySetting = setting.Setting()
        site = mySetting.json["sites"][0]
        category = site["categories"][0]
        myBoardScraper = boardScraper.BoardScraper()
        boardItems = myBoardScraper.getBoardItems(site["mainUrl"]+category["url"], 1
                        , category["title"]["tag"], category["title"]["class"], category["title"].get("selector"))
        boardItems = list(filter(lambda x: "예고편" not in x.title, boardItems))
        magnet = myBoardScraper.getMagnet(urllib.parse.urljoin(site["mainUrl"], boardItems[0].url))

        self.assertGreater(len(magnet), 0)