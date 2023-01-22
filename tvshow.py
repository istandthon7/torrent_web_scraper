import json
import stringHelper
import setting
import logging

class TVShow(stringHelper.StringHelper):
    def __init__(self, mySetting: setting.Setting):
        self.fileName = mySetting.configDirPath + mySetting.json["tvshow"]["list"]
        with open(self.fileName,"r", encoding='utf-8') as jsonFile:
            self.json = json.load(jsonFile)
        jsonFile.close()

    def getRegKeyword(self, boardTitle: str)->str:
        for tvShow in self.json['title_list']:
            if self.IsContainAllWordsInBoardTitle(tvShow['name'], boardTitle) is False:
                logging.debug(f'tvshow 키워드에 해당하지 않습니다.')
                continue
            if self.IsContainAllWordsInBoardTitle(tvShow['option'], boardTitle) is False:
                logging.info(f"option이 달라요. option: {tvShow['option']}")
                continue
            if self.IsContainAllWordsInBoardTitle(tvShow['option2'], boardTitle) is False:
                logging.info(f"option2가 달라요. option2: {tvShow['option2']}")
                continue
            return tvShow['name']
        return "" 