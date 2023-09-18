from __future__ import annotations
from typing import List, Optional, Union
from enum import unique, Enum

from py_client.aidm import AlgorithmTrainPathNodeReference
from py_client.aidm.aidm_time_window_classes import TimeWindow


@unique
class ConflictType(Enum):
    Crossing = "crossing"
    InvalidDrivingDirection = "invalidDrivingDirection"
    DrivingDirectionChange = "drivingDirectionChange"
    SimultaneousArrivalSeparationTime = "simultaneousArrivalSeparationTime"
    SameStationTrackSeparationTime = "sameStationTrackSeparationTime"
    SameSectionTrackSeparationTime = "sameSectionTrackSeparationTime"
    IncompatibleStationRoutes = "incompatibleStationRoutes"
    IncompatibleJunctionRoutes = "incompatibleJunctionRoutes"
    HeadwayTime = "headwayTime"
    Overtaking = "overtaking"
    CongestedNode = "congestedNode"
    ImpossibleStationEntryRoute = "impossibleStationEntryRoute"
    ImpossibleStationExitRoute = "impossibleStationExitRoute"
    ImpossibleJunctionRoute = "impossibleJunctionRoute"
    StopInJunction = "stopInJunction"
    NoStationTrackAssigned = "noStationTrackAssigned"
    StationTrackLength = "stationTrackLength"
    PlatformLength = "platformLength"
    LevelTrackCrossingTime = "levelTrackCrossingTime"
    ForbiddenStationTrack = "forbiddenStationTrack"


@unique
class AlgorithmConflictDetectionEventType(Enum):
    PreviousDeparture = "previousDeparture"
    Arrival = "arrival"
    Departure = "departure"


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
    # **kwargs is needed because operator ** cannot deal with double interheritance otherwise (as needed by json2Aidm conversion)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class _AlgorithmTrainConflict(_AlgorithmConflict):
    # **kwargs is needed because operator ** cannot deal with double interheritance otherwise (as needed by json2Aidm conversion)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AlgorithmSectionTrackConflict(_AlgorithmInfrastructureConflict):
    __section_track_id: int

    # **kwargs is needed because operator ** cannot deal with double interheritance otherwise (as needed by json2Aidm conversion)
    def __init__(self, section_track_id: int, **kwargs):
        super().__init__(**kwargs)
        self.__section_track_id = section_track_id

    @property
    def section_track_id(self) -> int:
        return self.__section_track_id


class AlgorithmNodeConflict(_AlgorithmInfrastructureConflict):
    __node_id: int

    # **kwargs is needed because operator ** cannot deal with double interheritance otherwise (as needed by json2Aidm conversion)
    def __init__(self, node_id: int, **kwargs):
        super().__init__(**kwargs)
        self.__node_id = node_id

    @property
    def node_id(self) -> int:
        return self.__node_id


