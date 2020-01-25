#!/usr/bin/env python3

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import subprocess
import re
import json
import web_scraper_lib
import sys
import ssl

class site_scraper:
    def __init__(self, name, siteJson):
        self.sitename = name
        self.mainUrl = siteJson.get('mainUrl')
        self.JD = siteJson
        #인증서 관련 에러
        ssl._create_default_https_context = ssl._create_unverified_context

    def getScrapUrl(self, category, count):
      return category.get("url").replace("1",str(count))

    def saveNewLatestIDwithCate(self, category, newId):
        tmp = self.JD.get('history')
        if category == 'kortv_ent':
            tmp.update(torrentwal_kortv_ent = newId)
            self.kortv_ent_id = newId
        elif category == 'kortv_social':
            tmp.update(torrentwal_kortv_soc = newId)
            self.kortv_soc_id = newId
        elif category == 'kortv_dra':
            tmp.update(torrentwal_kortv_dra = newId)
            self.kortv_dra_id = newId
        elif category == "movie":
            tmp.update(torrentwal_movie = newId)
            self.movie_id = newId
        else:
            print("Something Wrong, category = %s" % category)

        self.JD.set('history', tmp)
        return

    def needKeepGoing(self, category, id):
        tmp = None
        if category == 'kortv_ent':
            tmp = self.kortv_ent_id
        elif category == 'kortv_social':
            tmp = self.kortv_soc_id
        elif category == 'kortv_dra':
            tmp = self.kortv_dra_id
        elif category == "movie":
            tmp = self.movie_id
        else:
            print("Something Wrong, category = %s" % category)
            return False
        #print("info: tmp=%s" % tmp)
        if id > tmp:
            return True

        return False

    def getMainUrl(self):
        return self.mainUrl

    def checkMainUrl(self):
        ret = web_scraper_lib.checkUrl(self.mainUrl)
        return ret

    def getName(self):
        return (self.name)

    def getParseData(self, url):
        bsObj = web_scraper_lib.getBsObj(url)
        nameList = bsObj.find('table', attrs={'class' : 'board_list'}).find_all('a',href=True)
        return nameList

    #url을 기반으로 wr_id text를 뒤의 id parsing
    def get_wr_id(self, url):

        tmp = url.rfind('/')
        if (tmp < 0): # 둘다 검색 못하면 포기
            return 0
        else:
            checkStr = '/'

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
        tag = bsObj.findAll('a', href=re.compile('^magnet'))
# > fieldset > ul ')
#> li:nth-child(3)')
#.find('div', attrs={'id' : "f_list"}).next_sibling()
#.next_sibling()
# > table > tr > td > a")
#.find('div', attrs={'id' : 'main_body'}).find('table')
#\
#                        .find('tr').find('td')
#.find('a', recursive=False)
        #print("info, getmagnetDataFromPageUrl a tags %s" % a_tags)

        if len(tag)>0:

          magnet = tag[0].get('href')
          #print("info, getmagnetDataFromPageUrl magnet = %s" % magnet)

#        sys.exit()

        return magnet
