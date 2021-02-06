#!/usr/bin/env python3

import sys
import boardScraper
import scraperLibrary
import time
import config
import os

if __name__ == '__main__':

    setting = config.setting()
    setting.loadJson()
    movie = config.Moive(setting)
    tvshow = config.TVShow(setting)

    for siteIndex, site in enumerate(setting.json["sites"]):

        #Step 1.  test for access with main url
        if site['enable'] == False:
            continue;

        if not scraperLibrary.checkUrl(site["mainUrl"]):
            #site['mainUrl'] = scraperLibrary.updateUrl(site['mainUrl'])
            continue

        try:
            if "board" not in site:
                print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.{site['mainUrl']}")
                continue;
            elif site['board'] == "GNBoardBasicSkin":
                bdScraper = boardScraper.GNBoardBasicSkin()
            else:
                print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.({site['board']})")
                continue;
        except Exception as e:
            print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.({e})")
            continue;

        #Step 2.  Iterate category for this site
        for categoryIndex, category in enumerate(site["category"]):
            isNextPageScrap = True
            toSaveBoardItemNum = None
            #Step 4.  iterate page (up to 10) for this site/this category
            for pageCount in range(1, setting.json['page_scrap_max']+1):

                if isNextPageScrap == False:
                    break;

                boardList = bdScraper.getParseDataReverse(site["mainUrl"], category["url"], pageCount)

                if boardList is None:
                    #에러메시지는 getParseDataReverse에서 출력
                    continue

                #for board in boardList:
                for boardItemIndex, boardItem in enumerate(boardList, start=1):

                    #게시판 제목
                    boardItemTitle = boardItem.get_text().replace('\t', '').replace('\n', '')
                    boardItemUrl = boardItem.get('href').replace('..', site['mainUrl'])
                    boardItemNum = bdScraper.getWrId(boardItemUrl)

                    #print(f"탐색중... 제목: {boardItemTitle}")
                    #boardList의 첫 게시물의 id를 확인
                    if (category['history'] >= boardItemNum):
                        isNextPageScrap = False
                        break;

                    if "영화" in category['name']:
                        programTitle = movie.checkTitleWithMovieFile(boardItemTitle)
                    else:
                        programTitle = tvshow.checkTitleInTVShow(boardItemTitle)

                    if boardItemIndex == 1 and pageCount == 1:
                        toSaveBoardItemNum = boardItemNum

                    if not programTitle:

                        scraperLibrary.notiEmail(setting , site['name'], boardItemTitle )
                        continue

                    magnet = bdScraper.getMagnetDataFromPageUrl(boardItemUrl)

                    if magnet == "":
                      continue

                    #magnet was already downloaded.
                    if config.checkMagnetHistory(setting.TORRENT_HISTORY_FILE_NAME, magnet):
                        continue

                    if "영화" in category['name']:
                      downloadPath = setting.json["movie"]["download"]
                    else:
                      downloadPath = setting.json["download-base"]
                      if len(downloadPath) > 0:
                        downloadPath = downloadPath + "/" + programTitle
                        if not os.path.exists(downloadPath):
                          os.makedirs(downloadPath)

                    sessionId = scraperLibrary.getSessionIdTorrentRpc(setting.json)

                    if sessionId == None:
                        sys.exit()

                    scraperLibrary.addMagnetTransmissionRemote(magnet, setting.json, downloadPath, sessionId)

                    if "영화" in category['name']:
                        movie.removeLineInMovie(programTitle)
                    else:
                        scraperLibrary.removeTransmissionRemote(setting.json, sessionId, programTitle)

                    config.addMagnetInfoToFile(setting, site['name'], boardItemTitle, magnet, programTitle)
            #값이 있는 경우만 갱신
            if toSaveBoardItemNum is not None:
                setting.json["sites"][siteIndex]["category"][categoryIndex]["history"] = toSaveBoardItemNum
                
        #Step 5.  save scrap ID
        setting.saveJson()
