#!/usr/bin/env python3

from datetime import datetime as dtime
import os
import sys
import webScraperDaumMovie
import re
import json

__version__ = 'v1.00'

def setSeasonTorrentFile(settings, torrentTitle, season):

    sessionId = webScraperDaumMovie.getSessionIdTorrentRpc(settings)
    print(f"info, setSeasonTorrentFile session_id = {sessionId}")

    torrentId = webScraperDaumMovie.getIdTransmissionRemote(settings, sessionId, torrentTitle)
    print(f"info, setSeasonTorrentFile id = {torrentId}")

    torrents = webScraperDaumMovie.getFilesTorrentRemote(settings, sessionId, torrentId)
    print(f"info setSeasonTorrentFile files = {files}")

    for torrent in torrents:
      if "mp4" in torrent['name']:
        print(f"info setSeasonTorrentFile mp4_file {torrent['name']}")
        dir = os.path.dirname(torrent['name'])
        fileName = os.path.basename(torrent['name'])
        replaceString = f's{season}\g<epi>'
        #re.sub('패턴', '바꿀문자열', '문자열', 바꿀횟수)
        newFileName = re.sub('(?P<epi>E\d+.)', replaceString, fileName)
        print(f"info setSeasonTorrentFile newFileName = {newFileName}")

        webScraperDaumMovie.renameFileTorrentRpc(settings, torrentId, sessionId, torrent['name'], newFileName)

    return

if __name__ == '__main__':

    SETTING_PATH = os.path.realpath(os.path.dirname(__file__))+"/"
    SETTING_FILE = SETTING_PATH+"settings.json"
    HISTORY_FILE = SETTING_PATH+"web_scraper_history.csv"
    runTime = dtime.now().strftime("%Y-%m-%d %H:%M:%S")

    print( f"{os.path.basename(__file__)} {__version__} is going to work at {runTime}. { sys.getdefaultencoding()}")
    settings = webScraperDaumMovie.loadJson(SETTING_FILE)

    torrentTitle = sys.argv[1]
    print(f"info, main torrent_title = {torrentTitle}")

    # 시즌이 설정된 토렌트인가
    with open(settings["program-list"]) as programListFile:
      
        programList = json.load(programListFile)
      
        for programTitle in programList['title_list']:

            programTitleName = programTitle['name']

            if programTitleName in torrentTitle and len(programTitle) >= 4:

              print("info, main program name = %s, season = %d" % (torrentTitle, programTitle['season']))
              setSeasonTorrentFile(settings, torrentTitle, programTitle['season'])
            #else:
            #  print("not equal")
    sys.exit()

