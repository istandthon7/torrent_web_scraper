#!/usr/bin/env python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import subprocess
import re
import json
import scraperLibrary
import sys
import datetime

class SiteScraper:
    def __init__(self, setting):

        #today = datetime.date.today()
        #first = today.replace(day=1)
        #lastMonth = first - datetime.timedelta(days=1)

        #webpage_addr[RANKING] += lastMonth.strftime("%Y%m")
        self.setting = setting

    def checkUrl(self):
        ret = scraperLibrary.checkUrl(self.getScrapUrl())
        return ret

    def getScrapUrl(self):
        return (self.setting.json["movie"]["titleScrap"]["url"])

    # 리스트의 url링크 리스트
    def getParseData(self):
        bsObj = scraperLibrary.getBsObj(self.getScrapUrl())
        nameList = bsObj.find_all('a', attrs={'class' : 'link_txt'})
        if len(nameList) == 0:
            print(f"{__file__} getParseData 제목 클래스가 없어요. a tag's class: link_txt")
        return nameList

