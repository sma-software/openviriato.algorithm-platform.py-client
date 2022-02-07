from __future__ import annotations
from typing import List, Optional
from enum import unique, Enum
from py_client.aidm.aidm_time_window_classes import TimeWindow

@unique
class ConflictType(Enum):
    Crossing = "crossing"
    Trafficability = "trafficability"


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

class ConflictDetectionArguments:
    __filter_conflict_types: List[ConflictType]
    __filter_node_ids: List[int]
    __filter_section_track_ids: List[int]
    __filter_train_id: Optional[int]
    __time_window: TimeWindow
    __train_ids: List[int]

    def __init__(self, train_ids: List[int]):
        self.__train_ids = train_ids
        self.__filter_conflict_types = []
        self.__filter_node_ids = []
        self.__filter_section_track_ids = []
        self.__filter_train_id = None
        self.__time_window = None

    def _private_init__(
            self,
            filter_conflict_types: List[ConflictType],
            filter_node_ids: List[int] ,
            filter_section_track_ids: List[int],
            filter_train_id: Optional[int],
            time_window: TimeWindow) -> None:
        self.__filter_conflict_types = filter_conflict_types
        self.__filter_node_ids = filter_node_ids
        self.__filter_section_track_ids = filter_section_track_ids
        self.__filter_train_id = filter_train_id
        self.__time_window = time_window

    def with_type_filter(self, filter_conflict_types: List[ConflictType]) -> ConflictDetectionArguments:
        result = ConflictDetectionArguments(self.__train_ids)
        result._private_init__(
            filter_conflict_types,
            self.__filter_node_ids,
            self.__filter_section_track_ids,
            self.__filter_train_id,
            self.__time_window)
        return result

    def with_location_filter(self, filter_node_ids: List[int], filter_section_track_ids: List[int]) -> ConflictDetectionArguments:
        result = ConflictDetectionArguments(self.__train_ids)
        result._private_init__(
            self.__filter_conflict_types,
            filter_node_ids,
            filter_section_track_ids,
            self.__filter_train_id,
            self.__time_window)
        return result

    def with_train_filter(self, filter_train_id: Optional[int]) -> ConflictDetectionArguments:
        result = ConflictDetectionArguments(self.__train_ids)
        result._private_init__(
            self.__filter_conflict_types,
            self.__filter_node_ids,
            self.__filter_section_track_ids,
            filter_train_id,
            self.__time_window)
        return result

    def with_time_filter(self, time_window: TimeWindow) -> ConflictDetectionArguments:
        result = ConflictDetectionArguments(self.__train_ids)
        result._private_init__(
            self.__filter_conflict_types,
            self.__filter_node_ids,
            self.__filter_section_track_ids,
            self.__filter_train_id,
            time_window)
        return result

    @property
    def filter_conflict_types(self) -> List[ConflictType]:
        return self.__filter_conflict_types

    @property
    def filter_node_ids(self) -> List[int]:
        return self.__filter_node_ids

    @property
    def filter_section_track_ids(self) -> List[int]:
        return self.__filter_section_track_ids

    @property
    def filter_train_id(self) -> Optional[int]:
        return self.__filter_train_id

    @property
    def time_window(self) -> TimeWindow:
        return self.__time_window

    @property
    def train_ids(self) -> List[int]:
        return self.__train_ids