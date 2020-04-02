import datetime

from AIDMClasses.AIDM_base_classes import IhasID, IhasCode, IhasDebugString
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


class AlgorithmFormation(IhasID, IhasDebugString):
    __VehicleTypeIDs: list

    def __init__(self, ID: int, DebugString: str, VehicleTypeIDs: list):
        IhasID.__init__(self, ID)
        IhasDebugString.__init__(self, DebugString)
        self.__VehicleTypeIDs = VehicleTypeIDs

    @property
    def VehicleTypeIDs(self) -> list:
        return self.__VehicleTypeIDs


class AlgorithmVehicleType(IhasID, IhasDebugString):
    __IsEngine: bool

    def __init__(self, ID: int, DebugString: str, IsEngine: bool):
        IhasID.__init__(self, ID)
        IhasDebugString.__init__(self, DebugString)
        self.__IsEngine = IsEngine

    @property
    def IsEngine(self) -> bool:
        return self.__IsEngine
