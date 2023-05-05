import unittest

from model.BoardItem import BoardItem

class BoardItemTest(unittest.TestCase):
    def test_parseBoardItem(self):
        boardItem = BoardItem("우리는 세계사.E97.230505.720p-NEXT", "url", 1, 1)
        
        self.assertEqual(97, boardItem.getEpisode())

    def test_parseBoardItem2(self):
        boardItem = BoardItem("지구 세계여행 E09 1080p", "url", 1, 1)
        
        self.assertEqual(9, boardItem.getEpisode())
