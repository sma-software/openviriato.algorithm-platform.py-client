from enum import Enum, unique
from typing import List
from datetime import datetime, timedelta

from py_client.aidm.aidm_base_classes import _HasID


@unique
class AlgorithmTrainSimulationEventType(Enum):
    arrival = "arrival"
    departure = "departure"
    passing = "passing"


class AlgorithmTrainSimulationEvent(_HasID):
    __algorithm_train_id: int
    __algorithm_train_path_node_id: int
    __forecast_delay: timedelta
    __forecast_time: datetime
    __node_id: int
    __planned_time: datetime
    __type: AlgorithmTrainSimulationEventType

    def __init__(
        self,
        id: int,
        algorithm_train_id: int,
        algorithm_train_path_node_id: int,
        forecast_delay: timedelta,
        forecast_time: datetime,
        node_id: int,
        planned_time: datetime,
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