class AlgorithmTwoTrainsConflict(_AlgorithmTrainConflict):
    __causing_train_path_node: AlgorithmTrainPathNodeReference
    __causing_event_type: AlgorithmConflictDetectionEventType
    __affected_train_path_node: AlgorithmTrainPathNodeReference
    __affected_event_type: AlgorithmConflictDetectionEventType

    # **kwargs is needed because operator ** cannot deal with double interheritance otherwise (as needed by json2Aidm conversion)
    def __init__(
        self,
        causing_train_path_node: AlgorithmTrainPathNodeReference,
        causing_event_type: AlgorithmConflictDetectionEventType,
        affected_train_path_node: AlgorithmTrainPathNodeReference,
        affected_event_type: AlgorithmConflictDetectionEventType,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.__causing_train_path_node = causing_train_path_node
        self.__causing_event_type = causing_event_type
        self.__affected_train_path_node = affected_train_path_node
        self.__affected_event_type = affected_event_type

    @property
    def causing_train_path_node(self):
        return self.__causing_train_path_node

    @property
    def causing_event_type(self):
        return self.__causing_event_type

    @property
    def affected_train_path_node(self):
        return self.__affected_train_path_node

    @property
    def affected_event_type(self):
        return self.__affected_event_type


class AlgorithmOneTrainConflict(_AlgorithmTrainConflict):
    __affected_train_path_node: AlgorithmTrainPathNodeReference

    # **kwargs is needed because operator ** cannot deal with double interheritance otherwise (as needed by json2Aidm conversion)
    def __init__(self, affected_train_path_node: AlgorithmTrainPathNodeReference, **kwargs):
        super().__init__(**kwargs)
        self.__affected_train_path_node = affected_train_path_node

    @property
    def affected_train_path_node(self):
        return self.__affected_train_path_node


class AlgorithmMultipleTrainsConflict(_AlgorithmTrainConflict):
    __involved_train_path_node_references: List[AlgorithmTrainPathNodeReference]

    # **kwargs is needed because operator ** cannot deal with double interheritance otherwise (as needed by json2Aidm conversion)
    def __init__(self, involved_train_path_node_references: List[AlgorithmTrainPathNodeReference], **kwargs):
        super().__init__(**kwargs)
        self.__involved_train_path_node_references = involved_train_path_node_references

    @property
    def involved_train_path_node_references(self) -> List[AlgorithmTrainPathNodeReference]:
        return self.__involved_train_path_node_references


class _AlgorithmTwoTrainsSectionTrackConflict(AlgorithmTwoTrainsConflict, AlgorithmSectionTrackConflict):
    def __init__(
        self,
        conflict_type: ConflictType,
        time_window: TimeWindow,
        section_track_id: int,
        causing_train_path_node: AlgorithmTrainPathNodeReference,
        causing_event_type: AlgorithmConflictDetectionEventType,
        affected_train_path_node: AlgorithmTrainPathNodeReference,
        affected_event_type: AlgorithmConflictDetectionEventType,
    ):
        super().__init__(
            conflict_type=conflict_type,
            time_window=time_window,
            section_track_id=section_track_id,
            causing_train_path_node=causing_train_path_node,
            causing_event_type=causing_event_type,
            affected_train_path_node=affected_train_path_node,
            affected_event_type=affected_event_type,
        )


class _AlgorithmOneTrainSectionTrackConflict(AlgorithmOneTrainConflict, AlgorithmSectionTrackConflict):
    def __init__(self, conflict_type: ConflictType, time_window: TimeWindow, section_track_id: int, affected_train_path_node: AlgorithmTrainPathNodeReference):
        super().__init__(
            conflict_type=conflict_type, time_window=time_window, section_track_id=section_track_id, affected_train_path_node=affected_train_path_node
        )


class _AlgorithmOneTrainNodeConflict(AlgorithmOneTrainConflict, AlgorithmNodeConflict):
    def __init__(self, conflict_type: ConflictType, time_window: TimeWindow, node_id: int, affected_train_path_node: AlgorithmTrainPathNodeReference):
        super().__init__(conflict_type=conflict_type, time_window=time_window, affected_train_path_node=affected_train_path_node, node_id=node_id)


class _AlgorithmTwoTrainsNodeConflict(AlgorithmTwoTrainsConflict, AlgorithmNodeConflict):
    def __init__(
        self,
        conflict_type: ConflictType,
        time_window: TimeWindow,
        node_id: int,
        causing_train_path_node: AlgorithmTrainPathNodeReference,
        causing_event_type: AlgorithmConflictDetectionEventType,
        affected_train_path_node: AlgorithmTrainPathNodeReference,
        affected_event_type: AlgorithmConflictDetectionEventType,
    ):
        super().__init__(
            conflict_type=conflict_type,
            time_window=time_window,
            causing_train_path_node=causing_train_path_node,
            causing_event_type=causing_event_type,
            affected_train_path_node=affected_train_path_node,
            affected_event_type=affected_event_type,
            node_id=node_id,
        )


class _AlgorithmMultipleTrainsNodeConflict(AlgorithmMultipleTrainsConflict, AlgorithmNodeConflict):
    def __init__(
        self, conflict_type: ConflictType, time_window: TimeWindow, involved_train_path_node_references: List[AlgorithmTrainPathNodeReference], node_id: int
    ):
        super().__init__(
            conflict_type=conflict_type, time_window=time_window, involved_train_path_node_references=involved_train_path_node_references, node_id=node_id
        )


AlgorithmConflict = Union[
    AlgorithmTwoTrainsConflict, AlgorithmOneTrainConflict, AlgorithmMultipleTrainsConflict, AlgorithmSectionTrackConflict, AlgorithmNodeConflict
]


class ConflictDetectionArguments:
    __filter_conflict_types: List[ConflictType]
    __filter_node_ids: List[int]
    __filter_section_track_ids: List[int]
    __filter_train_id: Optional[int]
    __time_window: TimeWindow
    __train_ids: List[int]

    def __init__(self, train_ids: List[int]):
        self.__train_ids = train_ids
        self.__filter_conflict_types = None
        self.__filter_node_ids = None
        self.__filter_section_track_ids = None
        self.__filter_train_id = None
        self.__time_window = None

    def _private_init__(
        self,
        filter_conflict_types: List[ConflictType],
        filter_node_ids: List[int],
        filter_section_track_ids: List[int],
        filter_train_id: Optional[int],
        time_window: TimeWindow,
    ) -> None:
        self.__filter_conflict_types = filter_conflict_types
        self.__filter_node_ids = filter_node_ids
        self.__filter_section_track_ids = filter_section_track_ids
        self.__filter_train_id = filter_train_id
        self.__time_window = time_window

    def with_type_filter(self, filter_conflict_types: List[ConflictType]) -> ConflictDetectionArguments:
        result = ConflictDetectionArguments(self.__train_ids)
        result._private_init__(filter_conflict_types, self.__filter_node_ids, self.__filter_section_track_ids, self.__filter_train_id, self.__time_window)
        return result

    def with_location_filter(self, filter_node_ids: List[int], filter_section_track_ids: List[int]) -> ConflictDetectionArguments:
        result = ConflictDetectionArguments(self.__train_ids)
        result._private_init__(self.__filter_conflict_types, filter_node_ids, filter_section_track_ids, self.__filter_train_id, self.__time_window)
        return result

    def with_train_filter(self, filter_train_id: Optional[int]) -> ConflictDetectionArguments:
        result = ConflictDetectionArguments(self.__train_ids)
        result._private_init__(self.__filter_conflict_types, self.__filter_node_ids, self.__filter_section_track_ids, filter_train_id, self.__time_window)
        return result

    def with_time_filter(self, time_window: TimeWindow) -> ConflictDetectionArguments:
        result = ConflictDetectionArguments(self.__train_ids)
        result._private_init__(self.__filter_conflict_types, self.__filter_node_ids, self.__filter_section_track_ids, self.__filter_train_id, time_window)
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
