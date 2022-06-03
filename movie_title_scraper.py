#!/usr/bin/env python3

import sys
import daumMovieTitleScraper
import config



if __name__ == '__main__':

    setting = config.setting()
    setting.loadJson()
    movie = config.Moive(setting)

    movieTitleScraper = daumMovieTitleScraper.SiteScraper(setting)

    if not movieTitleScraper.checkUrl():
        print("info, main scraper.checkUrl = false")
        sys.exit()
    movieTitles = movieTitleScraper.getParseData()
    # <strong class="tit_join"><a class="link_g #list #monthly @1" href="/moviedb/main?movieId=111292">기생충</a></strong>, ...
    #print("info, main titles_tag = ", titles_tag)

    f = open(movie.fileName, 'a', encoding="utf-8")

    for index, movieTitle in enumerate(movieTitles, start=1):

        title = movieTitle.text
        print(title)

        f.write(title+"\n")

        if index == setting.json["movie"]["ranking"]:
            break
    f.close()

    sys.exit()
