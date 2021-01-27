#!/usr/bin/env python3
from datetime import datetime as dtime
import os
import sys
import boardTorrentScraper
import webScraperLib
import time

__version__ = 'v1.00'

if __name__ == '__main__':

    SETTING_PATH = os.path.realpath(os.path.dirname(__file__)) + "/"

    SETTING_FILE = SETTING_PATH + "settings.json"
    HISTORY_FILE = SETTING_PATH + "web_scraper_history.csv"
    MAIL_NOTI_HISTORY = SETTING_PATH + "mail_noti_history.csv"
    runTime = dtime.now().strftime("%Y-%m-%d %H:%M:%S")

    settings = webScraperLib.loadJson(SETTING_FILE)
    movieScraper = webScraperLib.MoiveScraper(settings['movie'])

    for siteIndex, site in enumerate(settings["sites"]):

        #Step 1.  test for access with main url
        if site['enable'] == False:
            continue;

        if not webScraperLib.checkUrl(site["mainUrl"]):
            #site['mainUrl'] = webScraperLib.updateUrl(site['mainUrl'])
            continue

        try:
            if "board" not in site:
                print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.{site['mainUrl']}")
                continue;
            elif site['board'] == "GNBoardBasicSkin":
                boardScraper = boardTorrentScraper.GNBoardBasicSkin()
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
            for pageCount in range(1, settings['page_scrap_max']+1):

                if isNextPageScrap == False:
                    break;

                boardList = boardScraper.getParseDataReverse(site["mainUrl"], category["url"], pageCount)

                if boardList is None:
                    #에러메시지는 getParseDataReverse에서 출력
                    continue

                #for board in boardList:
                for boardItemIndex, boardItem in enumerate(boardList, start=1):

                    #게시판 제목
                    boardItemTitle = boardItem.get_text().replace('\t', '').replace('\n', '')
                    boardItemUrl = boardItem.get('href').replace('..', site['mainUrl'])
                    boardItemNum = boardScraper.getWrId(boardItemUrl)

                    #print(f"탐색중... 제목: {boardItemTitle}")
                    #boardList의 첫 게시물의 id를 확인
                    if (category['history'] >= boardItemNum):
                        isNextPageScrap = False
                        break;
                    
                    if "영화" in category['name']:
                        programTitle = movieScraper.checkTitleWithMovieList(boardItemTitle, dtime.now().strftime("%Y"))
                    else:
                        programTitle = webScraperLib.checkTitleWithProgramList(boardItemTitle, settings["program-list"])
                    
                    if boardItemIndex == 1 and pageCount == 1:
                        toSaveBoardItemNum = boardItemNum

                    if not programTitle:

                        webScraperLib.notiEmail(settings["mail-noti"], MAIL_NOTI_HISTORY, site['name'], boardItemTitle, runTime)
                        continue

                    magnet = boardScraper.getMagnetDataFromPageUrl(boardItemUrl)

                    if magnet == "":
                      continue

                    #magnet was already downloaded.
                    if webScraperLib.checkMagnetHistory(HISTORY_FILE, magnet):
                        continue

                    if "영화" in category['name']:
                      downloadPath = settings["movie"]["download"]
                    else:
                      downloadPath = settings["download-base"]
                      if len(downloadPath) > 0:
                        downloadPath = downloadPath + "/" + programTitle
                        if not os.path.exists(downloadPath):
                          os.makedirs(downloadPath)

                    sessionId = webScraperLib.getSessionIdTorrentRpc(settings)

                    if sessionId == None:
                        continue

                    webScraperLib.addMagnetTransmissionRemote(magnet, settings, downloadPath, sessionId)

                    if "영화" in category['name']:
                        movieScraper.removeLineFromMovieListFile(programTitle)
                    else:
                        webScraperLib.removeTransmissionRemote(settings, sessionId, programTitle)

                    webScraperLib.addMagnetInfoToFile(HISTORY_FILE,runTime, site['name'], boardItemTitle, magnet, programTitle)
            #값이 있는 경우만 갱신
            if toSaveBoardItemNum is not None:
                settings["sites"][siteIndex]["category"][categoryIndex]["history"] = toSaveBoardItemNum
                
        #Step 5.  save scrap ID
        webScraperLib.saveJson(SETTING_FILE, settings)
