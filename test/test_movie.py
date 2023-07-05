import os
import unittest
import movie
import setting

class MovieTest(unittest.TestCase):
    def setUp(self):
        self.mySetting = setting.Setting()
        self.movieSetting = self.mySetting.json['movie']
        self.myMovie = movie.Movie(self.movieSetting)
        self.testFilePath = os.path.join(self.mySetting.configDirPath, 'test_movie_list.json')
        open(self.testFilePath, 'w').close()
        self.myMovie.load(os.path.join(self.mySetting.configDirPath, self.testFilePath))

    def tearDown(self):
        os.remove(self.testFilePath)

    def test_getRegKeyword_대소문자_있으면(self):
        regKeywordOrg = "Title like this and that"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword_소문자만_있으면(self):
        regKeywordOrg = "title like this and that"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword(self):
        regKeywordOrg = "이런 저런 제목 2022"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword_등록된것이_없으면(self):
        regKeywordOrg = "재미난 영화"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertIsNone(regKeyword)
        
    def test_getRegKeyword_년도가_없어도(self):
        regKeywordOrg = "이런 저런 제목"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword['name'])
    
    def test_getRegKeyword_년도가_다르면(self):
        regKeywordOrg = "이런 저런 제목 2021"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertIsNone(regKeyword)

    def test_getRegKeyword_해상도가_같으면(self):
        self.myMovie.movieSetting['resolution'] = 1080
        regKeywordOrg = "이런 저런 제목"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword_해상도가_다르면(self):
        self.myMovie.movieSetting['resolution'] = 720
        regKeywordOrg = "이런 저런 제목"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertIsNone(regKeyword)

    def test_getRegKeyword_코덱이_같으면(self):
        self.myMovie.movieSetting['videoCodec'] = "264"
        regKeywordOrg = "이런 저런 제목"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword['name'])

    def test_getRegKeyword_코덱이_다르면(self):
        self.myMovie.movieSetting['videoCodec'] = "265"
        regKeywordOrg = "이런 저런 제목"
        self.myMovie.addKeyword(regKeywordOrg)
        regKeyword = self.myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertIsNone(regKeyword)

    def test_removeKeyword(self):
        # arrange
        # 직접 추가
        regKeyword = "영화제목"
        self.myMovie.addKeyword(regKeyword)

        # action
        self.myMovie.removeKeyword(regKeyword)

        # assert 
        self.assertFalse(self.myMovie.isExist(regKeyword))

    def test_removeKeyword_삭제하지말아야(self):
        # arrange
        # 키워드를 파일에 추가해 놓고
        regKeyword = "영화제목"
        self.myMovie.addKeyword(regKeyword)
        # 로딩

        # action
        self.myMovie.removeKeyword("전혀 다른 영화제목")

        # assert 
        self.assertTrue(self.myMovie.isExist(regKeyword))

    def test_removeKeyword_두개이면(self):
        # arrange
        self.myMovie.addKeyword("제목1")
        self.myMovie.addKeyword("제목2")
        self.myMovie.addKeyword("제목3")

        # action
        self.myMovie.removeKeyword("제목1")
        self.myMovie.removeKeyword("제목2")
        # assert 
        
        self.assertTrue(self.myMovie.isExist("제목3"))
        self.assertFalse(self.myMovie.isExist("제목1"))
        self.assertFalse(self.myMovie.isExist("제목2"))

    def test_removeKeyword_콜론이_들어있으면(self):
        # arrange
        regKeywordOrg = "제목: 부제"
        self.myMovie.addKeyword(regKeywordOrg)

        # action
        regKeyword = self.myMovie.getRegKeyword("제목 부제 1080 264")

        # assert 
        self.assertIsNotNone(regKeyword)

    def test_getRegKeyword_exclude_keyword(self):
        # arrange
        boardTitle = "영화제목"
        self.myMovie.addKeyword(boardTitle)
        self.myMovie.movieSetting['exclude'] = "제외"

        # action
        result = self.myMovie.getRegKeyword(boardTitle + " 제외")

        # assert
        self.assertIsNone(result)

    def test_getRegKeyword_exclude_keywords(self):
        # arrange
        boardTitle = "영화제목"
        self.myMovie.addKeyword(boardTitle)
        self.myMovie.movieSetting['exclude'] = "제외, 너도"

        # action
        result = self.myMovie.getRegKeyword(boardTitle + " 너도")

        # assert
        self.assertIsNone(result)

    def test_getRegKeyword_exclude_keyword_not_contain(self):
        # arrange
        self.myMovie.movieSetting["resolution"] = 1080
        self.myMovie.movieSetting["videoCodec"] = ''
        movieTitle = "영화제목"
        boardTitle = f"{movieTitle} 1080"
        self.myMovie.addKeyword(movieTitle)
        self.myMovie.movieSetting['exclude'] = "제외, 너도"

        # action
        result = self.myMovie.getRegKeyword(boardTitle)

        # assert
        self.assertEqual(result['name'], movieTitle)

    def test_getRegKeyword_exclude_keywords_space(self):
        # arrange
        boardTitle = "영화제목너도"
        self.myMovie.addKeyword(boardTitle)
        self.myMovie.movieSetting['exclude'] = "제외, 너도"

        # action
        result = self.myMovie.getRegKeyword(boardTitle)

        # assert
        self.assertIsNone(result)

    def test_getRegKeyword_exclude_keywords_space_word(self):
        # arrange
        boardTitle = "영화제목 너도"
        self.myMovie.addKeyword(boardTitle)
        self.myMovie.movieSetting['exclude'] = "제외, 너도"

        # action
        result = self.myMovie.getRegKeyword(boardTitle)

        # assert
        self.assertIsNone(result)

    def test_getRegKeyword_exclude_keywords_endof_comma(self):
        # arrange
        boardTitle = "영화제목 너도"
        self.myMovie.addKeyword(boardTitle)
        self.myMovie.movieSetting['exclude'] = "제외, 너도,"

        # action
        result = self.myMovie.getRegKeyword(boardTitle)

        # assert
        self.assertIsNone(result)

if __name__ == '__main__':  
    unittest.main()
    