from __future__ import annotations
from enum import Enum, unique
from typing import List, Optional
from datetime import datetime, timedelta

from py_client.aidm import TimeWindow
from py_client.aidm.aidm_base_classes import _HasID


@unique
class AlgorithmTrainSimulationEventType(Enum):
    arrival = "arrival"
    departure = "departure"
    passing = "passing"


class AlgorithmTrainSimulationEvent(_HasID):
    __algorithm_train_id: int
    __algorithm_train_path_node_id: int
    __algorithm_train_path_node_sequence_number: int
    __forecast_delay: timedelta
    __forecast_time: datetime
    __node_id: int
    __planned_time: datetime
    __type: AlgorithmTrainSimulationEventType
    __from_section_track_id: Optional[int]
    __node_track_id: Optional[int]
    __to_section_track_id: Optional[int]

    def __init__(
        self,
        id: int,
        algorithm_train_path_node_id: int,
        forecast_delay: timedelta,
        forecast_time: datetime,
        node_id: int,
        planned_time: datetime,
        type: AlgorithmTrainSimulationEventType,
        algorithm_train_path_node_sequence_number: int,
        algorithm_train_id: int,
        from_section_track_id: Optional[int] = None,
        node_track_id: Optional[int] = None,
        to_section_track_id: Optional[int] = None,
    ):
        _HasID.__init__(self, id)
        self.__algorithm_train_id = algorithm_train_id
        self.__algorithm_train_path_node_id = algorithm_train_path_node_id
        self.__algorithm_train_path_node_sequence_number = algorithm_train_path_node_sequence_number
        self.__forecast_delay = forecast_delay
        self.__forecast_time = forecast_time
        self.__node_id = node_id
        self.__planned_time = planned_time
        self.__type = type
        self.__from_section_track_id = from_section_track_id
        self.__node_track_id = node_track_id
        self.__to_section_track_id = to_section_track_id

    @property
    def algorithm_train_id(self) -> int:
        return self.__algorithm_train_id

    @property
    def algorithm_train_path_node_id(self) -> int:
        return self.__algorithm_train_path_node_id

    @property
    def forecast_delay(self) -> timedelta:
        return self.__forecast_delay

    @property
    def forecast_time(self) -> datetime:
        return self.__forecast_time

    @property
    def node_id(self) -> int:
        return self.__node_id

    @property
    def planned_time(self) -> datetime:
        return self.__planned_time

    @property
    def type(self) -> AlgorithmTrainSimulationEventType:
        return self.__type

    @property
    def from_section_track_id(self):
        return self.__from_section_track_id

    @property
    def node_track_id(self):
        return self.__node_track_id

    @property
    def to_section_track_id(self):
        return self.__to_section_track_id

    @property
    def algorithm_train_path_node_sequence_number(self):
        return self.__algorithm_train_path_node_sequence_number


class AlgorithmTrainSimulationTrain:
    __algorithm_train_id: int
    __next_event_id: Optional[int]
    __events: List[AlgorithmTrainSimulationEvent]

    def __init__(
        self,
        algorithm_train_id: int,
        events: List[AlgorithmTrainSimulationEvent],
        next_event_id: Optional[int],
    ):
        self.__algorithm_train_id = algorithm_train_id
        self.__events = events
        self.__next_event_id = next_event_id

    @property
    def algorithm_train_id(self):
        return self.__algorithm_train_id

    @property
    def events(self):
        return self.__events

    @property
    def next_event_id(self):
        return self.__next_event_id


class AlgorithmTrainSimulationRealizationForecast:
    __next_realizable_event: AlgorithmTrainSimulationEvent

    def __init__(self, next_realizable_event: AlgorithmTrainSimulationEvent):
        self.__next_realizable_event = next_realizable_event

    @property
    def next_realizable_event(self) -> AlgorithmTrainSimulationEvent:
        return self.__next_realizable_event


class _AlgorithmDispatcherDelayReason:
    def __init__(self):
        # Base class for dispatcher delay reasons; defined for polymorphic conversion.
        pass


class AlgorithmDispatcherConnectionDelayReason(_AlgorithmDispatcherDelayReason):
    __causing_train_path_node_id: Optional[int]

    def __init__(self, causing_train_path_node_id: Optional[int]):
        super().__init__()
        self.__causing_train_path_node_id = causing_train_path_node_id

    @property
    def causing_train_path_node_id(self) -> Optional[int]:
        return self.__causing_train_path_node_id


class AlgorithmDispatcherOtherDelayReason(_AlgorithmDispatcherDelayReason):
    __causing_train_path_node_id: Optional[int]
    __reason: str

    def __init__(self, causing_train_path_node_id: Optional[int], reason: str):
        super().__init__()
        self.__causing_train_path_node_id = causing_train_path_node_id
        self.__reason = reason

    @property
    def causing_train_path_node_id(self) -> Optional[int]:
        return self.__causing_train_path_node_id

    @property
    def reason(self) -> str:
        return self.__reason


class AlgorithmTrainSimulationCreationArguments:
    __ignore_timetable_conflicts: bool
    __perimeter_restricted_to_node_ids: List[int]
    __time_window: TimeWindow
    __algorithm_train_ids: List[int]
    __deactivate_deadlock_prevention: bool

    def __init__(
        self,
        time_window: TimeWindow,
        ignore_timetable_conflicts: bool = None,
        perimeter_restricted_to_node_ids: List[int] = None,
        algorithm_train_ids: List[int] = None,
        deactivate_deadlock_prevention: bool = None,
    ):
        self.__time_window = time_window
        self.__perimeter_restricted_to_node_ids = perimeter_restricted_to_node_ids
        self.__ignore_timetable_conflicts = ignore_timetable_conflicts
        self.__algorithm_train_ids = algorithm_train_ids
        self.__deactivate_deadlock_prevention = deactivate_deadlock_prevention

    def with_ignore_timetable_conflicts(self, ignore_timetable_conflicts: bool) -> AlgorithmTrainSimulationCreationArguments:
        self.__ignore_timetable_conflicts = ignore_timetable_conflicts
        return self

    def with_perimeter_restricted_to_node_ids(self, perimeter_restricted_to_node_ids: List[int]) -> AlgorithmTrainSimulationCreationArguments:
        self.__perimeter_restricted_to_node_ids = perimeter_restricted_to_node_ids
        return self

    def with_algorithm_train_ids(self, algorithm_train_ids: List[int]) -> AlgorithmTrainSimulationCreationArguments:
        self.__algorithm_train_ids = algorithm_train_ids
        return self

    def with_deactivate_deadlock_prevention(self, deactivate_deadlock_prevention: bool) -> AlgorithmTrainSimulationCreationArguments:
        self.__deactivate_deadlock_prevention = deactivate_deadlock_prevention
        return self

    @property
    def ignore_timetable_conflicts(self) -> bool:
        return self.__ignore_timetable_conflicts

    @property
    def perimeter_restricted_to_node_ids(self) -> List[int]:
        return self.__perimeter_restricted_to_node_ids

    @property
    def time_window(self) -> TimeWindow:
        return self.__time_window

    @property
    def algorithm_train_ids(self) -> List[int]:
        return self.__algorithm_train_ids

    @property
    def deactivate_deadlock_prevention(self) -> bool:
        return self.__deactivate_deadlock_prevention
