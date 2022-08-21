import configHelper 
import setting
import logging

class Movie(configHelper.ConfigHelper):
    def __init__(self, mySetting: setting.Setting):
        self.listFileName = mySetting.configDirPath + mySetting.json["movie"]['list']
        self.movieSetting = mySetting.json['movie']
        self.load()

    def load(self)->None:
        with open(self.listFileName, "r", encoding="utf-8") as f:
            self.keywords = list(filter(None, f.readlines()))
        f.close()

    def getRegKeyword(self, boardTitle: str)->str:
        """
        게시판 제목에 등록된 키워드가 포함되어 있으면 키워드를 반환한다.
        등록되어 있지 않다면 빈문자열을 반환한다.
        """
        for keyword in self.keywords:
            keyword = keyword.rstrip("\r\n")
            searchKeyword = keyword.lower()
            if searchKeyword == "":
                continue
            searchKeyword = searchKeyword.replace(":", " ")
            
            if self.IsContainAllWordsInBoardTitle(searchKeyword, boardTitle) is False:
                logging.debug(f'Movie 키워드에 해당하지 않습니다.')
                continue
            if self.IsContainAllWordsInBoardTitle(str(self.movieSetting['resolution']), boardTitle) is False:
                logging.info(f"해상도가 달라요. 설정된 해상도: {self.movieSetting['resolution']}")
                continue
            if self.IsContainAllWordsInBoardTitle(self.movieSetting['videoCodec'], boardTitle) is False:
                logging.info(f"코덱이 달라요. 설정된 코덱: {self.movieSetting['videoCodec']}")
                continue
            return keyword
        return ""

    def removeLineInMovie(self, regKeyword: str)->None:
        """movie_list에서 삭제하기"""
        if not regKeyword:
            return
        buffer = ""

        for keyword in self.keywords:
            if keyword == "":
                continue

            if not regKeyword in keyword:
                buffer += keyword
            else:
                # 영화리스트 파일에 매치되어 파일에 기록하지 않으니 다운받았다는 메시지다.
                # 영화는 자주 다운로드 하지 않으니 일단 로그 놔두고, 메일 받는 것으로 하자.
                print("info, remove in movie_list, matchedName = "+regKeyword+", line = "+keyword)
        self.keywords = list(filter(None, buffer.split("\n")))
        for index in range(len(self.keywords)):
            if self.keywords[index].endswith("\n") == False:
                self.keywords[index] += "\n"
        with open(self.listFileName, "w", encoding="utf-8") as f:
            f.write(buffer)
        f.close()