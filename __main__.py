#!/usr/bin/python3

import argparse
import os
import notification
import setting
import movie
import tvshow
import logging
import stat
import sys
import boardScraper
import scraperHelpers
import history
import osHelper
import rpc

if __name__ == '__main__':

    mySetting = setting.Setting()
    movieSetting = mySetting.json['movie']
    tvSetting = mySetting.json["tvshow"]
    transSetting = mySetting.json["transmission"]

    myMovie = movie.Movie(movieSetting)
    myMovie.load(os.path.join(mySetting.configDirPath, movieSetting['list']))
    myTvShow = tvshow.TVShow()
    myTvShow.load(os.path.join(mySetting.configDirPath, tvSetting["list"]))
    myNoti = notification.Notification(mySetting.configDirPath, mySetting.json["notification"])
    
    logging.info(f'--------------------------------------------------------')
    logging.info('Started.')

    parser = argparse.ArgumentParser()
    parser.add_argument("--transPass", help="트랜스미션 접속 비밀번호")
    args = parser.parse_args()
    mySetting.transPass = args.transPass
    url = mySetting.getRpcUrl()

    torrentHistoryPath = os.path.join(mySetting.configDirPath, mySetting.json["torrentHistory"])
    torrentFailPath = os.path.join(mySetting.configDirPath, mySetting.json["torrentFail"])
    magnetHistory = history.MagnetHistory(torrentHistoryPath, torrentFailPath)
        
    for siteIndex, site in enumerate(mySetting.json["sites"]):
        #Step 1.  test for access with main url
        if site['enable'] is False:
            logging.info(f'[{site["name"]}] 비활성화되어 있습니다.')
            continue;
        logging.info(f'사이트 스크랩을 시작합니다. [{site["name"]}]')
        
        response = scraperHelpers.getResponse(site["mainUrl"])
        if response is None:
            msg = f'[{site["name"]}] 접속할 수 없습니다. {site["mainUrl"]}'
            logging.critical(msg)
            print(msg, file=sys.stderr)
            continue;
        site["mainUrl"] = scraperHelpers.getMainUrl(site["mainUrl"], response.url)
        isScrapFail = False
        myBoardScraper = boardScraper.BoardScraper()
        #Step 2.  Iterate categories for this site
        for categoryIndex, category in enumerate(site["categories"]):
            logging.info(f'게시판 스크랩을 시작합니다. {category["name"]}')
            isNextPageScrap = True
            toSaveBoardId = None
            toSaveBoardNumber = None

            #Step 3.  iterate page for this site/this category
            for pageNumber in range(1, category['scrapPage']+1):
                logging.info(f'페이지 스크랩을 시작합니다. page: {pageNumber}')
                if isNextPageScrap == False:
                    logging.info(f'페이지 스크랩을 마칩니다.')
                    break;

                boardItems = myBoardScraper.getBoardItems(site["mainUrl"]+category["url"], pageNumber
                                , category["title"].get("tag"), category["title"].get("class"), category["title"].get("selector"))

                if not boardItems:
                    isScrapFail = True
                    msg = f"[{site['name']}] 사이트 '{category['name']}' 게시판에서 제목리스트 얻기에 실패하였습니다."
                    logging.error(msg)
                    print(msg, file=sys.stderr)
                    continue;
                # 필터링 하기 전의 마지막 아이디. 
                # 필터링 한 후의 아이디가 더 커진다면 다음 페이지는 갈 필요없음.
                lastID = boardItems[-1].id

                boardItems = list(filter(lambda x: x.id>category['history'], boardItems))

                if len(boardItems) == 0:
                    logging.info(f'모든 게시물을 검색하였으므로 다음 게시판으로 넘어갑니다. history: {category["history"]}')
                    break;

                for boardItemIndex, boardItem in enumerate(boardItems, start=1):
                    if boardItem.url.startswith("http") is False:
                        boardItem.url = (str(site["mainUrl"])[:-1])+boardItem.url
                    logging.debug(f'게시물 제목검색을 시작합니다. id: {boardItem.id}, {boardItem.title}, {boardItem.url}')

                    if "영화" in category['name']:
                        regKeyword = myMovie.getRegKeyword(boardItem.title)
                    else:
                        regKeyword = myTvShow.getRegKeyword(boardItem.title)

                    if boardItemIndex == 1 and pageNumber == 1:
                        toSaveBoardId = boardItem.id
                        toSaveBoardNumber = boardItem.number

                    if not regKeyword:
                        myNoti.executeNotiScript(site['name'], boardItem.title)
                        continue;

                    logging.info(f"게시물을 검색하였습니다. '{boardItem.title}'")

                    magnet = myBoardScraper.getMagnet(boardItem.url)

                    downloadPath = ""
                    if "영화" in category['name']:
                        downloadPath = myMovie.getSavePath(regKeyword, movieSetting["download"], False)
                    else:
                        downloadPath = myTvShow.getSavePath(regKeyword, tvSetting['download'], tvSetting.get("createTitleFolder", True))
                    if len(downloadPath) > 0:
                        if not os.path.exists(downloadPath):
                            os.makedirs(downloadPath)
                            logging.info(f'폴더를 만들었어요. [{downloadPath}]')
                        if not osHelper.isOwner(downloadPath, transSetting["puid"], transSetting["pgid"]):
                            osHelper.changeOwner(downloadPath, transSetting["puid"], transSetting["pgid"])
                        if not osHelper.isPermission(downloadPath, stat.S_IRWXU):
                            osHelper.appendPermisson(downloadPath, stat.S_IRWXU)
                            
                    if not magnet:
                        magnetHistory.addTorrentFailToFile(site['name'], boardItem.title, boardItem.url, regKeyword['name'], downloadPath)
                        msg = f"매그넷 검색에 실패하였습니다. [{regKeyword['name']}]  '{boardItem.title}' {boardItem.url} 폴더: [{downloadPath}]"
                        logging.error(msg)
                        continue;
                    #magnet was already downloaded.
                    if magnetHistory.checkMagnetHistory(magnet):
                        logging.info(f"이미 다운로드 받은 파일입니다. [{regKeyword['name']}] {magnet}")
                        continue;

                    if not "영화" in category['name']:
                        episodeNumber = myTvShow.getEpisodeNumber(boardItem.title)
                        if tvSetting.get("checkEpisodeNubmer", False):
                            if magnetHistory.checkSameEpisode(regKeyword["name"], episodeNumber):
                                logging.info(f"이미 다운로드 받은 회차입니다. [{regKeyword['name']}] '{boardItem.title}'")
                                continue;

                    sessionId = rpc.getSessionIdTransRpc(mySetting.getRpcUrl())

                    if sessionId == None:
                        msg = f'Transmission 세션아이디를 구하지 못했습니다. {url}'
                        logging.critical(msg)
                        print(msg, file=sys.stderr)
                        sys.exit()
                    rpc.addMagnetTransmissionRemote(magnet, mySetting.getRpcUrl(), downloadPath, sessionId)
                    logging.info(f'Transmission에 추가하였습니다. [{regKeyword["name"]}] {magnet}, 폴더: [{downloadPath}]')
                    if "영화" in category['name']:
                        myMovie.removeKeyword(regKeyword["name"])
                        logging.info(f"영화 리스트에서 삭제했습니다. [{regKeyword['name']}]")
                    else:
                        rpc.removeTransmissionRemote(mySetting.getRpcUrl(), sessionId, regKeyword["name"], episodeNumber)
                        
                    magnetHistory.addMagnetToHistory(site['name'], boardItem.title, magnet, regKeyword["name"])
                    
                # --> 현재 페이지의 게시물 검색 완료
                # 필터링 한 후의 아이디가 필터링 전 아이디보다 더 크다면 다음 페이지는 갈 필요없음
                if boardItems[-1].id > lastID:
                    logging.info(f'다음 페이지는 검색할 필요없음. 현재 페이지: {pageNumber}')
                    break;
            # pageNumber 완료
            if toSaveBoardId is not None:
                mySetting.json["sites"][siteIndex]["categories"][categoryIndex]["history"] = toSaveBoardId
                mySetting.json["sites"][siteIndex]["categories"][categoryIndex]["number"] = toSaveBoardNumber
                logging.info(f'history를 변경했습니다. {toSaveBoardId}')
        # category 완료
        # 스크랩을 완료하고 사이트 주소가 변경되었으면 변경.
        if isScrapFail == False and site["mainUrl"] != mySetting.json["sites"][siteIndex]["mainUrl"]:
            mySetting.json["sites"][siteIndex]["mainUrl"] = site["mainUrl"]
            logging.info(f'변경된 도메인을 저장했어요. {site["mainUrl"]}')
        #Step 4.  save json
        mySetting.saveJson()
        logging.info(f'설정파일을 저장했습니다.')
logging.info(f'--------------------------------------------------------')