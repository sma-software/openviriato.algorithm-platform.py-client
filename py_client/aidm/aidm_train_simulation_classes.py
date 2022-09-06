from enum import Enum, unique
from typing import List, Optional
import datetime

from py_client.aidm import StopStatus
from py_client.aidm.aidm_base_classes import _HasID


@unique
class AlgorithmTrainSimulationEventType(Enum):
    arrival = 'arrival'
    departure = 'departure'


class AlgorithmTrainSimulationTrainPathNode(_HasID):
    __arrival_delay: datetime.timedelta
    __departure_delay: datetime.timedelta
    __estimated_arrival_time: datetime.datetime
    __estimated_departure_time: datetime.datetime
    __estimated_stop_status: StopStatus
    __minimum_run_time: Optional[datetime.timedelta]
    __minimum_stop_time: datetime.timedelta
    __planned_arrival_time: datetime.datetime
    __planned_departure_time: datetime.datetime
    __planned_stop_status: StopStatus
    __node_id: int

    def __init__(self, id: int, arrival_delay: datetime.timedelta, departure_delay: datetime.timedelta,
                 estimated_arrival_time: datetime.datetime, estimated_departure_time: datetime.datetime,
                 estimated_stop_status: StopStatus, minimum_run_time: datetime.timedelta,
                 minimum_stop_time: datetime.timedelta, planned_arrival_time: datetime.datetime,
                 planned_departure_time: datetime.datetime, planned_stop_status: StopStatus, node_id: int):
        _HasID.__init__(self, id)
        self.__arrival_delay = arrival_delay
        self.__departure_delay = departure_delay
        self.__estimated_arrival_time = estimated_arrival_time
        self.__estimated_departure_time = estimated_departure_time
        self.__estimated_stop_status = estimated_stop_status
        self.__minimum_run_time = minimum_run_time
        self.__minimum_stop_time = minimum_stop_time
        self.__planned_arrival_time = planned_arrival_time
        self.__planned_departure_time = planned_departure_time
        self.__planned_stop_status = planned_stop_status
        self.__node_id = node_id

    @property
    def arrival_delay(self) -> datetime.timedelta:
        return self.__arrival_delay

    @property
    def departure_delay(self) -> datetime.timedelta:
        return self.__departure_delay

    @property
    def estimated_arrival_time(self) -> datetime.datetime:
        return self.__estimated_arrival_time

    @property
    def estimated_departure_time(self) -> datetime.datetime:
        return self.__estimated_departure_time

    @property
    def estimated_stop_status(self) -> StopStatus:
        return self.__estimated_stop_status

    @property
    def minimum_run_time(self) -> Optional[datetime.timedelta]:
        return self.__minimum_run_time

    @property
    def minimum_stop_time(self) -> datetime.timedelta:
        return self.__minimum_stop_time

    @property
    def planned_arrival_time(self) -> datetime.datetime:
        return self.__planned_arrival_time

    @property
    def planned_departure_time(self) -> datetime.datetime:
        return self.__planned_departure_time

    @property
    def planned_stop_status(self) -> StopStatus:
        return self.__planned_stop_status

    @property
    def node_id(self) -> int:
        return self.__node_id


class AlgorithmTrainSimulationEvent(_HasID):
    __absolute_time: datetime.datetime
    __train_simulation_train_path_node_id: int
    __type: AlgorithmTrainSimulationEventType

    def __init__(self, id: int, absolute_time: datetime.datetime, train_simulation_train_path_node_id: int, type: AlgorithmTrainSimulationEventType):
        _HasID.__init__(self, id)
        self.__absolute_time = absolute_time
        self.__train_simulation_train_path_node_id = train_simulation_train_path_node_id
        self.__type = type

    @property
    def absolute_time(self) -> datetime.datetime:
        return self.__absolute_time

    @property
    def train_simulation_train_path_node_id(self) -> int:
        return self.__train_simulation_train_path_node_id

    @property
    def type(self) -> AlgorithmTrainSimulationEventType:
        return self.__type


class AlgorithmTrainSimulationTrain(_HasID):
    __train_path_nodes: List[AlgorithmTrainSimulationTrainPathNode]

    def __init__(self, train_path_nodes: List[AlgorithmTrainSimulationTrainPathNode], id: int):
        _HasID.__init__(self, id)
        self.__train_path_nodes = train_path_nodes

    @property
    def train_path_nodes(self) -> List[AlgorithmTrainSimulationTrainPathNode]:
        return self.__train_path_nodes


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
    