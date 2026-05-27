from enum import Enum
from typing import Optional, Union


class RoutingEdgeSide(Enum):
    A = "a"
    B = "b"


# --- Request types (for sending to the API) ---


class _RoutingEdgeRequest:
    __node_id: int

    def __init__(self, node_id: int):
        self.__node_id = node_id

    @property
    def node_id(self) -> int:
        return self.__node_id


class _IncomingRoutingEdgeRequest(_RoutingEdgeRequest):
    __start_section_track_id: int

    def __init__(self, node_id: int, start_section_track_id: int):
        super().__init__(node_id)
        self.__start_section_track_id = start_section_track_id

    @property
    def start_section_track_id(self) -> int:
        return self.__start_section_track_id


class _OutgoingRoutingEdgeRequest(_RoutingEdgeRequest):
    __end_section_track_id: int

    def __init__(self, node_id: int, end_section_track_id: int):
        super().__init__(node_id)
        self.__end_section_track_id = end_section_track_id

    @property
    def end_section_track_id(self) -> int:
        return self.__end_section_track_id


class CrossingRoutingEdgeRequest(_RoutingEdgeRequest):
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


class IncomingRoutingEdgeRequest(_IncomingRoutingEdgeRequest):
    def __init__(self, node_id: int, start_section_track_id: int):
        super().__init__(node_id, start_section_track_id)


class IncomingNodeTrackRoutingEdgeRequest(_IncomingRoutingEdgeRequest):
    __end_node_track_id: int

    def __init__(self, node_id: int, start_section_track_id: int, end_node_track_id: int):
        super().__init__(node_id, start_section_track_id)
        self.__end_node_track_id = end_node_track_id

    @property
    def end_node_track_id(self) -> int:
        return self.__end_node_track_id


class OutgoingRoutingEdgeRequest(_OutgoingRoutingEdgeRequest):
    def __init__(self, node_id: int, end_section_track_id: int):
        super().__init__(node_id, end_section_track_id)


class OutgoingNodeTrackRoutingEdgeRequest(_OutgoingRoutingEdgeRequest):
    __start_node_track_id: int

    def __init__(self, node_id: int, start_node_track_id: int, end_section_track_id: int):
        super().__init__(node_id, end_section_track_id)
        self.__start_node_track_id = start_node_track_id

    @property
    def start_node_track_id(self) -> int:
        return self.__start_node_track_id


# --- Response types (received from the API) ---


class _RoutingEdgeResponse:
    __node_id: int

    def __init__(self, node_id: int):
        self.__node_id = node_id

    @property
    def node_id(self) -> int:
        return self.__node_id


class CrossingRoutingEdgeResponse(_RoutingEdgeResponse):
    __start_section_track_id: int
    __incoming_side: Optional[RoutingEdgeSide]
    __outgoing_side: Optional[RoutingEdgeSide]
    __end_section_track_id: int

    def __init__(
        self,
        node_id: int,
        start_section_track_id: int,
        end_section_track_id: int,
        incoming_side: Optional[RoutingEdgeSide] = None,
        outgoing_side: Optional[RoutingEdgeSide] = None,
    ):
        super().__init__(node_id)
        self.__start_section_track_id = start_section_track_id
        self.__incoming_side = incoming_side
        self.__outgoing_side = outgoing_side
        self.__end_section_track_id = end_section_track_id

    @property
    def start_section_track_id(self) -> int:
        return self.__start_section_track_id

    @property
    def incoming_side(self) -> Optional[RoutingEdgeSide]:
        return self.__incoming_side

    @property
    def outgoing_side(self) -> Optional[RoutingEdgeSide]:
        return self.__outgoing_side

    @property
    def end_section_track_id(self) -> int:
        return self.__end_section_track_id


class IncomingNodeTrackRoutingEdgeResponse(_RoutingEdgeResponse):
    __start_section_track_id: int
    __incoming_side: Optional[RoutingEdgeSide]
    __end_node_track_id: int

    def __init__(
        self,
        node_id: int,
        start_section_track_id: int,
        end_node_track_id: int,
        incoming_side: Optional[RoutingEdgeSide] = None,
    ):
        super().__init__(node_id)
        self.__start_section_track_id = start_section_track_id
        self.__incoming_side = incoming_side
        self.__end_node_track_id = end_node_track_id

    @property
    def start_section_track_id(self) -> int:
        return self.__start_section_track_id

    @property
    def incoming_side(self) -> Optional[RoutingEdgeSide]:
        return self.__incoming_side

    @property
    def end_node_track_id(self) -> int:
        return self.__end_node_track_id


class OutgoingNodeTrackRoutingEdgeResponse(_RoutingEdgeResponse):
    __start_node_track_id: int
    __outgoing_side: Optional[RoutingEdgeSide]
    __end_section_track_id: int

    def __init__(
        self,
        node_id: int,
        start_node_track_id: int,
        end_section_track_id: int,
        outgoing_side: Optional[RoutingEdgeSide] = None,
    ):
        super().__init__(node_id)
        self.__start_node_track_id = start_node_track_id
        self.__outgoing_side = outgoing_side
        self.__end_section_track_id = end_section_track_id

    @property
    def start_node_track_id(self) -> int:
        return self.__start_node_track_id

    @property
    def outgoing_side(self) -> Optional[RoutingEdgeSide]:
        return self.__outgoing_side

    @property
    def end_section_track_id(self) -> int:
        return self.__end_section_track_id


class RoutingEdgePairResponse:
    __incoming_routing_edge: Optional[IncomingNodeTrackRoutingEdgeResponse]
    __outgoing_routing_edge: Optional[OutgoingNodeTrackRoutingEdgeResponse]

    def __init__(
        self,
        incoming_routing_edge: Optional[IncomingNodeTrackRoutingEdgeResponse],
        outgoing_routing_edge: Optional[OutgoingNodeTrackRoutingEdgeResponse],
    ):
        self.__incoming_routing_edge = incoming_routing_edge
        self.__outgoing_routing_edge = outgoing_routing_edge

    @property
    def incoming_routing_edge(self) -> Optional[IncomingNodeTrackRoutingEdgeResponse]:
        return self.__incoming_routing_edge

    @property
    def outgoing_routing_edge(self) -> Optional[OutgoingNodeTrackRoutingEdgeResponse]:
        return self.__outgoing_routing_edge


AnyRoutingEdgeIncomingOrCrossingOrOutgoing = Union[
    CrossingRoutingEdgeResponse,
    IncomingNodeTrackRoutingEdgeResponse,
    OutgoingNodeTrackRoutingEdgeResponse,
]

AnyRoutingEdgeIncomingOrOutgoing = Union[
    IncomingRoutingEdgeRequest,
    IncomingNodeTrackRoutingEdgeRequest,
    OutgoingRoutingEdgeRequest,
    OutgoingNodeTrackRoutingEdgeRequest,
]
