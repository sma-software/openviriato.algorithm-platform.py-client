import datetime

from py_client.aidm.aidm_base_classes import _HasDebugString
from py_client.aidm.aidm_base_classes import _HasID
from py_client.aidm.aidm_time_window_classes import TimeWindow
from typing import List


class AlgorithmSectionRunningTimePenaltyTrack:
    __from_node_id: int
    __from_node_time_window: TimeWindow
    __section_track_id: int
    __to_node_id: int
    __to_node_time_window: TimeWindow

    def __init__(self, from_node_id: int, from_node_time_window: TimeWindow, section_track_id: int, to_node_id: int, to_node_time_window: TimeWindow):
        self.__from_node_id = from_node_id
        self.__from_node_time_window = from_node_time_window
        self.__section_track_id = section_track_id
        self.__to_node_id = to_node_id
        self.__to_node_time_window = to_node_time_window

    @property
    def from_node_id(self) -> int:
        return self.__from_node_id

    @property
    def to_node_id(self) -> int:
        return self.__to_node_id

    @property
    def from_node_time_window(self) -> TimeWindow:
        return self.__from_node_time_window

    @property
    def to_node_time_window(self) -> TimeWindow:
        return self.__to_node_time_window

    @property
    def section_track_id(self) -> int:
        return self.__section_track_id


class AlgorithmSectionRunningTimePenalty(_HasID, _HasDebugString):
    __affected_section_tracks: List[AlgorithmSectionRunningTimePenaltyTrack]
    __total_penalty: datetime.timedelta

    def __init__(self, affected_section_tracks: List[AlgorithmSectionRunningTimePenaltyTrack], total_penalty: datetime.timedelta, debug_string: str, id: int):
        _HasDebugString.__init__(self, debug_string)
        _HasID.__init__(self, id)
        self.__affected_section_tracks = affected_section_tracks
        self.__total_penalty = total_penalty

    @property
    def affected_section_tracks(self) -> List[AlgorithmSectionRunningTimePenaltyTrack]:
        return self.__affected_section_tracks

    @property
    def total_penalty(self) -> datetime.timedelta:
        return self.__total_penalty


class RunningTimePenaltyOnTrainPath:
    __from_train_path_node_id: int
    __possession_id: int
    __required_running_time_penalty: datetime.timedelta
    __to_train_path_node_id: int

    def __init__(self, from_train_path_node_id: int, possession_id: int, required_running_time_penalty: datetime.timedelta, to_train_path_node_id: int):
        self.__from_train_path_node_id = from_train_path_node_id
        self.__possession_id = possession_id
        self.__required_running_time_penalty = required_running_time_penalty
        self.__to_train_path_node_id = to_train_path_node_id

    @property
    def from_train_path_node_id(self):
        return self.__from_train_path_node_id

    @property
    def possession_id(self):
        return self.__possession_id

    @property
    def required_running_time_penalty(self):
        return self.__required_running_time_penalty

    @property
    def to_train_path_node_id(self):
        return self.__to_train_path_node_id
