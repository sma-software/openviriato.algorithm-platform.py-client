from py_client.aidm.aidm_base_classes import _HasDebugString
from py_client.aidm.aidm_time_window_classes import TimeWindow


class AlgorithmNodeTrackClosure(_HasDebugString):
    __node_id: int
    __node_track_id: int
    __closure_time_window: TimeWindow

    def __init__(self, debug_string: str, node_id: int, node_track_id: int, closure_time_window: TimeWindow):
        _HasDebugString.__init__(self, debug_string)
        self.__closure_time_window = closure_time_window
        self.__node_id = node_id
        self.__node_track_id = node_track_id

    @property
    def node_id(self) -> int:
        return self.__node_id

    @property
    def node_track_id(self) -> int:
        return self.__node_track_id

    @property
    def closure_time_window(self) -> TimeWindow:
        return self.__closure_time_window


class AlgorithmSectionTrackClosure(_HasDebugString):
    __section_track_id: int
    __from_node_id: int
    __to_node_id: int
    __closure_time_window_from_node: TimeWindow
    __closure_time_window_to_node: TimeWindow

    def __init__(
        self,
        debug_string: str,
        section_track_id: int,
        from_node_id: int,
        to_node_id: int,
        closure_time_window_from_node: TimeWindow,
        closure_time_window_to_node: TimeWindow,
    ):
        _HasDebugString.__init__(self, debug_string)
        self.__section_track_id = section_track_id
        self.__from_node_id = from_node_id
        self.__to_node_id = to_node_id
        self.__closure_time_window_from_node = closure_time_window_from_node
        self.__closure_time_window_to_node = closure_time_window_to_node

    @property
    def section_track_id(self) -> int:
        return self.__section_track_id

    @property
    def from_node_id(self) -> int:
        return self.__from_node_id

    @property
    def to_node_id(self) -> int:
        return self.__to_node_id

    @property
    def closure_time_window_from_node(self) -> TimeWindow:
        return self.__closure_time_window_from_node

    @property
    def closure_time_window_to_node(self) -> TimeWindow:
        return self.__closure_time_window_to_node
