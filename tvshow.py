import json
import stringHelper
import logging
import re

class TVShow(stringHelper.StringHelper):
    def load(self, listFileName: str):
        with open(listFileName,"r", encoding='utf-8') as jsonFile:
            self.json = json.load(jsonFile)

    def getRegKeyword(self, boardTitle: str)->str:
        for tvShow in self.json['title_list']:
            if 'exclude' in tvShow and tvShow['exclude'] and self.IsContainAnyCommaSeparatedWordsInBoardTitle(tvShow['exclude'], boardTitle):
                logging.info(f"[{tvShow['name']}] 제외 키워드가 포함되어 있어요. [{tvShow['exclude']}]")
                continue
            if not self.IsContainAllWordsInBoardTitle(tvShow['name'], boardTitle):
                logging.debug(f'tvshow 키워드에 해당하지 않습니다.')
                continue
            if not self.IsContainAllWordsInBoardTitle(tvShow['option'], boardTitle):
                logging.info(f"[{tvShow['name']}] option이 달라요. [{tvShow['option']}]")
                continue
            if not self.IsContainAllWordsInBoardTitle(tvShow['option2'], boardTitle):
                logging.info(f"[{tvShow['name']}] option2가 달라요. [{tvShow['option2']}]")
                continue
            return tvShow['name']
        return "" 

    def getEpisodeNumber(self, boardTitle: str) -> int:
        match = re.search(r'\.E(\d+)\.', boardTitle)
        if match:
            return int(match.group(1))
        else:
            return None
