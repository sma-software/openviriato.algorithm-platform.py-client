import AlgorithmStatic
import datetime


def assert_non_negative_weight(weight: int):
    assert not (weight < 0), 'only non-negative values for weights permitted'


def parse_to_datetime(datetime_rawstr: str) -> datetime.datetime:
    return datetime.datetime.strptime(datetime_rawstr, '%Y-%m-%dT%H:%M:%S')


class hasID:
    __ID: int

    def __init__(self, node_id: int):
        AlgorithmStatic.assert_parameter_is_int(node_id, 'node_id', '__init()__')
        self.__ID = node_id

    @property
    def ID(self) -> int:
        return self.__ID


class hasCode:
    __Code: str

    def __init__(self, code_string: str):
        AlgorithmStatic.assert_parameter_is_str(code_string, 'code_string', '__init()__')
        self.__Code = code_string

    @property
    def Code(self) -> str:
        return self.__Code


class hasDebugString:
    __DebugString: str

    def __init__(self, debug_string: str = None):
        if debug_string is not None:
            AlgorithmStatic.assert_parameter_is_str(debug_string, 'debug_string', '__init()__')
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
        assert_non_negative_weight(section_weight)
        hasID.__init__(self, section_id)
        hasCode.__init__(self, code_string)
        hasDebugString.__init__(self, debug_string)
        self.__Weight = section_weight
        self.__SectionCode = section_code

    @property
    def Weight(self) -> int:
        return self.__Weight

    @property
    def SectionCode(self) -> str:
        return self.__SectionCode


class AlgorithmTimeNode:
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


class UpdateTrainTimesNode(AlgorithmTimeNode):
    # missing attributes here:

    def __init__(self, arrival_time: datetime.datetime, departure_time: datetime.datetime, minimum_run_time: str = None,
                 minimum_stop_time: str = None, ):
        super().__init__(arrival_time, departure_time, minimum_run_time, minimum_stop_time)
        raise NotImplementedError
        # self.


class AlgorithmTrainPathNode(hasID, AlgorithmTimeNode):
    # raise NotImplementedError
    __ArrivalTime: datetime.datetime
    __DepartureTime: datetime.datetime

    def __init__(self, node_id: int, arrival_time: datetime.datetime, departure_time: datetime.datetime,
                 minimum_run_time, minimum_stop_time):
        hasID.__init__(self, node_id)
        AlgorithmTimeNode.__init__(self, arrival_time, departure_time, minimum_run_time, minimum_stop_time)
        raise NotImplementedError
        self.__ArrivalTime = arrival_time
        self.__DepartureTime = departure_time
        self.__FormationID = int
        self.__MinimumRunTime = int
        self.__MinimumStopTime = int
        self.__NodeID = int
        self.__NodeTrackID = int
        self.__SectionTrackID = int
        self.__SequenceNumber = int
        self.__StopStatus = None


class AlgorithmTrain(hasID, hasDebugString):
    __trainPathNodes: list

    def __init__(self, id: int, debug_string: str, train_path_nodes: list):
        hasID.__init__(self, id)
        hasDebugString.__init__(self, debug_string)
        self.__trainPathNodes = train_path_nodes

    @property
    def trainPathNodes(self):
        return self.__trainPathNodes



class AlgorithmTimeWindow:
    __FromTime: datetime
    __ToTime: datetime

    def __init__(self):
        raise NotImplementedError
