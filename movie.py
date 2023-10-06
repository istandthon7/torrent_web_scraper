import keywords
from typing import Union
import logging

class Movie(keywords.Keywords):

    def __init__(self, movieSetting: dict): #mySetting.json['movie']
        self.movieSetting = movieSetting

    def addKeyword(self, name: str) -> None:
        newKeyword = {
            "name": name
        }
        if self.isExist(name):
            logging.info(f"이미 존재하는 키워드입니다. '{name}'")
            return
        if 'keywords' in self.json:
            self.json['keywords'].append(newKeyword)
            logging.info(f"키워드를 추가했습니다. '{newKeyword}'")
            # 저장은 직접
            #self.save()

    def getRegKeyword(self, boardTitle: str) -> Union[dict, None]:
        for keyword in self.json['keywords']:
            if not self.isWordContainedInParam(keyword['name'].replace(":", " "), boardTitle):
                logging.debug(f'[{keyword["name"]}] 키워드에 해당하지 않습니다. {boardTitle}')
                continue
            if 'exclude' in self.movieSetting and self.movieSetting['exclude'] and self.IsContainAnyCommaSeparatedWordsInBoardTitle(self.movieSetting['exclude'], boardTitle):
                logging.info(f"[{keyword['name']}] 제외 키워드가 포함되어 있어요. [{self.movieSetting['exclude']}] '{boardTitle}'")
                continue
            if not self.isWordContainedInParam(str(self.movieSetting['resolution']), boardTitle):
                logging.info(f"[{keyword['name']}] 해상도가 달라요. [{self.movieSetting['resolution']}] '{boardTitle}'")
                continue
            if not self.isWordContainedInParam(self.movieSetting['videoCodec'], boardTitle):
                logging.info(f"[{keyword['name']}] 코덱이 달라요. [{self.movieSetting['videoCodec']}] '{boardTitle}'")
                continue
            return keyword
