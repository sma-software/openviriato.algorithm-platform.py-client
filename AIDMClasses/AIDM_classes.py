import datetime

from AIDMClasses.AIDM_base_classes import hasID, hasCode, hasDebugString
from AIDMClasses.AIDM_enum_classes import StopStatus


class AlgorithmNodeTrack(hasID, hasCode, hasDebugString):

    def __init__(self, ID: int, Code: str, DebugString: str):
        hasID.__init__(self, ID)
        hasCode.__init__(self, Code)
        hasDebugString.__init__(self, DebugString)


class AlgorithmNode(hasID, hasCode, hasDebugString):
    __NodeTracks: []

    def __init__(self, ID: int, Code: str, DebugString: str, NodeTracks: list = []):
        hasID.__init__(self, ID)
        hasCode.__init__(self, Code)
        hasDebugString.__init__(self, DebugString)
        self.__NodeTracks = NodeTracks

    @property
    def NodeTracks(self) -> list:
        return self.__NodeTracks


class AlgorithmSectionTrack(hasID, hasCode, hasDebugString):
    __Weight: int
    __SectionCode: str

    def __init__(self, ID: int, Code: str, DebugString: str, Weight: int, SectionCode: str):
        hasID.__init__(self, ID)
        hasCode.__init__(self, Code)
        hasDebugString.__init__(self, DebugString)
        self.__Weight = Weight
        self.__SectionCode = SectionCode

    @property
    def Weight(self) -> int:
        return self.__Weight

    @property
    def SectionCode(self) -> str:
        return self.__SectionCode


class AlgorithmTrain(hasID, hasDebugString):
    __trainPathNodes: list

    def __init__(self, ID: int, DebugString: str, TrainPathNodes: list):
        hasID.__init__(self, ID)
        hasDebugString.__init__(self, DebugString)
        self.__TrainPathNodes = TrainPathNodes

    @property
    def TrainPathNodes(self) -> list:
        return self.__TrainPathNodes


class TrainPathNode(hasID):
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
        hasID.__init__(self, ID)
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
    def TrainPathNodeId(self):
        return self.__TrainPathNodeId

    @property
    def ArrivalTime(self):
        return self.__ArrivalTime

    @property
    def DepartureTime(self):
        return self.__DepartureTime


class TimeWindow:
    __FromTime: datetime.datetime
    __ToTime: datetime.datetime

    def __init__(self, FromTime: datetime.datetime, ToTime: datetime.datetime):
        self.__FromTime = FromTime
        self.__ToTime = ToTime

    @property
    def FromTime(self):
        return self.__FromTime

    @property
    def ToTime(self):
        return self.__ToTime


class AlgorithmNodeTrackClosure(hasDebugString):
    __NodeID: int
    __NodeTrackID: int
    __ClosureTimeWindow: TimeWindow

    def __init__(self, DebugString: str, ClosureTimeWindow: TimeWindow, NodeID: int, NodeTrackID: int):
        hasDebugString.__init__(self, DebugString)
        self.__ClosureTimeWindow = ClosureTimeWindow
        self.__NodeID = NodeID
        self.__NodeTrackID = NodeTrackID

    @property
    def ClosureTimeWindow(self):
        return self.__ClosureTimeWindow

    @property
    def NodeID(self):
        return self.__NodeID

    @property
    def NodeTrackID(self):
        return self.__NodeTrackID


class AlgorithmSectionTrackClosure(hasDebugString):
    __ClosureTimeWindowFromNode: TimeWindow
    __ClosureTimeWindowToNode: TimeWindow
    __FromNodeID: int
    __SectionTrackID: int
    __ToNodeID: int

    def __init__(self, DebugString: str, ClosureTimeWindowFromNode: TimeWindow, ClosureTimeWindowToNode: TimeWindow,
                 FromNodeID: int, SectionTrackID: int, ToNodeID: int):
        hasDebugString.__init__(self, DebugString)
        self.__ClosureTimeWindowFromNode = ClosureTimeWindowFromNode
        self.__ClosureTimeWindowToNode = ClosureTimeWindowToNode
        self.__FromNodeID = FromNodeID
        self.__SectionTrackID = SectionTrackID
        self.__ToNodeID = ToNodeID

    @property
    def ClosureTimeWindowFromNode(self):
        return self.__ClosureTimeWindowFromNode

    @property
    def ClosureTimeWindowToNode(self):
        return self.__ClosureTimeWindowToNode

    @property
    def FromNodeID(self):
        return self.__FromNodeID

    @property
    def SectionTrackID(self):
        return self.__SectionTrackID

    @property
    def ToNodeID(self):
        return self.__ToNodeID


