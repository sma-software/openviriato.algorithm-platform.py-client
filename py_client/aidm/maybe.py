from __future__ import annotations

from typing import Optional, Generic, TypeVar, Callable, Type

MaybeType = TypeVar("MaybeType")


class Maybe(Generic[MaybeType]):
    __has_value: bool
    __value: MaybeType

    def __init__(self, value: Optional[MaybeType]):
        self.__has_value = value is not None
        self.__value = value

    @property
    def has_value(self) -> bool:
        return self.__has_value

    @property
    def get_value(self) -> MaybeType:
        if self.__has_value:
            return self.__value
        else:
            raise ValueError("Tried to get a None-value from a {0}".format(self.__class__.__name__))

    @staticmethod
    def create_from_json(
            response: Optional[object],
            converter: Callable[[Type[MaybeType], object], MaybeType],
            aidm_class: Type[MaybeType]) -> Maybe[MaybeType]:
        if response is None:
            return Maybe(None)
        else:
            return Maybe(converter(aidm_class, response))
