import os
import keywords
import unittest


class KeywordsTest(unittest.TestCase):
    def test_getSavePath(self):
        myKeywords = keywords.Keywords()
        downloadPath = myKeywords.getSavePath({"name": "제목", "option": "720","option2":"Next", "exclude":"제외, 완결" }, "", True)
        self.assertEqual("", downloadPath)

    def test_getSavePath2(self):
        myKeywords = keywords.Keywords()
        regKeyword = {"name": "제목", "option": "720","option2":"Next", "exclude":"제외, 완결" }
        basePath = "/test"
        downloadPath = myKeywords.getSavePath(regKeyword, basePath, True)
        self.assertEqual(os.path.join(basePath, regKeyword["name"]), downloadPath)


if __name__ == '__main__':
    unittest.main()