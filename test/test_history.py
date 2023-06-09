import unittest
from history import MagnetHistory

class TestMagnetHistory(unittest.TestCase):
    def setUp(self):
        self.csvFileName = 'test.csv'
        self.failFileName = 'fail.csv'
        self.magnetHistory = MagnetHistory(self.csvFileName, self.failFileName)

    def test_checkMagnetHistory(self):
        magnet = 'magnet:?xt=urn:btih:example'
        self.assertFalse(self.magnetHistory.checkMagnetHistory(magnet))
        self.magnetHistory.addMagnetToHistory('siteName', 'boardTitle', magnet, 'keyword')
        self.assertTrue(self.magnetHistory.checkMagnetHistory(magnet))

    def test_addMagnetToHistory(self):
        magnet = 'magnet:?xt=urn:btih:example'
        self.magnetHistory.addMagnetToHistory('siteName', 'boardTitle', magnet, 'keyword')
        with open(self.csvFileName, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            self.assertTrue(len(lines) > 1)
            self.assertIn(magnet, lines[0])

    def test_addTorrentFailToFile(self):
        siteName = 'siteName'
        boardTitle = 'boardTitle'
        boardUrl = 'http://example.com'
        keyword = 'keyword'
        downloadDir = '/path/to/download/dir'
        self.magnetHistory.addTorrentFailToFile(siteName, boardTitle, boardUrl, keyword, downloadDir)
        with open(self.failFileName, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            self.assertTrue(len(lines) > 1)
            self.assertIn(siteName, lines[0])
            self.assertIn(boardTitle, lines[0])
            self.assertIn(boardUrl, lines[0])
            self.assertIn(keyword, lines[0])
            self.assertIn(downloadDir, lines[0])

if __name__ == '__main__':
    unittest.main()
