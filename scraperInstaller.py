#!/usr/bin/env python3
from datetime import datetime as dtime
import os
import sys
import scraperLibrary
import json
import shutil
from pathlib import Path
import config

def create(path):
    p = Path(path)
    if p.is_file() == False:
      f = open(path, "w+")
      f.close()
      return True
    return False

if __name__ == '__main__':

    setting = config.setting()

    if os.path.isdir(setting.CONFIG_PATH) == False:
        os.mkdir(setting.CONFIG_PATH)
    
    # 설정파일 생성
    isNotExist = create(setting.SETTING_FILE_NAME)

        # 설정파일
    if isNotExist:

      print(f"\n\ntransmission 연결정보를 {setting.SETTING_FILE_NAME}에 설정해주세요\n")

      shutil.copyfile(f"./{setting.SETTING_FILE_NAME_ONLY}.sample", f"{setting.SETTING_FILE_NAME}")

    setting.loadJson()
    TVShow = setting.CONFIG_PATH + setting.json["program-list"]
    Movie = setting.CONFIG_PATH + setting.json['movie']['list']

    # 영화목록
    create(Movie)

    # 프로그램 파일
    isNotExist = create(TVShow)

    if isNotExist:
      shutil.copyfile(f"./{setting.json['program-list']}.sample", TVShow)

      print(f"다운로드할 tv프로그램을 {TVShow}에 추가하세요.\n")

    # 트랜스미션 스크립트
    if os.path.isdir(setting.TRANSMISSION_SCRIPT_PATH) == False:
        os.mkdir(setting.TRANSMISSION_SCRIPT_PATH)
    shutil.copyfile(f"./{setting.TORRENT_DONE_SH}.sample", f"{setting.TRANSMISSION_SCRIPT_PATH}{setting.TORRENT_DONE_SH}")
    shutil.copyfile(f"./{setting.RENAME_SEASON_TRANSMISSION_PY}", f"{setting.TRANSMISSION_SCRIPT_PATH}{setting.RENAME_SEASON_TRANSMISSION_PY}")
    shutil.copyfile(f"./{setting.SCRAPERLIBRARY_PY}.sample", f"{setting.TRANSMISSION_SCRIPT_PATH}{setting.SCRAPERLIBRARY_PY}")
      


