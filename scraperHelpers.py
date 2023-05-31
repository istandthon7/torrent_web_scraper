from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import subprocess
import time
import subprocess
import csv
import random
import os
import setting
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
            logging.error(f"사이트가 정상적으로 작동하지 않거나 사이트보안이 강화되었거나 url이 잘못되었습니다. 에러코드: {er.code}, url: {url}")
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
        print("Exception getSoupFromFile path: "+filePath+" , error: " + str(e))


def executeNotiScript(mySetting: setting.Setting, siteName: str, boardTitle: str)->bool:
    """
    스크립트를 실행했으면 true를 리턴하고
    이미 실행한 경우나 실행하지 못한 경우는 false를 리턴한다.
    """
    notiSetting = mySetting.json["notification"]

    if notiSetting == "":
        return False

    if notiSetting["cmd"] == "":
        return False

    for keyword in notiSetting["keywords"]:
        
        if keyword in boardTitle:
            if checkNotiHistory(mySetting.notiHistoryPath, boardTitle):
                return False
            cmd = notiSetting["cmd"]
            cmd = cmd.replace("$board_title", "["+siteName+"]" + boardTitle.replace("'", "`"))
            try:
                # check가 참이고, 프로세스가 0이 아닌 종료 코드로 종료되면, CalledProcessError 예외가 발생합니다.
                subprocess.run(cmd, shell=True, check=True)

            except Exception as e:
                print("executeNotiScript error, message: "+str(e))
                return False
            else:
                addNotiHistory(mySetting.notiHistoryPath, mySetting.runTime
                                  , siteName, boardTitle, keyword)
                return True

def checkNotiHistory(csvFile: str, title: str)->bool:
        if os.path.isfile(csvFile) is False:
            return False

        with open(csvFile, 'r', encoding="utf-8") as f:
            ff = csv.reader(f)
            for row in ff:
                if title == row[2]:
                    #print("\t\t-> magnet was already downloaded at
                    #web_scraper_history.csv")
                    return True
        return False

def addNotiHistory(csvFile: str, runtime: str, sitename: str, title: str, keyword: str)->None:
    new = [runtime, sitename, title, keyword]
    with open(csvFile, 'a', newline = '\n', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(new)
    f.close()