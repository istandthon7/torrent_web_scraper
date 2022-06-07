
import re
import bs4
import scraperLibrary

class BoardItemInfo:

    def __init__(self, title: str, url: str, ID: int) -> None:
        self.Title = title
        self.Url = url
        self.ID = ID


#그누보드 BASIC스킨
class GNBoardBasicSkin():
    def getScrapUrl(self, mainUrl: str, categoryUrl: str, page: int)->str:
        if page > 1:
            return mainUrl + categoryUrl + "&page="+str(page)
        else:
            return mainUrl + categoryUrl


    def getParseData(self, mainUrl: str, categoryUrl: str, page: int)->list:
        url = self.getScrapUrl(mainUrl, categoryUrl, page)
        bsObj = scraperLibrary.getBsObj(url)

        if bsObj is None:
            print("게시판 접속에 실패하였습니다. "+url)
            return []
        listBoardDiv = bsObj.find('div', attrs={'class' : 'list-board'})

        if listBoardDiv is None:
            print("게시판 리스트 얻기에 실패하였습니다. "+url)
            return [];
        items = listBoardDiv.find_all('a', href= lambda x: "wr_id" in x)

        items = list(filter(lambda x: len(x.text.strip())>0, items))
        results = []
        for item in items:
            boardItemInfo = self.GetBoardItemInfo(item)
            results.append(boardItemInfo)
        return results


    #게시판 아이디 파싱, url을 기반으로 wr_id text를 뒤의 id parsing
    def getWrID(self, url: str)->int:
        results = re.findall(r"[^&?]+=[^&?]+", url)
        for result in results:
            if result.startswith("wr_id"):
                return int(result.replace("wr_id=", ""))
        return -1

    def GetBoardItemInfo(self, boardItem: bs4.element.Tag) -> BoardItemInfo:
        url = boardItem.get('href')
        boardItemInfo = BoardItemInfo(boardItem.text.strip(), url, self.getWrID(url))
        return boardItemInfo

    def getMagnetDataFromPageUrl(self, url: str)->str:
        bsObj = scraperLibrary.getBsObj(url)
        # a 태그 중에 href가 magnet으로 시작하는 태그.
        tag = bsObj.findAll('a', href=re.compile('^magnet'))

        if len(tag)>0:
          magnet = tag[0].get('href')
        else:
          magnet = ""
        return magnet
