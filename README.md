**실행 환경**  
테스트 OS : 리눅스(우분투, 데비안, 라즈베리파이OS), 윈도우10, 윈도우11  
실행 언어 : Python3.9이상  
토렌트 클라이언트: [Transmission](https://transmissionbt.com), [qBittorrent](https://www.qbittorrent.org/)

# 1. 소개
등록된 키워드로 게시판을 검색하여 토렌트(magnet)를 추가 해주는 스크랩퍼(크롤러)입니다.

# 1.1 설치
## 1.1.1 토렌트 클라이언트 설치
Transmission 혹은 qBittorrent를 설치합니다.
### 1.1.1.1 transmission 설치 
[https://transmissionbt.com](https://transmissionbt.com)에서 운영체제에 맞는 프로그램을 다운받아 설치합니다. 윈도우의 경우 transmission-daemon이 설치되도록 설치옵션을 변경해야 합니다.
### 1.1.1.2 qBittorrent 설치 
https://github.com/qbittorrent/qBittorrent/wiki/Installing-qBittorrent

## 1.1.2 스크래퍼 설치
소스를 다운로드 받은 후에 다음 스크립트를 실행합니다. 관리자 권한이 필요합니다.

    # ./install.sh
 혹은 가상환경 경로를 지정할 수 있습니다.

    # ./install.sh venv

# 1.2 설정
설치가 완료되면 config디렉토리의 setting.json 파일을 환경에 맞게 수정해야 합니다.  
'online json editor'를 검색하여 수정하는 것을 추천합니다.

## 1.2.1 접속정보 설정
토렌트 클라이언트와 통신할 호스트명(아이피), 포트, 아이디를 지정합니다. 
Transmission은 웹브라우저에서 http://[transmission이 실행중인 아이피]:9091로 접속을 확인해 보는 것이 좋습니다. 비밀번호는 설정파일에 저장하지 않으므로 실행할 때 파라미터로 전달할 수 있습니다.

    "torrentClient": {
      "type": "qBittorrent" 혹은 "transmission"
      "host": "127.0.0.1",
      "port": 9091 혹은 8080,
      "id": "transmission" 혹은 "admin"
    }

## 1.2.2 토렌트 사이트 설정 
mainUrl과 게시판을 설정합니다. 게시판은 여러 개로 구성할 수 있고, url은 mainUrl을 제외한 나머지 주소입니다. title selector는 브라우저의 개발자 도구를 이용하여 css selector를 지정합니다. 

    "mainUrl": "https://mainUrl.com/",
    "boards": [
      {
        "name": "게시판명",
        "url": "subUrl",
        "title": {
          "selector": "ul.list-body > li.list-item"
        },
        "downloadRule": "secondRule",
        "history": 0,
        "number": 0,
        "scrapPage": 3
      },
      {
        "name": "게시판2",
        "url": "usbUrl",
        "title": {
          "selector": "ul.list-body > li.list-item"
        },
        "downloadRule": "firstRule",
        "history": 0,
        "number": 0,
        "scrapPage": 3
      }
    ]

## 1.2.3 downloadRules 설정
게시판에서 사용할 다운로드 규칙의 프리셋입니다. name은 게시판의 downloadRule과 연결되므로 적당한 이름을 사용하세요. download는 다운로드 경로입니다. list는 키워드 리스트의 파일명이고 config폴더에 위치합니다. createTitleFolder는 키워드 폴더를 생성할지 여부입니다. checkEpisodeNubmer는 회차가 동일한 경우 처음 검색한 것만 추가할지 여부입니다. deleteOlderEpisodes는 토렌트 추가 후 이전 에피소드를 토렌트 클라이언트에서 삭제할지 여부입니다. include는 제외, exclude는 제외할 키워드이며 쉼표로 구분됩니다. removeFromList는 토렌트 추가 후 키워드 리스트에서 삭제할지 여부입니다.

    "downloadRules":[
      {
        "name": "firstRule",
        "download": "",
        "list": "first.json",
        "createTitleFolder": false,
        "checkEpisodeNubmer": false,
        "deleteOlderEpisodes": true
      },
      {
        "name": "secondRule",
        "download": "",
        "list": "second.json",
        "include": "",
        "exclude": "",
        "removeFromList": true
      }
    ],

# 1.3 키워드 추가
 downloadRules의 list에 해당하는 파일에 name과 option에 키워드를, 제외 키워드에 쉼표로 구분된 키워드를 추가할 수 있고, 상위 폴더와 하위 폴더를 지정할 수 있습니다. 폴더는 downloadRules에서 download 경로가 지정된 경우에 지정할 수 있어요.

    "keywords": [
        {"name": "키워드", "option": "포함1", "option2":"포함2", "exclude":"제외, 제외2", "parentDir": "상위폴더", "subDir": "하위폴더" }
        ,{"name": "간단한", "option": "", "option2":""}
    ]

# 1.4 실행
__main__.py 폴더에서 다음 명령어를 실행하면 게시판에서 등록한 키워드를 검색하여 토렌트 클라이언트에 추가됩니다. 스크랩은 아주 느리게 작동됩니다. 

    $ python3 . --password 비밀번호

# 1.5 스케줄러 등록
주기적으로 실행하도록 cron 등의 스케줄러에 설정해서 스크랩을 실행할 수 있습니다.
  
**주의** 

토렌트 사이트를 스크래핑하는 것은 불법이 아닙니다. 하지만, 토렌트 클라이언트는 일반적으로 다운로드 중에 업로드되고, 이로 인한 배포로 저작권을 침해하는 것이므로 불법입니다. 이점을 이해하고 키워드 등록에 각별히 유의하세요.


# 변경이력
## 2.4
* download rule추가 (setting.json)
  * tvshow와 movie를 downloadRules로 이동하고 name을 tvshow로 설정하고 사용할 수 있어요. movie는 include에 해상도와 코덱 등을 설정할 수 있어요.
* sites하위의 categories를 boards로 변경하고 하위에 "downloadRule":"tvshow"로 설정
* 키워드 파일(downloadRules의 list에 해당하는 파일) 포맷 변경
## 2.3.2
* torrentHistory.csv 컬럼 추가 #82 (기존 파일은 삭제/백업이 필요할 수 있어요.)
## 2.3.1
* log 회전
```
"logging": {
  "maxBytes": 1048576,
  "backupCount": 5
}
```
## 2.3
* qBittorrent 지원 #65 (setting.json파일 변경이 필요합니다. transmission -> torrentClient, owners)
```
  "torrentClient": {
    "host": "",
    "port": 9091,
    "id": "client id",
    "type": "transmission" or "qBittorrent"
  },
  "owners": {
    "puid": 1000,
    "pgid": 1000
  }
```
* 알림 중복 개선 #74
* urllib3 1.26.17 (보안이슈)
## 2.2.06.2
* "logFile": "scraper.log" 로 폴더 제거 #62
* notiHistory파일 config 폴더에 생성 #61
* notiHistory url추가
## 2.2.06.1
* KeyError: 'parentDir' #57
## 2.2.06
* Movie.txt를 Movie.json으로 변경 (이전 버전 사용자는 setting.json에서 변경해야 합니다.)
* transmission 패스워드 제거
## 2.2.05.2
* NameError: name 'episodeNumber' is not defined #53
## 2.2.05.1
* 에피소드 체크를 설정한 경우 스크랩이 중단되는 버그 #51
## 2.2.05
* url 변경 버그. */home.php #43
* "checkEpisodeNubmer"키가 생성되지 않는 버그 #37 upgrade시 발생할 수 있는 부분 수정
* tvshow title 폴더생성 옵션 #35
## 2.2.04.1
* 이전 회차 삭제되지 않는 버그 수정
## 2.2.04
* Python3.6 지원 중단
* 중분류가 있는 경우 스크랩이 누락되는 버그 수정
## 2.2.03.1
* 제외 키워드 추가(setting.json: movie)
## 2.2.03
* 에피소드 체크 추가 (setting.json: tvshow의 checkEpisodeNubmer이 true인 경우에 작동)
* 제외 키워드 추가(TVShow.json)
## 2.2.02
* requests 업그레이드(취약점은 Proxy-Authorization 헤더가 목적지 서버로 유출될 수 있는 문제)
* 샘플 사이트 변경
## 2.2.01
* 기본 폴더에 magnet추가
## 2.2
* 로그파일 위치 이동
## 2.1.10
* 이전 에피소드 삭제 버그 수정
## 2.1.09
* 사이트 주소 갱신 개선
* 게시판 아이디 처리 개선
## 2.1.08
* uid, gid지원 (폴더권한)
## 2.1.07
* 폴더를 설정하지 않은 경우 다운로드가 완료되지 않았던 버그 수정
* transmission 로그인 설정이 되지 않은 경우 버그 수정
## 2.1.06
* 사이트 주소 갱신 개선
## 2.1.05
* magnet검색 버그 수정
## 2.1.04
* 스크랩 페이지 수 게시판별로 설정
* 지원 사이트 추가
* 사이트 접속시에 예외처리 추가
* selector 지원
## 2.1.03
* 실행방식 변경(비밀번호 파라미터 추가)
* 다운로드 폴더 권한 변경 개선
## 2.1.02
* 간헐적으로 사이트 주소가 바로 적용되지 않았던 버그 수정
## 2.1.01
* 간헐적으로 사이트 주소 갱신이 되지 않는 버그 수정
## 2.1.00 
* 사이트 주소 자동갱신
## 2.0.00
* 로그 개선
* 스크랩 사이트 추가 지원
## 2.0.00-beta2.11
* 디버그용 로그 개선
## 2.0.00-beta2.1
* 폴더 권한의 간헐적인 버그 수정
## 2.0.00-beta2
* 폴더 권한 관련 개선
## 2.0.00-beta1
* Movie.txt 에서 간헐적으로 삭제되지 않았던 버그 수정
* transmission 보안연결 지원
* 스크랩 페이지 2에서 3페이지 늘림(config/setting.json: scrapPage)
## 2.0.00-alpha3
* 폴더 권한 처리
## 2.0.00-alpha2
* 로그 추가
  * 설정파일 "logging" 추가
## 2.0.00-alpha1
* 설정파일 변경
  * "movie"에서 
    * "resolution": "1080"를 "resolution": 1080 숫자로 변경.
    * "video_codec"을 "videoCodec"으로 변경.
  * "sites"에서 
    * "board"제거(사용안함)
    * "category"를 "categories"로 변경.및 "title" 추가. 
  * "page_scrap_max"를 "scrapPage"로 변경.
  * torrentHistory, torrentFail 추가
