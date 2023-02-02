import argparse
import json
import logging
import re
import bs4
import scraperHelpers
import setting
from urllib import parse

class BoardItemInfo:
    def __init__(self, title: str, url: str, ID: int, number: int) -> None:
        self.title = title
        self.url = url
        self.id = ID
        self.number = number

class BoardScraper():
    def getScrapUrl(self, url: str, page: int)->str:
        if page > 1:
            if not "?" in url:
                url += "?"
            return url + "&page="+str(page)
        else:
            return url

    def getBoardItemInfos(self, urlOrFilePath: str, page: int, titleTag: str, titleClass: str)->list:
        """
        게시판에서 제목리스트 얻기
        """
        logging.debug(f'게시판에서 제목리스트를 추출합니다. {urlOrFilePath}, tag: {titleTag}, class: {titleClass}')
        if urlOrFilePath.startswith("http"):
            urlOrFilePath = self.getScrapUrl(urlOrFilePath, page)
            soup = scraperHelpers.getSoup(urlOrFilePath)
        else:
            soup = scraperHelpers.getSoupFromFile(urlOrFilePath)
        
        titles = soup.find_all(titleTag, class_=titleClass)
        if titles is None or not any(titles):
            logging.error(f"게시판에서 제목리스트 얻기에 실패하였습니다. {urlOrFilePath}, tag: {titleTag}, class: {titleClass}")
            return [];
        results = []
        for title in titles:
            aTag = title.a
            if len(aTag.text.strip()) == 0 or aTag.get('href') == "#":
                continue;
        
            title.parent.contents.remove('\n')
            boardNumber = title.parent.contents[0].string.strip()
            boardItemInfo = self.GetBoardItemInfo(aTag, int(boardNumber))
            if boardItemInfo.id > 10:
                results.append(boardItemInfo)
            elif boardItemInfo.id == -1:
                logging.info(f"게시물 아이디를 확인할 수 없습니다. title: {boardItemInfo.title}")

        return results
 
    #게시판 아이디 파싱, url을 기반으로 wr_id text를 뒤의 id parsing
    def getID(self, url: str)->int:

        match = re.search(r"wr_id=[^&?\n]+", url)
        if match:
            return int(match.group().replace("wr_id=", ""))

        match = re.search(r"[&?](id)=[0-9]+", url)
        if match:
            return int(match.group().replace("&", "").replace("?","").replace("id=", ""))

        match = re.search(r"[/][0-9]{6,}", url)
        if match:
            return int(match.group().replace("/",""))

        match = re.search(r"([0-9]){6,}", url)
        if match:
            return int(match.group())
        #print("게시물 아이디 얻기에 실패하였습니다. "+url)
        return -1

    def GetBoardItemInfo(self, aTag: bs4.element.Tag, boardNumber: int) -> BoardItemInfo:
        url = aTag.get('href')
        boardItemInfo = BoardItemInfo(aTag.text.strip(), url, self.getID(url), boardNumber)
        return boardItemInfo

    def getMagnet(self, url: str)->str:
        logging.debug(f'magnet을 검색합니다. url: {url}')
        html = scraperHelpers.getHtml(url)

        if html is None:
            logging.error(f'url로부터 html을 얻지 못했어요. url: {url}')
            return ""
        
        match = re.search(r"[^\w]([A-Za-z0-9]){40}[^\w]", html)
        if match:
            return "magnet:?xt=urn:btih:"+ match.group()[1:-1]
        f = open("/tmp/magnet.html", 'w')
        f.write(html)
        f.close()
        logging.error(f'html에서 magnet을 찾지 못했어요. url: {url}')
        return ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("urlOrFilePath", help="스크랩할 url이나 html파일경로")
    parser.add_argument("--titleTag", help="제목 태그")
    parser.add_argument("--titleClass", help="제목 클래스")
    args = parser.parse_args()
    # 로그파일 초기화용
    mySetting = setting.Setting()
    myBoardScraper = BoardScraper()
    if args.titleTag is None:
        url = parse.unquote(args.urlOrFilePath)
        print(myBoardScraper.getMagnet(url))
    else:
        logging.info(f'스크랩 테스트를 시작합니다. [{args.urlOrFilePath}], [{args.titleTag}], [{args.titleClass}]')
        boardItems = myBoardScraper.getBoardItemInfos(args.urlOrFilePath, 1
                        , args.titleTag, args.titleClass)
        print(json.dumps(boardItems, default=lambda x: x.__dict__))
        logging.info("스크랩 테스트를 마쳤습니다.")