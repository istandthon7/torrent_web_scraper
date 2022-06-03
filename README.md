**실행 환경**  
테스트 OS : 리눅스(우분투, 데비안, 라즈베리파이OS), 윈도우10, 윈도우11  
실행 언어 : Python3
토렌트 클라이언트: [Transmission](https://transmissionbt.com)

# 1. 소개
torrent_web_scraper는 등록된 키워드로 게시판을 검색하여 토렌트(마그넷)를 자동 추가 해주는 웹스크랩퍼(웹크롤러)입니다.

# 1.1 설치
## 1.1.1 transmission 설치
[https://transmissionbt.com](https://transmissionbt.com)에서 운영체제에 맞는 프로그램을 다운받아 설치합니다. 윈도우의 경우 transmission-daemon이 설치되도록 설치옵션을 변경해야 합니다.

## 1.1.2 torrent_web_scraper 설치

    $ ./install.sh

# 1.2 설정
설치가 완료되면 config디렉토리의 setting.json 파일을 자신의 환경에 맞게 수정해주어야 합니다.

## 1.2.1 transmission 접속정보 설정
torrent_web_scraper이 transmission과 통신할 호스트(아이피), 아이디와 패스워드, 포트를 지정합니다. "trans-host"는 torrent_web_scraper와 transmission이 동일한 컴퓨터가 아닌 경우 웹브라우저에서 http://[transmission이 실행중인 아이피]:9091로 접속을 확인해 보는 것이 좋습니다. 우분투, 데비안의 경우 트랜스미션 데몬의 기본값을 변경하지 않은 경우에는 아래 설정을 변경하지 않아도 된다. 

    "trans-host": "127.0.0.1",
    "trans-id": "transmission",
    "trans-pw": "transmission",
    "trans-port": "9091"

## 1.2.2 토렌트 사이트 설정 
도메인에 숫자가 변경되는 경우가 있을 때에는 수정합니다. 

    "mainUrl": "https://torrentsir58.com/",

# 1.3 키워드 추가
TVShow.json 파일에 제목과 해상도 등은 옵션으로 추가로 지정할 수 있습니다. 시즌이 있는 경우 해당 숫자를 넣어주면 되고 없으면 생략합니다.

    ,
    {
        "name": "놀면 뭐하니",
        "option": "720",
        "option2": "NEXT"
        "season": 1
     }

Movie.txt 파일에 추가할 수 있습니다.

    제목1
    제목2

# 1.4 실행
torrent_web_scraper.py를 실행시키면 게시판을 읽어와서 TVShow.json와 Movie.txt에 등록한 키워드를 검색하여 transmission에 추가됩니다. 웹사이트에서 데이터를 가지고 오는 것은 다소 시간이 걸릴 수 있습니다. 

    $ ./torrent_web_scraper.py

# 1.5 스케줄러 등록
torrent_web_scraper를 주기적으로 실행하게 설정해두면, 토렌트 사이트를 방문하여 새로 등록된 마그넷 파일이 있는지 확인하고, 자동으로 추가해줍니다. 

**주의** 
토렌트 사이트를 웹 스크래핑하는 것은 불법이 아닙니다.  하지만, 토렌트를 사용하여 TV 프로그램 동영상을 다운로드하는 것은 저작권을 침해하는 불법 행위입니다.  이점을 이해하고 torrent_web_scraper 스크립트를 실행 여부를 결정하세요.  


# 변경이력
## 1.2
1. 설정파일 변경(setting.json파일에서 download-base, program-list 삭제, tvshow로 이동)
## 1.1.2
1. 기본 사이트 torrentsir로 변경
## 1.1.1
1. 기본 사이트 torrentview로 변경

## 1.1
1. 파일명 변경
* settings.json -> config/setting.json
* program_list.json -> config/TVShow.json 
* movie_list.txt -> config/Movie.txt 

