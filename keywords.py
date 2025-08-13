import json
import logging
import os
import stringHelper

class Keywords(stringHelper.StringHelper):

    def addKeyword(self, keyword: str) -> None:
        newKeyword = {"name": keyword, "option": "","option2":"", "exclude": ""}
        if self.isExist(keyword):
            logging.info(f"이미 존재하는 키워드입니다. '{keyword}'")
            return
        if 'keywords' in self.json:
            self.json['keywords'].append(newKeyword)
            logging.info(f"키워드를 추가했습니다. '{newKeyword}'")
            # 저장은 직접
            #self.save()

    def isKeywordMatchForTitle(self, keyword: dict, title: str) -> bool:
        if not self.isWordContainedInParam(keyword['name'].replace(":", " "), title):
            logging.debug(f'[{keyword["name"]}] 키워드에 해당하지 않습니다. {title}')
            return False
        if 'exclude' in self.downloadRuleSetting and self.downloadRuleSetting['exclude'] and self.IsContainAnyCommaSeparatedWordsInBoardTitle(self.downloadRuleSetting['exclude'], title):
            logging.info(f"[{keyword['name']}] 전체 제외 키워드가 포함되어 있어요. [{self.downloadRuleSetting['exclude']}] '{title}'")
            return False
        if 'exclude' in keyword and keyword['exclude'] and self.IsContainAnyCommaSeparatedWordsInBoardTitle(keyword['exclude'], title):
            logging.info(f"[{keyword['name']}] 제외 키워드가 포함되어 있어요. [{keyword['exclude']}]")
            return False
        if not self.isWordContainedInParam(keyword['option'], title):
            logging.info(f"[{keyword['name']}] option이 달라요. [{keyword['option']}] '{title}'")
            return False
        if not self.isWordContainedInParam(keyword['option2'], title):
            logging.info(f"[{keyword['name']}] option2가 달라요. [{keyword['option2']}] '{title}'")
            return False
        if 'include' in self.downloadRuleSetting and self.downloadRuleSetting['include']:
            includes = self.downloadRuleSetting['include'].split(', ')
            for include in includes:
                if not self.isWordContainedInParam(include, title):
                    logging.info(f"[{keyword['name']}] 포함되어야 하는 단어가 없어요. [{include}] '{title}'")
                    return False
        return True

    def getRegKeyword(self, boardTitle: str) -> dict:
        for keyword in self.json['keywords']:
            if self.isKeywordMatchForTitle(keyword, boardTitle):
                return keyword
        return {}
            
    def load(self, configDirPath: str, downloadRuleSetting: dict) -> None:
        try:
            listFileName = os.path.join(configDirPath, downloadRuleSetting['list'])
            with open(listFileName, "r", encoding='utf-8') as jsonFile:
                self.json = json.load(jsonFile)
        except json.JSONDecodeError:
            self.json = {'keywords':[]}
        self.listFileName = listFileName
        self.downloadRuleSetting = downloadRuleSetting

    def save(self):
        if self.listFileName is None:
            logging.warning("파일명이 지정되어 있지 않아요.")
            return
        with open(self.listFileName, "w", encoding='utf-8') as jsonFile:
            json.dump(self.json, jsonFile, ensure_ascii=False, indent=2)

    def removeKeyword(self, keyword: str) -> None:
        if 'keywords' in self.json:
            self.json['keywords'] = [k for k in self.json['keywords'] if k['name'] != keyword]
            self.save()
            logging.info(f"키워드 리스트에서 삭제했습니다. [{keyword}]")

    def isExist(self, name: str) -> bool:
        if 'keywords' in self.json:
            return any(k['name'] == name for k in self.json['keywords'])
        return False

    def getSavePath(self, regKeyword: dict, basePath: str, createTitleFolder: bool) -> str:
        if not basePath:
            logging.debug("basePath가 지정된 경우만 하위폴더를 생성합니다.")
            return ""
        downloadPath = basePath
        if regKeyword.get('parentDir'):
            downloadPath = os.path.join(downloadPath, regKeyword['parentDir'])
        if createTitleFolder:
            downloadPath = os.path.join(downloadPath, regKeyword['name'])
        if regKeyword.get('subDir'):
            downloadPath = os.path.join(downloadPath, regKeyword['subDir'])
        return downloadPath