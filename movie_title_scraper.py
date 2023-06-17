#!/usr/bin/python3

import sys
import daumMovieTitleScraper
import setting
import movie
import logging

if __name__ == '__main__':

    mySetting = setting.Setting()
    myMovie = movie.Movie(mySetting.configDirPath, mySetting.json['movie'])

    movieTitleScraper = daumMovieTitleScraper.SiteScraper(mySetting)

    if not movieTitleScraper.checkUrl():
        logging.info("main scraper.checkUrl = false")
        sys.exit()
    movieTitles = movieTitleScraper.getParseData()

    with open(mySetting.json['movie']['list'], 'a', encoding="utf-8") as f:
        for index, movieTitle in enumerate(movieTitles, start=1):
            title = movieTitle.text
            logging.info(title)
            f.write(title+"\n")
            if index == mySetting.json["movie"]["titleScrap"]["ranking"]:
                break

    sys.exit()
