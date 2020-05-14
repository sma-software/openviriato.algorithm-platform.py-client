from typing import List, Optional


class HasID:
    __ID: int

    def __init__(self, ID: int):
        self.__ID = ID

    @property
    def ID(self) -> int:
        return self.__ID


class HasCode:
    __Code: str

    def __init__(self, Code: str):
        self.__Code = Code

    @property
    def Code(self) -> str:
        return self.__Code


class HasDebugString:
    __DebugString: Optional[str]

    def __init__(self, DebugString: Optional[str] = None):
        if DebugString is not None:
            self.__DebugString = DebugString

    @property
    def DebugString(self) -> (str, None):
        return self.__DebugString


class UpdateTrain:
    __TrainID: int

    def __init__(self, TrainID):
        self.__TrainID = TrainID

    @property
    def TrainID(self) -> int:
        return self.__TrainID


class RoutingEdge:
    __NodeID: int

    def __init__(self, NodeID):
        self.__NodeID = NodeID

    @property
    def NodeID(self) -> int:
        return self.__NodeID


class RoutingEdgeSet:
    __RoutingEdges = List[RoutingEdge]

    def __init__(self, RoutingEdges: List[RoutingEdge]):
        self.__RoutingEdges = RoutingEdges

    @property
    def RoutingEdges(self) -> List[RoutingEdge]:
        return self.__RoutingEdges
