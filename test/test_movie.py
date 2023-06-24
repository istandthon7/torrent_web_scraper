import unittest
import movie
import setting

class MovieTest(unittest.TestCase): 
    def test_getRegKeyword_대소문자_있으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        regKeywordOrg = "Title like this and that"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword)

    def test_getRegKeyword_소문자만_있으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        regKeywordOrg = "title like this and that"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword)

    def test_getRegKeyword(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        regKeywordOrg = "이런 저런 제목 2022"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword)

    def test_getRegKeyword_등록된것이_없으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        regKeywordOrg = "재미난 영화"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual("", regKeyword)
        
    def test_getRegKeyword_년도가_없어도(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        regKeywordOrg = "이런 저런 제목"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword)
    
    def test_getRegKeyword_년도가_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        regKeywordOrg = "이런 저런 제목 2021"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual("", regKeyword)

    def test_getRegKeyword_해상도가_같으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.movieSetting['resolution'] = 1080
        regKeywordOrg = "이런 저런 제목"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword)

    def test_getRegKeyword_해상도가_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.movieSetting['resolution'] = 720
        regKeywordOrg = "이런 저런 제목"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual("", regKeyword)

    def test_getRegKeyword_코덱이_같으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.movieSetting['videoCodec'] = "264"
        regKeywordOrg = "이런 저런 제목"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(regKeywordOrg, regKeyword)

    def test_getRegKeyword_코덱이_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.movieSetting['videoCodec'] = "265"
        regKeywordOrg = "이런 저런 제목"
        myMovie.keywords.insert(0, regKeywordOrg)
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual("", regKeyword)

    def test_removeLineInMovie(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        # 직접 추가
        regKeyword = "영화제목"
        myMovie.removeLineInMovieDotTxt(regKeyword)
        with open(mySetting.json['movie']['list'], "a", encoding="utf-8") as f:
            f.write(regKeyword)

        # action
        myMovie.removeLineInMovieDotTxt(regKeyword)

        # assert 
        self.assertFalse(regKeyword in myMovie.keywords)

    def test_removeLineInMovie_삭제하지말아야(self):
        # arrange
        mySetting = setting.Setting()
        # 키워드를 파일에 추가해 놓고
        regKeyword = "영화제목"
        with open(mySetting.configDirPath+mySetting.json['movie']['list'], "w", encoding="utf-8") as f:
            f.write(regKeyword)
        # 로딩
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])

        # action
        myMovie.removeLineInMovieDotTxt("전혀 다른 영화제목")

        # assert 
        self.assertTrue(regKeyword in myMovie.keywords)

    def test_removeLineInMovie_두개이면(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.keywords = ["제목1\n", "제목2\n", "제목3\n"]

        # action
        myMovie.removeLineInMovieDotTxt("제목1")
        myMovie.removeLineInMovieDotTxt("제목2")
        # assert 
        
        self.assertTrue("제목3\n" in myMovie.keywords)
        self.assertFalse("제목1\n" in myMovie.keywords)
        self.assertFalse("제목2\n" in myMovie.keywords)

    def test_removeLineInMovie_콜론이_들어있으면(self):
        # arrange
        mySetting = setting.Setting()
        regKeywordOrg = "제목: 부제\n"
        with open(mySetting.configDirPath+mySetting.json['movie']['list'], "w", encoding="utf-8") as f:
            f.write(regKeywordOrg)

        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        regKeyword = myMovie.getRegKeyword("제목 부제 1080 264")

        # action
        myMovie.removeLineInMovieDotTxt(regKeyword)

        # assert 
        self.assertFalse(myMovie.keywords)

    def test_getRegKeyword_exclude_keyword(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        boardTitle = "영화제목"
        myMovie.keywords.append(boardTitle)
        myMovie.movieSetting['exclude'] = "제외"

        # action
        result = myMovie.getRegKeyword(boardTitle + " 제외")

        # assert
        self.assertEqual(result, "")

    def test_getRegKeyword_exclude_keywords(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        boardTitle = "영화제목"
        myMovie.keywords.append(boardTitle)
        myMovie.movieSetting['exclude'] = "제외, 너도"

        # action
        result = myMovie.getRegKeyword(boardTitle + " 너도")

        # assert
        self.assertEqual(result, "")

    def test_getRegKeyword_exclude_keyword_not_contain(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.movieSetting["resolution"] = 1080
        myMovie.movieSetting["videoCodec"] = ''
        movieTitle = "영화제목"
        boardTitle = f"{movieTitle} 1080"
        myMovie.keywords.append(movieTitle)
        myMovie.movieSetting['exclude'] = "제외, 너도"

        # action
        result = myMovie.getRegKeyword(boardTitle)

        # assert
        self.assertEqual(result, movieTitle)

    def test_getRegKeyword_exclude_keywords_space(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        boardTitle = "영화제목너도"
        myMovie.keywords.append(boardTitle)
        myMovie.movieSetting['exclude'] = "제외, 너도"

        # action
        result = myMovie.getRegKeyword(boardTitle)

        # assert
        self.assertEqual(result, "")

    def test_getRegKeyword_exclude_keywords_space_word(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        boardTitle = "영화제목 너도"
        myMovie.keywords.append(boardTitle)
        myMovie.movieSetting['exclude'] = "제외, 너도"

        # action
        result = myMovie.getRegKeyword(boardTitle)

        # assert
        self.assertEqual(result, "")

    def test_getRegKeyword_exclude_keywords_endof_comma(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        boardTitle = "영화제목 너도"
        myMovie.keywords.append(boardTitle)
        myMovie.movieSetting['exclude'] = "제외, 너도,"

        # action
        result = myMovie.getRegKeyword(boardTitle)

        # assert
        self.assertEqual(result, "")

if __name__ == '__main__':  
    unittest.main()
    