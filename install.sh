#!/bin/bash

# ubuntu or debian
sudo apt update
sudo apt install -y python3-pip python3-testresources

#alpine
#apk add python3
#apk add py3-pip


pip3 install requests
pip3 install -r requirements.txt

./webScraperInstall.py
