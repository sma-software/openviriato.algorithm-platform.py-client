from typing import Optional


class RoutingPoint:
    __nodeID: int
    __nodeTrackID: Optional[int]

    def __init__(self, nodeID: int, nodeTrackID: Optional[int] = None):
        self.__nodeID = nodeID
        self.__nodeTrackID = nodeTrackID

    @property
    def NodeID(self) -> int:
        return self.__nodeID

    @property
    def NodeTrackID(self) -> Optional[int]:
        return self.__nodeTrackID