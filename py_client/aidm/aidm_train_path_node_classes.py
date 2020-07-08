import datetime
from typing import Optional
from py_client.aidm.aidm_base_classes import _HasID
from py_client.aidm.aidm_enum_classes import StopStatus


class AlgorithmTrainPathNode(_HasID):
    __arrival_time: datetime.datetime
    __departure_time: datetime.datetime
    __section_track_id: Optional[int]
    __node_id: int
    __node_track_id: Optional[int]
    __formation_id: Optional[int]
    __minimum_run_time: Optional[datetime.timedelta]
    __minimum_stop_time: datetime.timedelta
    __stop_status: StopStatus
    __sequence_number: int

    def __init__(
            self,
            id: int,
            arrival_time: datetime.datetime,
            departure_time: datetime.datetime,
            section_track_id: Optional[int],
            node_id: int,
            node_track_id: Optional[int],
            formation_id: Optional[int],
            minimum_run_time: Optional[datetime.timedelta],
            minimum_stop_time: datetime.timedelta,
            stop_status: StopStatus,
            sequence_number: int
    ):
        _HasID.__init__(self, id)
        self.__arrival_time = arrival_time
        self.__departure_time = departure_time
        self.__section_track_id = section_track_id
        self.__node_id = node_id
        self.__node_track_id = node_track_id
        self.__formation_id = formation_id
        self.__minimum_run_time = minimum_run_time
        self.__minimum_stop_time = minimum_stop_time
        self.__stop_status = stop_status
        self.__sequence_number = sequence_number

    @property
    def section_track_id(self) -> Optional[int]:
        return self.__section_track_id

    @property
    def node_id(self) -> int:
        return self.__node_id

    @property
    def node_track_id(self) -> Optional[int]:
        return self.__node_track_id

    @property
    def formation_id(self) -> Optional[int]:
        return self.__formation_id

    @property
    def arrival_time(self) -> datetime.datetime:
        return self.__arrival_time

    @property
    def departure_time(self) -> datetime.datetime:
        return self.__departure_time

    @property
    def minimum_run_time(self) -> Optional[datetime.timedelta]:
        return self.__minimum_run_time

    @property
    def minimum_stop_time(self) -> datetime.timedelta:
        return self.__minimum_stop_time

    @property
    def stop_status(self) -> StopStatus:
        return self.__stop_status

    @property
    def sequence_number(self) -> int:
        return self.__sequence_number
