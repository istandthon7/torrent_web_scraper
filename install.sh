#!/bin/bash

# ubuntu or debian
apt update
apt install -y python3-pip python3-testresources curl

#alpine
#apk add python3
#apk add py3-pip

python3 -m pip install --upgrade pip
python3 -m pip install --requirement requirements.txt

python3 ./scraperInstaller.py
