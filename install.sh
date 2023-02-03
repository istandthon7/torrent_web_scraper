#!/bin/bash

# sudo: command not found ==> apt install sudo
# ubuntu or debian
sudo apt update
sudo apt install -y python3-pip python3-testresources curl

#alpine
#apk add python3
#apk add py3-pip

# for window: python -m pip install -r requirements.txt
pip3 install -r requirements.txt

python3 ./scraperInstaller.py
