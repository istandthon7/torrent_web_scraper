
class ConfigHelper:
    def checkTitleInBoardTitle(self, title: str, boardTitle: str)->bool:
        keyArray = title.lower().split()
        for tmp in keyArray:
            if not tmp in boardTitle:
                return False
        return True