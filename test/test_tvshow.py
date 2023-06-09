import unittest
from tvshow import TVShow

class TvShowTest(unittest.TestCase): 
    def test_getRegKeyword_대소문자_있으면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "Star Trek Picard", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_소문자만_있으면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "star trek picard", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "스타트렉 피카드", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)
        
    def test_getRegKeyword_시즌이_없어도(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "스타트렉 피카드", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)
    
    def test_getRegKeyword_시즌이_다르면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "스타트렉 피카드 시즌02", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_같으면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "스타트렉 피카드", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_다르면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "스타트렉 피카드", "option": "1080","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_같으면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "스타트렉 피카드", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_다르면(self):
        myTvShow = TVShow()
        myTvShow.json ={'title_list': [{"name": "스타트렉 피카드", "option": "720","option2":"265" }]}
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_exclude_keyword(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "Star Trek Picard", "option": "720","option2":"264", "exclude": "exclude1, exclude2" }]}
        regKeyword = myTvShow.getRegKeyword("Star Trek Picard exclude1")
        self.assertEqual(len(regKeyword), 0)
        
        regKeyword = myTvShow.getRegKeyword("Star Trek Picard exclude2")
        self.assertEqual(len(regKeyword), 0)
        
        regKeyword = myTvShow.getRegKeyword("Star Trek Picard 720p x264")
        self.assertGreater(len(regKeyword), 0)

if __name__ == '__main__':  
    unittest.main()