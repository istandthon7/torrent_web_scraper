#!/usr/bin/python3

import sys
import boardScraper
import scraperHelpers
import os
import csv
import setting
import movie
import tvshow


def checkMagnetHistory(csvFileName: str, magnet: str)->bool:
    if not os.path.isfile(csvFileName):
        return False

    with open(csvFileName, 'r', encoding="utf-8") as f:
        ff = csv.reader(f)
        for row in ff:
            if magnet == row[3]:
                return True
    return False


def addMagnetInfoToFile(mySetting: setting.Setting, siteName: str, boardTitle: str
    , magnet: str, keyword: str)->None:
    
    runtime = mySetting.runTime
    magnetInfo = [runtime, siteName, boardTitle, magnet, keyword]
    with open(mySetting.torrentHistoryPath, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(magnetInfo)
    f.close()


def addTorrentFailToFile(mySetting: setting.Setting, siteName: str, boardTitle: str
    , boardUrl: str, keyword: str, downloadDir: str)->None:
    
    runtime = mySetting.runTime
    torrentFailInfo = [runtime, siteName, boardTitle, boardUrl, keyword, downloadDir]
    with open(mySetting.torrentFailPath, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(torrentFailInfo)
    f.close()


if __name__ == '__main__':

    mySetting = setting.Setting()
    myMovie = movie.Movie(mySetting)
    myTvShow = tvshow.TVShow(mySetting)

    for siteIndex, site in enumerate(mySetting.json["sites"]):

        #Step 1.  test for access with main url
        if site['enable'] is False:
            continue;
        if scraperHelpers.checkUrl(site["mainUrl"]) is False:
            #site['mainUrl'] = scraperLibrary.updateUrl(site['mainUrl'])
            continue
        myBoardScraper = boardScraper.BoardScraper()
        #Step 2.  Iterate categories for this site
        for categoryIndex, category in enumerate(site["categories"]):
            isNextPageScrap = True
            toSaveBoardItemNum = None

            if "영화" in category['name']:
                downloadPath = mySetting.json["movie"]["download"]

            #Step 4.  iterate page (up to 10) for this site/this category
            for pageNumber in range(1, mySetting.json['scrapPage']+1):

                if isNextPageScrap == False:
                    break;
                boardItems = myBoardScraper.getBoardItemInfos(site["mainUrl"]+category["url"], pageNumber
                                , category["title"]["tag"], category["title"]["class"])

                if not boardItems:
                    #에러메시지는 getParseDataReverse에서 출력
                    continue
                #for board in boardList:
                for boardItemIndex, boardItem in enumerate(boardItems, start=1):

                    #print(f"탐색중... 제목: {boardItemTitle}")
                    #boardList의 첫 게시물의 id를 확인
                    if (category['history'] >= boardItem.id):
                        isNextPageScrap = False
                        break;
                    
                    if "영화" in category['name']:
                        regKeyword = myMovie.getRegKeyword(boardItem.title)
                    else:
                        regKeyword = myTvShow.getRegKeyword(boardItem.title)

                    if boardItemIndex == 1 and pageNumber == 1:
                        toSaveBoardItemNum = boardItem.id
                    
                    if not regKeyword:
                        scraperHelpers.executeNotiScript(mySetting , site['name'], boardItem.title)
                        continue

                    if boardItem.url.startswith("http") is False:
                        boardItem.url = (str(site["mainUrl"])[:-1])+boardItem.url
                    magnet = myBoardScraper.getMagnetDataFromPageUrl(boardItem.url)

                    if not "영화" in category['name']:
                        downloadPath = mySetting.json["tvshow"]["download"]
                        if len(downloadPath) > 0:
                            downloadPath = downloadPath + "/" + regKeyword
                            # rpc로 하는 경우는 만들 필요가 없는 것 같은데...
                            if os.path.exists(downloadPath) is False:
                                os.makedirs(downloadPath)
                    if not magnet:
                        addTorrentFailToFile(mySetting, site['name'], boardItem.title, boardItem.url, regKeyword, downloadPath)
                        print(f"매그넷 검색에 실패하였습니다. {regKeyword}  {boardItem.title} {boardItem.url}  {downloadPath}")
                        continue
                    #magnet was already downloaded.
                    if checkMagnetHistory(mySetting.torrentHistoryPath, magnet):
                        continue
                   
                    sessionId = scraperHelpers.getSessionIdTorrentRpc(mySetting.json)

                    if sessionId == None:
                        sys.exit()
                    scraperHelpers.addMagnetTransmissionRemote(magnet, mySetting.json, downloadPath, sessionId)

                    if "영화" in category['name']:
                        myMovie.removeLineInMovie(regKeyword)
                    else:
                        scraperHelpers.removeTransmissionRemote(mySetting.json, sessionId, regKeyword)
                    addMagnetInfoToFile(mySetting, site['name'], boardItem.title, magnet, regKeyword)
            #값이 있는 경우만 갱신
            if toSaveBoardItemNum is not None:
                mySetting.json["sites"][siteIndex]["categories"][categoryIndex]["history"] = toSaveBoardItemNum
        #Step 5.  save scrap ID
        mySetting.saveJson()
