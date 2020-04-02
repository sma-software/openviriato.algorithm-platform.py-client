from AIDMClasses.AIDM_base_classes import IRoutingEdge, IRoutingEdgeSet


class CrossingRoutingEdge(IRoutingEdge):
    __StartSectionTrackID: int
    __EndSectionTrackID: int

    def __init__(self, nodeID: int, startSectionTrackID: int, endSectionTrackID: int):
        IRoutingEdge.__init__(self, nodeID)
        self.__StartSectionTrackID = startSectionTrackID
        self.__EndSectionTrackID = endSectionTrackID

    @property
    def StartSectionTrackID(self) -> int:
        return self.__StartSectionTrackID

    @property
    def EndSectionTrackID(self) -> int:
        return self.__EndSectionTrackID


class IncomingRoutingEdge(IRoutingEdge):
    __EndNodeTrackID: int
    __StartSectionTrackID: int

    def __init__(self, nodeID: int, endNodeTrackID: int, startSectionTrackID: int):
        IRoutingEdge.__init__(self, nodeID)
        self.__EndNodeTrackID = endNodeTrackID
        self.__StartSectionTrackID = startSectionTrackID

    @property
    def EndNodeTrackID(self) -> int:
        return self.__EndNodeTrackID

    @property
    def StartSectionTrackID(self) -> int:
        return self.__StartSectionTrackID


class OutgoingRoutingEdge(IRoutingEdge):
    __EndSectionTrackID: int
    __StartNodeTrackID: int

    def __init__(self, nodeID: int, endSectionTrackID: int, startNodeTrackID: int):
        IRoutingEdge.__init__(self, nodeID)
        self.__EndSectionTrackID = endSectionTrackID
        self.__StartNodeTrackID = startNodeTrackID

    @property
    def StartSectionTrackID(self) -> int:
        return self.__EndSectionTrackID

    @property
    def StartNodeTrackID(self) -> int:
        return self.__StartNodeTrackID


class IncomingRoutingEdgeSet(IRoutingEdgeSet):

    def __init__(self, incomingEdges):
        IRoutingEdgeSet.__init__(self, incomingEdges)


class OutgoingRoutingEdgeSet(IRoutingEdgeSet):

    def __init__(self, outgoingEdges):
        IRoutingEdgeSet.__init__(self, outgoingEdges)


class CrossingRoutingEdgeSet(IRoutingEdgeSet):

    def __init__(self, crossingEdges):
        IRoutingEdgeSet.__init__(self, crossingEdges)
