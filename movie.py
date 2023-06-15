import stringHelper 
import logging
import os

class Movie(stringHelper.StringHelper):
    keywords = []

    def __init__(self, configDirPath: str, movieSetting: dict): #mySetting.json['movie']
        self.movieSetting = movieSetting
        self.listFileName = os.path.join(configDirPath, self.movieSetting['list'])
        if os.path.exists(self.listFileName):
            with open(self.listFileName, "r", encoding="utf-8") as f:
                self.keywords = [line.rstrip("\r\n") for line in f if line.strip()]

    def removeLineInMovieDotTxt(self, regKeyword: str) -> None:
        """Movie.txt에서 삭제하기"""
        if not regKeyword:
            return

        # self.keywords에서 regKeyword가 포함된 키워드를 찾아서 제거합니다.
        for i, keyword in enumerate(self.keywords):
            if regKeyword in keyword:
                del self.keywords[i]
                with open(self.listFileName, "w", encoding="utf-8") as f:
                    f.write('\n'.join(self.keywords))
                break

    def getRegKeyword(self, boardTitle: str)->str:
        """
        게시판 제목에 등록된 키워드가 포함되어 있으면 키워드를 반환한다.
        등록되어 있지 않다면 빈문자열을 반환한다.
        """
        filtered_keywords = filter(lambda keyword: keyword.rstrip("\r\n").replace(":", " ") != "", map(lambda keyword: keyword.lower(), self.keywords))

        if 'exclude' in self.movieSetting and self.movieSetting['exclude'] and self.IsContainAnyCommaSeparatedWordsInBoardTitle(self.movieSetting['exclude'], boardTitle):
            logging.info(f"[{boardTitle}] 제외 키워드가 포함되어 있어요. [{self.movieSetting['exclude']}]")
            return ""
        for keyword in filtered_keywords:
            if not self.IsContainAllWordsInBoardTitle(keyword, boardTitle):
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
    
