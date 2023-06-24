from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import time
import subprocess
import random
import ssl
import logging

def getSoup(url: str):
    try:
        html = getHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        return soup
    except Exception as e:
        print(f"Exception getSoup url: {url} , error: {str(e)}")
    return None

def getHtml(url: str):
    try:
        time.sleep(random.randrange(1, 4))
        return getResponse(url).read().decode('utf-8','replace')
    except Exception as e:
        print("Exception getHtml url: "+url+" , error: " + str(e))
    return None

def getResponse(url):
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        # python 3.6이상에서
        context = ssl._create_unverified_context()
        # urlopen(request, context=context) as response
        return urlopen(request, context=context)
    except HTTPError as er:
        if er.code > 400:
            logging.error(f"일시적 접속실패이거나 사이트가 정상적으로 작동하지 않거나 사이트보안이 강화되었거나 url이 잘못되었습니다. 에러코드: {er.code}, url: {url}")
        else:
            raise
    except URLError as er:
        logging.error(f"사이트 주소가 변경등으로 정상적으로 작동하지 않아요. 원인: {er.reason}, url: {url}")
    except ConnectionResetError as er:
        logging.error(f"서버가 연결을 종료했습니다. 원인: {er.strerror}, url: {url}")

def getSoupFromFile(filePath: str):
    try:
        soup = BeautifulSoup(open(filePath), "html.parser")
        return soup
    except Exception as e:
        logging.error("Exception getSoupFromFile path: "+filePath+" , error: " + str(e))
