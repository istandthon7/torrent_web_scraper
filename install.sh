#!/bin/bash

sudo apt update
sudo apt install -y python3-pip
pip3 install -r requirements.txt
./torrent_web_scraper_install.py

echo "./torrent_web_scraper.py 를 실행하세요"
echo "cron에 등록하여 사용할 수 있습니다."