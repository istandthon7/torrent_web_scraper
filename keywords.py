import json
import logging
import os
import stringHelper


class Keywords(stringHelper.StringHelper):
    def load(self, listFileName: str):
        try:
            with open(listFileName, "r", encoding='utf-8') as jsonFile:
                self.json = json.load(jsonFile)
        except json.JSONDecodeError:
            self.json = {'keywords':[]}
        if 'title_list' in self.json:
            self.json['keywords'] = self.json.pop('title_list')
        self.listFileName = listFileName

    def save(self):
        if self.listFileName is None:
            logging.warn("파일명이 지정되어 있지 않아요.")
            return
        with open(self.listFileName, "w", encoding='utf-8') as jsonFile:
            json.dump(self.json, jsonFile, ensure_ascii=False, indent=2)

    def removeKeyword(self, keyword: str) -> None:
        if 'keywords' in self.json:
            self.json['keywords'] = [k for k in self.json['keywords'] if k['name'] != keyword]
            self.save()

    def isExist(self, name: str) -> bool:
        if 'keywords' in self.json:
            return any(k['name'] == name for k in self.json['keywords'])
        return False

    def getSavePath(self, regKeyword: dict, basePath: str, createTitleFolder: bool) -> str:
        if not basePath:
            return ""
        downloadPath = basePath
        if regKeyword['prefixDir']:
            downloadPath = os.path.join(downloadPath, regKeyword['prefixDir'])
        if createTitleFolder:
            downloadPath = os.path.join(downloadPath, regKeyword['name'])
        if regKeyword['suffixDir']:
            downloadPath = os.path.join(downloadPath, regKeyword['suffixDir'])
        return downloadPath