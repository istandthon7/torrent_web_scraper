#!/usr/bin/python3

import sys
import daumMovieTitleScraper
import setting
import movie

if __name__ == '__main__':

    mySetting = setting.Setting()
    mySetting.loadJson()
    myMovie = movie.Movie(mySetting)

    movieTitleScraper = daumMovieTitleScraper.SiteScraper(mySetting)

    if not movieTitleScraper.checkUrl():
        print("info, main scraper.checkUrl = false")
        sys.exit()
    movieTitles = movieTitleScraper.getParseData()
    # <strong class="tit_join"><a class="link_g #list #monthly @1" href="/moviedb/main?movieId=111292">기생충</a></strong>, ...
    #print("info, main titles_tag = ", titles_tag)

    f = open(myMovie.fileName, 'a', encoding="utf-8")

    for index, movieTitle in enumerate(movieTitles, start=1):

        title = movieTitle.text
        print(title)

        f.write(title+"\n")

        if index == mySetting.json["movie"]["ranking"]:
            break
    f.close()

    sys.exit()
