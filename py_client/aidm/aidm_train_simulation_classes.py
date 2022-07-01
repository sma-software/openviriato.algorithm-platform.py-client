from enum import Enum, unique
from typing import List
import datetime

from py_client.aidm.aidm_base_classes import _HasID

@unique
class AlgorithmTrainSimulationEventType(Enum):
    arrival = 'arrival'#"The event describes the arrival at a node."
    departure = 'departure'#"The event describes a departure from a node."

class AlgorithmTrainSimulationTrainPathNode(_HasID):
    __arrival_time: datetime.datetime
    __departure_time: datetime.datetime
    __node_id: int

    def __init__(self, id: int, arrival_time, departure_time, node_id: int):
        _HasID.__init__(self, id)
        self.__arrival_time = arrival_time
        self.__departure_time = departure_time
        self.__node_id = node_id

    @property
    def arrival_time(self) -> datetime.datetime:
        return self.__arrival_time

    @property
    def departure_time(self) -> datetime.datetime:
        return self.__departure_time

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
