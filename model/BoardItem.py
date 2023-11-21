import logging
import re
from typing import Optional
from bs4 import Tag

class BoardItem:
    number : Optional[int]

    def __init__(self, title: str = '', url: str = '', ID: int = -1, number: int = -1):
        self.title = title
        self.url = url
        self.id = ID
        self.number = number

    def setItem(self, aTag: Tag, boardNumber: Optional[int]):
        self.number = boardNumber
        url = aTag.get('href')
        if url is None or not isinstance(url, str):
            logging.error("Invalid URL")
            return
        self.setUrl(str(url))
        self.id = self.getIDFromUrl(self.url)
        if self.id == -1:
            if boardNumber is None:
                self.id = -1
            else:
                self.id = boardNumber
        self.title = re.sub(r'\s+', ' ', aTag.text).strip()
    
    def setUrl(self, url: str):
        """Set the url of the BoardItem"""
        self.url = url
        if url is not None:
            self.id = self.getIDFromUrl(url)
    
    def getIDFromUrl(self, url: str) -> int:
        """게시물 아이디 파싱, url을 기반으로 wr_id text를 뒤의 id parsing"""
        
        match = re.search(r"wr_id=[^&?\n]+", url)
        if match:
            id = int(match.group().replace("wr_id=", ""))
            logging.debug(f'[T1]게시물 아이디: {id}')
            return id

        match = re.search(r"[&?](id)=([0-9]+)", url)
        if match:
            id = int(match.group(2))
            logging.debug(f'[T2]게시물 아이디: {id}')
            return id

        match = re.search(r"[/]([0-9]{6,})", url)
        if match:
            id = int(match.group(1))
            logging.debug(f'[T3]게시물 아이디: {id}')
            return id

        match = re.search(r"[/]([0-9]+)[.]html", url)
        if match:
            id = int(match.group(1))
            logging.debug(f'[T4]게시물 아이디: {id}')
            return id
        match = re.search(r"[/]([0-9]+)$", url)
        if match:
            id = int(match.group(1))
            logging.debug(f'[T5]게시물 아이디: {id}')
            return id
        return -1
