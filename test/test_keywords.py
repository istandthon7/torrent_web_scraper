import os
import keywords
import unittest


class KeywordsTest(unittest.TestCase):
    def test_getSavePath(self):
        myKeywords = keywords.Keywords()
        downloadPath = myKeywords.getSavePath({"name": "우분투", "option": "22.04","option2":"arm64", "exclude":"preview, night build" }, "", True)
        self.assertEqual("", downloadPath)

    def test_getSavePath2(self):
        myKeywords = keywords.Keywords()
        regKeyword = {"name": "우분투", "option": "22.04","option2":"arm64", "exclude":"preview, night build"}
        basePath = "/test"
        downloadPath = myKeywords.getSavePath(regKeyword, basePath, True)
        self.assertEqual(os.path.join(basePath, regKeyword["name"]), downloadPath)


if __name__ == '__main__':
    unittest.main()