from typing import Optional


class RoutingPoint:
    __node_id: int
    __node_track_id: Optional[int]

    def __init__(self, node_id: int, node_track_id: Optional[int] = None):
        self.__node_id = node_id
        self.__node_track_id = node_track_id

    @property
    def node_id(self) -> int:
        return self.__node_id

    @property
    def node_track_id(self) -> Optional[int]:
        return self.__node_track_id