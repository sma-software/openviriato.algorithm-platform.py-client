from typing import List
from enum import unique, Enum
from py_client.aidm.aidm_time_window_classes import TimeWindow

@unique
class ConflictType(Enum):
    Crossing = "crossing"


class AlgorithmConflict:
    __conflict_type: ConflictType
    __involved_train_ids: List[int]
    __time_window: TimeWindow
    __section_track_id: int

    def __init__(self, conflict_type: ConflictType, involved_train_ids: List[int], time_window: TimeWindow, section_track_id: int):
        self.__conflict_type = conflict_type
        self.__involved_train_ids = involved_train_ids
        self.__time_window = time_window
        self.__section_track_id = section_track_id

    @property
    def conflict_type(self) -> ConflictType:
        return self.__conflict_type

    @property
    def involved_train_ids(self) -> List[int]:
        return self.__involved_train_ids

    @property
    def time_window(self) -> TimeWindow:
        return self.__time_window

    @property
    def section_track_id(self) -> int:
        return self.__section_track_id
