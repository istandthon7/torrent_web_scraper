토렌트(마그넷) 자동 다운로드 프로젝트 - torrent_web_scraper는 원하는 토렌트 파일을 자동으로 다운로드 해주는 웹스크랩퍼(웹크롤러)입니다.  
torrent_web_scraper를 사용하면 토렌트(마그넷) 다운로드를 위해 토렌트 사이트를 방문할 필요가 없어집니다.  

**토렌트 자동 다운로드 프로젝트 - torrent_web_scraper 실행 환경**  
테스트 OS : 리눅스 - 우분투, 데비안, 라즈베리파이(라즈비안)   
실행 언어 : Python3

## 1. torrent_web_scraper
### 1.0 소개
torrent_web_scraper는 매일 새로 업로드되는 tv 프로그램을 다운로드하기 위해 토렌트 사이트를 돌아다니기 귀찮아서 제작을 구상하게 되었습니다.  
tv 프로그램 제목을 추가한 후에 토렌트사이트에 새로운 에피소드가 등록되면 [Transmission](https://transmissionbt.com)에 추가해줍니다.  

### 1.1 설치
#### 1.1.1 transmission설치
[https://transmissionbt.com](https://transmissionbt.com)에서 운영체제에 맞는 프로그램을 다운받아 설치합니다.(우분투, 데비안은 sudo apt install transmission-daemon 설정파일은  /etc/transmission-daemon/settings.json)  
시놀로지의 경우 패키지 센터를 통해 추가할 수 있습니다.  

#### 1.1.2 소스파일 다운로드
    $ git clone https://github.com/istandthon7/torrent_web_scraper.git
    $ cd torrent_web_scraper
#### 1.1.3 설치 
다음 명령을 실행하면 설치됩니다.  

    $ ./install.sh
### 1.2 설정파일 수정
설치가 완료되면 settings.json 파일을 자신의 환경에 맞게 수정해주어야 합니다.  
일반적으로 수정할 항목은 다음과 같습니다.  
#### 1.2.1 다운로드 경로(tv)를 지정  
다운받고자 하는 경로로 변경합니다.

    "download-base": "~/Downloads"
#### 1.2.2 transmission관련 설정  
트랜스미션 서버의 호스트(아이피), 아이디와 패스워드, 포트를 지정합니다.

    "trans-host": "",
    "trans-id": "",
    "trans-pw": "",
    "trans-port": "9091"
#### 1.2.3 다운받을 사이트 지정(site url) 
일반적으로 변경하지 않아도 되지만, 도메인에 숫자가 변경되는 경우가 있을 때에는 수정해 주어야 한다.  
category와 mainUrl을 변경해 주어야 한다.

    "url": "https://torrentsir29.com/bbs/board.php?bo_table=entertain"
    "mainUrl": "https://torrentsir29.com/",
사이트 자체가 폐쇄된 경우에는 [Issue](https://github.com/istandthon7/torrent_web_scraper/issues)에 등록하여 수정요청한다.     
### 1.3 다운로드 받을 프로그램 추가(program_list.json)
프로그램의 제목과 해상도 등은 옵션으로 추가로 지정할 수 있다. 시즌이 있는 경우 해당 숫자를 넣어주면 되고 없으면 생략해도 된다.

    {
        "name": "프로그램 제목",
        "option": "720",
        "option2": "NEXT"
        "season": 1
     }
### 1.4 tv프로그램 다운로드 받기
torrent_web_scraper.py를 실행시키면 게시판을 읽어와서 program_list.json에 등록한 tvshow를 transmission서버에 자동으로 추가되어 다운로드 받게 됩니다.

    $ ./torrent_web_scraper.py

torrent_web_scraper를 주기적으로 실행하게 설정해두면, 토렌트 사이트를 방문하여 새로 등록된 마그넷 파일이 있는지 확인하고, 자동으로 다운로드를 해줍니다.  
따라서 토렌트 파일이 업로드 되었는지 토렌트 사이트를 확인할 필요가 없어집니다.  

torrent_web_scraper는 파이썬3 기반으로 작성되었으며, 리눅스 기반인 우분투,데비안과 라즈베리파이(라즈비안)에서 동작을 확인하였습니다.  

**주의** 토렌트 사이트를 웹 스크래핑하는 것은 불법이 아닙니다. 하지만, 토렌트를 사용하여 TV 프로그램 동영상을 다운로드하는 것은 저작권을 침해하는 불법 행위입니다.  
이점을 이해하고 torrent_web_scraper 스크립트를 실행 여부를 결정하세요.  

web_scraper_daum_movie.py: 다음영화 관련 파싱 라이브러리  
movie_title_scraper.py: 다음 인기영화 스크래퍼  
"movie_list.txt": 다운받을 영화들, settings.json파일의 movie->list에서 설정     
