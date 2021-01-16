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
            continue

        try:
            if "board" not in site: 
                print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.{site['mainUrl']}")
                continue;
            
            elif site['board'] == "GnBoardBasicSkin":
                boardScraper = boardTorrentScraper.GnBoardBasicSkin()
            else:
                print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.({site['board']})")
                continue;
        except Exception as e:
            print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.({e})")
            continue;

        #Step 2.  Iterate category for this site
        for categoryIndex, category in enumerate(site["category"]):
            
            #Step 3.  setup Latest Id for this site/this category, 
            needNewLatestId = True

            #Step 4.  iterate page (up to 10) for this site/this category
            for pageCount in range(1, settings['page_scrap_max'] + 1):
                
                needKeepgoing = True
                boardList = boardScraper.getParseData(site["mainUrl"], category["url"], pageCount)

                if boardList is None:
                    continue

                #for board in boardList:
                for boardIndex, boardItem in enumerate(boardList, start=1):
                    
                    #게시판 제목
                    boardTitle = boardItem.get_text().replace('\t', '').replace('\n', '')
                    boardUrl = boardItem.get('href').replace('..', site['mainUrl'])
                    boardIdNum = boardScraper.getWrId(boardUrl)

                    if needNewLatestId:
                        
                        newLatestId = boardScraper.getWrId(boardUrl)
                        
                        if newLatestId > 0:
                            #웹페이지상의 게시판번호와 실제 게시물번호는 다를 수 있음
                            needNewLatestId = False
                        else:
                            print(f"Something wrong, cannot get new latest ID -{newLatestId}")

                    #boardList의 첫 게시물의 id를 확인
                    if boardIndex == 1:
                        if (category['history'] > boardIdNum):
                            needKeepgoing = False
                            break

                    if "영화" in category['name']:
                        programTitle = movieScraper.checkTitleWithMovieList(boardTitle, dtime.now().strftime("%Y"))
                    else:
                        programTitle = webScraperLib.checkTitleWithProgramList(boardTitle, settings["program-list"])

                    if not programTitle:

                        webScraperLib.notiEmail(settings["mail-noti"], MAIL_NOTI_HISTORY, site['name'], boardTitle, runTime)
                        continue

                    if (category['history'] > boardIdNum):
                        needKeepgoing = False
                        break

                    magnet = boardScraper.getMagnetDataFromPageUrl(boardUrl)

                    if magnet == "":
                      continue

                    time.sleep(3)

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

                    webScraperLib.addMagnetInfoToFile(HISTORY_FILE,runTime, site['name'], boardTitle, magnet, programTitle)

                if not needKeepgoing:
                    break

            #Step 5.  save scrap ID
            settings["sites"][siteIndex]["category"][categoryIndex]["history"] = newLatestId
            webScraperLib.SaveJson(SETTING_FILE, settings)
