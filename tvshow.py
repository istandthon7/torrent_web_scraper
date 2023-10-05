import keywords
import logging
import re
from typing import Union

class TVShow(keywords.Keywords):

    def getRegKeyword(self, boardTitle: str) -> Union[dict, None]:
        for keyword in self.json['keywords']:
            if not self.isShorterParamWordsContainedInLongerParam(keyword['name'], boardTitle):
                logging.debug(f'[{keyword["name"]}] tvshow 키워드에 해당하지 않습니다. {boardTitle}')
                continue
            if 'exclude' in keyword and keyword['exclude'] and self.IsContainAnyCommaSeparatedWordsInBoardTitle(keyword['exclude'], boardTitle):
                logging.info(f"[{keyword['name']}] 제외 키워드가 포함되어 있어요. [{keyword['exclude']}]")
                continue
            if not self.isShorterParamWordsContainedInLongerParam(keyword['option'], boardTitle):
                logging.info(f"[{keyword['name']}] option이 달라요. [{keyword['option']}] '{boardTitle}'")
                continue
            if not self.isShorterParamWordsContainedInLongerParam(keyword['option2'], boardTitle):
                logging.info(f"[{keyword['name']}] option2가 달라요. [{keyword['option2']}] '{boardTitle}'")
                continue
            return keyword

    def getEpisodeNumber(self, boardTitle: str) -> Union[int, None]:
        match = re.search(r'[\.\s][Ss]?\d*[Ee](\d+)', boardTitle)
        if match:
            episode = int(match.group(1))
            logging.debug(f'에피소드 번호: {episode}')
            return episode
        logging.debug('에피소드 번호를 찾을 수 없습니다')
        return None
