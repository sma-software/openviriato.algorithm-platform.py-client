from typing import Optional

from py_client.aidm.maybe import Maybe


class FloatingPoint:
    __mantissa: Maybe[int]
    __decimal_places: int

    def __init__(self, mantissa: Maybe[Optional[int]], decimal_places: int):
        self.__decimal_places = decimal_places
        self.__mantissa = mantissa

    @property
    def mantissa(self) -> Maybe[int]:
        return self.__mantissa

    @property
    def decimal_places(self) -> int:
        return self.__decimal_places
