import unittest
import movie
import setting

class MovieTest(unittest.TestCase): 
    def test_getRegKeyword_대소문자_있으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.keywords.insert(0, "Title like this and that")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_소문자만_있으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.keywords.insert(0, "title like this and that")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.keywords.insert(0, "이런 저런 제목 2022")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_등록된것이_없으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.keywords.insert(0, "재미난 영화")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(len(regKeyword), 0)
        
    def test_getRegKeyword_년도가_없어도(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.keywords.insert(0, "이런 저런 제목")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertGreater(len(regKeyword), 0)
    
    def test_getRegKeyword_년도가_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.keywords.insert(0, "이런 저런 제목 2021")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_같으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.movieSetting['resolution'] = 1080
        myMovie.keywords.insert(0, "이런 저런 제목")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.movieSetting['resolution'] = 720
        myMovie.keywords.insert(0, "이런 저런 제목")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_같으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.movieSetting['videoCodec'] = "264"
        myMovie.keywords.insert(0, "이런 저런 제목")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])
        myMovie.movieSetting['videoCodec'] = "265"
        myMovie.keywords.insert(0, "이런 저런 제목")
        regKeyword = myMovie.getRegKeyword("이런 저런 제목.Title like this and that,2022.1080p.KOR.FHDRip.H264.AAC.REEL")
        self.assertEqual(len(regKeyword), 0)

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
        self.assertFalse(myMovie.keywords)

if __name__ == '__main__':  
    unittest.main()
    