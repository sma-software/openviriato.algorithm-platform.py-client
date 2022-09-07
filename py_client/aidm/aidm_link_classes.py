import datetime
from enum import Enum, unique
from typing import Optional

from py_client.aidm.aidm_base_classes import _HasID
from py_client.aidm.aidm_base_classes import _HasDebugString


@unique
class LinkType(Enum):
    await_arrival = "awaitArrival"
    connection = "connection"
    roster = "roster"


class _AlgorithmLink(_HasDebugString, _HasID):
    __from_node_id: int
    __from_train_id: int
    __from_train_path_node_id: int
    __to_node_id: int
    __to_train_id: int
    __to_train_path_node_id: int

    def __init__(
        self,
        debug_string: str,
        from_node_id: int,
        from_train_id: int,
        from_train_path_node_id: int,
        to_node_id: int,
        to_train_id: int,
        to_train_path_node_id: int,
        id: int,
    ):
        _HasDebugString.__init__(self, debug_string)
        _HasID.__init__(self, id)
        self.__from_node_id = from_node_id
        self.__from_train_id = from_train_id
        self.__from_train_path_node_id = from_train_path_node_id
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
    def to_node_id(self) -> int:
        return self.__to_node_id

    @property
    def to_train_id(self) -> int:
        return self.__to_train_id

    @property
    def to_train_path_node_id(self) -> int:
        return self.__to_train_path_node_id


class AlgorithmConnectionLink(_AlgorithmLink, _HasID):
    __minimum_duration: datetime.timedelta
    __maximum_deviation: Optional[datetime.timedelta]
    __weight: Optional[int]

    def __init__(
        self,
        debug_string: str,
        from_node_id: int,
        from_train_id: int,
        from_train_path_node_id: int,
        to_node_id: int,
        to_train_id: int,
        to_train_path_node_id: int,
        minimum_duration: datetime.timedelta,
        maximum_deviation: Optional[datetime.timedelta],
        weight: Optional[int],
        id: int,
    ):
        _AlgorithmLink.__init__(self, debug_string, from_node_id, from_train_id, from_train_path_node_id, to_node_id, to_train_id, to_train_path_node_id, id)

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


class AlgorithmAwaitArrivalLink(_AlgorithmLink, _HasID):
    __minimum_duration: datetime.timedelta

    def __init__(
        self,
        debug_string: str,
        from_node_id: int,
        from_train_id: int,
        from_train_path_node_id: int,
        to_node_id: int,
        to_train_id: int,
        to_train_path_node_id: int,
        minimum_duration: datetime.timedelta,
        id: int,
    ):
        _AlgorithmLink.__init__(self, debug_string, from_node_id, from_train_id, from_train_path_node_id, to_node_id, to_train_id, to_train_path_node_id, id)
        self.__minimum_duration = minimum_duration

    @property
    def minimum_duration(self) -> datetime.timedelta:
        return self.__minimum_duration


class AlgorithmRosterLink(_AlgorithmLink, _HasID):
    __from_vehicle_position_in_formation: int
    __to_vehicle_position_in_formation: int

    def __init__(
        self,
        debug_string: str,
        from_node_id: int,
        from_train_id: int,
        from_train_path_node_id: int,
        to_node_id: int,
        to_train_id: int,
        to_train_path_node_id: int,
        to_vehicle_position_in_formation: int,
        from_vehicle_position_in_formation: int,
        id: int,
    ):
        _AlgorithmLink.__init__(self, debug_string, from_node_id, from_train_id, from_train_path_node_id, to_node_id, to_train_id, to_train_path_node_id, id)
        self.__to_vehicle_position_in_formation = to_vehicle_position_in_formation
        self.__from_vehicle_position_in_formation = from_vehicle_position_in_formation

    @property
    def to_vehicle_position_in_formation(self) -> int:
        return self.__to_vehicle_position_in_formation

    @property
    def from_vehicle_position_in_formation(self) -> int:
        return self.__from_vehicle_position_in_formation


class _AlgorithmLinkDefinition:
    def __init__(self, from_train_path_node_id: int, to_train_path_node_id: int):
        self.__from_train_path_node_id = from_train_path_node_id
        self.__to_train_path_node_id = to_train_path_node_id

    @property
    def from_train_path_node_id(self) -> int:
        return self.__from_train_path_node_id
        pass

    @property
    def to_train_path_node_id(self) -> int:
        return self.__to_train_path_node_id


class AlgorithmRosterLinkDefinition(_AlgorithmLinkDefinition):
    __from_vehicle_position_in_formation: int
    __to_vehicle_position_in_formation: int

    def __init__(
        self,
        from_train_path_node_id: int,
        to_train_path_node_id: int,
        from_vehicle_position_in_formation: int,
        to_vehicle_position_in_formation: int,
    ):
        super().__init__(from_train_path_node_id, to_train_path_node_id)
        self.__from_vehicle_position_in_formation = from_vehicle_position_in_formation
        self.__to_vehicle_position_in_formation = to_vehicle_position_in_formation

    @property
    def to_vehicle_position_in_formation(self) -> int:
        return self.__to_vehicle_position_in_formation

    @property
    def from_vehicle_position_in_formation(self) -> int:
        return self.__from_vehicle_position_in_formation
