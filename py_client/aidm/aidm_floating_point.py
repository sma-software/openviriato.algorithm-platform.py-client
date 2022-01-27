from typing import Optional

class FloatingPoint:
    __mantissa: int
    __decimal_places: int

    def __init__(self, mantissa: int, decimal_places: int):
        self.__decimal_places = decimal_places
        self.__mantissa = mantissa

    @property
    def mantissa(self) -> int:
        return self.__mantissa

    @property
    def decimal_places(self) -> int:
        return self.__decimal_places
