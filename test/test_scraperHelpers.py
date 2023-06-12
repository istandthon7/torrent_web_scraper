import unittest
import scraperHelpers

class ScraperHelpersTest(unittest.TestCase):
    def test_getSoup(self):
        self.assertIsNotNone(scraperHelpers.getSoup("http://naver.com"))

    def test_getSoup_https(self):
        self.assertIsNotNone(scraperHelpers.getSoup("https://daum.net"))


if __name__ == '__main__':  
    unittest.main()