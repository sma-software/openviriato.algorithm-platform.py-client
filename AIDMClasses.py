import AlgorithmTypeCheck
import datetime
from enum import Enum

# rename to AIDM Classes,

def assert_non_negative_weight(weight: int):
    assert not (weight < 0), 'only non-negative values for weights permitted'


def parse_to_datetime(datetime_raw_str: str) -> datetime.datetime:
    return datetime.datetime.strptime(datetime_raw_str, '%Y-%m-%dT%H:%M:%S')


def assert_stop_status(stop_status: str) -> None:
    assert isinstance(stop_status, StopStatus), \
        'required to be of type StopStatus\nbut it was a instead: {0}'.format(stop_status.__class__)


def assert_datetime(date_time_obj: datetime.datetime):
    assert isinstance(date_time_obj, datetime.datetime), 'value has to be a datetime object'



class StopStatus(Enum):
    CommercialStop = 0
    OperationalStop = 1
    Passing = 2


class hasID:
    __ID: int

    def __init__(self, element_id: int):
        AlgorithmTypeCheck.assert_parameter_is_int(element_id, 'element_id', '__init()__')
        self.__ID = element_id

    @property
    def ID(self) -> int:
        return self.__ID


class hasCode:
    __Code: str

    def __init__(self, code_string: str):
        AlgorithmTypeCheck.assert_parameter_is_str(code_string, 'code_string', '__init()__')
        self.__Code = code_string

    @property
    def Code(self) -> str:
        return self.__Code


class hasDebugString:
    __DebugString: str

    def __init__(self, debug_string: str = None):
        if debug_string is not None:
            AlgorithmTypeCheck.assert_parameter_is_str(debug_string, 'debug_string', '__init()__')
        self.__DebugString = debug_string

    @property
    def DebugString(self):
        return self.__DebugString


class AlgorithmNode(hasID, hasCode, hasDebugString):
    __NodeTracks: []

    def __init__(self, node_id: int, code_string: str, debug_string: str, node_tracks: list = None):
        hasID.__init__(self, node_id)
        hasCode.__init__(self, code_string)
        hasDebugString.__init__(self, debug_string)
        if node_tracks is None:
            node_tracks = []
        self.__NodeTracks = node_tracks

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
        # assert_non_negative_weight(section_weight) --> is too much
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
        self.__trainPathNodes = train_path_nodes

    @property
    def trainPathNodes(self):
        return self.__trainPathNodes


class AlgorithmTimeWindow:
    __FromTime: datetime.datetime
    __ToTime: datetime.datetime

    def __init__(self, from_time: datetime.datetime, to_time: datetime.datetime):
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


class AlgorithmGenericTimeNode: # this is a bad idea, for maintenance in future.
    # no assertions so far!
    __ArrivalTime = datetime.datetime
    __DepartureTime: datetime.datetime
    __MinimumRunTime: str
    __MinimumStopTime: str

    def __init__(self, arrival_time: datetime.datetime, departure_time: datetime.datetime,
                 minimum_run_time: str = None, minimum_stop_time: str = None):
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
        super().__init__(arrival_time, departure_time, minimum_run_time, minimum_stop_time)
        AlgorithmTypeCheck.assert_parameter_is_int(train_path_node_id, 'train_path_node_id', '__init__')
        if not(stop_status is None):
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
        hasID.__init__(self, node_id)
        AlgorithmGenericTimeNode.__init__(self, arrival_time, departure_time, minimum_run_time, minimum_stop_time)
        self.__FormationID = int
        self.__NodeID = int
        self.__NodeTrackID = int
        self.__SectionTrackID = int
        self.__SequenceNumber = int

        # if not StopStatus is None:
        #     assert_stop_status(stop_status)
        # self.__StopStatus = stop_status
