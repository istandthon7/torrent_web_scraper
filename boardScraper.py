import argparse
import json
import logging
import re
from model.BoardItem import BoardItem
from typing import List
import scraperHelpers
import setting
from urllib import parse

class BoardScraper():
    def getScrapUrl(self, url: str, page: int) -> str:
        if page > 1:
            if not "?" in url:
                url += "?"
            return f"{url}&page={page}"
        else:
            return url

    def getBoardItems(self, urlOrFilePath: str, page: int, titleTag: str, titleClass: str, titleSelector: str)->List[BoardItem]:
        """
        게시판에서 제목리스트 얻기
        """
        logging.debug(f'게시판에서 제목리스트를 추출합니다. {urlOrFilePath}, tag: {titleTag}, class: {titleClass}, selecotr: {titleSelector}')
        if urlOrFilePath.startswith("http"):
            urlOrFilePath = self.getScrapUrl(urlOrFilePath, page)
            soup = scraperHelpers.getSoup(urlOrFilePath)
        else:
            soup = scraperHelpers.getSoupFromFile(urlOrFilePath)
        if soup is None:
            return [];
        if not titleSelector:
            titles = soup.find_all(titleTag, class_=titleClass)
        else:
            titles = soup.select(titleSelector)
        if not titles:
            return [];
        results = []
        for title in titles:
            aTags = [a for a in title.find_all('a') if len(a.text.strip()) >= 10]
            aTag = aTags[-1] if aTags else None
            if not aTag:
                logging.debug("게시물 제목을 찾을 수 없어요.")
                continue
            if aTag.get('href') == "#":
                logging.debug("지원되지 않는 링크")
                continue

            # 하위 태그 중에 클래스에 icon, badge, comment가 포함되어 있는 태그를 삭제
            for unwanted_tag in aTag.find_all(True, {'class': ['icon', 'badge', 'comment']}):
                unwanted_tag.extract()

            boardNumber = None
            for child in title.descendants:
                if child.name and re.fullmatch(r'\d+', child.text.strip()):
                    boardNumber = child.text.strip()
                    break
            logging.debug(f"게시물 번호: {boardNumber}")

            boardItem = BoardItem()
            # boardNumber: int? 
            boardItem.setItem(aTag, int(boardNumber) if boardNumber else None)
            if boardItem.id is None:
                logging.info(f"게시물 아이디를 확인할 수 없습니다. '{boardItem.title}''")
            elif boardItem.id > 10:
                results.append(boardItem)

        return results
 
    def intTryParse(self, value):
        try:
            return int(value)
        except ValueError:
            return ;

    def getMagnet(self, url: str)->str:
        logging.debug(f'magnet을 검색합니다. url: {url}')
        html = scraperHelpers.getHtml(url)

        if not html:
            logging.error(f'url로부터 html을 얻지 못했어요. url: {url}')
            return ""
        
        match = re.search(r"[ :]([A-Za-z0-9]){40}[^\w.]", html)
        if match:
            logging.debug(f'magnet을 찾았어. {match.group()[1:-1]}')
            return "magnet:?xt=urn:btih:"+ match.group()[1:-1]
        f = open("/tmp/magnet_fail.html", 'w')
        f.write(html)
        f.close()
        logging.error(f'html에서 magnet을 찾지 못했어요. url: {url}')
        return ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("urlOrFilePath", help="스크랩할 url이나 html파일경로")
    parser.add_argument("--titleTag", help="제목 태그")
    parser.add_argument("--titleClass", help="제목 클래스")
    parser.add_argument("--titleSelector", help="제목 selector")
    args = parser.parse_args()
    # 로그파일 초기화용
    mySetting = setting.Setting()
    myBoardScraper = BoardScraper()
    # 매그넷 구하기
    if args.titleTag is not None or args.titleSelector is not None:
        logging.info(f'스크랩 테스트를 시작합니다. [{args.urlOrFilePath}], selector: [{args.titleSelector}], tag: [{args.titleTag}], class: [{args.titleClass}]')
        boardItems = myBoardScraper.getBoardItems(args.urlOrFilePath, 1, args.titleTag, args.titleClass, args.titleSelector)
        if not boardItems:
            logging.error(f"게시판에서 제목리스트 얻기에 실패하였습니다.")
        print(json.dumps(boardItems, default=lambda x: x.__dict__))
        logging.info("스크랩 테스트를 마쳤습니다.")
    else:
        url = parse.unquote(args.urlOrFilePath)
        print(myBoardScraper.getMagnet(url))