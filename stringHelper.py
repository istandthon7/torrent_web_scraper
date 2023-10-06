import re

class StringHelper:
    def splitIntoWords(self, param: str) -> list:
        """Split the parameter into words based on special characters and spaces."""
        return [word for word in re.split(r'[.,;:\s]\s*', param.lower()) if word]

    def isExactWordInParam(self, param1: str, param2: str) -> bool:
        """Check if all words in the shorter parameter are exactly in the longer parameter."""
        param1Array = self.splitIntoWords(param1)
        param2Array = self.splitIntoWords(param2)

        # Compare based on the shorter parameter
        if len(param1) < len(param2):
            return all(word in param2Array for word in param1Array)
        else:
            return all(word in param1Array for word in param2Array)

    def isWordContainedInParam(self, param1: str, param2: str) -> bool:
        """Check if all words in the shorter parameter are contained in the longer parameter."""
        param1Array = self.splitIntoWords(param1)
        param2 = param2.lower()

        # Check if each word in the shorter parameter is contained in the longer parameter
        if len(param1) < len(param2):
            return all(word in param2 for word in param1Array)
        else:
            return all(word in param1 for word in param2.split())
    
    def IsContainAnyCommaSeparatedWordsInBoardTitle(self, keywords: str, boardTitle: str) -> bool:
        boardTitle = boardTitle.lower()
        wordArray = keywords.lower().split(',')
        return any(tmp.strip() in boardTitle for tmp in wordArray)
