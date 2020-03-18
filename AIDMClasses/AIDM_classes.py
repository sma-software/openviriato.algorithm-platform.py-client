import datetime

from AIDMClasses.AIDM_base_classes import IhasID, IhasCode, IhasDebugString, IUpdateTrain, IRoutingEdge
from AIDMClasses.AIDM_enum_classes import StopStatus


class AlgorithmNodeTrack(IhasID, IhasCode, IhasDebugString):

    def __init__(self, ID: int, Code: str, DebugString: str):
        IhasID.__init__(self, ID)
        IhasCode.__init__(self, Code)
        IhasDebugString.__init__(self, DebugString)


class AlgorithmNode(IhasID, IhasCode, IhasDebugString):
    __NodeTracks: []

    def __init__(self, ID: int, Code: str, DebugString: str, NodeTracks: list = []):
        IhasID.__init__(self, ID)
        IhasCode.__init__(self, Code)
        IhasDebugString.__init__(self, DebugString)
        self.__NodeTracks = NodeTracks

    @property
    def NodeTracks(self) -> list:
        return self.__NodeTracks


class AlgorithmSectionTrack(IhasID, IhasCode, IhasDebugString):
    __Weight: int
    __SectionCode: str

    def __init__(self, ID: int, Code: str, DebugString: str, Weight: int, SectionCode: str):
        IhasID.__init__(self, ID)
        IhasCode.__init__(self, Code)
        IhasDebugString.__init__(self, DebugString)
        self.__Weight = Weight
        self.__SectionCode = SectionCode

    @property
    def Weight(self) -> int:
        return self.__Weight

    @property
    def SectionCode(self) -> str:
        return self.__SectionCode


class AlgorithmTrain(IhasID, IhasDebugString):
    __trainPathNodes: list

    def __init__(self, ID: int, DebugString: str, TrainPathNodes: list):
        IhasID.__init__(self, ID)
        IhasDebugString.__init__(self, DebugString)
        self.__TrainPathNodes = TrainPathNodes

    @property
    def TrainPathNodes(self) -> list:
        return self.__TrainPathNodes


class TrainPathNode(IhasID):
    __ArrivalTime: datetime.datetime
    __DepartureTime: datetime.datetime
    __SectionTrackID: int
    __NodeID: int
    __NodeTrackID: int
    __FormationID: int
    __MinimumRunTime: (datetime.timedelta, None)
    __MinimumStopTime: datetime.timedelta
    __StopStatus: StopStatus
    __SequenceNumber: int

    def __init__(self, ID: int, ArrivalTime: datetime.datetime, DepartureTime: datetime.datetime,
                 SectionTrackID: (int, None), NodeID: int, NodeTrackID: (int, None), FormationID: int,
                 MinimumRunTime: (datetime.timedelta, None), MinimumStopTime: datetime.timedelta,
                 StopStatus: StopStatus, SequenceNumber: int):
        IhasID.__init__(self, ID)
        self.__ArrivalTime = ArrivalTime
        self.__DepartureTime = DepartureTime
        self.__SectionTrackID = SectionTrackID
        self.__NodeID = NodeID
        self.__NodeTrackID = NodeTrackID
        self.__FormationID = FormationID
        self.__MinimumRunTime = MinimumRunTime
        self.__MinimumStopTime = MinimumStopTime
        self.__StopStatus = StopStatus
        self.__SequenceNumber = SequenceNumber

    @property
    def SectionTrackID(self) -> int:
        return self.__SectionTrackID

    @property
    def NodeID(self) -> int:
        return self.__NodeID

    @property
    def NodeTrackID(self) -> int:
        return self.__NodeTrackID

    @property
    def FormationID(self) -> int:
        return self.__FormationID

    @property
    def ArrivalTime(self) -> datetime.datetime:
        return self.__ArrivalTime

    @property
    def DepartureTime(self) -> datetime.datetime:
        return self.__DepartureTime

    @property
    def MinimumRunTime(self) -> datetime.timedelta:
        return self.__MinimumRunTime

    @property
    def MinimumStopTime(self) -> datetime.timedelta:
        return self.__MinimumStopTime

    @property
    def StopStatus(self) -> StopStatus:
        return self.__StopStatus

    @property
    def SequenceNumber(self) -> int:
        return self.__SequenceNumber


