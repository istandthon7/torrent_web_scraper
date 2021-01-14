#!/bin/bash

# ubuntu or debian
sudo apt update
sudo apt install -y python3-pip python3-testresources

#alpine
#apk add python3
#apk add py3-pip


pip3 install requests
pip3 install beautifulsoup4
pip3 install -r requirements.txt

echo "./torrent_web_scraper_install.py 를 실행하세요"
echo "./torrent_web_scraper.py 를 실행하세요"
echo "cron에 등록하여 사용할 수 있습니다."
