import unittest
from tvshow import TVShow

class TvShowTest(unittest.TestCase): 
    def test_getEpisodeNumber(self):
        myTvShow = TVShow()
        episode = myTvShow.getEpisodeNumber("우리는 세계사.E97.230505.720p-NEXT")
        self.assertEqual(97, episode)

    def test_getEpisodeNumber2(self):
        myTvShow = TVShow()
        episode = myTvShow.getEpisodeNumber("지구 세계여행 E09 1080p")
        self.assertEqual(9, episode)

    def test_getEpisodeNumber3(self):
        myTvShow = TVShow()
        episode = myTvShow.getEpisodeNumber("화성오락실 S02E08.1080p.WEB-Sniper")
        self.assertEqual(8, episode)

    def test_getRegKeyword_대소문자_있으면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "My TVShow", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword), "My TVShow")

    def test_getRegKeyword_소문자만_있으면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "my tvshow", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword), "my tvshow")

    def test_getRegKeyword(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "나의 티비쇼", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword), "나의 티비쇼")
        
    def test_getRegKeyword2(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": ".23", "option": "","option2":"", "exclude": "" }]}
        regKeyword = myTvShow.getRegKeyword("태어난 김에 세계일주2.E02.230618.1080p.WANNA")
        self.assertEqual((regKeyword), ".23")

    def test_getRegKeyword_시즌이_없어도(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "나의 티비쇼", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword), "나의 티비쇼")
    
    def test_getRegKeyword_시즌이_다르면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "나의 티비쇼 시즌02", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_같으면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "나의 티비쇼", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword), "나의 티비쇼")

    def test_getRegKeyword_해상도가_다르면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "나의 티비쇼", "option": "1080","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_같으면(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "나의 티비쇼", "option": "720","option2":"264" }]}
        regKeyword = myTvShow.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword), "나의 티비쇼")

    def test_getRegKeyword_코덱이_다르면(self):
        myTvShow = TVShow()
        myTvShow.json ={'title_list': [{"name": "나의 티비쇼", "option": "720","option2":"265" }]}
        regKeyword = myTvShow.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_exclude_keyword(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "My TVShow", "option": "720","option2":"264", "exclude": "exclude1, exclude2" }]}
        regKeyword = myTvShow.getRegKeyword("My TVShow exclude1")
        self.assertEqual(len(regKeyword), 0)
        
        regKeyword = myTvShow.getRegKeyword("My TVShow exclude2")
        self.assertEqual(len(regKeyword), 0)
        
        regKeyword = myTvShow.getRegKeyword("My TVShow 720p x264")
        self.assertEqual((regKeyword), "My TVShow")

    def test_getRegKeyword_exclude_keyword_is_empty_string(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "My TVShow", "option": "","option2":"", "exclude": "" }]}
        regKeyword = myTvShow.getRegKeyword("My TVShow exclude1")
        self.assertEqual((regKeyword), "My TVShow")

    def test_getRegKeyword_exclude_keyword2(self):
        myTvShow = TVShow()
        myTvShow.json = {'title_list': [{"name": "My TVShow", "option": "","option2":"", "exclude": "exclude" },
                                        {"name": "second title", "option": "","option2":"", "exclude": "" }]}
        regKeyword = myTvShow.getRegKeyword("second title")
        self.assertEqual((regKeyword), "second title")
        
if __name__ == '__main__':  
    unittest.main()