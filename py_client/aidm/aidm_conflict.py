from __future__ import annotations
from typing import List, Optional
from enum import unique, Enum
from py_client.aidm.aidm_time_window_classes import TimeWindow
from py_client.aidm.aidm_train_path_node_classes import AlgorithmTrainPathNode
from py_client.aidm.aidm_algorithm_classes import AlgorithmTrain

@unique
class ConflictType(Enum):
    Crossing = "crossing"
    WrongDrivingDirection = "wrongDrivingDirection"
    ChangeDirection = "changeDirection"


class _AlgorithmConflict:
    __conflict_type: ConflictType
    __time_window: TimeWindow

    def __init__(self, conflict_type: ConflictType, time_window: TimeWindow):
        self.__conflict_type = conflict_type
        self.__time_window = time_window

    @property
    def conflict_type(self) -> ConflictType:
        return self.__conflict_type

    @property
    def time_window(self) -> TimeWindow:
        return self.__time_window

class _AlgorithmInfrastructureConflict(_AlgorithmConflict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class _AlgorithmTrainConflict(_AlgorithmConflict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class _AlgorithmSectionTrackConflict(_AlgorithmInfrastructureConflict):
    __section_track_id: int

    def __init__(self, section_track_id: int, **kwargs):
        super().__init__(**kwargs)
        self.__section_track_id = section_track_id

    @property
    def section_track_id(self) -> int:
        return self.__section_track_id

class _AlgorithmNodeConflict(_AlgorithmInfrastructureConflict):
    __node_id: int

    def __init__(self, node_id: int, **kwargs):
        super().__init__(**kwargs)
        self.__node_id = node_id

    @property
    def node_id(self) -> int:
        return self.__node_id

class _AlgorithmTwoTrainConflict(_AlgorithmTrainConflict):
    __preceding_train_id: int
    __preceding_train_path_node_id: int
    __succeeding_train_id: int
    __succeeding_train_path_node_id: int

    # **kwargs is needed because operator ** cannot deal with double interheritance otherwise (as needed by json2Aidm conversion)
    def __init__(self, preceding_train_id: int, preceding_train_path_node_id: int, succeeding_train_id: int, succeding_train_path_node_id: int, **kwargs):
        super().__init__(**kwargs)
        self.__succeeding_train_id = succeeding_train_id
        self.__succeeding_train_path_node_id = succeding_train_path_node_id
        self.__preceding_train_id = preceding_train_id
        self.__preceding_train_path_node_id = preceding_train_path_node_id

    @property
    def succeeding_train_id(self) -> int:
        return self.__succeeding_train_id

    @property
    def succeeding_train_path_node_id(self) -> int:
        return self.__succeeding_train_path_node_id

    @property
    def preceding_train_id(self) -> int:
        return self.__preceding_train_id

    @property
    def preceding_train_path_node_id(self) -> int:
        return self.__preceding_train_path_node_id

class _AlgorithmOneTrainConflict(_AlgorithmTrainConflict):
    __train_id: int
    __train_path_node_id: int

    def __init__(self, train_id: int, train_path_node_id: int, **kwargs):
        super().__init__(**kwargs)
        self.__train_id = train_id
        self.__train_path_node_id = train_path_node_id

    @property
    def train_id(self) -> int:
        return self.__train_id

    @property
    def train_path_node_id(self) -> int:
        return self.__train_path_node_id

class _AlgorithmMultipleTrainsConflict(_AlgorithmTrainConflict):
    __train_ids: List[int]
    __train_path_node_ids: List[int]

    def __init__(self, train_ids: List[int], train_path_node_ids: List[int], **kwargs):
        super().__init__(**kwargs)
        self.__train_ids = train_ids
        self.__train_path_node_ids = train_path_node_ids

    @property
    def train_ids(self) -> List[int]:
        return self.__train_ids

    @property
    def train_path_node_ids(self) -> List[int]:
        return self.__train_path_node_ids

class AlgorithmTwoTrainSectionTrackConflict(_AlgorithmTwoTrainConflict, _AlgorithmSectionTrackConflict):
    def __init__(self,
                 conflict_type: ConflictType,
                 time_window: TimeWindow,
                 section_track_id: int,
                 preceding_train_id: int,
                 preceding_train_path_node_id: int,
                 succeeding_train_id: int,
                 succeeding_train_path_node_id: int):
        super().__init__(
            conflict_type=conflict_type,
            time_window=time_window,
            preceding_train_id=preceding_train_id,
            preceding_train_path_node_id=preceding_train_path_node_id,
            succeeding_train_id=succeeding_train_id,
            succeding_train_path_node_id=succeeding_train_path_node_id,
            section_track_id=section_track_id)

class AlgorithmOneTrainSectionTrackConflict(_AlgorithmOneTrainConflict, _AlgorithmSectionTrackConflict):
    def __init__(self,
                 conflict_type: ConflictType,
                 time_window: TimeWindow,
                 section_track_id: int,
                 train_id: int,
                 train_path_node_id: int
                 ):
        super().__init__(
            conflict_type=conflict_type,
            time_window=time_window,
            train_id=train_id,
            train_path_node_id=train_path_node_id,
            section_track_id=section_track_id)

class AlgorithmOneTrainNodeConflict(_AlgorithmOneTrainConflict, _AlgorithmNodeConflict):
    def __init__(self,
                 conflict_type: ConflictType,
                 time_window: TimeWindow,
                 node_id: int,
                 train_id: int,
                 train_path_node_id: int
                 ):
        super().__init__(
            conflict_type=conflict_type,
            time_window=time_window,
            train_id=train_id,
            train_path_node_id=train_path_node_id,
            node_id=node_id)


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