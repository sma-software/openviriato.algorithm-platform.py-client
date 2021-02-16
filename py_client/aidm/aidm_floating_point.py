class FloatingPoint:
    __decimal_places: int
    __mantissa: int

    def __init__(self, decimal_places: int, mantissa: int):
        self.__decimal_places = decimal_places
        self.__mantissa = mantissa

    @property
    def decimal_places(self) -> int:
        return self.__decimal_places

    @property
    def mantissa(self) -> int:
        return self.__mantissa
