
class ConfigHelper:
    def IsContainAllWordsInBoardTitle(self, allWords: str, boardTitle: str)->bool:
        boardTitle = boardTitle.lower()
        wordArray = allWords.lower().split()
        for tmp in wordArray:
            if not tmp in boardTitle:
                return False
        return True