import unittest

from model.BoardItem import BoardItem

class BoardItemTest(unittest.TestCase):

    def test_getID(self):
        boardItem = BoardItem()
        id = 999333
        boardItem.setUrl("https://xxx22.com/bbs/board.php?bo_table=torrent_movieko2&wr_id="+str(id))
        self.assertEqual(boardItem.id, id)

    def test_getID_찾을수_없는(self):
        boardItem = BoardItem()
        id = 99934
        boardItem.setUrl("https://xxx22.com/bbs/board.php?bo_table=torrent_movieko2&post_id="+str(id))
        self.assertEqual(boardItem.id, -1)

    def test_getID_id_로만_끝나는(self):
        boardItem = BoardItem()
        id = 999355
        boardItem.setUrl("https://www.xxxxxxx89.top/view.php?b_id=tmovie&id="+str(id))
        self.assertEqual(boardItem.id, id)

    def test_getID_숫자_html(self):
        boardItem = BoardItem()
        id = 999365
        boardItem.setUrl("https://xxxx146.com/torrent/mov/"+str(id)+".html")
        self.assertEqual(boardItem.id, id)

    def test_getID_숫자(self):
        boardItem = BoardItem()
        id = 999365
        boardItem.setUrl("https://xxxxxxxxx3333.com/komovie/"+str(id))
        self.assertEqual(boardItem.id, id)

    def test_getID_숫자2(self):
        boardItem = BoardItem()
        id = 2829
        boardItem.setUrl(f"https://www.xxxx.com/movie/{str(id)}.html")
        self.assertEqual(boardItem.id, id)

    def test_getID_wr_id_뒤에_더_있어(self):
        boardItem = BoardItem()
        id = 999377
        boardItem.setUrl("https://xxxxxxx62.com/bbs/board.php?bo_table=netflix&wr_id="+str(id)+"&sca=%EB%84%B7%ED%94%8C%EB%A6%AD%EC%8A%A4")
        self.assertEqual(boardItem.id, id)
