#!/usr/bin/env python3

from datetime import datetime as dtime
import os
import sys
import scraperLibrary
import re
import json
import config 

def setSeasonTorrentFile(setting, torrentTitle, season):

    sessionId = scraperLibrary.getSessionIdTorrentRpc(setting)
    print(f"info, setSeasonTorrentFile session_id = {sessionId}")

    torrentId = scraperLibrary.getIdTransmissionRemote(setting, sessionId, torrentTitle)
    print(f"info, setSeasonTorrentFile id = {torrentId}")

    torrents = scraperLibrary.getFilesTorrentRemote(setting, sessionId, torrentId)
    print(f"info setSeasonTorrentFile torrents = {torrents}")

    for torrent in torrents:
      if "mp4" in torrent['name']:
        print(f"info setSeasonTorrentFile mp4_file {torrent['name']}")
        dir = os.path.dirname(torrent['name'])
        fileName = os.path.basename(torrent['name'])
        replaceString = f's{season}\g<epi>'
        #re.sub('패턴', '바꿀문자열', '문자열', 바꿀횟수)
        newFileName = re.sub('(?P<epi>E\d+.)', replaceString, fileName)
        print(f"info setSeasonTorrentFile newFileName = {newFileName}")

        scraperLibrary.renameFileTorrentRpc(setting, torrentId, sessionId, torrent['name'], newFileName)

    return

if __name__ == '__main__':

    setting = config.setting()
    setting.loadJson()

    torrentTitle = sys.argv[1]
    print(f"info, main torrent_title = {torrentTitle}")

    # 시즌이 설정된 토렌트인가
    with open(setting.CONFIG_PATH + setting.json["program-list"]) as TVShow:
      
        tvshowJson = json.load(TVShow)
      
        for tvshowTitle in tvshowJson['title_list']:

            tvshowTitleName = tvshowTitle['name']

            if tvshowTitleName in torrentTitle and len(tvshowTitle) >= 4:

              print(f"info, main program name = {torrentTitle}, season = {tvshowTitle['season']}")
              setSeasonTorrentFile(setting.json, torrentTitle, tvshowTitle['season'])
            #else:
            #  print("not equal")
    sys.exit()

