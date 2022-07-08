import unittest
import movie
import setting

class MovieTest(unittest.TestCase): 
    def test_getRegKeyword_대소문자_있으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.keywords.insert(0, "Fearless Kungfu King")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_소문자만_있으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.keywords.insert(0, "fearless kungfu king")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.keywords.insert(0, "천하종사 곽원갑 2022")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_등록된것이_없으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.keywords.insert(0, "재미난 영화")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertEqual(len(regKeyword), 0)
        
    def test_getRegKeyword_년도가_없어도(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.keywords.insert(0, "천하종사 곽원갑")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertGreater(len(regKeyword), 0)
    
    def test_getRegKeyword_년도가_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.keywords.insert(0, "천하종사 곽원갑 2021")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_같으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.movieSetting['resolution'] = 1080
        myMovie.keywords.insert(0, "천하종사 곽원갑")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.movieSetting['resolution'] = 720
        myMovie.keywords.insert(0, "천하종사 곽원갑")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_같으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.movieSetting['videoCodec'] = "264"
        myMovie.keywords.insert(0, "천하종사 곽원갑")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.movieSetting['videoCodec'] = "265"
        myMovie.keywords.insert(0, "천하종사 곽원갑")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertEqual(len(regKeyword), 0)

    def test_removeLineInMovie(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        regKeyword = "영화제목"
        myMovie.removeLineInMovie(regKeyword)
        with open(myMovie.listFileName, "a", encoding="utf-8") as f:
            f.write(regKeyword)
        f.close()

        # action
        myMovie.removeLineInMovie(regKeyword)

        # assert 
        myMovie.load()
        self.assertFalse(regKeyword in myMovie.keywords)

    def test_removeLineInMovie_삭제하지말아야(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        regKeyword = "영화제목"
        
        with open(myMovie.listFileName, "w", encoding="utf-8") as f:
            f.write(regKeyword)
        f.close()
        myMovie.load()

        # action
        myMovie.removeLineInMovie("전혀 다른 영화제목")

        # assert 
        myMovie.load()
        self.assertTrue(regKeyword in myMovie.keywords)

    def test_removeLineInMovie_두개이면(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.keywords = ["제목1\n", "제목2\n", "제목3\n"]

        # action
        myMovie.removeLineInMovie("제목1")
        myMovie.removeLineInMovie("제목2")
        # assert 
        
        self.assertTrue("제목3\n" in myMovie.keywords)
        self.assertFalse("제목1\n" in myMovie.keywords)
        self.assertFalse("제목2\n" in myMovie.keywords)

    def test_removeLineInMovie_콜론이_들어있으면(self):
        # arrange
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        regKeywordOrg = "제목: 부제\n"
        with open(myMovie.listFileName, "w", encoding="utf-8") as f:
            f.write(regKeywordOrg)
        f.close()
        myMovie.load()
        regKeyword = myMovie.getRegKeyword("제목 부제 1080 264")

        # action
        myMovie.removeLineInMovie(regKeyword)

        # assert 
        self.assertFalse(myMovie.keywords)
        myMovie.load()
        self.assertFalse(myMovie.keywords)
        
        

if __name__ == '__main__':  
    unittest.main()
    