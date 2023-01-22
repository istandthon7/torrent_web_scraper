
class StringHelper:
    """tvshow와 movie에서 상속받는다."""
    def IsContainAllWordsInBoardTitle(self, allWords: str, boardTitle: str)->bool:
        boardTitle = boardTitle.lower()
        wordArray = allWords.lower().split()
        for tmp in wordArray:
            if not tmp in boardTitle:
                return False
        return True