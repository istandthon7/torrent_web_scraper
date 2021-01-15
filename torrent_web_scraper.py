#!/usr/bin/env python3
from datetime import datetime as dtime
import os
import sys
import web_scraper_tofiles
import BoardTorrentScraper
import web_scraper_lib
import time

__version__ = 'v1.00'

if __name__ == '__main__':

    SETTING_PATH = os.path.realpath(os.path.dirname(__file__)) + "/"

    SETTING_FILE = SETTING_PATH + "settings.json"
    HISTORY_FILE = SETTING_PATH + "web_scraper_history.csv"
    MAIL_NOTI_HISTORY = SETTING_PATH + "mail_noti_history.csv"
    runTime = dtime.now().strftime("%Y-%m-%d %H:%M:%S")

    settings = web_scraper_lib.loadJson(SETTING_FILE)
    movieScraper = web_scraper_lib.MoiveScraper(settings['movie'])

    for site_index, site in enumerate(settings["sites"]):
        
        #Step 1.  test for access with main url
        if site['enable'] == False:
            continue;

        if not web_scraper_lib.checkUrl(site["mainUrl"]):
            continue

        try:
            if "board" not in site: 
                print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.{site['mainUrl']}")
                continue;
            
            elif site['board'] == "GnBoardBasicSkin":
                scraper = BoardTorrentScraper.GnBoardBasicSkin()
            else:
                print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.({site['board']})")
                continue;
        except Exception as e:
            print(f"https://github.com/istandthon7/torrent_web_scraper/issues 에 도움을 요청할 수 있습니다.({e})")
            continue;

        #Step 2.  Iterate category for this site
        for index, category in enumerate(site["category"]):
            
            #Step 3.  setup Latest Id for this site/this category
            needNewLatestId = True

            #Step 4.  iterate page (up to 10) for this site/this category
            for count in range(1, settings['page_scrap_max'] + 1):
                
                needKeepgoing = True
                boardList = scraper.getParseData(site["mainUrl"], category["url"], count)

                if boardList is None:
                    continue
                #for board in boardList:
                for num, boardItem in enumerate(boardList, start=1):
                    
                    #게시판 제목
                    boardTitle = boardItem.get_text().replace('\t', '').replace('\n', '')
                    href = boardItem.get('href').replace('..', site['mainUrl'])
                    boardIdNum = scraper.get_wr_id(href)

                    if needNewLatestId:
                        newLatestId = scraper.get_wr_id(href)
                        if newLatestId > 0:
                            #웹페이지상의 게시판번호와 실제 게시물번호는 다를 수 있음
                            needNewLatestId = False
                        else:
                            print(f"Something wrong, cannot get new latest ID -{newLatestId}")

                    #boardList의 첫 게시물의 id를 확인
                    if num == 1:
                        if (category['history'] > boardIdNum):
                            needKeepgoing = False
                            break

                    if "영화" in category['name']:
                      matched_name = movieScraper.checkTitleWithMovieList(boardTitle, dtime.now().strftime("%Y"))
                    else:
                      matched_name = web_scraper_lib.checkTitleWithProgramList(boardTitle, settings["program-list"])

                    if not matched_name:

                        web_scraper_lib.notiEmail(settings["mail-noti"], MAIL_NOTI_HISTORY, site['name'], boardTitle, runTime)
                        continue

                    if (category['history'] > boardIdNum):
                        needKeepgoing = False
                        break

                    magnet = scraper.getmagnetDataFromPageUrl(href)

                    if magnet == "":
                      continue

                    time.sleep(3)

                    #magnet was already downloaded.
                    if web_scraper_lib.check_magnet_history(HISTORY_FILE, magnet):
                        continue

                    if "영화" in category['name']:
                      download_dir = settings["movie"]["download"]
                    else:
                      download_dir = settings["download-base"]
                      if len(download_dir) > 0:
                        download_dir = download_dir + "/" + matched_name
                        if not os.path.exists(download_dir):
                          os.makedirs(download_dir)

                    session_id = web_scraper_lib.get_session_id_torrent_rpc(settings)
                    if session_id == None:
                        continue

                    web_scraper_lib.add_magnet_transmission_remote(magnet, settings, download_dir, session_id)

                    if "영화" in category['name']:
                        movieScraper.removeLineFromMovieListFile(matched_name)
                    else:
                      web_scraper_lib.remove_transmission_remote(settings, session_id, matched_name)

                    web_scraper_lib.add_magnet_info_to_file(HISTORY_FILE,
                            runTime, site['name'], boardTitle, magnet, matched_name)

                if not needKeepgoing:
                    break

            #Step 5.  save scrap ID
            #scraper.saveNewLatestIDwithCate(cateIdx, newLatestId)
            settings["sites"][site_index]["category"][index]["history"] = newLatestId
            web_scraper_lib.SaveJson(SETTING_FILE, settings)
