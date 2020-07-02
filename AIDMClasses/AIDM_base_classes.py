from typing import List, Optional


class HasID:
    __id: int

    def __init__(self, id: int):
        self.__id = id

    @property
    def id(self) -> int:
        return self.__id


class HasCode:
    __code: str

    def __init__(self, code: str):
        self.__code = code

    @property
    def code(self) -> str:
        return self.__code


class HasDebugString:
    __debug_string: Optional[str]

    def __init__(self, debug_string: Optional[str] = None):
        if debug_string is not None:
            self.__debug_string = debug_string

    @property
    def debug_string(self) -> (str, None):
        return self.__debug_string


class UpdateTrain:
    __train_id: int

    def __init__(self, train_id):
        self.__train_id = train_id

    @property
    def train_id(self) -> int:
        return self.__train_id


class RoutingEdge:
    __node_id: int

    def __init__(self, node_id):
        self.__node_id = node_id

    @property
    def node_id(self) -> int:
        return self.__node_id


class RoutingEdgeSet:
    __routing_edges = List[RoutingEdge]

    def __init__(self, routing_edges: List[RoutingEdge]):
        self.__routing_edges = routing_edges

    @property
    def routing_edges(self) -> List[RoutingEdge]:
        return self.__routing_edges
