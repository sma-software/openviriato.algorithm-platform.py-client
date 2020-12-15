import datetime
from enum import Enum, unique
from typing import Optional

from py_client.aidm.aidm_base_classes import _HasDebugString


@unique
class LinkType(Enum):
    await_arrival = 1
    connection = 2


class AlgorithmLink(_HasDebugString):
    __from_node_id: int
    __from_train_id: int
    __from_train_path_node_id: int
    __link_type: LinkType
    __to_node_id: int
    __to_train_id: int
    __to_train_path_node_id: int

    def __init__(self,
                 debug_string: str,
                 from_node_id: int,
                 from_train_id: int,
                 from_train_path_node_id: int,
                 link_type: LinkType,
                 to_node_id: int,
                 to_train_id: int,
                 to_train_path_node_id: int):
        _HasDebugString.__init__(self, debug_string)
        self.__from_node_id = from_node_id
        self.__from_train_id = from_train_id
        self.__from_train_path_node_id = from_train_path_node_id
        self.__link_type = link_type
        self.__to_node_id = to_node_id
        self.__to_train_id = to_train_id
        self.__to_train_path_node_id = to_train_path_node_id

    @property
    def from_node_id(self) -> int:
        return self.__from_node_id

    @property
    def from_train_id(self) -> int:
        return self.__from_train_id

    @property
    def from_train_path_node_id(self) -> int:
        return self.__from_train_path_node_id

    @property
    def link_type(self) -> LinkType:
        return self.__link_type

    @property
    def to_node_id(self) -> int:
        return self.__to_node_id

    @property
    def to_train_id(self) -> int:
        return self.__to_train_id

    @property
    def to_train_path_node_id(self) -> int:
        return self.__to_train_path_node_id


class AlgorithmConnectionLink(AlgorithmLink):
    __minimum_duration: datetime.timedelta
    __maximum_deviation: Optional[datetime.timedelta]
    __weight: Optional[int]

    def __init__(self,
                 debug_string: str,
                 from_node_id: int,
                 from_train_id: int,
                 from_train_path_node_id: int,
                 link_type: LinkType,
                 to_node_id: int,
                 to_train_id: int,
                 to_train_path_node_id: int,
                 minimum_duration: datetime.timedelta,
                 maximum_deviation: Optional[datetime.timedelta],
                 weight: Optional[int]):
        AlgorithmLink.__init__(self,
                               debug_string,
                               from_node_id,
                               from_train_id,
                               from_train_path_node_id,
                               link_type,
                               to_node_id,
                               to_train_id,
                               to_train_path_node_id)

        self.__minimum_duration = minimum_duration
        self.__maximum_deviation = maximum_deviation
        self.__weight = weight

    @property
    def minimum_duration(self) -> datetime.timedelta:
        return self.__minimum_duration

    @property
    def maximum_deviation(self) -> Optional[datetime.timedelta]:
        return self.__maximum_deviation

    @property
    def weight(self) -> Optional[int]:
        return self.__weight


class AlgorithmAwaitArrivalLink(AlgorithmLink):
    __minimum_duration: datetime.timedelta

    def __init__(self,
                 debug_string: str,
                 from_node_id: int,
                 from_train_id: int,
                 from_train_path_node_id: int,
                 link_type: LinkType,
                 to_node_id: int,
                 to_train_id: int,
                 to_train_path_node_id: int,
                 minimum_duration: datetime.timedelta):
        AlgorithmLink.__init__(self,
                               debug_string,
                               from_node_id,
                               from_train_id,
                               from_train_path_node_id,
                               link_type,
                               to_node_id,
                               to_train_id,
                               to_train_path_node_id)
        self.__minimum_duration = minimum_duration

    @property
    def minimum_duration(self) -> datetime.timedelta:
        return self.__minimum_duration
