#!/usr/bin/env python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import subprocess
import re
import json
import webScraperLib
import sys
import datetime

#태그에 의존적이므로 설정파일로 빼지 않음, 즉 변경의 의미가 없음
RANKING = 0
webpage_addr = ["https://movie.daum.net/boxoffice/monthly?yyyymm="]

class SiteScraper:
    def __init__(self):

        today = datetime.date.today()
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)

        webpage_addr[RANKING] += lastMonth.strftime("%Y%m")

    def checkUrl(self):
        ret = webScraperLib.checkUrl(self.getScrapUrl())
        return ret

    def getScrapUrl(self):
        return (webpage_addr[RANKING])

    # 리스트의 url링크 리스트
    def getParseData(self):
        bsObj = webScraperLib.getBsObj(self.getScrapUrl())
        nameList = bsObj.find_all('a', attrs={'class' : 'name_movie'})
        if len(nameList) == 0:
            print("webScraperDaumMovie.py getParseData 제목 클래스가 없어요. a tag's class: name_movie")
        return nameList

