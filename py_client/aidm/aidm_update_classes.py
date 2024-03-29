from datetime import datetime, timedelta
from typing import List, Optional

from py_client.aidm import StopStatus
from py_client.aidm.aidm_base_classes import _UpdateTrain
from py_client.aidm.aidm_routing_edge_classes import _RoutingEdge


class UpdateTrainRoute:
    __start_train_path_node_id: int
    __end_train_path_node_id: int
    __routing_edges: List[_RoutingEdge]

    def __init__(
        self,
        start_train_path_node_id: int,
        end_train_path_node_id: int,
        routing_edges: List[_RoutingEdge],
    ):
        self.__start_train_path_node_id = start_train_path_node_id
        self.__end_train_path_node_id = end_train_path_node_id
        self.__routing_edges = routing_edges

    @property
    def start_train_path_node_id(self) -> int:
        return self.__start_train_path_node_id

    @property
    def end_train_path_node_id(self) -> int:
        return self.__end_train_path_node_id

    @property
    def routing_edges(self) -> List[_RoutingEdge]:
        return self.__routing_edges


class UpdateTimesTrainPathNode:
    __train_path_node_id: int
    __arrival_time: datetime
    __departure_time: datetime
    __minimum_run_time: Optional[timedelta] = None
    __minimum_stop_time: Optional[timedelta] = None
    __stop_status: Optional[StopStatus] = None

    def __init__(
        self,
        train_path_node_id: int,
        arrival_time: datetime,
        departure_time: datetime,
        minimum_run_time: Optional[timedelta] = None,
        minimum_stop_time: Optional[timedelta] = None,
        stop_status: Optional[StopStatus] = None,
    ):
        self.__train_path_node_id = train_path_node_id
        self.__arrival_time = arrival_time
        self.__departure_time = departure_time
        self.__minimum_run_time = minimum_run_time
        self.__minimum_stop_time = minimum_stop_time
        self.__stop_status = stop_status

    @property
    def train_path_node_id(self) -> int:
        return self.__train_path_node_id

    @property
    def arrival_time(self) -> datetime:
        return self.__arrival_time

    @property
    def departure_time(self) -> datetime:
        return self.__departure_time

    @property
    def minimum_run_time(self) -> Optional[timedelta]:
        return self.__minimum_run_time

    @property
    def minimum_stop_time(self) -> Optional[timedelta]:
        return self.__minimum_stop_time

    @property
    def stop_status(self) -> Optional[StopStatus]:
        return self.__stop_status


class UpdateTimesTrain(_UpdateTrain):
    __update_times_train_path_nodes: List[UpdateTimesTrainPathNode]

    def __init__(self, train_id: int, update_times_train_path_nodes: List[UpdateTimesTrainPathNode]):
        _UpdateTrain.__init__(self, train_id)
        self.__update_times_train_path_nodes = update_times_train_path_nodes

    @property
    def update_times_train_path_nodes(self) -> List[UpdateTimesTrainPathNode]:
        return self.__update_times_train_path_nodes


class UpdateStopTimesTrainPathNode:
    __train_path_node_id: int
    __arrival_time: datetime
    __departure_time: datetime
    __minimum_stop_time: Optional[timedelta] = None
    __stop_status: Optional[StopStatus] = None

    def __init__(
        self,
        train_path_node_id: int,
        arrival_time: datetime,
        departure_time: datetime,
        minimum_stop_time: Optional[timedelta] = None,
        stop_status: Optional[StopStatus] = None,
    ):
        self.__train_path_node_id = train_path_node_id
        self.__arrival_time = arrival_time
        self.__departure_time = departure_time
        self.__minimum_stop_time = minimum_stop_time
        self.__stop_status = stop_status

    @property
    def train_path_node_id(self) -> int:
        return self.__train_path_node_id

    @property
    def arrival_time(self) -> datetime:
        return self.__arrival_time

    @property
    def departure_time(self) -> datetime:
        return self.__departure_time

    @property
    def minimum_stop_time(self) -> Optional[timedelta]:
        return self.__minimum_stop_time

    @property
    def stop_status(self) -> Optional[StopStatus]:
        return self.__stop_status


class UpdateRunTimesTrainPathSegment:
    __to_train_path_node_id: int
    __from_node_departure_time: datetime
    __to_node_arrival_time: datetime
    __minimum_run_time: Optional[timedelta]

    def __init__(
        self,
        to_train_path_node_id: int,
        from_node_departure_time: datetime,
        to_node_arrival_time: datetime,
        minimum_run_time: Optional[timedelta],
    ):
        self.__to_train_path_node_id = to_train_path_node_id
        self.__from_node_departure_time = from_node_departure_time
        self.__to_node_arrival_time = to_node_arrival_time
        self.__minimum_run_time = minimum_run_time

    @property
    def to_train_path_node_id(self) -> int:
        return self.__to_train_path_node_id

    @property
    def from_node_departure_time(self) -> datetime:
        return self.__from_node_departure_time

    @property
    def to_node_arrival_time(self) -> datetime:
        return self.__to_node_arrival_time

    @property
    def minimum_run_time(self) -> Optional[int]:
        return self.__minimum_run_time
