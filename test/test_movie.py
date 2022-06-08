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
        myMovie.movieSetting['resolution'] = "1080"
        myMovie.keywords.insert(0, "천하종사 곽원갑")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_해상도가_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.movieSetting['resolution'] = "720"
        myMovie.keywords.insert(0, "천하종사 곽원갑")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertEqual(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_같으면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.movieSetting['video_codec'] = "264"
        myMovie.keywords.insert(0, "천하종사 곽원갑")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertGreater(len(regKeyword), 0)

    def test_getRegKeyword_코덱이_다르면(self):
        mySetting = setting.Setting()
        myMovie = movie.Movie(mySetting)
        myMovie.movieSetting['video_codec'] = "265"
        myMovie.keywords.insert(0, "천하종사 곽원갑")
        regKeyword = myMovie.getRegKeyword("[액션] 천하종사 곽원갑 Fearless Kungfu King,2022.1080p.KOR.FHDRip.H264.AAC-REEL")
        self.assertEqual(len(regKeyword), 0)

if __name__ == '__main__':  
    unittest.main()