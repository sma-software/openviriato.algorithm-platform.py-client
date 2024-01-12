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


class AlgorithmTrainSimulationUnrealizableEvent:
    __additional_forecast_delay: timedelta
    __event: AlgorithmTrainSimulationEvent

    def __init__(self, additional_forecast_delay: timedelta, event: AlgorithmTrainSimulationEvent):
        self.__additional_forecast_delay = additional_forecast_delay
        self.__event = event

    @property
    def additional_forecast_delay(self) -> timedelta:
        return self.__additional_forecast_delay

    @property
    def event(self) -> AlgorithmTrainSimulationEvent:
        return self.__event


class AlgorithmTrainSimulationRealizationForecast:
    __next_realizable_event: AlgorithmTrainSimulationEvent
    __unrealizable_events: List[AlgorithmTrainSimulationUnrealizableEvent]

    def __init__(
        self,
        next_realizable_event: AlgorithmTrainSimulationEvent,
        unrealizable_events: List[AlgorithmTrainSimulationUnrealizableEvent],
    ):
        self.__next_realizable_event = next_realizable_event
        self.__unrealizable_events = unrealizable_events

    @property
    def next_realizable_event(self) -> AlgorithmTrainSimulationEvent:
        return self.__next_realizable_event

    @property
    def unrealizable_events(self) -> List[AlgorithmTrainSimulationUnrealizableEvent]:
        return self.__unrealizable_events


class AlgorithmTrainSimulationPerimeter:
    __node_ids: List[int]

    def __init__(self, node_ids: List[int]):
        self.__node_ids = node_ids

    @property
    def node_ids(self) -> List[int]:
        return self.__node_ids


class AlgorithmTrainSimulationCreationArguments:
    __ignore_timetable_conflicts: bool
    __perimeter: AlgorithmTrainSimulationPerimeter
    __time_window: TimeWindow

    def __init__(self, ignore_timetable_conflicts: bool, time_window: TimeWindow, perimeter: AlgorithmTrainSimulationPerimeter):
        self.__time_window = time_window
        self.__perimeter = perimeter
        self.__ignore_timetable_conflicts = ignore_timetable_conflicts

    @property
    def ignore_timetable_conflicts(self) -> bool:
        return self.__ignore_timetable_conflicts

    @property
    def perimeter(self) -> AlgorithmTrainSimulationPerimeter:
        return self.__perimeter

    @property
    def time_window(self) -> TimeWindow:
        return self.__time_window
