class FloatingPoint:
    __decimal_places: int
    __value: int

    def __init__(self, decimal_places: int, value: int):
        self.__decimal_places = decimal_places
        self.__value = value

    @property
    def decimal_places(self) -> int:
        return self.__decimal_places

    @property
    def value(self) -> int:
        return self.__value
