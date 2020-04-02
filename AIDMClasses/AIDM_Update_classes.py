import datetime

from AIDMClasses.AIDM_base_classes import IUpdateTrain
from AIDMClasses import StopStatus


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


class UpdateTrainTimes(IUpdateTrain):
    __Times: list

    def __init__(self, TrainID: int, Times: list):
        IUpdateTrain.__init__(self, TrainID)
        self.__Times = Times

    @property
    def Times(self) -> list:
        return self.__Times


class UpdateTrainTimesNode:
    __ArrivalTime: datetime.datetime
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