#!/usr/bin/env python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import subprocess
import re
import json
import sys
import webScraperLib

#그누보드 BASIC스킨
class GnBoardBasicSkin:
    
    def getScrapUrl(self, mainUrl, categoryUrl, count):
      return mainUrl + categoryUrl + "&page="+str(count)

    def getParseData(self, mainUrl, categoryUrl, count):
        url = self.getScrapUrl(mainUrl, categoryUrl, count)
        bsObj = webScraperLib.getBsObj(url)
        listBoardDiv = bsObj.find('div', attrs={'class' : 'list-board'})

        if listBoardDiv is None:
            print(f"게시판 리스트 얻기에 실패하였습니다. {url}")
        else:
            return listBoardDiv.find_all('a', href=re.compile(".*wr_id.*"))

    #게시판 아이디 파싱, url을 기반으로 wr_id text를 뒤의 id parsing
    def getWrId(self, url):

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

    def getMagnetDataFromPageUrl(self, url):
        bsObj = webScraperLib.getBsObj(url)
        # a 태그 중에 href가 magnet으로 시작하는 태그.
        tag = bsObj.findAll('a', href=re.compile('^magnet'))

        if len(tag)>0:
          magnet = tag[0].get('href')
        else:
          magnet = ""

        return magnet
