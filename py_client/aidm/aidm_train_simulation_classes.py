from enum import Enum, unique
from typing import List, Optional
import datetime

from py_client.aidm import StopStatus
from py_client.aidm.aidm_base_classes import _HasID, _HasDebugString


@unique
class AlgorithmTrainSimulationEventType(Enum):
    arrival = "arrival"
    departure = "departure"
    passing = "passing"


class AlgorithmTrainSimulationEvent(_HasID):
    __algorithm_train_id: int
    __algorithm_train_path_node_id: int
    __forecast_delay: datetime.timedelta
    __forecast_time: datetime.datetime
    __node_id: int
    __planned_time: datetime.datetime
    __type: AlgorithmTrainSimulationEventType

    def __init__(
        self,
        id: int,
        algorithm_train_id: int,
        algorithm_train_path_node_id: int,
        forecast_delay: datetime.timedelta,
        forecast_time: datetime.datetime,
        node_id: int,
        planned_time: datetime.datetime,
        type: AlgorithmTrainSimulationEventType,
    ):
        _HasID.__init__(self, id)
        self.__algorithm_train_id = algorithm_train_id
        self.__algorithm_train_path_node_id = algorithm_train_path_node_id
        self.__forecast_delay = forecast_delay
        self.__forecast_time = forecast_time
        self.__node_id = node_id
        self.__planned_time = planned_time
        self.__type = type

    @property
    def algorithm_train_id(self) -> int:
        return self.__algorithm_train_id

    @property
    def algorithm_train_path_node_id(self) -> int:
        return self.__algorithm_train_path_node_id

    @property
    def forecast_delay(self) -> datetime.timedelta:
        return self.__forecast_delay

    @property
    def forecast_time(self) -> datetime.datetime:
        return self.__forecast_time

    @property
    def node_id(self) -> int:
        return self.__node_id

    @property
    def planned_time(self) -> datetime.datetime:
        return self.__planned_time

    @property
    def type(self) -> AlgorithmTrainSimulationEventType:
        return self.__type


class AlgorithmTrainSimulationUnrealizableEvent:
    __estimated_delay: datetime.timedelta
    __event: AlgorithmTrainSimulationEvent

    def __init__(self, estimated_delay: datetime.timedelta, event: AlgorithmTrainSimulationEvent):
        self.__estimated_delay = estimated_delay
        self.__event = event

    @property
    def estimated_delay(self) -> datetime.timedelta:
        return self.__estimated_delay

    @property
    def event(self) -> datetime.timedelta:
        return self.__event


class AlgorithmTrainSimulationRealizationForecast:
    __next_event: AlgorithmTrainSimulationEvent
    __unrealizable_events: List[AlgorithmTrainSimulationUnrealizableEvent]

    def __init__(self, next_event: AlgorithmTrainSimulationEvent, unrealizable_events: List[AlgorithmTrainSimulationUnrealizableEvent]):
        self.__unrealizable_events = unrealizable_events
        self.__next_event = next_event

    @property
    def next_event(self) -> AlgorithmTrainSimulationEvent:
        return self.__next_event

    @property
    def unrealizable_events(self) -> List[AlgorithmTrainSimulationUnrealizableEvent]:
        return self.__unrealizable_events
