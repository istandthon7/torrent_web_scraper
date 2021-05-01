토렌트(마그넷) 신규 에피소드 자동 다운로드 프로젝트 
torrent_web_scraper는 원하는 토렌트 파일을 자동으로 다운로드 해주는 웹스크랩퍼(웹크롤러)입니다.  torrent_web_scraper를 사용하면 토렌트(마그넷) 다운로드를 위해 토렌트 사이트를 방문할 필요가 없어집니다.  

**토렌트 자동 다운로드 프로젝트 - torrent_web_scraper 실행 환경**  
테스트 OS : 리눅스(우분투, 데비안, 라즈베리파이OS), 윈도우10   
실행 언어 : Python3

## 1. torrent_web_scraper
### 1.0 소개
torrent_web_scraper는 매일 새로 업로드되는 tv 프로그램을 다운로드하기 위해 토렌트 사이트를 돌아다니기 귀찮아서 제작을 구상하게 되었습니다. tv 프로그램 제목이나 영화 제목을 등록해 놓으면 토렌트사이트에 새로운 에피소드와 영화가 등록되면 [Transmission](https://transmissionbt.com)에 추가됩니다.  

### 1.1 설치
#### 1.1.1 transmission설치
[https://transmissionbt.com](https://transmissionbt.com)에서 운영체제에 맞는 프로그램을 다운받아 설치합니다.(우분투, 데비안은 sudo apt install transmission-daemon 설정파일은  /etc/transmission-daemon/settings.json)  윈도우의 경우 transmission-daemon이 설치되도록 설치옵션을 변경해 줘야 합니다.

#### 1.1.2 소스파일 다운로드

    $ git clone https://github.com/istandthon7/torrent_web_scraper.git
    $ cd torrent_web_scraper

#### 1.1.3 설치 
다음 명령을 실행하면 설치됩니다.  

    $ ./install.sh

### 1.2 설정파일 수정
설치가 완료되면 config디렉토리의 setting.json 파일을 자신의 환경에 맞게 수정해주어야 합니다.  일반적으로 수정할 항목은 다음과 같습니다.  

#### 1.2.1 transmission관련 설정  
트랜스미션 데몬의 호스트(아이피), 아이디와 패스워드, 포트를 지정합니다.  호스트는 동일한 컴퓨터가 아닌 경우 웹브라우저에서 http://[데몬이 실행중인 아이피]:9091로 접속을 확인해 보는 것이 좋다.  우분투, 데비안의 경우 트랜스미션 데몬의 기본값을 변경하지 않은 경우에는 아래 설정을 변경하지 않아도 된다.  

    "trans-host": "127.0.0.1",
    "trans-id": "transmission",
    "trans-pw": "transmission",
    "trans-port": "9091"

#### 1.2.2 토렌트를 다운받을 사이트 설정  
도메인에 숫자가 변경되는 경우가 있을 때에는 수정합니다.  

    "mainUrl": "https://torrentview30.com/",

사이트 자체가 폐쇄된 경우에는 [Issue](https://github.com/istandthon7/torrent_web_scraper/issues)에 등록하여 수정요청할 수 있습니다.   

#### 1.2.3 영화 해상도
영화파일은 1080p를 받도록 설정되어 있습니다.  720p등으로 변경하려면 "movie"의 "resolution"을 변경해야 합니다.  

### 1.3 다운로드 받을 tv프로그램 추가(TVShow.json)
프로그램의 제목과 해상도 등은 옵션으로 추가로 지정할 수 있다. 시즌이 있는 경우 해당 숫자를 넣어주면 되고 없으면 생략해도 된다.

    ,
    {
        "name": "프로그램 이름",
        "option": "720",
        "option2": "NEXT"
        "season": 1
     }

### 1.4 다운받을 영화 제목 추가(Movie.txt)

    영화제목1
    영화제목2

### 1.5 tv프로그램 다운로드 받기
torrent_web_scraper.py를 실행시키면 게시판을 읽어와서 TVShow.json에 등록한 tvshow를 transmission서버에 자동으로 추가되어 다운로드 받게 됩니다.  웹사이트에서 데이터를 가지고 오는 것은 다소 시간이 걸릴 수 있다. 

    $ ./torrent_web_scraper.py

### 1.6 스케줄러 등록
torrent_web_scraper를 주기적으로 실행하게 설정해두면, 토렌트 사이트를 방문하여 새로 등록된 마그넷 파일이 있는지 확인하고, 자동으로 다운로드를 해줍니다.  

**주의** 
토렌트 사이트를 웹 스크래핑하는 것은 불법이 아닙니다.  하지만, 토렌트를 사용하여 TV 프로그램 동영상을 다운로드하는 것은 저작권을 침해하는 불법 행위입니다.  이점을 이해하고 torrent_web_scraper 스크립트를 실행 여부를 결정하세요.  

movie_title_scraper.py: 다음 인기영화 스크래퍼 (지난 달 인기영화 제목을 스크랩하여 "Movie.txt"에 저장해준다.)  


# 변경이력
## 1.1
1. 파일명 변경
* settings.json -> config/setting.json (setting.json파일은 내용 변경이 있으니 trans- 부분의 연결정보를 갱신하세요.)  
* program_list.json -> config/TVShow.json  
* movie_list.txt -> config/Movie.txt  

