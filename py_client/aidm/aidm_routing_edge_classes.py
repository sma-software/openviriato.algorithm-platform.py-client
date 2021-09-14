from typing import Union


class _RoutingEdge:
    __node_id: int

    def __init__(self, node_id: int):
        self.__node_id = node_id

    @property
    def node_id(self) -> int:
        return self.__node_id


class _CrossingRoutingEdgeBase(_RoutingEdge):
    __start_section_track_id: int
    __end_section_track_id: int

    def __init__(self, node_id: int, start_section_track_id: int, end_section_track_id: int):
        super().__init__(node_id)
        self.__start_section_track_id = start_section_track_id
        self.__end_section_track_id = end_section_track_id

    @property
    def start_section_track_id(self) -> int:
        return self.__start_section_track_id

    @property
    def end_section_track_id(self) -> int:
        return self.__end_section_track_id


class CrossingRoutingEdge(_CrossingRoutingEdgeBase):
    def __init__(self, node_id: int, start_section_track_id: int, end_section_track_id: int):
        super().__init__(node_id, start_section_track_id, end_section_track_id)


class _IncomingRoutingEdgeBase(_RoutingEdge):
    __start_section_track_id: int

    def __init__(self, node_id: int, start_section_track_id: int):
        super().__init__(node_id)
        self.__start_section_track_id = start_section_track_id

    @property
    def start_section_track_id(self) -> int:
        return self.__start_section_track_id


class _OutgoingRoutingEdgeBase(_RoutingEdge):
    __end_section_track_id: int

    def __init__(self, node_id: int, end_section_track_id: int):
        super().__init__(node_id)
        self.__end_section_track_id = end_section_track_id

    @property
    def end_section_track_id(self) -> int:
        return self.__end_section_track_id


class IncomingRoutingEdge(_IncomingRoutingEdgeBase):
    def __init__(self, node_id: int, start_section_track_id: int):
        super().__init__(node_id, start_section_track_id)


class OutgoingRoutingEdge(_OutgoingRoutingEdgeBase):
    def __init__(self, node_id: int, end_section_track_id: int):
        super().__init__(node_id, end_section_track_id)


class IncomingNodeTrackRoutingEdge(_IncomingRoutingEdgeBase):
    __end_node_track_id: int

    def __init__(self, node_id: int, start_section_track_id: int, end_node_track_id: int):
        super().__init__(node_id, start_section_track_id)
        self.__end_node_track_id = end_node_track_id

    @property
    def end_node_track_id(self) -> int:
        return self.__end_node_track_id


class OutgoingNodeTrackRoutingEdge(_OutgoingRoutingEdgeBase):
    __start_node_track_id: int

    def __init__(self, node_id: int, start_node_track_id: int, end_section_track_id: int):
        super().__init__(node_id, end_section_track_id)
        self.__start_node_track_id = start_node_track_id

    @property
    def start_node_track_id(self) -> int:
        return self.__start_node_track_id


class RoutingEdgePair:
    __incoming_routing_edge: IncomingNodeTrackRoutingEdge
    __outgoing_routing_edge: OutgoingNodeTrackRoutingEdge

    def __init__(
        self,
        incoming_routing_edge: IncomingNodeTrackRoutingEdge,
        outgoing_routing_edge: OutgoingNodeTrackRoutingEdge,
    ):
        self.__incoming_routing_edge = incoming_routing_edge
        self.__outgoing_routing_edge = outgoing_routing_edge

    @property
    def incoming_routing_edge(self) -> IncomingNodeTrackRoutingEdge:
        return self.__incoming_routing_edge

    @property
    def outgoing_routing_edge(self) -> OutgoingNodeTrackRoutingEdge:
        return self.__outgoing_routing_edge


AnyRoutingEdgeIncomingOrCrossingOrOutgoing = Union[
    CrossingRoutingEdge,
    IncomingRoutingEdge,
    IncomingNodeTrackRoutingEdge,
    OutgoingRoutingEdge,
    OutgoingNodeTrackRoutingEdge,
]

AnyRoutingEdgeIncomingOrOutgoing = Union[
    IncomingRoutingEdge,
    IncomingNodeTrackRoutingEdge,
    OutgoingRoutingEdge,
    OutgoingNodeTrackRoutingEdge,
]
