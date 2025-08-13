import os
import unittest
import keywords
import setting


class KeywordsTest3(unittest.TestCase): 
    def setUp(self):
        mySetting = setting.Setting()
        self.myKeywords = keywords.Keywords()
        self.downloadRuleSetting = next((rule for rule in mySetting.json['downloadRules'] if rule['name'] == 'tvshow'), None)
        self.myKeywords.load(mySetting.configDirPath, self.downloadRuleSetting)
        
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
        self.myKeywords.json = {'keywords': [{"name": "My Title", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 제목 시즌01 My Title S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword['name']), "My Title")

    def test_getRegKeyword_소문자만_있으면(self):
        self.myKeywords.json = {'keywords': [{"name": "my title", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 제목 시즌01 My Title S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword['name']), "my title")

    def test_getRegKeyword(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 제목", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 제목 시즌01 My Title S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword['name']), "나의 제목")
        
    def test_getRegKeyword2(self):
        self.myKeywords.json = {'keywords': [{"name": ".23", "option": "","option2":"", "exclude": "" }]}
        regKeyword = self.myKeywords.getRegKeyword("검은 김의 세계일2.E02.230618.1080p.WANNA")
        self.assertEqual((regKeyword['name']), ".23")

    def test_getRegKeyword_시즌이_없어도(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 제목", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 제목 시즌01 My Title S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword['name']), "나의 제목")
    
    def test_getRegKeyword_시즌이_다르면(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 제목 시즌02", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 제목 시즌01 My Title S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(regKeyword, {})

    def test_getRegKeyword_option_같으면(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 제목", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 제목 시즌01 My Title S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword['name']), "나의 제목")

    def test_getRegKeyword_option_다르면(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 제목", "option": "1080","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 제목 시즌01 My Title S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(regKeyword, {})

    def test_getRegKeyword_option2_같으면(self):
        self.myKeywords.json = {'keywords': [{"name": "나의 제목", "option": "720","option2":"264" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 제목 시즌01 My Title S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual((regKeyword['name']), "나의 제목")

    def test_getRegKeyword_option2_다르면(self):
        self.myKeywords.json ={'keywords': [{"name": "나의 제목", "option": "720","option2":"265" }]}
        regKeyword = self.myKeywords.getRegKeyword("나의 제목 시즌01 My Title S01 720p.KOR.HDRip.H264.AAC-RTM")
        self.assertEqual(regKeyword, {})

    def test_getRegKeyword_exclude_keyword(self):
        self.myKeywords.json = {'keywords': [{"name": "My Title", "option": "720","option2":"264", "exclude": "exclude1, exclude2" }]}
        regKeyword = self.myKeywords.getRegKeyword("My Title exclude1")
        self.assertEqual(regKeyword, {})
        
        regKeyword = self.myKeywords.getRegKeyword("My Title exclude2")
        self.assertEqual(regKeyword, {})
        
        regKeyword = self.myKeywords.getRegKeyword("My Title 720p x264")
        self.assertEqual((regKeyword['name']), "My Title")

    def test_getRegKeyword_exclude_keyword_is_empty_string(self):
        self.myKeywords.json = {'keywords': [{"name": "My Title", "option": "","option2":"", "exclude": "" }]}
        regKeyword = self.myKeywords.getRegKeyword("My Title exclude1")
        self.assertEqual((regKeyword['name']), "My Title")

    def test_getRegKeyword_exclude_keyword2(self):
        self.myKeywords.json = {'keywords': [{"name": "My Title", "option": "","option2":"", "exclude": "exclude" },
                                        {"name": "second title", "option": "","option2":"", "exclude": "" }]}
        regKeyword = self.myKeywords.getRegKeyword("second title")
        self.assertEqual((regKeyword['name']), "second title")
        
if __name__ == '__main__':  
    unittest.main()