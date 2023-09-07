class UserOutputSettings:
    __preferred_culture: str

    def __init__(self, preferred_culture: str):
        self.__preferred_culture = preferred_culture

    @property
    def preferred_culture(self) -> str:
        return self.__preferred_culture
