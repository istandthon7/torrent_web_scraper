class StringHelper:
    """tvshow와 movie에서 상속받는다."""
    def IsContainAllWordsInBoardTitle(self, keyword: str, boardTitle: str)->bool:
        boardTitle = boardTitle.lower()
        wordArray = keyword.lower().split()
        return all(tmp in boardTitle for tmp in wordArray)
    
    def IsContainAnyCommaSeparatedWordsInBoardTitle(self, keywords: str, boardTitle: str) -> bool:
        boardTitle = boardTitle.lower()
        wordArray = keywords.lower().split(',')
        return any(tmp.strip() in boardTitle for tmp in wordArray)
