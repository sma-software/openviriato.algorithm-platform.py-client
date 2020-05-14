from AIDMClasses.AIDM_TimeWindow_classes import TimeWindow
from AIDMClasses.AIDM_base_classes import HasDebugString


class AlgorithmNodeTrackClosure(HasDebugString):
    __NodeID: int
    __NodeTrackID: int
    __ClosureTimeWindow: TimeWindow

    def __init__(self, DebugString: str, ClosureTimeWindow: TimeWindow, NodeID: int, NodeTrackID: int):
        HasDebugString.__init__(self, DebugString)
        self.__ClosureTimeWindow = ClosureTimeWindow
        self.__NodeID = NodeID
        self.__NodeTrackID = NodeTrackID

    @property
    def ClosureTimeWindow(self) -> TimeWindow:
        return self.__ClosureTimeWindow

    @property
    def NodeID(self) -> int:
        return self.__NodeID

    @property
    def NodeTrackID(self) -> int:
        return self.__NodeTrackID


class AlgorithmSectionTrackClosure(HasDebugString):
    __ClosureTimeWindowFromNode: TimeWindow
    __ClosureTimeWindowToNode: TimeWindow
    __FromNodeID: int
    __SectionTrackID: int
    __ToNodeID: int

    def __init__(self, DebugString: str, ClosureTimeWindowFromNode: TimeWindow, ClosureTimeWindowToNode: TimeWindow,
                 FromNodeID: int, SectionTrackID: int, ToNodeID: int):
        HasDebugString.__init__(self, DebugString)
        self.__ClosureTimeWindowFromNode = ClosureTimeWindowFromNode
        self.__ClosureTimeWindowToNode = ClosureTimeWindowToNode
        self.__FromNodeID = FromNodeID
        self.__SectionTrackID = SectionTrackID
        self.__ToNodeID = ToNodeID

    @property
    def ClosureTimeWindowFromNode(self) -> TimeWindow:
        return self.__ClosureTimeWindowFromNode

    @property
    def ClosureTimeWindowToNode(self) -> TimeWindow:
        return self.__ClosureTimeWindowToNode

    @property
    def FromNodeID(self) -> int:
        return self.__FromNodeID

    @property
    def SectionTrackID(self) -> int:
        return self.__SectionTrackID

    @property
    def ToNodeID(self) -> int:
        return self.__ToNodeID