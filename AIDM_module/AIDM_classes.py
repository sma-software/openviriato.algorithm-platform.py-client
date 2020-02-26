import AlgorithmTypeCheck
from enum import Enum

from AIDM_module.AIDM_baseclasses_to_inherit_from import hasID, hasCode, hasDebugString
from AIDM_module.AIDM_helpers import adjust_dict_keys_for_hidden_objects, parse_to_datetime


class StopStatus(Enum):
    CommercialStop = 0
    OperationalStop = 1
    Passing = 2


class AlgorithmNodeTrack(hasID, hasCode, hasDebugString):
    __NodeTracks: []

    def __init__(self, node_track_id: int, code_string: str, debug_string: str):
        hasID.__init__(self, node_track_id)
        hasCode.__init__(self, code_string)
        hasDebugString.__init__(self, debug_string)


class AlgorithmNode(hasID, hasCode, hasDebugString):
    __NodeTracks: []

    def __init__(self, node_id: int, code_string: str, debug_string: str, node_tracks: list = None):
        hasID.__init__(self, node_id)
        hasCode.__init__(self, code_string)
        hasDebugString.__init__(self, debug_string)
        self.__NodeTracks = []
        if node_tracks is not None:
            for node_track in node_tracks:
                self.__NodeTracks.append(node_track)

    @property
    def NodeTracks(self) -> list:
        return self.__NodeTracks


class AlgorithmSectionTrack(hasID, hasCode, hasDebugString):
    __Weight: int
    __SectionCode: str

    def __init__(self, section_id: int, code_string: str, debug_string: str, section_weight: int, section_code: str):
        hasID.__init__(self, section_id)
        hasCode.__init__(self, code_string)
        hasDebugString.__init__(self, debug_string)
        AlgorithmTypeCheck.assert_parameter_is_int(section_weight, 'section_weight', '__init__')
        AlgorithmTypeCheck.assert_parameter_is_str(section_code, 'section_code', '__init__')
        self.__Weight = section_weight
        self.__SectionCode = section_code

    @property
    def Weight(self) -> int:
        return self.__Weight

    @property
    def SectionCode(self) -> str:
        return self.__SectionCode


class AlgorithmTrain(hasID, hasDebugString):
    __trainPathNodes: list

    def __init__(self, train_id: int, debug_string: str, train_path_nodes: list):
        hasID.__init__(self, train_id)
        hasDebugString.__init__(self, debug_string)
        self.__trainPathNodes = list()
        for i in range(len(train_path_nodes)):
            self.__trainPathNodes.append(TrainPathNode(train_path_nodes[i]))

    @property
    def TrainPathNodes(self):
        return self.__trainPathNodes


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

    @property
    def SectionTrackID(self):
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
