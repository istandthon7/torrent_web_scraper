class BoardItem:
    episode = 0
    resolution = 480

    def __init__(self, title: str, url: str, ID: int, number: int) -> None:
        self.title = title
        self.url = url
        self.id = ID
        self.number = number