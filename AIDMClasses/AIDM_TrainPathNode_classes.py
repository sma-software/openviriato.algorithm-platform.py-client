import datetime
from typing import Optional
from AIDMClasses.AIDM_base_classes import HasID
from AIDMClasses.AIDM_enum_classes import StopStatus


class AlgorithmTrainPathNode(HasID):
    __ArrivalTime: datetime.datetime
    __DepartureTime: datetime.datetime
    __SectionTrackID: Optional[int]
    __NodeID: int
    __NodeTrackID: Optional[int]
    __FormationID: Optional[int]
    __MinimumRunTime: Optional[datetime.timedelta]
    __MinimumStopTime: datetime.timedelta
    __StopStatus: StopStatus
    __SequenceNumber: int

    def __init__(
            self,
            ID: int,
            ArrivalTime: datetime.datetime,
            DepartureTime: datetime.datetime,
            SectionTrackID: Optional[int],
            NodeID: int,
            NodeTrackID: Optional[int],
            FormationID: Optional[int],
            MinimumRunTime: Optional[datetime.timedelta],
            MinimumStopTime: datetime.timedelta,
            StopStatus: StopStatus,
            SequenceNumber: int
    ):
        HasID.__init__(self, ID)
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
    def SectionTrackID(self) -> Optional[int]:
        return self.__SectionTrackID

    @property
    def NodeID(self) -> int:
        return self.__NodeID

    @property
    def NodeTrackID(self) -> Optional[int]:
        return self.__NodeTrackID

    @property
    def FormationID(self) -> Optional[int]:
        return self.__FormationID

    @property
    def ArrivalTime(self) -> datetime.datetime:
        return self.__ArrivalTime

    @property
    def DepartureTime(self) -> datetime.datetime:
        return self.__DepartureTime

    @property
    def MinimumRunTime(self) -> Optional[datetime.timedelta]:
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
