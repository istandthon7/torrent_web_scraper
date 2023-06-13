import stringHelper 
import logging
import os

class Movie(stringHelper.StringHelper):
    def __init__(self, configDirPath: str, movieSetting: dict): #mySetting.json['movie']
        self.movieSetting = movieSetting
        self.listFileName = os.path.join(configDirPath, self.movieSetting['list'])
        self.keywords = []
        if os.path.exists(self.listFileName):
            with open(self.listFileName, "r", encoding="utf-8") as f:
                self.keywords = list(filter(None, f.readlines()))

    def removeLineInMovieDotTxt(self, regKeyword: str) -> None:
        """Movie.txt에서 삭제하기"""
        if not regKeyword:
            return

        # self.keywords에서 regKeyword가 포함된 키워드를 제외한 나머지 키워드들을 선택합니다.
        self.keywords = list(filter(lambda x: regKeyword not in x, self.keywords))

        # 선택된 키워드들을 파일에 저장합니다.
        with open(self.listFileName, "w", encoding="utf-8") as f:
            f.write('\n'.join(self.keywords))

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
            
            if not self.IsContainAllWordsInBoardTitle(searchKeyword, boardTitle):
                logging.debug(f'Movie 키워드에 해당하지 않습니다.')
                continue
            if not self.IsContainAllWordsInBoardTitle(str(self.movieSetting['resolution']), boardTitle):
                logging.info(f"해상도가 달라요. 설정된 해상도: {self.movieSetting['resolution']} {boardTitle}")
                continue
            if not self.IsContainAllWordsInBoardTitle(self.movieSetting['videoCodec'], boardTitle):
                logging.info(f"코덱이 달라요. 설정된 코덱: {self.movieSetting['videoCodec']} {boardTitle}")
                continue
            return keyword
        return ""
    
