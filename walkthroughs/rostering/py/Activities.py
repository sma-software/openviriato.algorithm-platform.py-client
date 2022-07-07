from datetime import datetime
from typing import List


class SingleActivity:
    __id: int
    __position: int
    __from_node_id: int
    __arrival_tpn_id: int
    __to_node_id: int
    __departure_tpn_id: int
    __departure_time: datetime
    __arrival_time: datetime
    __rolling_stock_type_id: int

    def __init__(self, id: int, departure_tpn_id: int, departure_time: datetime, from_node_id: int, arrival_tpn_id: int, arrival_time: datetime, to_node_id: int, position: int, rolling_stock_type_id: int):
        self.__id = id
        self.__position = position
        self.__from_node_id = from_node_id
        self.__arrival_tpn_id = arrival_tpn_id
        self.__to_node_id = to_node_id
        self.__departure_tpn_id = departure_tpn_id
        self.__departure_time = departure_time
        self.__arrival_time = arrival_time
        self.__rolling_stock_type_id = rolling_stock_type_id

    @property
    def position(self) -> int:
        return self.__position

    @property
    def from_node_id(self) -> int:
        return self.__from_node_id

    @property
    def arrival_tpn_id(self) -> int:
        return self.__arrival_tpn_id

    @property
    def to_node_id(self) -> int:
        return self.__to_node_id

    @property
    def departure_tpn_id(self) -> int:
        return self.__departure_tpn_id

    @property
    def departure_time(self) -> datetime:
        return self.__departure_time

    @property
    def arrival_time(self) -> datetime:
        return self.__arrival_time

    @property
    def rolling_stock_type_id(self) -> int:
        return self.__rolling_stock_type_id


class CommonActivity:
    __single_activities: List[SingleActivity]

    def __init__(self, single_activities: List[SingleActivity]):
        self.__single_activities = single_activities

    @property
    def single_activities(self) -> List[SingleActivity]:
        return self.__single_activities
