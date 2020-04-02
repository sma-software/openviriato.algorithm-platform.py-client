import datetime

from AIDMClasses.AIDM_base_classes import IhasID
from AIDMClasses.AIDM_enum_classes import StopStatus


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
