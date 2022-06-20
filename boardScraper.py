"""
파일명 변경시: app settings
"""
import argparse
import json
import logging
import re
import bs4
import scraperHelpers

class BoardItemInfo:

    def __init__(self, title: str, url: str, ID: int) -> None:
        self.title = title
        self.url = url
        self.id = ID


class BoardScraper():

    def getScrapUrl(self, url: str, page: int)->str:
        if page > 1:
            if not "?" in url:
                url += "?"
            return url + "&page="+str(page)
        else:
            return url


    def getBoardItemInfos(self, urlOrFilePath: str, page: int, titleTag: str, titleClass: str)->list:

        if urlOrFilePath.startswith("http"):
            urlOrFilePath = self.getScrapUrl(urlOrFilePath, page)
            soup = scraperHelpers.getSoup(urlOrFilePath)
        else:
            soup = scraperHelpers.getSoupFromFile(urlOrFilePath)
        
        titles = soup.find_all(titleTag, class_=titleClass)
        if titles is None or not any(titles):
            msg = f"게시판에서 제목리스트 얻기에 실패하였습니다. {urlOrFilePath}, tag: {titleTag}, class: {titleClass}"
            print(msg)
            logging.error(msg)
            return [];
        items = []
        for title in titles:
            items.extend(title.find_all('a'))
        items = list(filter(lambda x: len(x.text.strip())>0 and x.get('href') != "#", items))
        results = []
        isNotSupportID = False
        for item in items:
            boardItemInfo = self.GetBoardItemInfo(item)
            if boardItemInfo.id > 10:
                results.append(boardItemInfo)
            elif boardItemInfo.id == -1:
                isNotSupportID = True
        if isNotSupportID:
            msg = "게시물 아이디를 확인할 수 없습니다."
            print(msg)
            logging.error(msg)
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


    def GetBoardItemInfo(self, boardItem: bs4.element.Tag) -> BoardItemInfo:
        url = boardItem.get('href')
        boardItemInfo = BoardItemInfo(boardItem.text.strip(), url, self.getID(url))
        return boardItemInfo


    def getMagnetDataFromPageUrl(self, url: str)->str:
        html = scraperHelpers.getHtml(url)

        if html is None:
            return ""
        
        match = re.search(r"[^\w]([A-Za-z0-9]){40}[^\w]", html)
        if match:
            return "magnet:?xt=urn:btih:"+ match.group()[1:-1]

        return ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("urlOrFilePath", help="스크랩할 url이나 html파일경로")
    parser.add_argument("--titleTag", help="제목 태그")
    parser.add_argument("--titleClass", help="제목 클래스")
    args = parser.parse_args()
    myBoardScraper = BoardScraper()
    if args.titleTag is None:
        print(myBoardScraper.getMagnetDataFromPageUrl(args.urlOrFilePath))
    else:
        boardItems = myBoardScraper.getBoardItemInfos(args.urlOrFilePath, 1
                        , args.titleTag, args.titleClass)
        print(json.dumps(boardItems, default=lambda x: x.__dict__))