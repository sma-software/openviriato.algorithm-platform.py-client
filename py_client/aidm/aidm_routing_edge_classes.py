from enum import unique, Enum

from py_client.aidm.aidm_base_classes import _RoutingEdge


@unique
class RoutingEdgeType(Enum):
    incoming = "incoming"
    outgoing = "outgoing"
    crossing = "crossing"


class CrossingRoutingEdge(_RoutingEdge):
    __start_section_track_id: int
    __end_section_track_id: int

    def __init__(self, node_id: int, start_section_track_id: int, end_section_track_id: int):
        _RoutingEdge.__init__(self, node_id)
        self.__start_section_track_id = start_section_track_id
        self.__end_section_track_id = end_section_track_id

    @property
    def start_section_track_id(self) -> int:
        return self.__start_section_track_id

    @property
    def end_section_track_id(self) -> int:
        return self.__end_section_track_id


class IncomingRoutingEdge(_RoutingEdge):
    __end_node_track_id: int
    __start_section_track_id: int

    def __init__(self, node_id: int, start_section_track_id: int, end_node_track_id: int):
        _RoutingEdge.__init__(self, node_id)
        self.__end_node_track_id = end_node_track_id
        self.__start_section_track_id = start_section_track_id

    @property
    def end_node_track_id(self) -> int:
        return self.__end_node_track_id

    @property
    def start_section_track_id(self) -> int:
        return self.__start_section_track_id


class OutgoingRoutingEdge(_RoutingEdge):
    __end_section_track_id: int
    __start_node_track_id: int

    def __init__(self, node_id: int, start_node_track_id: int, end_section_track_id: int):
        _RoutingEdge.__init__(self, node_id)
        self.__end_section_track_id = end_section_track_id
        self.__start_node_track_id = start_node_track_id

    @property
    def end_section_track_id(self) -> int:
        return self.__end_section_track_id

    @property
    def start_node_track_id(self) -> int:
        return self.__start_node_track_id
