#!/usr/bin/python3

import sys
import gnBoardBasicSkin
import scraperLibrary
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

def addMagnetInfoToFile(mySetting: setting.Setting, siteName: str, title: str, magnet: str, keyword: str)->None:
    runtime = mySetting.runTime
    magnetInfo = [runtime, siteName, title, magnet, keyword]
    with open(mySetting.torrentHistoryPath, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(magnetInfo)
    f.close()

if __name__ == '__main__':

    mySetting = setting.Setting()
    myMovie = movie.Movie(mySetting)
    myTvShow = tvshow.TVShow(mySetting)

    for siteIndex, site in enumerate(mySetting.json["sites"]):

        #Step 1.  test for access with main url
        if site['enable'] is False:
            continue;
        if scraperLibrary.checkUrl(site["mainUrl"]) is False:
            #site['mainUrl'] = scraperLibrary.updateUrl(site['mainUrl'])
            continue
        try:
            if "board" not in site:
                print("https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다." + site['mainUrl'])
                continue;
            elif site['board'] == "GNBoardBasicSkin":
                myBoardScraper = gnBoardBasicSkin.GNBoardBasicSkin()
            else:
                print("https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다."+site['board'])
                continue;
        except Exception as e:
            print("https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다." + str(e))
            continue;
        #Step 2.  Iterate category for this site
        for categoryIndex, category in enumerate(site["category"]):
            isNextPageScrap = True
            toSaveBoardItemNum = None
            #Step 4.  iterate page (up to 10) for this site/this category
            for pageNumber in range(1, mySetting.json['page_scrap_max']+1):

                if isNextPageScrap == False:
                    break;
                boardList = myBoardScraper.getParseData(site["mainUrl"], category["url"], pageNumber)

                if not boardList:
                    #에러메시지는 getParseDataReverse에서 출력
                    continue
                #for board in boardList:
                for boardItemIndex, boardItem in enumerate(boardList, start=1):

                    #print(f"탐색중... 제목: {boardItemTitle}")
                    #boardList의 첫 게시물의 id를 확인
                    if (category['history'] >= boardItem.ID):
                        isNextPageScrap = False
                        break;
                    if "영화" in category['name']:
                        regKeyword = myMovie.getRegKeyword(boardItem.Title)
                    else:
                        regKeyword = myTvShow.getRegKeyword(boardItem.Title)
                    if boardItemIndex == 1 and pageNumber == 1:
                        toSaveBoardItemNum = boardItem.ID
                    if not regKeyword:
                        scraperLibrary.executeNotiScript(mySetting , site['name'], boardItem.Title )
                        continue
                    magnet = myBoardScraper.getMagnetDataFromPageUrl(boardItem.Url)

                    if not magnet:
                      continue
                    #magnet was already downloaded.
                    if checkMagnetHistory(mySetting.torrentHistoryPath, magnet):
                        continue
                    if "영화" in category['name']:
                        downloadPath = mySetting.json["movie"]["download"]
                    else:
                        downloadPath = mySetting.json["tvshow"]["download"]
                        if len(downloadPath) > 0:
                            downloadPath = downloadPath + "/" + regKeyword
                            if os.path.exists(downloadPath) is False:
                                os.makedirs(downloadPath)
                    sessionId = scraperLibrary.getSessionIdTorrentRpc(mySetting.json)

                    if sessionId == None:
                        sys.exit()
                    scraperLibrary.addMagnetTransmissionRemote(magnet, mySetting.json, downloadPath, sessionId)

                    if "영화" in category['name']:
                        myMovie.removeLineInMovie(regKeyword)
                    else:
                        scraperLibrary.removeTransmissionRemote(mySetting.json, sessionId, regKeyword)
                    addMagnetInfoToFile(mySetting, site['name'], boardItem.Title, magnet, regKeyword)
            #값이 있는 경우만 갱신
            if toSaveBoardItemNum is not None:
                mySetting.json["sites"][siteIndex]["category"][categoryIndex]["history"] = toSaveBoardItemNum
        #Step 5.  save scrap ID
        mySetting.saveJson()
