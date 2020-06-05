#!/usr/bin/env python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import subprocess
import re
import json
import web_scraper_lib
import sys

class site_scraper:
    def __init__(self, name, siteJson):
        self.name = name
        self.mainUrl = siteJson.get('mainUrl')
        self.JD = siteJson

    def getMainUrl(self):
        return self.mainUrl

    def getScrapUrl(self, category, count):
      return category.get("url") + "&page="+str(count)

    def checkMainUrl(self):
        ret = web_scraper_lib.checkUrl(self.mainUrl)
        return ret

    def getName(self):
        return (self.name)

    def getParseData(self, url):
        bsObj = web_scraper_lib.getBsObj(url)
        nameList = bsObj.find('div', attrs={'class' : 'list-board'}).find_all('a', href=re.compile(".*wr_id.*"))
        #nameList = bsObj.find('table', attrs={'class' : 'table table-hover'}).find_all('a',href=True)
        return nameList

    #게시판 아이디 파싱, url을 기반으로 wr_id text를 뒤의 id parsing
    def get_wr_id(self, url):

        tmp = url.rfind('wr_id=')
        if (tmp < 0): # 둘다 검색 못하면 포기
            return 0
        else:
            checkStr = 'wr_id='

            startp = tmp+len(checkStr)
            endp = startp

            for endp in range(startp,len(url)):
                if (url[endp]).isdigit():
                    continue
                else:
                    endp = endp-1
                    break
        
            endp = endp+1
        return int((url[startp:endp]))

    def getmagnetDataFromPageUrl(self, url):
        #print("info, getmagnetDataFromPageUrl url = %s" % url)
        bsObj = web_scraper_lib.getBsObj(url)
        # a 태그 중에 href가 magnet으로 시작하는 태그.
        tag = bsObj.findAll('a', href=re.compile('^magnet'))

        if len(tag)>0:
          magnet = tag[0].get('href')
          #print("info, getmagnetDataFromPageUrl magnet = %s" % magnet)
        else:
          magnet = ""

        return magnet
