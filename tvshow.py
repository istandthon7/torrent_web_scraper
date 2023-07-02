import json
from typing import Union
import stringHelper
import logging
import re

class TVShow(stringHelper.StringHelper):
    def load(self, listFileName: str):
        with open(listFileName,"r", encoding='utf-8') as jsonFile:
            self.json = json.load(jsonFile)

    def getRegKeyword(self, boardTitle: str)->str:
        for tvShow in self.json['title_list']:
            if not self.IsContainAllWordsInBoardTitle(tvShow['name'], boardTitle):
                logging.debug(f'[{tvShow["name"]}] tvshow 키워드에 해당하지 않습니다. {boardTitle}')
                continue
            if 'exclude' in tvShow and tvShow['exclude'] and self.IsContainAnyCommaSeparatedWordsInBoardTitle(tvShow['exclude'], boardTitle):
                logging.info(f"[{tvShow['name']}] 제외 키워드가 포함되어 있어요. [{tvShow['exclude']}]")
                continue
            if not self.IsContainAllWordsInBoardTitle(tvShow['option'], boardTitle):
                logging.info(f"[{tvShow['name']}] option이 달라요. [{tvShow['option']}]")
                continue
            if not self.IsContainAllWordsInBoardTitle(tvShow['option2'], boardTitle):
                logging.info(f"[{tvShow['name']}] option2가 달라요. [{tvShow['option2']}]")
                continue
            return tvShow['name']
        return "" 

    def getEpisodeNumber(self, boardTitle: str) -> Union[int, None]:
        match = re.search(r'[\.\s][Ss]?\d*[Ee](\d+)', boardTitle)
        if match:
            episode = int(match.group(1))
            logging.debug(f'에피소드 번호: {episode}')
            return episode
        logging.debug('에피소드 번호를 찾을 수 없습니다')
        return None
