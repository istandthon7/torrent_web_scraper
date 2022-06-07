import configHelper 
import setting

class Movie(configHelper.ConfigHelper):
    def __init__(self, mySetting: setting.Setting):
        self.listFileName = mySetting.configDirPath + mySetting.json["movie"]['list']
        self.movieSetting = mySetting.json['movie']
        with open(self.listFileName, "r", encoding="utf-8") as f:
            self.keywords = f.readlines()
        f.close()

    def getRegKeyword(self, boardTitle: str)->str:
        """
        게시판 제목에 등록된 키워드가 포함되어 있으면 키워드를 반환한다.
        등록되어 있지 않다면 빈문자열을 반환한다.
        """

        for keyword in self.keywords:
            keyword = keyword.lower().rstrip("")
            if keyword == "":
                continue
            keyword = keyword.replace(":", " ")
            
            if self.IsContainAllWordsInBoardTitle(keyword, boardTitle) is False:
                continue
            if self.IsContainAllWordsInBoardTitle(self.movieSetting['resolution'], boardTitle) is False:
                continue
            if self.IsContainAllWordsInBoardTitle(self.movieSetting['video_codec'], boardTitle) is False:
                continue
            return keyword
        return ""

    def removeLineInMovie(self, matchedName: str)->None:
        """movie_list에서 삭제하기"""
        
        buffer = ""

        for line in self.keywords:
            if not matchedName in line:
                buffer += line
            else:
                # 영화리스트 파일에 매치되어 파일에 기록하지 않으니 다운받았다는 메시지다.
                # 영화는 자주 다운로드 하지 않으니 일단 로그 놔두고, 메일 받는 것으로 하자.
                print("info, remove in movie_list, matchedName = "+matchedName+", line = "+line)

        with open(self.listFileName, "w", encoding="utf-8") as f:
            f.write(buffer)
        f.close()