#!/usr/bin/env python3

from datetime import datetime as dtime
import os
import sys
import web_scraper_lib
import re
import json

__version__ = 'v1.00'

def set_season_torrent_file(JD, torrent_title, season):

    session_id = web_scraper_lib.get_session_id_torrent_rpc(JD)
    print("info, set_season_torrent_file session_id = %s" % session_id)

    torrent_id = web_scraper_lib.get_id_transmission_remote(JD, session_id, torrent_title)
    print("info, set_season_torrent_file id = %s" % torrent_id)

    files = web_scraper_lib.get_files_torrent_remote(JD, session_id, torrent_id)
    #get_mp4_file_torrent_rpc(JD, torrent_id, session_id)
    print("info set_season_torrent_file files = %s" % files)

    for item in files:
      if "mp4" in item['name']:
        mp4_file = item['name']
        print("info set_season_torrent_file mp4_file", mp4_file)
        dir = os.path.dirname(mp4_file)
        file = os.path.basename(mp4_file)
        replace_string = 's%s\g<epi>' % (season)
        dest_file = re.sub('(?P<epi>E\d+.)', replace_string, file)
        print("info set_season_torrent_file dest_file = %s" % dest_file)

        web_scraper_lib.rename_file_torrent_prc(JD, torrent_id, session_id, mp4_file, dest_file)

    return

if __name__ == '__main__':

    SETTING_PATH = os.path.realpath(os.path.dirname(__file__))+"/"
    SETTING_FILE = SETTING_PATH+"web_scraper_settings.json"
    HISTORY_FILE = SETTING_PATH+"web_scraper_history.csv"
    runTime = dtime.now().strftime("%Y-%m-%d %H:%M:%S")

    print( "%s %s is going to work at %s. %s" % (os.path.basename(__file__),
        __version__, runTime, sys.getdefaultencoding()) )

    JD = web_scraper_lib.JsonParser(SETTING_FILE)

    torrent_title = sys.argv[1]
    print("info, main torrent_title = %s" % torrent_title)

    # 시즌이 설정된 토렌트인가
    with open(JD.get("program-list")) as program_file:
      data = json.load(program_file)
      for prog in data['title_list']:

        prog_name = prog['name']
        #print("info, main program name = %s, torrent_title = %s, prog length = %d" % (prog_name, torrent_title, len(prog)))

        if prog_name in torrent_title and len(prog) >= 4:

          print("info, main program name = %s, season = %d" % (torrent_title, prog['season']))
          set_season_torrent_file(JD, torrent_title, prog['season'])
        #else:
        #  print("not equal")
    sys.exit()

