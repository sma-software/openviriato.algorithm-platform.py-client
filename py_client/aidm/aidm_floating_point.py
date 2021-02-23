from typing import Optional

from py_client.aidm.maybe import Maybe


class FloatingPoint:
    __decimal_places: int
    __mantissa: Maybe[int]

    def __init__(self, decimal_places: int, mantissa: Maybe[Optional[int]]):
        self.__decimal_places = decimal_places
        self.__mantissa = mantissa

    @property
    def decimal_places(self) -> int:
        return self.__decimal_places

    @property
    def mantissa(self) -> Maybe[int]:
        return self.__mantissa
