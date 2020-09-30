import datetime
from typing import List, Optional

from py_client.aidm import StopStatus
from py_client.aidm.aidm_base_classes import _UpdateTrain, _RoutingEdge


class UpdateTrainRoute(_UpdateTrain):
    __end_train_path_node_id: int
    __routing_edges: List[_RoutingEdge]
    __start_train_path_node_id: int

    def __init__(
            self,
            train_id: int,
            end_train_path_node_id: int,
            routing_edges: List[_RoutingEdge],
            start_train_path_node_id: int
    ):
        _UpdateTrain.__init__(self, train_id)
        self.__end_train_path_node_id = end_train_path_node_id
        self.__routing_edges = routing_edges
        self.__start_train_path_node_id = start_train_path_node_id

    @property
    def end_train_path_node_id(self) -> int:
        return self.__end_train_path_node_id

    @property
    def routing_edges(self) -> List[_RoutingEdge]:
        return self.__routing_edges

    @property
    def start_train_path_node_id(self) -> int:
        return self.__start_train_path_node_id


class UpdateTimesTrainPathNode:
    __arrival_time: datetime.datetime
    __departure_time: datetime.datetime
    __minimum_run_time: Optional[datetime.timedelta] = None
    __minimum_stop_time: Optional[datetime.timedelta] = None
    __stop_status: Optional[StopStatus] = None
    __train_path_node_id: int

    def __init__(
            self,
            train_path_node_id: int,
            arrival_time: datetime.datetime,
            departure_time: datetime.datetime,
            minimum_run_time: Optional[datetime.timedelta] = None,
            minimum_stop_time: Optional[datetime.timedelta] = None,
            stop_status: Optional[StopStatus] = None
    ):
        self.__train_path_node_id = train_path_node_id
        self.__arrival_time = arrival_time
        self.__departure_time = departure_time
        self.__minimum_run_time = minimum_run_time
        self.__minimum_stop_time = minimum_stop_time
        self.__stop_status = stop_status

    @property
    def arrival_time(self) -> datetime.datetime:
        return self.__arrival_time

    @property
    def departure_time(self) -> datetime.datetime:
        return self.__departure_time

    @property
    def minimum_run_time(self) -> Optional[datetime.timedelta]:
        return self.__minimum_run_time

    @property
    def minimum_stop_time(self) -> Optional[datetime.timedelta]:
        return self.__minimum_stop_time

    @property
    def train_path_node_id(self) -> int:
        return self.__train_path_node_id

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


class UpdateTrainStopTimesNode:
    __arrival_time: datetime.datetime
    __departure_time: datetime.datetime
    __minimum_stop_time: Optional[datetime.timedelta] = None
    __stop_status: Optional[StopStatus] = None
    __train_path_node_id: int

    def __init__(
            self,
            train_path_node_id: int,
            arrival_time: datetime.datetime,
            departure_time: datetime.datetime,
            minimum_stop_time: Optional[datetime.timedelta] = None,
            stop_status: Optional[StopStatus] = None
    ):
        self.__train_path_node_id = train_path_node_id
        self.__arrival_time = arrival_time
        self.__departure_time = departure_time
        self.__minimum_stop_time = minimum_stop_time
        self.__stop_status = stop_status

    @property
    def arrival_time(self) -> datetime.datetime:
        return self.__arrival_time

    @property
    def departure_time(self) -> datetime.datetime:
        return self.__departure_time

    @property
    def minimum_stop_time(self) -> Optional[datetime.timedelta]:
        return self.__minimum_stop_time

    @property
    def train_path_node_id(self) -> int:
        return self.__train_path_node_id

    @property
    def stop_status(self) -> Optional[StopStatus]:
        return self.__stop_status
