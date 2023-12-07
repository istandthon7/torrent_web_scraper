import argparse
from http.client import HTTPResponse
import sys
from typing import Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import time
import random
import ssl
import logging

import setting

def getSoup(url: str):
    try:
        html = getHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        return soup
    except Exception as e:
        logging.error(f"Exception getSoup url: {url} , error: {str(e)}")
    return None

def getHtml(url: str):
    try:
        time.sleep(random.randrange(1, 4))
        response = getResponse(url)
        if response is not None:
            return response.read().decode('utf-8','replace')
    except Exception as e:
        logging.error("Exception getHtml url: "+url+" , error: " + str(e))
    return None

def getResponse(url) -> Optional[HTTPResponse]:
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
    return None

def getSoupFromFile(filePath: str):
    try:
        soup = BeautifulSoup(open(filePath), "html.parser")
        return soup
    except Exception as e:
        logging.error("Exception getSoupFromFile path: "+filePath+" , error: " + str(e))

def getMainUrl(url: str, responseUrl: str) -> str:
    if responseUrl != url:
        parsedUrl = urlparse(responseUrl)
        mainDomain = f"https://{parsedUrl.netloc}/"
        if mainDomain != url:
            logging.info(f'url이 변경되었네요. [{url}]->[{mainDomain}]')
        return mainDomain
    return url


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="저장할 url")
    parser.add_argument("--savePath", help="HTML을 저장할 경로")
    args = parser.parse_args()
    # 로그파일 초기화용
    mySetting = setting.Setting()
    logging.info("HTML을 가져오는 중...")
    html = getHtml(args.url)
    if html is not None:
        with open(args.savePath, 'w', encoding='utf-8') as f:
            f.write(html)
    else:
        message = f"HTML을 가져오는 데 실패했습니다: {args.url}"
        logging.error(message)
        sys.stderr.write(message)

