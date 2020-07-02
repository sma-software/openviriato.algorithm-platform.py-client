from AIDMClasses.AIDM_base_classes import RoutingEdge, RoutingEdgeSet
from typing import List


class CrossingRoutingEdge(RoutingEdge):
    __start_section_track_id: int
    __end_section_track_id: int

    def __init__(self, node_id: int, start_section_track_id: int, end_section_track_id: int):
        RoutingEdge.__init__(self, node_id)
        self.__start_section_track_id = start_section_track_id
        self.__end_section_track_id = end_section_track_id

    @property
    def start_section_track_id(self) -> int:
        return self.__start_section_track_id

    @property
    def end_section_track_id(self) -> int:
        return self.__end_section_track_id


class IncomingRoutingEdge(RoutingEdge):
    __end_node_track_id: int
    __start_section_track_id: int

    def __init__(self, node_id: int, end_node_track_id: int, start_section_track_id: int):
        RoutingEdge.__init__(self, node_id)
        self.__end_node_track_id = end_node_track_id
        self.__start_section_track_id = start_section_track_id

    @property
    def end_node_track_id(self) -> int:
        return self.__end_node_track_id

    @property
    def start_section_track_id(self) -> int:
        return self.__start_section_track_id


class OutgoingRoutingEdge(RoutingEdge):
    __end_section_track_id: int
    __start_node_track_id: int

    def __init__(self, node_id: int, end_section_track_id: int, start_node_track_id: int):
        RoutingEdge.__init__(self, node_id)
        self.__end_section_track_id = end_section_track_id
        self.__start_node_track_id = start_node_track_id

    @property
    def end_section_track_id(self) -> int:
        return self.__end_section_track_id

    @property
    def start_node_track_id(self) -> int:
        return self.__start_node_track_id


class IncomingRoutingEdgeSet(RoutingEdgeSet):

    def __init__(self, incoming_edges: List[IncomingRoutingEdge]):
        super().__init__(incoming_edges)

    @property
    def routing_edges(self) -> List[IncomingRoutingEdge]:
        return super().routing_edges


class OutgoingRoutingEdgeSet(RoutingEdgeSet):

    def __init__(self, outgoing_edges: List[OutgoingRoutingEdge]):
        super().__init__(outgoing_edges)

    @property
    def routing_edges(self) -> List[OutgoingRoutingEdge]:
        return super().routing_edges


class CrossingRoutingEdgeSet(RoutingEdgeSet):

    def __init__(self, crossing_edges: List[CrossingRoutingEdge]):
        super().__init__(crossing_edges)

    @property
    def routing_edges(self) -> List[CrossingRoutingEdge]:
        return super().routing_edges
