import keywords
import os
import unittest
import setting

class KeywordsTest2(unittest.TestCase):
    def setUp(self):
        mySetting = setting.Setting()
        # 'downloadRules' 섹션에서 'name'이 'movie'인 설정을 찾습니다.
        self.movieRuleSetting = next(rule for rule in mySetting.json['downloadRules'] if rule['name'] == 'movie')
        self.myKeywords = keywords.Keywords()
        self.testFilePath = os.path.join(mySetting.configDirPath, 'test_movie_list.json')
        open(self.testFilePath, 'w').close()
        self.myKeywords.load(os.path.join(mySetting.configDirPath, self.testFilePath))

    def tearDown(self):
        os.remove(self.testFilePath)

    def test_getRegKeyword_대소문자_있으면(self):
        regKeywordOrg = "Title like this and that"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword_소문자만_있으면(self):
        regKeywordOrg = "title like this and that"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword(self):
        regKeywordOrg = "이런 저런 제목 2022"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword_등록된것이_없으면(self):
        regKeywordOrg = "재미난 영화"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertIsNone(regKeyword)
        
    def test_getRegKeyword_년도가_없어도(self):
        regKeywordOrg = "이런 저런 제목"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertEqual(regKeywordOrg, regKeyword['name'])
    
    def test_getRegKeyword_년도가_다르면(self):
        regKeywordOrg = "이런 저런 제목 2021"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertIsNone(regKeyword)

    def test_getRegKeyword_해상도가_같으면(self):
        self.movieRuleSetting['include'] = "1080"
        regKeywordOrg = "이런 저런 제목"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword_해상도가_다르면(self):
        self.movieRuleSetting['include'] = "720"
        regKeywordOrg = "이런 저런 제목"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertIsNone(regKeyword)

    def test_getRegKeyword_코덱이_같으면(self):
        self.movieRuleSetting['include'] = "264"
        regKeywordOrg = "이런 저런 제목"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword_코덱이_다르면(self):
        self.movieRuleSetting['include'] = "265"
        regKeywordOrg = "이런 저런 제목"
        self.myKeywords.addKeyword(regKeywordOrg)
        regKeyword = self.myKeywords.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL", self.movieRuleSetting)
        self.assertIsNone(regKeyword)

    def test_removeKeyword(self):
        # arrange
        # 직접 추가
        regKeyword = "영화제목"
        self.myKeywords.addKeyword(regKeyword)

        # action
        self.myKeywords.removeKeyword(regKeyword)

        # assert 
        self.assertFalse(self.myKeywords.isExist(regKeyword))

    def test_removeKeyword_삭제하지말아야(self):
        # arrange
        # 키워드를 파일에 추가해 놓고
        regKeyword = "영화제목"
        self.myKeywords.addKeyword(regKeyword)
        # 로딩

        # action
        self.myKeywords.removeKeyword("전혀 다른 영화제목")

        # assert 
        self.assertTrue(self.myKeywords.isExist(regKeyword))

    def test_removeKeyword_두개이면(self):
        # arrange
        self.myKeywords.addKeyword("제목1")
        self.myKeywords.addKeyword("제목2")
        self.myKeywords.addKeyword("제목3")

        # action
        self.myKeywords.removeKeyword("제목1")
        self.myKeywords.removeKeyword("제목2")
        # assert 
        
        self.assertTrue(self.myKeywords.isExist("제목3"))
        self.assertFalse(self.myKeywords.isExist("제목1"))
        self.assertFalse(self.myKeywords.isExist("제목2"))

    def test_removeKeyword_콜론이_들어있으면(self):
        # arrange
        regKeywordOrg = "제목: 부제"
        self.myKeywords.addKeyword(regKeywordOrg)

        # action
        regKeyword = self.myKeywords.getRegKeyword("제목 부제 1080 264", self.movieRuleSetting)

        # assert 
        self.assertIsNotNone(regKeyword)

    def test_getRegKeyword_exclude_keyword(self):
        # arrange
        boardTitle = "영화제목"
        self.myKeywords.addKeyword(boardTitle)
        self.movieRuleSetting['exclude'] = "제외"

        # action
        result = self.myKeywords.getRegKeyword(boardTitle + " 제외", self.movieRuleSetting)

        # assert
        self.assertIsNone(result)

    def test_getRegKeyword_exclude_keywords(self):
        # arrange
        boardTitle = "영화제목"
        self.myKeywords.addKeyword(boardTitle)
        self.movieRuleSetting['exclude'] = "제외, 너도"

        # action
        result = self.myKeywords.getRegKeyword(boardTitle + " 너도", self.movieRuleSetting)

        # assert
        self.assertIsNone(result)

    def test_getRegKeyword_exclude_keyword_not_contain(self):
        # arrange
        self.movieRuleSetting["include"] = "1080"
        movieTitle = "영화제목"
        boardTitle = f"{movieTitle} 1080"
        self.myKeywords.addKeyword(movieTitle)
        self.movieRuleSetting['exclude'] = "제외, 너도"

        # action
        result = self.myKeywords.getRegKeyword(boardTitle, self.movieRuleSetting)

        # assert
        self.assertEqual(result['name'], movieTitle)

    def test_getRegKeyword_exclude_keywords_space(self):
        # arrange
        boardTitle = "영화제목너도"
        self.myKeywords.addKeyword(boardTitle)
        self.movieRuleSetting['exclude'] = "제외, 너도"

        # action
        result = self.myKeywords.getRegKeyword(boardTitle, self.movieRuleSetting)

        # assert
        self.assertIsNone(result)

    def test_getRegKeyword_exclude_keywords_space_word(self):
        # arrange
        boardTitle = "영화제목 너도"
        self.myKeywords.addKeyword(boardTitle)
        self.movieRuleSetting['exclude'] = "제외, 너도"

        # action
        result = self.myKeywords.getRegKeyword(boardTitle, self.movieRuleSetting)

        # assert
        self.assertIsNone(result)

    def test_getRegKeyword_exclude_keywords_endof_comma(self):
        # arrange
        boardTitle = "영화제목 너도"
        self.myKeywords.addKeyword(boardTitle)
        self.movieRuleSetting['exclude'] = "제외, 너도,"

        # action
        result = self.myKeywords.getRegKeyword(boardTitle, self.movieRuleSetting)

        # assert
        self.assertIsNone(result)

if __name__ == '__main__':  
    unittest.main()
    