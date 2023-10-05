import re


class StringHelper:
    """tvshow와 movie에서 상속받는다."""
    def isShorterParamWordsContainedInLongerParam(self, param1: str, param2: str)->bool:
        param1 = param1.lower()
        param2 = param2.lower()
        param1Array = re.split(r'[.,;:\s]\s*', param1)
        param2Array = re.split(r'[.,;:\s]\s*', param2)

        # Compare based on the shorter parameter
        if len(param1) < len(param2):
            return all(word in param2Array for word in param1Array)
        else:
            return all(word in param1Array for word in param2Array)
    
    def IsContainAnyCommaSeparatedWordsInBoardTitle(self, keywords: str, boardTitle: str) -> bool:
        boardTitle = boardTitle.lower()
        wordArray = keywords.lower().split(',')
        return any(tmp.strip() in boardTitle for tmp in wordArray)
