#!/bin/bash

# 첫 번째 파라미터를 가상 환경의 경로로 사용
VENV_PATH=$1

# 스크립트에서 어떤 명령어가 실패하면 즉시 스크립트 실행을 중단
set -e

# ubuntu or debian
apt update
apt install -y python3-pip python3-testresources curl

# 가상 환경 생성 및 활성화
if [ -n "$VENV_PATH" ]; then
    apt install -y python3-venv
    python3 -m venv $VENV_PATH
    source $VENV_PATH/bin/activate
fi

#alpine
#apk add python3
#apk add py3-pip

python3 -m pip install --upgrade pip
python3 -m pip install --requirement requirements.txt

python3 ./scraperInstaller.py
