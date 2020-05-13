from AIDMClasses.AIDM_base_classes import IRoutingEdge, IRoutingEdgeSet
from typing import List


class CrossingRoutingEdge(IRoutingEdge):
    __StartSectionTrackID: int
    __EndSectionTrackID: int

    def __init__(self, NodeID: int, StartSectionTrackID: int, EndSectionTrackID: int):
        IRoutingEdge.__init__(self, NodeID)
        self.__StartSectionTrackID = StartSectionTrackID
        self.__EndSectionTrackID = EndSectionTrackID

    @property
    def StartSectionTrackID(self) -> int:
        return self.__StartSectionTrackID

    @property
    def EndSectionTrackID(self) -> int:
        return self.__EndSectionTrackID


class IncomingRoutingEdge(IRoutingEdge):
    __EndNodeTrackID: int
    __StartSectionTrackID: int

    def __init__(self, NodeID: int, EndNodeTrackID: int, StartSectionTrackID: int):
        IRoutingEdge.__init__(self, NodeID)
        self.__EndNodeTrackID = EndNodeTrackID
        self.__StartSectionTrackID = StartSectionTrackID

    @property
    def EndNodeTrackID(self) -> int:
        return self.__EndNodeTrackID

    @property
    def StartSectionTrackID(self) -> int:
        return self.__StartSectionTrackID


class OutgoingRoutingEdge(IRoutingEdge):
    __EndSectionTrackID: int
    __StartNodeTrackID: int

    def __init__(self, NodeID: int, EndSectionTrackID: int, StartNodeTrackID: int):
        IRoutingEdge.__init__(self, NodeID)
        self.__EndSectionTrackID = EndSectionTrackID
        self.__StartNodeTrackID = StartNodeTrackID

    @property
    def EndSectionTrackID(self) -> int:
        return self.__EndSectionTrackID

    @property
    def StartNodeTrackID(self) -> int:
        return self.__StartNodeTrackID


class IncomingRoutingEdgeSet(IRoutingEdgeSet):

    def __init__(self, IncomingEdges: List[IncomingRoutingEdge]):
        super().__init__(IncomingEdges)

    @property
    def RoutingEdges(self) -> List[IncomingRoutingEdge]:
        return super().RoutingEdges


class OutgoingRoutingEdgeSet(IRoutingEdgeSet):

    def __init__(self, OutgoingEdges: List[OutgoingRoutingEdge]):
        super().__init__(OutgoingEdges)

    @property
    def RoutingEdges(self) -> List[OutgoingRoutingEdge]:
        return super().RoutingEdges


class CrossingRoutingEdgeSet(IRoutingEdgeSet):

    def __init__(self, CrossingEdges: List[CrossingRoutingEdge]):
        super().__init__(CrossingEdges)

    @property
    def RoutingEdges(self) -> List[CrossingRoutingEdge]:
        return super().RoutingEdges
