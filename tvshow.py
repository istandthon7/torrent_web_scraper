import json
from math import fabs
import configHelper
import setting

class TVShow(configHelper.ConfigHelper):
    def __init__(self, mySetting: setting.Setting):
        self.fileName = mySetting.configDirPath + mySetting.json["tvshow"]["list"]
        with open(self.fileName,"r", encoding='utf-8') as jsonFile:
            self.json = json.load(jsonFile)
        jsonFile.close()

    def getRegKeyword(self, boardTitle: str)->str:
        boardTitle = boardTitle.lower()

        for prog in self.json['title_list']:
            title = prog['name']
            option = prog['option']
            option2 = prog['option2']

            if self.checkTitleInBoardTitle(title, boardTitle) is False:
                continue
            if self.checkOptionInTitle(option, boardTitle) is False:
                continue
            if self.checkOptionInTitle(option2, boardTitle) is False:
                continue
            return title
        return ""

    def checkOptionInTitle(self, option: str, boardTitle: str)->bool:
        if option is False:
            return True
        if option.lower() in boardTitle:
            return True
        return False

    
    

    