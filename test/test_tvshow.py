import unittest
import tvshow
import setting

class TvShowTest(unittest.TestCase): 
    def test_getRegKeyword_대소문자_있으면(self):
        mySetting = setting.Setting()
        myTvShow = tvshow.TVShow(mySetting)
        myTvShow.json['title_list'] =[{"name": "Star Trek Picard", "option": "720","option2":"264" }]
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_소문자만_있으면(self):
        mySetting = setting.Setting()
        myTvShow = tvshow.TVShow(mySetting)
        myTvShow.json['title_list'] =[{"name": "star trek picard", "option": "720","option2":"264" }]
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword(self):
        mySetting = setting.Setting()
        myTvShow = tvshow.TVShow(mySetting)
        myTvShow.json['title_list'] =[{"name": "스타트렉 피카드", "option": "720","option2":"264" }]
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)
        
    def test_getRegKeyword_시즌이_없어도(self):
        mySetting = setting.Setting()
        myTvShow = tvshow.TVShow(mySetting)
        myTvShow.json['title_list'] =[{"name": "스타트렉 피카드", "option": "720","option2":"264" }]
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)
    
    def test_getRegKeyword_시즌이_다르면(self):
        mySetting = setting.Setting()
        myTvShow = tvshow.TVShow(mySetting)
        myTvShow.json['title_list'] =[{"name": "스타트렉 피카드 시즌02", "option": "720","option2":"264" }]
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_같으면(self):
        mySetting = setting.Setting()
        myTvShow = tvshow.TVShow(mySetting)
        myTvShow.json['title_list'] =[{"name": "스타트렉 피카드", "option": "720","option2":"264" }]
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_다르면(self):
        mySetting = setting.Setting()
        myTvShow = tvshow.TVShow(mySetting)
        myTvShow.json['title_list'] =[{"name": "스타트렉 피카드", "option": "1080","option2":"264" }]
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_같으면(self):
        mySetting = setting.Setting()
        myTvShow = tvshow.TVShow(mySetting)
        myTvShow.json['title_list'] =[{"name": "스타트렉 피카드", "option": "720","option2":"264" }]
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_다르면(self):
        mySetting = setting.Setting()
        myTvShow = tvshow.TVShow(mySetting)
        myTvShow.json['title_list'] =[{"name": "스타트렉 피카드", "option": "720","option2":"265" }]
        regKeyword = myTvShow.getRegKeyword("스타트렉 피카드 시즌01 Star Trek Picard S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(len(regKeyword), 0)

if __name__ == '__main__':  
    unittest.main()