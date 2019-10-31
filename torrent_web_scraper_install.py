#!/usr/bin/env python3
from datetime import datetime as dtime
import os
import sys
import web_scraper_lib
import json

__version__ = 'v1.00'

if __name__ == '__main__':

    SETTING_PATH = os.path.realpath(os.path.dirname(__file__))+"/"
    SETTING_FILE = SETTING_PATH+"web_scraper_settings_test.json"
    progarm_file_name="web_scraper_program_list.json"
    PROGRAM_FILE = SETTING_PATH+progarm_file_name
    default_download="/home/pi"
    default_movie_list= "movie_list.txt"
    runTime = dtime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print("%s %s is going to work at %s. %s" % (os.path.basename(__file__),
    #    __version__, runTime,sys.getdefaultencoding()) )

    # 영화목록
    web_scraper_lib.create(SETTING_PATH+default_movie_list)
    # 설정파일 생성
    isExist = web_scraper_lib.create(SETTING_FILE)

    # 설정파일
    if isExist:
      data ={}
      
      print("기본 다운로드 경로는 "+default_download+ "입니다. \n"+SETTING_FILE+"에서 변경할 수 있습니다.")
      data["download-base"]= default_download

      movie = {}
      movie["download"]=default_download
      movie["list"]= default_movie_list
      movie["ranking"]= 8
      movie["resolution"]= "1080"
      movie["video_codec"]= "264"
      data['movie']=movie

      data["page_scrwap_max"]= 1
      
      print("transmission을 설치하고 연결정보를 설정해주세요")
      data["trans-host"] = ""
      data["trans-id"] = ""
      data["trans-port"]= "9091"
      data["trans-pw"]= ""

      data["program-list"]=progarm_file_name

      data['tofiles']={}
      data['tofiles']['category']=[]
      data['tofiles']['category'].append({"history": 0,"idx": "torrent_kortv_ent","name": "예능","url": "https://tofiles7.net/bbs/board.php?bo_table=torrent_kortv_ent"})
      data['tofiles']['category'].append({"history": 0,"idx": "torrent_kortv_social","name": "다큐","url": "https://tofiles7.net/bbs/board.php?bo_table=torrent_kortv_social"})
      data['tofiles']['category'].append({"history": 0,"idx": "torrent_kortv_drama","name": "드라마","url": "https://tofiles7.net/bbs/board.php?bo_table=torrent_kortv_drama"})
      data['tofiles']['category'].append({
                "history": 0,
                "idx": "torrent_movie_kor",
                "name": "한국영화",
                "url": "https://tofiles7.net/bbs/board.php?bo_table=torrent_movie_kor"
            })
      data['tofiles']['category'].append({
                "history": 0,
                "idx": "torrent_movie_eng",
                "name": "외국영화",
                "url": "https://tofiles7.net/bbs/board.php?bo_table=torrent_movie_eng"
            })
      with open(SETTING_FILE, 'w', encoding='utf-8') as dataFile:
        json.dump(data, dataFile, sort_keys = True, ensure_ascii=False, indent = 4)

    # 프로그램 파일
    isExist = web_scraper_lib.create(PROGRAM_FILE)

    if isExist:
      data = {}
      data["title_list"]=[]
      data['title_list'].append({
        "name": "백종원의 골목식당",
        "option": "720",
        "option2": "NEXT",
        "season": ""
      })
      with open(PROGRAM_FILE, 'w', encoding='utf-8') as dataFile:
        json.dump(data, dataFile, sort_keys = True, ensure_ascii=False, indent = 4)

