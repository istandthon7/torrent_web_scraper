import os
import unittest
import keywords
import setting


class KeywordsTest3(unittest.TestCase): 
    def setUp(self):
        mySetting = setting.Setting()
        self.tvshowRuleSetting = next(rule for rule in mySetting.json['downloadRules'] if rule['name'] == 'tvshow')
        self.myKeywords = keywords.Keywords()
        self.testFilePath = os.path.join(mySetting.configDirPath, 'test_tvshow_list.json')
        open(self.testFilePath, 'w').close()
        self.myKeywords.load(os.path.join(mySetting.configDirPath, self.testFilePath))

    def tearDown(self):
        os.remove(self.testFilePath)
        
    def test_parseBoardItem(self):
        episode = self.myKeywords.getEpisodeNumber("우리는 세계사.E97.230505.720p-NEXT")
        self.assertEqual(97, episode)

    def test_parseBoardItem2(self):
        episode = self.myKeywords.getEpisodeNumber("지구 세계여행 E09 1080p")
        self.assertEqual(9, episode)

    def test_getEpisodeNumber3(self):
        episode = self.myKeywords.getEpisodeNumber("화성오락실 S02E08.1080p.WEB-Sniper")
        self.assertEqual(8, episode)

    def test_getEpisodeNumber4(self):
        episode = self.myKeywords.getEpisodeNumber("화성오락실.E07-08.1080p.WEB-Sniper")
        self.assertEqual(7, episode)

    def test_getRegKeyword_대소문자_있으면(self):
        self.myKeywords.json = {'keywords': [{"name": "My TVShow", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), "My TVShow")

    def test_getRegKeyword_소문자만_있으면(self):
        self.myKeywords.json = {'keywords': [{"name": "my tvshow", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), "my tvshow")

    def test_getRegKeyword(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 티비쇼", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), "나의 티비쇼")
        
    def test_getRegKeyword2(self):
        self.myKeywords.json = {'keywords': [{"name": ".23", "option": "","option2":"", "exclude": "" }]}
        regKeyword = self.myKeywords.getRegKeyword("검은 김의 세계일주2.E02.230618.1080p.WANNA", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), ".23")

    def test_getRegKeyword_시즌이_없어도(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 티비쇼", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), "나의 티비쇼")
    
    def test_getRegKeyword_시즌이_다르면(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 티비쇼 시즌02", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM", self.tvshowRuleSetting)
        self.assertIsNone((regKeyword))

    def test_getRegKeyword_해상도가_같으면(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 티비쇼", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), "나의 티비쇼")

    def test_getRegKeyword_해상도가_다르면(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 티비쇼", "option": "1080","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM", self.tvshowRuleSetting)
        self.assertIsNone((regKeyword))

    def test_getRegKeyword_코덱이_같으면(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 티비쇼", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), "나의 티비쇼")

    def test_getRegKeyword_코덱이_다르면(self):
        self.myKeywords.json ={'keywords': [{"name": "나의 티비쇼", "option": "720","option2":"265" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 티비쇼 시즌01 My TVShow S01 720p.KOR.HDRip.H264.AAC-RTM", self.tvshowRuleSetting)
        self.assertIsNone((regKeyword))

    def test_getRegKeyword_exclude_keyword(self):
        self.myKeywords.json = {'keywords': [{"name": "My TVShow", "option": "720","option2":"264", "exclude": "exclude1, exclude2" }]}
        regKeyword = self.myKeywords.getRegKeyword("My TVShow exclude1", self.tvshowRuleSetting)
        self.assertIsNone((regKeyword))
        
        regKeyword = self.myKeywords.getRegKeyword("My TVShow exclude2", self.tvshowRuleSetting)
        self.assertIsNone((regKeyword))
        
        regKeyword = self.myKeywords.getRegKeyword("My TVShow 720p x264", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), "My TVShow")

    def test_getRegKeyword_exclude_keyword_is_empty_string(self):
        self.myKeywords.json = {'keywords': [{"name": "My TVShow", "option": "","option2":"", "exclude": "" }]}
        regKeyword = self.myKeywords.getRegKeyword("My TVShow exclude1", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), "My TVShow")

    def test_getRegKeyword_exclude_keyword2(self):
        self.myKeywords.json = {'keywords': [{"name": "My TVShow", "option": "","option2":"", "exclude": "exclude" },
                                        {"name": "second title", "option": "","option2":"", "exclude": "" }]}
        regKeyword = self.myKeywords.getRegKeyword("second title", self.tvshowRuleSetting)
        self.assertEqual((regKeyword['name']), "second title")
        
if __name__ == '__main__':  
    unittest.main()