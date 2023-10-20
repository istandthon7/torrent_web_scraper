import os
import unittest
import history

class TestMagnetHistory(unittest.TestCase):
    def setUp(self):
        self.csvFileName = 'test.csv'
        self.failFileName = 'fail.csv'
        self.magnetHistory = history.MagnetHistory(self.csvFileName, self.failFileName)

    def tearDown(self):
        if os.path.exists(self.csvFileName):
            os.remove(self.csvFileName)
        if os.path.exists(self.failFileName):
            os.remove(self.failFileName)

    def test_isMagnetAppended(self):
        magnet = 'magnet:?xt=urn:btih:example1'
        self.assertFalse(self.magnetHistory.isMagnetAppended(magnet))
        self.magnetHistory.appendMagnet('siteName', 'boardTitle', magnet, 'keyword')
        self.assertTrue(self.magnetHistory.isMagnetAppended(magnet))

    def test_appendMagnet(self):
        magnet = 'magnet:?xt=urn:btih:example2'
        self.magnetHistory.appendMagnet('siteName', 'boardTitle', magnet, 'keyword')
        with open(self.csvFileName, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            self.assertTrue(len(lines) > 0)
            self.assertIn(magnet, lines[-1])

    def test_appendTorrentFail(self):
        siteName = 'siteName'
        boardTitle = 'boardTitle'
        boardUrl = 'http://example.com'
        keyword = 'keyword'
        downloadDir = '/path/to/download/dir'
        self.magnetHistory.appendTorrentFail(siteName, boardTitle, boardUrl, keyword, downloadDir)
        with open(self.failFileName, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            self.assertTrue(len(lines) > 0)
            self.assertIn(siteName, lines[-1])
            self.assertIn(boardTitle, lines[-1])
            self.assertIn(boardUrl, lines[-1])
            self.assertIn(keyword, lines[-1])
            self.assertIn(downloadDir, lines[-1])

if __name__ == '__main__':
    unittest.main()
