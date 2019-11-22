#!/usr/bin/env python3
from datetime import datetime as dtime
import os
import sys
import web_scraper_lib
import json
import shutil

__version__ = 'v1.00'

if __name__ == '__main__':

    SETTING_PATH = os.path.realpath(os.path.dirname(__file__))+"/"
    SETTING_FILE = SETTING_PATH+"web_scraper_settings.json"
    progarm_file_name="web_scraper_program_list.json"
    PROGRAM_FILE = SETTING_PATH+progarm_file_name
    default_download="/home/pi"
    default_movie_list= "movie_list.txt"
    mainUrl = "https://tofiles8.net"
    runTime = dtime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print("%s %s is going to work at %s. %s" % (os.path.basename(__file__),
    #    __version__, runTime,sys.getdefaultencoding()) )

    # 영화목록
    web_scraper_lib.create(SETTING_PATH+default_movie_list)
    # 설정파일 생성
    isNotExist = web_scraper_lib.create(SETTING_FILE)

    # 설정파일
    if isNotExist:
      
      print("기본 다운로드 경로는 "+default_download+ "입니다.")
      print(SETTING_FILE+"에서 변경할 수 있습니다.\n")

      print("transmission을 설치하고 연결정보를 설정해주세요")
      print(SETTING_FILE+"에서 변경할 수 있습니다.\n")

      shutil.copyfile("./web_scraper_settings.json.sample", SETTING_FILE)

    # 프로그램 파일
    isNotExist = web_scraper_lib.create(PROGRAM_FILE)

    if isNotExist:
      shutil.copyfile("./web_scraper_program_list.json.sample", PROGRAM_FILE)

      print("다운로드할 프로그램을 설정하세요.")
      print(PROGRAM_FILE+"에서 변경할 수 있습니다.\n")


