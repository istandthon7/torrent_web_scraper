#!/usr/bin/python3

import argparse
import setting
import movie
import tvshow
import logging
import stat
import sys
import boardScraper
import scraperHelpers
from pathlib import Path
import history
import osHelper
import rpc

if __name__ == '__main__':

    mySetting = setting.Setting()
    myMovie = movie.Movie(mySetting)
    myTvShow = tvshow.TVShow(mySetting)

    logging.info(f'--------------------------------------------------------')
    logging.info('Started.')

    parser = argparse.ArgumentParser()
    parser.add_argument("--transPass", help="트랜스미션 접속 비밀번호")
    args = parser.parse_args()
    mySetting.transPass = args.transPass
    url = mySetting.getRpcUrl()
    
    movieDownloadPath = mySetting.json["movie"]["download"]
    if len(movieDownloadPath) > 0 and osHelper.isPermission(movieDownloadPath, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG) is False:
        # 777
        osHelper.appendPermisson(movieDownloadPath, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG)
        # 755
        osHelper.appendPermisson(Path(movieDownloadPath).parent.absolute(), stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
    tvshowDownloadPath = mySetting.json["tvshow"]["download"]
    if len(tvshowDownloadPath) > 0 and osHelper.isPermission(tvshowDownloadPath, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG) is False:
        # 777
        osHelper.appendPermisson(tvshowDownloadPath, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG)
        # 755
        osHelper.appendPermisson(Path(tvshowDownloadPath).parent.absolute(), stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
        
    for siteIndex, site in enumerate(mySetting.json["sites"]):
        logging.info(f'사이트 스크랩을 시작합니다. {site["name"]}')
        #Step 1.  test for access with main url
        if site['enable'] is False:
            logging.info(f'[{site["name"]}] 비활성화되어 있습니다.')
            continue;
        response = scraperHelpers.getResponse(site["mainUrl"])
        if response is None:
            #site['mainUrl'] = scraperLibrary.updateUrl(site['mainUrl'])
            logging.critical(f'[{site["name"]}] 접속할 수 없습니다. {site["mainUrl"]}')
            continue;
        if response.url != site["mainUrl"]:
            logging.info(f'url을 갱신합니다. {site["mainUrl"]}->{response.url}')
            mySetting.json["sites"][siteIndex]["mainUrl"] = response.url
            site["mainUrl"] = response.url
        myBoardScraper = boardScraper.BoardScraper()
        #Step 2.  Iterate categories for this site
        for categoryIndex, category in enumerate(site["categories"]):
            logging.info(f'게시판 스크랩을 시작합니다. {category["name"]}')
            isNextPageScrap = True
            toSaveBoardId = None
            toSaveBoardNumber = None

            #Step 4.  iterate page (up to 10) for this site/this category
            for pageNumber in range(1, category['scrapPage']+1):
                logging.info(f'페이지 스크랩을 시작합니다. page: {pageNumber}')
                if isNextPageScrap == False:
                    logging.info(f'페이지 스크랩을 마칩니다.')
                    break;
                boardItems = myBoardScraper.getBoardItemInfos(site["mainUrl"]+category["url"], pageNumber
                                , category["title"]["tag"], category["title"]["class"])

                if not boardItems:
                    logging.warning(f'게시물 목록을 스크랩하지 못했습니다.')
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
                    logging.debug(f'게시물 제목검색을 시작합니다. {boardItem.id}, {boardItem.title}, {boardItem.url}')

                    if "영화" in category['name']:
                        regKeyword = myMovie.getRegKeyword(boardItem.title)
                    else:
                        regKeyword = myTvShow.getRegKeyword(boardItem.title)

                    if boardItemIndex == 1 and pageNumber == 1:
                        toSaveBoardId = boardItem.id
                        toSaveBoardNumber = boardItem.number

                    if not regKeyword:
                        scraperHelpers.executeNotiScript(mySetting , site['name'], boardItem.title)
                        continue;

                    logging.info(f'게시물을 검색하였습니다. {boardItem.title}')

                    magnet = myBoardScraper.getMagnet(boardItem.url)

                    downloadPath = ""
                    if "영화" in category['name']:
                        downloadPath += movieDownloadPath
                    else:
                        downloadPath += tvshowDownloadPath + "/" + regKeyword
                            
                    if not magnet:
                        history.addTorrentFailToFile(mySetting, site['name'], boardItem.title, boardItem.url, regKeyword, downloadPath)
                        msg = f"매그넷 검색에 실패하였습니다. {regKeyword}  {boardItem.title} {boardItem.url}  {downloadPath}"
                        print(msg)
                        logging.error(msg)
                        continue;
                    #magnet was already downloaded.
                    if history.checkMagnetHistory(mySetting.torrentHistoryPath, magnet):
                        logging.info(f'이미 다운로드 받은 파일입니다. {regKeyword}, {magnet}')
                        continue;

                    sessionId = rpc.getSessionIdTransRpc(url)

                    if sessionId == None:
                        msg = f'Transmission 세션아이디를 구하지 못했습니다. {url}'
                        logging.critical(msg)
                        print(msg, file=sys.stderr)
                        sys.exit()
                    rpc.addMagnetTransmissionRemote(magnet, mySetting.getRpcUrl(), downloadPath, sessionId)

                    if "영화" in category['name']:
                        myMovie.removeLineInMovie(regKeyword)
                        logging.info(f'영화 리스트에서 삭제했습니다. {regKeyword}')
                    else:
                        rpc.removeTransmissionRemote(mySetting.getRpcUrl(), sessionId, regKeyword)
                        logging.info(f'tvshow 이전 에피소드를 Transmission에서 삭제했습니다. {regKeyword}')
                    history.addMagnetToHistory(mySetting, site['name'], boardItem.title, magnet, regKeyword)
                    logging.info(f'Transmission에 추가하였습니다. {regKeyword}, {magnet}')
                # --> 현재 페이지의 게시물 검색 완료
                # 필터링 한 후의 아이디가 필터링 전 아이디보다 더 크다면 다음 페이지는 갈 필요없음
                if boardItems[-1].id > lastID:
                    logging.info(f'다음 페이지는 검색할 필요없음. 현재 페이지: {pageNumber}')
                    break;
            #값이 있는 경우만 갱신
            if toSaveBoardId is not None:
                mySetting.json["sites"][siteIndex]["categories"][categoryIndex]["history"] = toSaveBoardId
                mySetting.json["sites"][siteIndex]["categories"][categoryIndex]["number"] = toSaveBoardNumber
                logging.info(f'history를 변경했습니다. {toSaveBoardId}')
        #Step 5.  save scrap ID
        mySetting.saveJson()
        logging.info(f'설정파일을 저장했습니다.')
logging.info(f'--------------------------------------------------------')