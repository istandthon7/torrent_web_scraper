#!/usr/bin/python3

import os
import sys
import daumMovieTitleScraper
import setting
import movie
import logging

if __name__ == '__main__':

    mySetting = setting.Setting()
    myMovie = movie.Movie(mySetting.json['movie'])
    myMovie.load(os.path.join(mySetting.configDirPath, mySetting.json['movie']['list']))
    movieTitleScraper = daumMovieTitleScraper.DaumMovieTitleScraper(mySetting.json["movie"]["titleScrap"])

    if not movieTitleScraper.checkUrl():
        logging.info("main scraper.checkUrl = false")
        sys.exit()
    movieTitles = movieTitleScraper.getParseData()

    for index, movieTitle in enumerate(movieTitles, start=1):
        title = movieTitle.text.strip()
        myMovie.addKeyword(title)
        if index == mySetting.json["movie"]["titleScrap"]["ranking"]:
            myMovie.save()
            break

    sys.exit()