class AlgorithmTimeWindow:
    __FromTime: datetime.datetime
    __ToTime: datetime.datetime

    def __init__(self, FromTime: datetime.datetime, ToTime: datetime.datetime):
        self.__FromTime = FromTime
        self.__ToTime = ToTime

    @property
    def FromTime(self):
        return self.__FromTime

    @property
    def ToTime(self):
        return self.__ToTime


class UpdateTrainRoute:
    __EndTrainPathNodeID: int
    __RoutingEdges: list
    __StartTrainPathNodeID: int

    def __init__(self, EndTrainPathNodeID:int, RoutingEdges: list, StartTrainPathNodeID: int):
        self.__EndTrainPathNodeID = EndTrainPathNodeID
        self.__RoutingEdges = RoutingEdges
        self.__StartTrainPathNodeID = StartTrainPathNodeID

    @property
    def EndTrainPathNodeID(self):
        return self.__EndTrainPathNodeID

    @property
    def RoutingEdges(self):
        return self.__RoutingEdges

    @property
    def StartTrainPathNodeID(self):
        return self.__StartTrainPathNodeID


class RoutingEdge:
    __NodeID: int

    def __init__(self, NodeID):
        self.__NodeID = NodeID

    @property
    def NodeID(self):
        return self.__NodeID


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
    def ArrivalTime(self):
        return self.__ArrivalTime

    @property
    def DepartureTime(self):
        return self.__DepartureTime

    @property
    def MinimumRunTime(self):
        return self.__MinimumRunTime

    @property
    def MinimumStopTime(self):
        return self.__MinimumStopTime

    @property
    def TrainPathNodeID(self):
        return self.__TrainPathNodeID

    @property
    def StopStatus(self):
        return self.__StopStatus


"""
# NotImplemented!!,
class AlgorithmGenericTimeNode:  # this is a bad idea, for maintenance in future.
    # no assertions so far!
    __ArrivalTime = datetime.datetime
    __DepartureTime: datetime.datetime
    __MinimumRunTime: str
    __MinimumStopTime: str

    def __init__(self, arrival_time: datetime.datetime, departure_time: datetime.datetime,
                 minimum_run_time: str = None, minimum_stop_time: str = None):
        raise NotImplementedError
        self.__ArrivalTime = arrival_time
        self.__DepartureTime = departure_time
        self.__MinimumRunTime = minimum_run_time
        self.__MinimumStopTime = minimum_stop_time

    @property
    def ArrivalTime(self):
        return self.__ArrivalTime

    @property
    def DepartureTime(self):
        return self.__DepartureTime

    @property
    def MinimumRunTime(self):
        return self.__MinimumRunTime

    @property
    def MinimumStopTime(self):
        return self.__MinimumStopTime


# NotImplemented!!,



# NotImplemented!!,
class AlgorithmTrainPathNode(hasID, AlgorithmGenericTimeNode):
    __FormationID: int = None
    __NodeID: int
    __NodeTrackID: int
    __SectionTrackID: int = None
    __SequenceNumber: int
    __StopStatus: str

    def __init__(self, node_id: int, arrival_time: datetime.datetime, departure_time: datetime.datetime,
                 minimum_run_time, minimum_stop_time):
        hasID.__init__(self, node_id)
        self.__FormationID = int
        self.__NodeID = int
        self.__NodeTrackID = int
        self.__SectionTrackID = int
        self.__SequenceNumber = int
        
        
    @property
    def ArrivalTime(self):
        return self.__ArrivalTime

    @property
    def DepartureTime(self):
        return self.__DepartureTime

    @property
    def MinimumRunTime(self):
        return self.__MinimumRunTime

    @property
    def MinimumStopTime(self):
        return self.__MinimumStopTime
"""
