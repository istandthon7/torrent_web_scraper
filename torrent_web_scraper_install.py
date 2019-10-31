#!/usr/bin/env python3
from datetime import datetime as dtime
import os
import sys
import web_scraper_lib
import json

__version__ = 'v1.00'

if __name__ == '__main__':

    SETTING_PATH = os.path.realpath(os.path.dirname(__file__))+"/"
    SETTING_FILE = SETTING_PATH+"web_scraper_settings.json"
    progarm_file_name="web_scraper_program_list.json"
    PROGRAM_FILE = SETTING_PATH+progarm_file_name
    runTime = dtime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print("%s %s is going to work at %s. %s" % (os.path.basename(__file__),
    #    __version__, runTime,sys.getdefaultencoding()) )

    # 설정파일 생성
    isExist = web_scraper_lib.create(SETTING_FILE)

    # 설정파일
    if isExist:
      data ={}
      download="/home/pi"
      print("기본 다운로드 경로는 "+download+ "입니다. \n"+SETTING_FILE+"에서 변경할 수 있습니다.")
      data["download-base"]= "/home/pi"
      data["enable-torrentwal"]= "True"
      history = {}
      history["torrentwal_kortv_dra"]=0
      history["torrentwal_kortv_ent"]=0
      history["torrentwal_kortv_soc"]=0
      history["torrentwal_movie"]=0
      data['history'] = history

      movie = {}
      movie["download"]="/home/pi"
      movie["list"]= "movie_list.txt"
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

