class StringHelper:
    """tvshow와 movie에서 상속받는다."""
    def IsContainAllWordsInBoardTitle(self, keyword: str, boardTitle: str)->bool:
        boardTitle = boardTitle.lower()
        wordArray = keyword.lower().split()
        return all(tmp in boardTitle for tmp in wordArray)