class updateTrainTimesNode:
    TrainPathNodeId: int
    ArrivalTime: datetime.datetime
    DepartureTime: datetime.datetime

    def __init__(self, TrainPathNodeId: int, ArrivalTime: datetime.datetime, DepartureTime: datetime.datetime):
        self.__TrainPathNodeId = TrainPathNodeId
        self.__ArrivalTime = ArrivalTime
        self.__DepartureTime = DepartureTime

    @property
    def TrainPathNodeId(self) -> int:
        return self.__TrainPathNodeId

    @property
    def ArrivalTime(self) -> datetime.datetime:
        return self.__ArrivalTime

    @property
    def DepartureTime(self) -> datetime.datetime:
        return self.__DepartureTime


class TimeWindow:
    __FromTime: datetime.datetime
    __ToTime: datetime.datetime

    def __init__(self, FromTime: datetime.datetime, ToTime: datetime.datetime):
        self.__FromTime = FromTime
        self.__ToTime = ToTime

    @property
    def FromTime(self) -> datetime.datetime:
        return self.__FromTime

    @property
    def ToTime(self) -> datetime.datetime:
        return self.__ToTime


class AlgorithmNodeTrackClosure(IhasDebugString):
    __NodeID: int
    __NodeTrackID: int
    __ClosureTimeWindow: TimeWindow

    def __init__(self, DebugString: str, ClosureTimeWindow: TimeWindow, NodeID: int, NodeTrackID: int):
        IhasDebugString.__init__(self, DebugString)
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


class AlgorithmSectionTrackClosure(IhasDebugString):
    __ClosureTimeWindowFromNode: TimeWindow
    __ClosureTimeWindowToNode: TimeWindow
    __FromNodeID: int
    __SectionTrackID: int
    __ToNodeID: int

    def __init__(self, DebugString: str, ClosureTimeWindowFromNode: TimeWindow, ClosureTimeWindowToNode: TimeWindow,
                 FromNodeID: int, SectionTrackID: int, ToNodeID: int):
        IhasDebugString.__init__(self, DebugString)
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


class UpdateTrainRoute(IUpdateTrain):
    __EndTrainPathNodeID: int
    __RoutingEdges: list
    __StartTrainPathNodeID: int

    def __init__(self, TrainID: int, EndTrainPathNodeID: int, RoutingEdges: list, StartTrainPathNodeID: int):
        IUpdateTrain.__init__(self, TrainID)
        self.__EndTrainPathNodeID = EndTrainPathNodeID
        self.__RoutingEdges = RoutingEdges
        self.__StartTrainPathNodeID = StartTrainPathNodeID

    @property
    def EndTrainPathNodeID(self) -> int:
        return self.__EndTrainPathNodeID

    @property
    def RoutingEdges(self) -> list:
        return self.__RoutingEdges

    @property
    def StartTrainPathNodeID(self) -> int:
        return self.__StartTrainPathNodeID


class UpdateTrainTimesNode:
    __ArrivalTime = datetime.datetime
    __DepartureTime: datetime.datetime
    __MinimumRunTime: (datetime.timedelta, None) = None
    __MinimumStopTime: (datetime.timedelta, None) = None
    __StopStatus: (str, None) = None
    __TrainPathNodeID: int

    def __init__(self, TrainPathNodeID: int, ArrivalTime: datetime.datetime, DepartureTime: datetime.datetime,
                 MinimumRunTime: (datetime.timedelta, None) = None, MinimumStopTime: (datetime.timedelta, None) = None,
                 StopStatus: (StopStatus, None) = None):
        self.__TrainPathNodeID = TrainPathNodeID
        self.__ArrivalTime = ArrivalTime
        self.__DepartureTime = DepartureTime
        self.__MinimumRunTime = MinimumRunTime
        self.__MinimumStopTime = MinimumStopTime
        self.__StopStatus = StopStatus

    @property
    def ArrivalTime(self) -> datetime.datetime:
        return self.__ArrivalTime

    @property
    def DepartureTime(self) -> datetime.datetime:
        return self.__DepartureTime

    @property
    def MinimumRunTime(self) -> (None, datetime.timedelta):
        return self.__MinimumRunTime

    @property
    def MinimumStopTime(self) -> datetime.timedelta:
        return self.__MinimumStopTime

    @property
    def TrainPathNodeID(self) -> int:
        return self.__TrainPathNodeID

    @property
    def StopStatus(self) -> StopStatus:
        return self.__StopStatus


class CrossingRoutingEdge(IRoutingEdge):
    __StartSectionTrackID: int
    __EndSectionTrackID: int

    def __init__(self, NodeID: int, startSectionTrackID: int, endSectionTrackID: int):
        IRoutingEdge.__init__(self, NodeID)
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
    def StartSectionTrackID(self) -> int:
        return self.__EndSectionTrackID

    @property
    def StartNodeTrackID(self) -> int:
        return self.__StartNodeTrackID
