from enum import Enum

from AIDM_module.AIDM_base_classes import hasID, hasCode, hasDebugString
from AIDM_module.AIDM_helpers import adjust_dict_keys_for_hidden_objects, parse_to_datetime


class StopStatus(Enum):
    commercialStop = 0
    operationalStop = 1
    passing = 2


class AlgorithmNodeTrack(hasID, hasCode, hasDebugString):

    def __init__(self, ID: int, Code: str, DebugString: str):
        hasID.__init__(self, ID)
        hasCode.__init__(self, Code)
        hasDebugString.__init__(self, DebugString)

    @classmethod
    def from_json_dict_factory(cls, json_dict: dict):
        return cls(**json_dict)


class AlgorithmNode(hasID, hasCode, hasDebugString):
    __NodeTracks: []

    def __init__(self, ID: int, Code: str, DebugString: str, NodeTracks: list = []):
        hasID.__init__(self, ID)
        hasCode.__init__(self, Code)
        hasDebugString.__init__(self, DebugString)
        self.__NodeTracks = NodeTracks

    @classmethod
    def from_json_dict_factory(cls, json_dict: dict):
        json_dict['NodeTracks'] = \
            [AlgorithmNodeTrack.from_json_dict_factory(node_track_dict) for node_track_dict in json_dict['NodeTracks']]
        return cls(**json_dict)

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

    @classmethod
    def from_json_dict_factory(cls, json_dict: dict):
        return cls(**json_dict)

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

    @classmethod
    def from_json_dict_factory(cls, json_dict: dict):
        json_dict['TrainPathNodes'] = \
            [TrainPathNode.from_json_dict_factory(path_node_dict) for path_node_dict in json_dict['TrainPathNodes']]
        return cls(**json_dict)

    @property
    def TrainPathNodes(self) -> list:
        return self.__TrainPathNodes


class TrainPathNode(hasID):
    __ArrivalTime: str
    __DepartureTime: str
    __SectionTrackID: int
    __NodeID: int
    __NodeTrackID: int
    __FormationID: int
    __MinimumRunTime: int
    __MinimumStopTime: int
    __StopStatus: StopStatus
    __SequenceNumber: int

    def __init__(self, json_as_dict: dict):
        hasID.__init__(self, json_as_dict['ID'])
        json_as_dict.pop('ID')
        vars(self).update(adjust_dict_keys_for_hidden_objects(json_as_dict))

    @classmethod
    def from_json_dict_factory(cls, json_dict: dict):
        json_dict['StopStatus'] = StopStatus[json_dict['StopStatus']]
        return cls(json_dict)

    @property
    def SectionTrackID(self) -> int:
        return self.__SectionTrackID

    @property
    def NodeID(self):
        return self.__NodeID

    @property
    def NodeTrackID(self):
        return self.__NodeTrackID

    @property
    def FormationID(self):
        return self.__FormationID

    @property
    def ArrivalTime(self):
        return parse_to_datetime(self.__ArrivalTime)

    @property
    def DepartureTime(self):
        return parse_to_datetime(self.__DepartureTime)

    @property
    def MinimumRunTime(self):
        return self.__MinimumRunTime

    @property
    def MinimumStopTime(self):
        return self.__MinimumStopTime

    @property
    def StopStatus(self):
        return self.__StopStatus

    @property
    def SequenceNumber(self):
        return self.__SequenceNumber


"""
class AlgorithmTimeWindow:
    __FromTime: datetime.datetime
    __ToTime: datetime.datetime

    def __init__(self, from_time: datetime.datetime, to_time: datetime.datetime):
        raise NotImplementedError
        assert_datetime(from_time)
        assert_datetime(to_time)
        self.__FromTime = from_time
        self.__ToTime = to_time

    @property
    def FromTime(self):
        return self.__FromTime

    @property
    def ToTime(self):
        return self.__ToTime



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
class UpdateTrainTimesNode(AlgorithmGenericTimeNode):
    __TrainPathNodeID: int
    __StopStatus: str = None

    def __init__(self, arrival_time: datetime.datetime, departure_time: datetime.datetime, train_path_node_id: int,
                 minimum_run_time: str = None, minimum_stop_time: str = None, stop_status: str = None):
        raise NotImplementedError
        super().__init__(arrival_time, departure_time, minimum_run_time, minimum_stop_time)
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', '__init__')
        if not (stop_status is None):
            assert_stop_status(stop_status)
        self.__TrainPathNodeID = train_path_node_id
        self.__StopStatus = stop_status

    @property
    def TrainPathNodeID(self):
        return self.__TrainPathNodeID

    @property
    def StopStatus(self):
        return self.__StopStatus


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
        raise NotImplementedError
        hasID.__init__(self, node_id)
        AlgorithmGenericTimeNode.__init__(self, arrival_time, departure_time, minimum_run_time, minimum_stop_time)
        self.__FormationID = int
        self.__NodeID = int
        self.__NodeTrackID = int
        self.__SectionTrackID = int
        self.__SequenceNumber = int
"""
