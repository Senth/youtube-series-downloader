class Video:
    def __init__(self, id: str, date: str, title: str):
        self.id = id
        self.date = date
        self.title = title

    def __members(self):
        return (
            self.id,
            self.date,
            self.title,
        )

    def __eq__(self, other) -> bool:
        if type(other) is type(self):
            return self.__members() == other.__members()
        return False

    def __hash__(self) -> int:
        return hash(self.__members())

    def __repr__(self) -> str:
        return str(self.__members())
