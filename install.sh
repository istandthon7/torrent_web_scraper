#!/bin/bash

# sudo: command not found ==> apt install sudo
# ubuntu or debian
sudo apt update
sudo apt install -y python3-pip python3-testresources curl

#alpine
#apk add python3
#apk add py3-pip

# 윈도우에서는 python3 -> python
python3 -m pip install --upgrade pip
python3 -m pip install --requirement requirements.txt

python3 ./scraperInstaller.py
