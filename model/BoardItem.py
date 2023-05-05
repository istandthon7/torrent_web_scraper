import logging
import re


class BoardItem:
    episode = 0
    resolution = 480

    def __init__(self, title: str, url: str, ID: int, number: int) -> None:
        self.title = title
        self.url = url
        self.id = ID
        self.number = number
    
    def getEpisode(self) -> int:
        if self.episode > 0:
            return self.episode;
        match = re.search(r'[Ee](\d+)', self.title)
        if match:
            self.episode = int(match.group(1))
            logging.debug(f'에피소드 번호: {self.episode}')
        else:
            logging.debug('에피소드 번호를 찾을 수 없습니다')
        return self.episode