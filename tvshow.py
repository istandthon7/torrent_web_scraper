import json
import configHelper
import setting

class TVShow(configHelper.ConfigHelper):
    def __init__(self, mySetting: setting.Setting):
        self.fileName = mySetting.configDirPath + mySetting.json["tvshow"]["list"]
        with open(self.fileName,"r", encoding='utf-8') as jsonFile:
            self.json = json.load(jsonFile)
        jsonFile.close()

    def getRegKeyword(self, boardTitle: str)->str:
        for tvShow in self.json['title_list']:
            if self.IsContainAllWordsInBoardTitle(tvShow['name'], boardTitle) is False:
                continue
            if self.IsContainAllWordsInBoardTitle(tvShow['option'], boardTitle) is False:
                continue
            if self.IsContainAllWordsInBoardTitle( tvShow['option2'], boardTitle) is False:
                continue
            return tvShow['name']
        return "" 