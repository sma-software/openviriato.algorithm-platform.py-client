import datetime
from AIDMClasses.AIDM_base_classes import IUpdateTrain, IRoutingEdge
from AIDMClasses import StopStatus
from typing import List, Optional


class UpdateTrainRoute(IUpdateTrain):
    __EndTrainPathNodeID: int
    __RoutingEdges: List[IRoutingEdge]
    __StartTrainPathNodeID: int

    def __init__(
            self,
            TrainID: int,
            EndTrainPathNodeID: int,
            RoutingEdges: List[IRoutingEdge],
            StartTrainPathNodeID: int
    ):
        IUpdateTrain.__init__(self, TrainID)
        self.__EndTrainPathNodeID = EndTrainPathNodeID
        self.__RoutingEdges = RoutingEdges
        self.__StartTrainPathNodeID = StartTrainPathNodeID

    @property
    def EndTrainPathNodeID(self) -> int:
        return self.__EndTrainPathNodeID

    @property
    def RoutingEdges(self) -> List[IRoutingEdge]:
        return self.__RoutingEdges

    @property
    def StartTrainPathNodeID(self) -> int:
        return self.__StartTrainPathNodeID


class UpdateTrainTimesNode:
    __ArrivalTime: datetime.datetime
    __DepartureTime: datetime.datetime
    __MinimumRunTime: Optional[datetime.timedelta] = None
    __MinimumStopTime: Optional[datetime.timedelta] = None
    __StopStatus: Optional[StopStatus] = None
    __TrainPathNodeID: int

    def __init__(
            self,
            TrainPathNodeID: int,
            ArrivalTime: datetime.datetime,
            DepartureTime: datetime.datetime,
            MinimumRunTime: Optional[datetime.timedelta] = None,
            MinimumStopTime: Optional[datetime.timedelta] = None,
            StopStatus: Optional[StopStatus] = None
    ):
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
    def MinimumRunTime(self) -> Optional[datetime.timedelta]:
        return self.__MinimumRunTime

    @property
    def MinimumStopTime(self) -> Optional[datetime.timedelta]:
        return self.__MinimumStopTime

    @property
    def TrainPathNodeID(self) -> int:
        return self.__TrainPathNodeID

    @property
    def StopStatus(self) -> Optional[StopStatus]:
        return self.__StopStatus


class UpdateTrainTimes(IUpdateTrain):
    __Times: List[UpdateTrainTimesNode]

    def __init__(self, TrainID: int, Times: List[UpdateTrainTimesNode]):
        IUpdateTrain.__init__(self, TrainID)
        self.__Times = Times

    @property
    def Times(self) -> List[UpdateTrainTimesNode]:
        return self.__Times
