class RoutingPoint:
    __nodeID: int
    __nodeTrackID: (None, int)

    def __init__(self, nodeID: int, nodeTrackID: (None, int) = None):
        self.__nodeID = nodeID
        self.__nodeTrackID = nodeTrackID

    @property
    def NodeID(self) -> int:
        return self.__nodeID

    @property
    def NodeTrackID(self) -> (None, int):
        return self.__nodeTrackID