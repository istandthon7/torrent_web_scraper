#!/usr/bin/env python3

from datetime import datetime as dtime
import os
import sys
import webScraperLib
import webScraperDaumMovie

__version__ = 'v1.00'


if __name__ == '__main__':

    SETTING_PATH = os.path.realpath(os.path.dirname(__file__))+"/"
    SETTING_FILE = SETTING_PATH+"settings.json"
    HISTORY_FILE = SETTING_PATH+"web_scraper_history.csv"
    runTime = dtime.now().strftime("%Y-%m-%d %H:%M:%S")

    settings = webScraperLib.loadJson(SETTING_FILE)
    daumMovieScraper = webScraperDaumMovie.SiteScraper()

    if not daumMovieScraper.checkUrl():
      print("info, main scraper.checkUrl = false")
      sys.exit()

    movieTitles = daumMovieScraper.getParseData()
    # <strong class="tit_join"><a class="link_g #list #monthly @1" href="/moviedb/main?movieId=111292">기생충</a></strong>, ...
    #print("info, main titles_tag = ", titles_tag)

    movieListFileName = SETTING_PATH+settings.get("movie").get("list")
    f = open(movieListFileName, 'a', encoding="utf-8")

    for index, movieTitle in enumerate(movieTitles, start=1):

      title = movieTitle.text
      print(title)

      f.write(title+"\n")

      if index == settings.get("movie").get("ranking"):
        break;

    f.close()

    sys.exit()
